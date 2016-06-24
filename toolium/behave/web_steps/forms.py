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

from toolium.utils.configuration import map_param
from toolium.utils.dataset import prepare_param


@step(u'I fill in "{field}" field from "{resource}" page with "{value}"')
def fill_in_form_with_value(context, field, resource, value):
    # Check if the value of the param is a 'config mask' and get its real value in this case and prepare dataset
    value = map_param(value)
    value = prepare_param(value)

    context.page = context.get_page_object(resource)
    
    # Type field
    element = context.get_element_from_current_page(field)
    element.text = unicode(value)

    #Finally, variable is saved in context.filled_values to check values in further steps.
    # (e.g: context.filled_values['username'])
    context.filled_values.update({field: value})


@step(u'I fill in "{field}" field with "{value}"')
def fill_in_form_with_value(context, field, value):
    # Check if the value of the param is a 'config mask' and get its real value in this case and prepare dataset
    value = map_param(value)
    value = prepare_param(value)
    
    # Type field
    element = context.get_element_from_current_page(field)
    element.text = unicode(value)
       
    #Finally, variable is saved in context.filled_values to check values in further steps.
    # (e.g: context.filled_values['username'])
    context.filled_values.update({field: value})


@step(u'I clear "{field}" input value')
def fill_in_form_with_value(context, field):

    element = context.get_element_from_current_page(field)
    element.clear()
