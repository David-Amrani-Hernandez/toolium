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

import sys
import json
import logging
import re
from copy import deepcopy
from os import listdir
from os.path import isfile, isdir, join
from yaml import load
import codecs

__logger__ = logging.getLogger(__name__)

# Loaded configuration. Module variable with all loaded properties: JSON
config = None

# Loaded language properties as Python Dict
language_prop_list = None
language = None  # es, en, ...


def load_project_properties(json_file):
    """
    Parses the JSON configuration file located in the conf folder and
    stores the resulting dictionary in the config global variable.
    :param: (json_file) Path to properties file to be loaded.
    """

    __logger__.info("Loading project properties from %s", json_file)
    try:
        with open(json_file) as config_file:
            try:
                global config
                config = json.load(config_file)
            except Exception, e:
                __logger__.error('Error parsing config file: %s' % e)
                sys.exit(1)
    except IOError, e:
        __logger__.error('%s properties file CANNOT be opened: %s', json_file, e)

    __logger__.debug("Properties loaded: %s", config)


def load_message_properties(lang, lang_dir):
    """
    Loads all lang properties for the files located in the given lang_dir.
    File format to load: *.yaml
    :param lang: (string) Language property to load text messages from files.
    :param lang_dir: (string) Dir where the lang files are located
    :return: None. The loaded lang properties will be saved in the global var of this file: language_prop_list
    """

    __logger__.info("Language set to '%s'", lang)
    __logger__.info("Loading all language files from '%s'", lang_dir)
    if isdir(lang_dir):
        file_list = [join(lang_dir, f) for f in listdir(lang_dir) if isfile(join(lang_dir, f)) and
                     f.endswith(".yaml")]
        __logger__.debug("Language properties file list: '%s'", file_list)

        global language_prop_list, language

        language = lang
        language_prop_list = dict()
        for file in file_list:
            # Open the file with the correct encoding
            with codecs.open(file, 'r', encoding='utf-8') as f:
                language_prop_list.update(load(f))
        __logger__.debug("Language properties loaded for: '%s'", language_prop_list.keys())
    else:
        __logger__.warn("Dir with language property files not found.")


def get_message_property(key_string):
    """
    Gets the given property as String separated by points: "home.button.send"
    :param key_string: (string) Chain of keys to get
    :return: Value of the given property chain in the specified language
    """

    key_list = key_string.split(".")
    language_props_copy = deepcopy(language_prop_list)
    try:
        for key in key_list:
            language_props_copy = language_props_copy[key]

        __logger__.info("Mapping language param '%s' to its configured value '%s'", key_string, language_props_copy)
    except KeyError as e:
        __logger__.error("Mapping chain not found in the language properties file")
        raise e

    return language_props_copy[language]


def _is_conf_property_in_config(param):
    """
    Checks if the given param should be loaded from Environment Configuration File
    Format: [CONF:services.vamps.user]
    :param param: Parameter to check its value.
    :return: returning a match object, or None if no match was found.
    """

    return re.match("\[CONF:(.*)\]", param)


def _is_lang_property_in_config(param):
    """
    Checks if the given param should be loaded from Language Configuration File
    Format: [LANG:home.button.label]
    :param param: Parameter to check its value.
    :return: returning a match object, or None if no match was found.
    """

    return re.match("\[LANG:(.*)\]", param)


def map_param(param_value):
    """
    Analyzes the given parameter value and find out its real value into the loaded environment configuration file or
    language configuration file.
    :param param_value: Parameter value. If it should be replaced by its real value into configuration file, when
    the format is something like this: [CONF:services.vamps.user] or [LANG:home.button.label].
    :return: Real parameter value. If the param value does not suit this format,
    the returned param value is the same as the given one.
    """

    match_group = _is_conf_property_in_config(param_value)
    if match_group:
        return _map_config_param(match_group.group(1))
    else:
        match_group = _is_lang_property_in_config(param_value)
        if match_group:
            return get_message_property(match_group.group(1))
        else:
            return param_value


def _map_config_param(param_value, config_json=None):
    """
    Analyzes the given parameter value and find out its real value into the loaded environment configuration file.
    :param param_value: Parameter value. If it should be replaced by its real value into configuration file, when
    the format is something like this: [CONF:services.vamps.user], when I want to access to these properties:
        {
          "services":{
            "vamps":{
              "user": "cyber-sec-user@11paths.com",
              "password": "MyPassword"
            }
          }
        }
    :param config_json: (dict) Loaded configuration file (environment properties)
    :return: Real parameter value. In this case, the string "cyber-sec-user@11paths.com". If the param value
    does not suit this format, the returned param value is the same as the given one.
    """

    if not config_json:
        config_json = config

    properties_list = param_value.split(".")
    aux_config_json = deepcopy(config_json)
    try:
        for property in properties_list:
            aux_config_json = aux_config_json[property]

        __logger__.info("Mapping param '%s' to its configured value '%s'", param_value, aux_config_json)
    except KeyError as e:
        __logger__.error("Mapping chain not found in the configuration properties file")
        raise e
    return aux_config_json
