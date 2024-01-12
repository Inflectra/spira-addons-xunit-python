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

url = https://myserver/spiraservice.net
username = fredbloggs
token = {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXX}
project_id = 1

# Following are optional:
release_id = 5
test_set_id = 1
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

# Examples
`python spira_xunit_reader.py samples\junit-basic.xml spira.cfg`

and

`python spira_xunit_reader.py samples\junit-complete.xml spira.cfg`

