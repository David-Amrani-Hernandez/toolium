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


@step(u'the GUI of the "{resource}" page is the expected one')
def gui_page_check(context, resource):
    # Assert the full screen
    context.assert_full_screenshot('%s_fullpage' % resource)


@step(u'the GUI of the "{resource}" page is the expected one without checking the elements')
def gui_page_after_invalid_check(context, resource):

    exclude_element_list = list()
    for row in context.table:
        element = context.get_element_from_current_page(row['element_name'])
        exclude_element_list.append(element)

    # Assert the full screen excluding some elements
    context.assert_full_screenshot('%s_partialpage' % resource, exclude_elements=exclude_element_list)
