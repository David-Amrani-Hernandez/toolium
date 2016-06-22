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

from yaml import load
from toolium.pageobjects.page_object_autoloaded import PageObjectAutoloaded
import logging

from toolium.pageelements import *
from selenium.webdriver.common.by import By

__logger__ = None

PAGE_ELEMENT_CREATION_PATTERN = \
    "page_object.element_{att_name}={page_element_name}(By.{locator_type}, '{locator_value}')"

PAGE_OBJECT_ATT_IF_WAIT_PATTER = \
    "page_object.element_{att_name}.if_wait = {if_wait}"


def _init_logger():
    """
    Inits the logger manager for this file
    :return:
    """

    global __logger__
    __logger__ = logging.getLogger(__name__) if __logger__ is None else __logger__


def add_attributes_to_page_object(page_element, page_object):
    """
    Adds to the given page object the defined page elements using the PAGE_ELEMENT_CREATION_PATTERN.
    :param page_element: (dict) Page element loaded from YAML definition.
    :param page_object: (Toolium PageObjectAutoLoaded) PageObject where PageElements are created as attributes
    :return: None
    """

    for page_element_name in page_element:
        __logger__.debug("Creating element in PageObject '%s'", page_element_name)
        page_element_details = page_element[page_element_name]

        exec_string = PAGE_ELEMENT_CREATION_PATTERN.format(att_name=page_element_details['Name'],
                                                           page_element_name=page_element_name,
                                                           locator_type=page_element_details['Locator-Type'],
                                                           locator_value=page_element_details['Locator-Value'])
        __logger__.debug("Executing sentence: '%s'", exec_string)
        exec exec_string

        if_wait_value = page_element_details['Wait-For-Loaded'] if 'Wait-For-Loaded' in page_element_details else False
        exec_string = PAGE_OBJECT_ATT_IF_WAIT_PATTER.format(att_name=page_element_details['Name'],
                                                            if_wait=if_wait_value)
        __logger__.debug("Executing sentence: '%s'", exec_string)
        exec exec_string


def create_page_objects(page_object_definition_data):
    """
    Creates all PageObjects from the specification loaded from YAML file.
        Executes the code instruction defined in PAGE_ELEMENT_CREATION_PATTERN:
        Add the loaded page elements as attributes to the PageObject
    :param page_object_definition_data: (dict) Loaded page object definition from YAML file.
    :return: List of created PageObjects (Toolium PageObjectAutoLoaded) with all its PageElements (attributes)
    """

    created_page_objects_list = list()

    for page_object_name in page_object_definition_data:
        __logger__.info("Creating PageObject: '%s'", page_object_name)

        page_object = PageObjectAutoloaded()
        page_object.name = page_object_name

        for item in page_object_definition_data[page_object_name]:
            add_attributes_to_page_object(item, page_object)
        created_page_objects_list.append(page_object)

    __logger__.info("PageObjects loaded from YAML file '%s'", created_page_objects_list)

    return created_page_objects_list


def load_page_object_definition(file_path):
    """
    Loads the YAML document with the definition of all PageObjects
    :param file_path: (string) Path where the page objects definition file is located
    :return: (dict) Loaded data.
    """

    _init_logger()
    __logger__.info("Reading YAML file: '%s'", file_path)

    stream = file(file_path, 'r')

    try:
        loaded_data = load(stream)
    finally:
        stream.close()

    __logger__.debug("Loaded data", loaded_data)
    return loaded_data


def get_page_object(created_page_objects_list, page_object_name):
    """
    Retrieve PageObjects definition given the list of available pageobjects and the name of the required one.
    :param created_page_objects_list: (dict) list of Loaded page object definition from YAML file.
    :param page_object_name: (string) name of the required pageObject 
    :return: List of created PageObjects (Toolium PageObject) with all its PageElements (attributes)
    """

    current_page_object = None
    for page_object in created_page_objects_list:
        if page_object.name == page_object_name:
            current_page_object = page_object
            break

    return current_page_object


def get_element_from_page_object(page_object, element_name):
    """
    Retrieves the given element from the page_object by the element name.
    :param page_object: (PageObjectAutoLoaded) Page object
    :param element_name: Element name following the AutoLoader rules for element names.
    :return: PageElement
    """
    exec "element = page_object.element_{name}".format(name=element_name)
    return element

