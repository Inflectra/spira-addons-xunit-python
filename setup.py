"""
Defines the entry point of the extension
"""

import setuptools
import os
import codecs
import io

with io.open("README.md") as readme_file:
    long_description = readme_file.read()

# Register plugin with xUnit
setuptools.setup(
    name ='spira-addons-xunit',
    version = '1.0.0',
    author = 'Inflectra Corporation',
    author_email ='support@inflectra.com',
    url = 'http://www.inflectra.com/SpiraTest/Integrations/Unit-Test-Frameworks.aspx',
    description = 'Exports xUnit format test executions as test runs in Spira (SpiraTest/Team/Plan)',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    py_modules = ['spira_xunit_reader'],
    classifiers = [
        'Framework :: Pytest',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points = {
        'xunit': [
            'spira-addons-xunit = spira_xunit_reader',
        ],
    },
    include_package_data=True,
    package_data={'': ['**/samples/*.*', 'spira.cfg']},
)
