import requests
import re
import json
import datetime
import time
import configparser
import xml.etree.ElementTree as ET
import sys

'''
The config is only retrieved once
'''
config = None

def getConfig(config_file):
    global config
    # Only retrieve config once
    if config is None:
        # Model of config object:
        config = {
            "url": "",
            "username": "",
            "token": "",
            "project_id": -1,
            "release_id": -1,
            "test_set_id": -1,
            "test_case_ids": {
                "default": -1
            }
        }
        # Parse the config file
        parser = configparser.ConfigParser()
        parser.read(config_file)

        sections = parser.sections()

        # Process Configs
        for section in sections:
            # Handle credentials and test case mappings differently
            if section == "credentials":
                for (key, value) in parser.items(section):
                    config[key] = value
            elif section == "test_cases":
                for (key, value) in parser.items(section):
                    print("Config: added key='{}', value='{}'".format(key.lower(), value))
                    config["test_case_ids"][key.lower()] = value
    return config


# Name of this extension
RUNNER_NAME = "xUnit (Python)"


class SpiraTestRun:
    # The URL snippet used after the Spira URL
    REST_SERVICE_URL = "/Services/v6_0/RestService.svc/"
    # The URL spippet used to post an automated test run. Needs the project ID to work
    POST_TEST_RUN = "projects/%s/test-runs/record"
    '''
    A TestRun object model for Spira
    '''
    project_id = -1
    test_case_id = -1
    test_name = ""
    stack_trace = ""
    status_id = -1
    start_time = -1
    end_time = -1
    message = ""
    release_id = -1
    test_set_id = -1

    def __init__(self, project_id, test_case_id, test_name, stack_trace, status_id, start_time, end_time, message='', release_id=-1, test_set_id=-1):
        self.project_id = project_id
        self.test_case_id = test_case_id
        self.test_name = test_name
        self.stack_trace = stack_trace
        self.status_id = status_id
        self.start_time = start_time
        self.end_time = end_time
        self.message = message
        self.release_id = release_id
        self.test_set_id = test_set_id

    def post(self, spira_url, spira_username, spira_token):
        """
        Post the test run to Spira with the given credentials
        """
        url = spira_url + self.REST_SERVICE_URL + \
            (self.POST_TEST_RUN % self.project_id)
        # The credentials we need
        params = {
            'username': spira_username,
            'api-key': spira_token
        }

        # The headers we are sending to the server
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': RUNNER_NAME
        }

        # The body we are sending
        body = {
            # Constant for plain text
            'TestRunFormatId': 1,
            'StartDate': self.start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'EndDate': self.end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'RunnerName': RUNNER_NAME,
            'RunnerTestName': self.test_name,
            'RunnerMessage': self.message,
            'RunnerStackTrace': self.stack_trace,
            'TestCaseId': self.test_case_id,
            # Passes (2) if the stack trace length is 0
            'ExecutionStatusId': self.status_id
        }

        # Releases and Test Sets are optional
        if(self.release_id != -1):
            body["ReleaseId"] = int(self.release_id)
        if(self.test_set_id != -1):
            body["TestSetId"] = int(self.test_set_id)

        dumps = json.dumps(body)

        response = requests.post(url, data=json.dumps(
            body), params=params, headers=headers)

        if response.status_code == 404:
            # Test Case Not Found
            print ("Unable to find a matching Spira test case of id TC:{}, so not able to post result".format(self.test_case_id))
            return True
        elif response.status_code == 200:
            # OK
            return False
        else:
            # General Error
            print ("Unable to send results due to HTTP error: {} ({})".format(response.reason, response.status_code))
            return True
        
