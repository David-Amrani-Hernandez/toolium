# -*- coding: utf-8 -*-
u"""
Copyright (c) 2016 Telefonica Digital | ElevenPaths

This file is part of Toolium.

icensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from toolium.config_files import ConfigFiles
from toolium.behave.environment import before_all as toolium_before_all, before_scenario as toolium_before_scenario, \
    after_scenario as toolium_after_scenario, after_all as toolium_after_all
from toolium.utils.json_configuration import load_project_properties, load_message_properties, get_message_property


"""
This file inits the environment for a Behave! execution, according to the following test project structure:

    ├─ src (vamps-acceptance)
    │    ├─ common
    │    │   ├─ steps   (common steps)
    │    │   │    ├─ my_steps.py
    │    │   │    ├─ ...
    │    │   ├─ environment   (common environment)
    │    │   │    ├─ my_environment.py
    │    │   │    ├─ ...
    │    │   ├─ pageobjects   (custom page obejects)
    │    │   ├─ pageelements  (custom page elements)
    │    │   ├─ apiobjects (custom API obejects)
    │    │   └─ utils (general project utils)
    │    ├─ features
    │    │   ├─ component
    │    │   ├─ integration
    │    │   │    ├─ feature_1
    │    │   │    │    ├─ steps
    │    │   │    │    │    ├─ steps.py
    │    │   │    │    │    └─ __init__.py
    │    │   │    │    ├─ feature1.feature
    │    │   │    │    └─ environment.py
    │    │   │    └─ ...
    │    │   └─ e2e
    │    ├─ resources
    │    │   └─ page_object_definition.yaml
    │    ├─ settings
    │    │   ├─ pre-properties.json
    │    │   ├─ int-properties.json
    │    │   ├─ qa-properties.json  (default config)
    │    │   ├─ toolium.conf
    │    │   ├─ logging.conf
    │    │   └─ language
    │    │        ├─ es_<page>.cfg
    │    │        ├─ en_<page>.cfg
    │    │        └─ ...
    │    ├─ scripts
    │    ├─ requirements.txt
    │    ├─ Vagrantfile
    │    ├─ behave.ini
    │    ├─ README.md
    │    ├─ _output
    │    │   ├─ acceptance_int.log
    │    │   └─ ...
    │    └─ ...

"""

CONFIG_PROPERTIES_DIR = u'settings'
CONFIG_PROPERTIES_LANG_DIR = u'settings/language'
CONFIG_PROPERTIES_FRAMEWORK = u'toolium.conf'
CONFIG_PROPERTIES_LOGGING = u'logging.conf'
CONFIG_PROPERTIES_ENVIRONMENT = "{env}-properties.json"
OUTPUT_DIR = u'_output'
OUTPUT_LOGFILE_NAME = u'acceptance_int.log'


def before_all(context):
    """
    Initialization method that will be executed before all execution
    Variables added to Behave's context after execution:
        - context.driver_wrapper -> toolium.driver_wrapper.DriverWrapper
        - context.utils -> toolium.utils.Utils
        - context.toolium_config -> toolium.config_parser.ExtendedConfigParser
        - context.logger -> logging
        - context.config_files -> ConfigFiles
        - context.page_object_list_autoloaded: (list) PageObjectAutoloaded list
    Methods added to Behave's context:
        - context.get_page_object(page_object_name): (function) to retrieve a PageObject by its name
        - context.get_message_property(key_string): (function) to retrieve the text message in the specified language
            from the language properties file, using a key_string like this: "home.button.login".
    :param context: behave context
    """

    # Framework Configuration
    config_files = ConfigFiles()
    config_files.set_config_directory(CONFIG_PROPERTIES_DIR)
    config_files.set_config_log_filename(CONFIG_PROPERTIES_LOGGING)
    config_files.set_output_directory(OUTPUT_DIR)
    config_files.set_config_properties_filenames(CONFIG_PROPERTIES_FRAMEWORK)
    config_files.set_output_log_filename(OUTPUT_LOGFILE_NAME)
    context.config_files = config_files
    toolium_before_all(context)

    # Load environment variables from Behave UserData. Default: QA
    env_property = context.config.userdata.get("environment", "QA").lower()
    env_file_path = os.path.join(CONFIG_PROPERTIES_DIR, CONFIG_PROPERTIES_ENVIRONMENT.format(env=env_property))
    load_project_properties(env_file_path)

    # Load language properties from files.
    lang_property = context.config.userdata.get("language", "ES").lower()
    load_message_properties(lang_property, CONFIG_PROPERTIES_LANG_DIR)
    context.get_message_property = get_message_property


def before_scenario(context, scenario):
    """
    Scenario initialization. To be executed before each scenario. Creates and configures the Toolium
    DriverWrapper.
    Variables added to Behave's context after execution:
        - context.assert_screenshot -> Assert that a screenshot of an element is the same as a screenshot on disk,
        within a given threshold
        - context.assert_full_screenshot -> Assert that a screenshot of an element is the same as a screenshot on disk,
        within a given threshold
    :param context: behave context
    :param scenario: running scenario
    """

    toolium_before_scenario(context, scenario)

    # Context variable to manage the list of page objects (PageObject) generated by tests,
    # in order to be used in TearDown process.
    context.page_object_list = list()


def after_scenario(context, scenario):
    """
    Clean method that will be executed after each scenario
    :param context: behave context
    :param scenario: running scenario
    """

    toolium_after_scenario(context, scenario)


def after_all(context):
    """
    Clean method that will be executed after all features are finished.
    :param context: behave context
    """

    toolium_after_all(context)
