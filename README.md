# Spira xUnit Integration (Python)
This repository contains the source code for the Spira add-on that lets you read [xUnit](https://en.wikipedia.org/wiki/XUnit) XML files and import the test results into Spira. This add-on
works with SpiraTest, SpiraTeam and SpiraPlan editions on Spira.

## Overview
When you run automated tests using a framework such as JUnit, the test results are often generated in a standard XML format known as the xUnit format. This XML file contains a list of the test cases that were executed, the results that occured and potentially a list of associated screenshots or other attachments.

This application will read and parse the xUnit XML file and import the test results into the [Spira test management](https://www.inflectra.com/SpiraTest/) platform from [Inflectra](https://www.inflectra.com/). Spira already comes with a variety of dedicated integrations for different test automation frameworks such as JUnit, NUnit, PyTest, etc. however as new frameworks (such as WebDriver.io and Playwright) are released, this new **general purpose integration** will able to handle the integration from day one.

## About Spira
Spira is the end-to-end platform from [Inflectra](https://www.inflectra.com) for product creation, from idea to release. Whether you are building software yourself, or deploying third-party systems, Spira is the integrated hub into which you can plug in specialized tools for the rest of the software development lifecycle. 

Spira comes in three flavors:
- [SpiraTest](https://www.inflectra.com/SpiraTest/), powerful requirements and test management
- [SpiraTeam](https://www.inflectra.com/SpiraTeam/), agile planning and test management for teams
- [SpiraPlan](https://www.inflectra.com/SpiraPlan/), enterprise planning and testing platform

## Installing the Integration
This section outlines how to install the Spira plugin for xUnit. It assumes that you already have a working installation of Spira v6.0 or later. If you have an earlier version of Spira you will need to upgrade to at least v6.0 before trying to use this plugin. You will also need to have Python (with pip) installed.

To obtain the latest version of the plugin, simply run the following command:

`pip install spira-addons-xunit`

This command will install the latest version of the plugin straight from the Python Package Index (PyPI). Once the Spira plugin is successfully installed, all you need to do is configure the plugin, map your xUnit test cases to Spira test cases, then you can begin testing!

## How to Use the Integration
The integration consists of a Python module called `spira_xunit_reader.py` that is executed after your xUnit tests are executed, and the appropriate XML report file has been created. This module will then read the results in the xUnit report file and send the results to Spira, mapping each xUnit **test case** to a matching Spira test case.

For advanced users, you can also optionally map the xUnit **test suites** to corresponding Spira **test sets**, and/or have the plugin generate a new **build** in Spira that contains all of executed test cases and test suites.

### Configuring the Spira connection
In your test root folder (the folder you have your xUnit tests),
create a file named `spira.cfg` with the following:

```cfg
[credentials]
# Following are required
url = http://localhost/spira
username = administrator
token = {XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}}
project_id = 1
# Following are optional:
release_id = 5
test_set_id = 1
create_build = true

# Spira Test case for a specific classname.name
[test_cases]
LIS.Registration.registration1 = 2
LIS.Registration.registration2 = 3
LIS.Registration.registration3 = 4
LIS.Authentication.Login.login1 = 5
LIS.Authentication.Login.login2 = 9
LIS.Authentication.Login.login3 = 8
LIS.Authentication.auth1 = 6
LIS.Authentication.auth2 = 12
LIS.Authentication.auth3 = 13

LIS.Registration.registration4 = 5
LIS.Registration.registration5 = 9
LIS.Registration.registration6 = 8
LIS.Registration.registration7 = 6
LIS.Registration.registration8 = 12

# Spira Test sets for a specific name
# If not, the global value is used instead
[test_sets]
LIS.Registration = 2
LIS.Authentication = 5
LIS.Authentication.Login = 2
```

For the plugin to work, you must have the following in the credentials group:

- **url** -- The base url to your Spira installation, without a '/' at
the end.
- **username** -- The username you use to sign into Spira.
- **token** -- Your API Key / RSS Token. Found in your profile page as the "RSS
Token" field, you must have RSS Feeds enabled for this to work.
- **project_id** -- The ID of the project you would like the test runs to
be sent to

In addition, you can set the following **optional** configuration parameters as well:

- **release_id** -- Use if you would like to associate the
test run with a release.
- **test_set_id** -- Use if you would like to associate the
test run with a default test set.
- **create_build** -- Set to true if you would like the plugin to create a new Spira build artifact with every run that all the individual test case runs get associated with.

### Executing the Tests
Now you are ready to execute your tests and send the results back so Spira. This happens in two steps:
- Execute the unit tests and generate the `output.xml` xUnit style report file
- Parse the `output.xml` report file and send the results to Spira

First run your tests using your existing framework code. That will generate an output file. We have two supplied example files you can use:

- `junit-basic.xml` -- this is a minimalistic jUnit style example that contains several test cases nested in test suites with one test failure. It uses only the minimum set of attributes.
- `junit-complete.xml` -- this is a more advanced, complete example that includes file attachments, URL attachments, errors, warnings, failures and additional optional xUnit attributes such as assertions, properties and standard error/output streams.

Next, you need to run the Spira results parser module `spira_xunit_reader.py` to upload the results to Spira. For example, with the sample tests you can use either:

`python spira_xunit_reader.py samples\junit-basic.xml spira.cfg`

OR

`python spira_xunit_reader.py samples\junit-complete.xml spira.cfg`

The second parameter is the location and name of the Spira configuration file `spira.cfg`. One you run the XML parser, you should see a message similar to the following:

```
Sending test results to Spira at URL 'https://myserver/spiraservice.net'.
Successfully reported 4 test cases to Spira.
```

If there are any errors or warnings, they will be displayed instead.

### Viewing the Results
Finally, to view the results in Spira, you can go to the **Test Runs** tab to see the list of test runs:

![List of Robot Framework test runs in Spira](images/robot-framework-test-runs.png)

If you click on one of the **passed** test runs, it will display the name of the test case from Robot Framework, together with the status (pass), the test set, release and actual duration:

![A sample passed Robot test run as it looks in Spira](images/robot-framework-passed-test-run-1.png)

If you scroll down to the **Console Output** section, it displays the full name and path of the Robot Framework test case as well as the contents of the **Documentation** attribute and any messages.

![A sample passed Robot test run as it looks in Spira](images/robot-framework-passed-test-run-2.png)

If you click on one of the **failed** test runs, it will display the name of the test case from Robot Framework, together with the status (fail), the test set, release and actual duration:

![A sample failed Robot test run as it looks in Spira](images/robot-framework-failed-test-run-1.png)

If you scroll down to the **Console Output** section, it displays the full name and path of the Robot Framework test case as well as the contents of the **Documentation** attribute and in this case, the details of what caused the test to fail:

![A sample failed Robot test run as it looks in Spira](images/robot-framework-failed-test-run-2.png)

Congratulations, you have now executed your xUnit framework tests and integrated the reporting with Spira.

## Have Questions or Need Assistance?
If you are an Inflectra customer, please contact our customer support at:
- Email: support@inflectra.com
- Help Desk: https://www.inflectra.com/Support/

Otherwise, please feel free to post a question on our public forums:
- [Test Case Integration Forum](https://www.inflectra.com/Support/Forum/integrations/unit-testing/List.aspx)

# Examples
`python spira_xunit_reader.py samples\junit-basic.xml spira.cfg`

and

`python spira_xunit_reader.py samples\junit-complete.xml spira.cfg`