class SpiraPostResults():
    def __init__(self, config_file):
        # Get the configuration information
        self.config = getConfig(config_file)

    def sendResults(self, test_results):
        # Only do stuff if config is specified
        if self.config["url"] == "":
            print("Unable to report test results back to Spira since URL in configuration is empty")

        else:
            print("Sending test results to Spira at URL '{}'.".format(self.config["url"]))
            try:
                # Loop through all the tests
                success_count = 0
                for test_result in test_results:
                    # Get the current date/time
                    current_time = datetime.datetime.now(datetime.UTC)

                    # Send the result
                    is_error = self.sendResult(test_result, current_time)
                    if is_error == False:
                        success_count = success_count + 1

                # Report to the console
                print("Successfully reported {} test cases to Spira.\n".format(success_count))
        
            except Exception as exception:
                print("Unable to report test cases to Spira due to error '{}'.\n".format(exception))

    def sendResult(self, test_result, current_time):
        try:
            # Create the Spira test run
            test_run = SpiraTestRun(
                config["project_id"], 
                test_result["test_case_id"], 
                test_result["name"], 
                test_result["stack_trace"], 
                test_result["execution_status_id"], 
                current_time - datetime.timedelta(seconds=test_result["duration_seconds"]), 
                current_time,
                message=test_result["message"], 
                release_id=config["release_id"], 
                test_set_id=config["test_set_id"]
            )
            # Post the test run!
            is_error = test_run.post(config["url"], config["username"], config["token"])
            return is_error

        except Exception as exception:
            print("Unable to report test case '{}' to Spira due to error '{}'.\n".format(test_result["name"], exception))
            return True


class SpiraResultsParser():
    def __init__(self, config_file='spira.cfg'):
        # Create an array to store the results we want to send to Spira
        self.test_results = []
        self.config_file = config_file

    def parseResults(self, reportFile):
        # Get the config
        config = getConfig(config_file)

        # Open up the XML file
        # create element tree object 
        xmlDoc = ET.parse(reportFile) 

        # get root element 
        testsuites = xmlDoc.getroot()

        # iterate over the test suites 
        for testsuite in testsuites.findall('./testsuite'):

            # iterate over the test cases in the test suite 
            for testcase in testsuite.findall('./testcase'):

                # extract the basic test information
                testname = testcase.get('name')
                classname = testcase.get('classname')
                elapsedtime = float(testcase.get('time'))

                # find the matching Spira test case id for this classname.name combination
                fullname = classname + '.' + testname
                test_case_id = -1
                if fullname.lower() in config["test_case_ids"]:
                    test_case_id = config["test_case_ids"][fullname.lower()]
                
                if test_case_id == -1:
                    print("Unable to find Spira id tag for test case '{}', so skipping this test case.".format(fullname))

                else:
                    # Convert the test case status
                    execution_status_id = 2 # Passed
                    '''
                    if test.status == "PASS":
                        # 2 is passed
                        execution_status_id = 2
                    elif test.status == "SKIP":
                        # 4 is n/a
                        execution_status_id = 4
                    elif test.status == "FAIL":
                        #1 is failed
                        execution_status_id = 1
                    elif test.status == "NOT RUN":
                        #5 is blocked
                        execution_status_id = 5
                    elif test.status == "NOT SET":
                        #1 is n/a
                        execution_status_id = 4
                    '''

                    # Create the details and message, default to success
                    message = 'Success'
                    details = 'Nothing Reported\n'

                    # Create new test result object
                    test_result = {
                        'test_case_id': test_case_id,
                        'name': fullname,
                        'execution_status_id': execution_status_id,
                        'stack_trace': details,
                        'message': message,
                        'duration_seconds': elapsedtime * 1000
                    }

                    # Parse the test case ID, and append the result
                    self.test_results.append(test_result)

        # Send the results to Spira
        spira_results = SpiraPostResults(config_file)
        spira_results.sendResults(self.test_results)
                
if __name__ == '__main__':
    # Get the command arguments, if there are any
    try:
        report_file = sys.argv[1]
    except IndexError:
        report_file = "xunit.xml"
    try:
        config_file = sys.argv[2]
    except IndexError:
        config_file = "spira.cfg"

    # Parse the file and report the results
    spiraResults = SpiraResultsParser(config_file)
    spiraResults.parseResults(report_file)
