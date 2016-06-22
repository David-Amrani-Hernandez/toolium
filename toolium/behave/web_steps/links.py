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


@step(u'I press "{name}" button')
def press_button(context, name):
    """
    Press button but no new page is loaded. e.i: To check that an error arises.
    """
    element = context.get_element_from_current_page(name)
    element.click()


@step(u'I click on "{name}" button')
def click_button(context, name):
    """
    Press button and:
      - the SAME page is reloaded (reset the current page elements and page object)
      - or a NEW page is loaded but, in this last case, the 'context.page' is not updated.
      This way, it needs to be updated by calling the step: 'the "{resource}" page is loaded'
    """

    element = context.get_element_from_current_page(name)
    element.click()

    context.page.reset_object()


@step(u'I click "{name}" button to go to "{resource}" page')
def click_button_and_go_to(context, name, resource):
    """
    Press button, a new page is loaded and 'context.page' is updated with the given resource.
     e.i: Moving to another page.
    """
    element = context.get_element_from_current_page(name)
    element.click()

    context.page = context.get_page_object(resource)
    context.page.wait_until_loaded()
