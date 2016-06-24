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

from behave import step
import time
from toolium.utils.configuration import map_param


@step(u'I navigate to the "{url}" service url for "{resource}" web page')
def navigate_to_url(context, url, resource):

    # Check if the value of the param is a 'config mask' and get its real value in this case and prepare dataset
    context.url = map_param(url)

    # Set up correct PageObject depending on the resource accessed by the user
    context.page = context.get_page_object(resource)

    # Navigate to the expected url
    context.page.driver.get(context.url)


@step(u'the page is loaded')
def resource_page_is_loaded(context):

    # Check if certain elements of the new PageObject are loaded
    context.page.wait_until_loaded()


@step(u'the "{resource}" page is loaded')
def resource_page_is_loaded(context, resource):

    context.page = context.get_page_object(resource)

    # Check if certain elements of the new PageObject are loaded
    context.page.wait_until_loaded()


@step(u'I wait {seconds} seconds')
def wait_n_seconds(context, seconds):
    time.sleep(int(seconds))
