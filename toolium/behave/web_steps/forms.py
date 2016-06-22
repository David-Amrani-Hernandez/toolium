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

from toolium.utils.json_configuration import map_config_param
from toolium.utils.dataset import prepare_param


@step(u'I fill in "{field}" field from "{resource}" page with "{value}"')
def fill_in_form_with_value(context, field, resource, value):
    # Check if the value of the param is a 'config mask' and get its real value in this case and prepare dataset
    value = map_config_param(value)
    value = prepare_param(value)

    context.page = context.get_page_object(resource)
    
    # Type field
    exec "context.page.element_{field}.text = '{value}'".format(field=field, value=unicode(value))
       
    #Finally, variable is saved in context.'field' to check values in further steps. (e.g: context.username)
    exec "context.{field} = 'value'".format(field=field, value=value)


@step(u'I fill in "{field}" field with "{value}"')
def fill_in_form_with_value(context, field, value):
    # Check if the value of the param is a 'config mask' and get its real value in this case and prepare dataset
    value = map_config_param(value)
    value = prepare_param(value)
    
    # Type field
    exec "context.page.element_{field}.text = '{value}'".format(field=field, value=unicode(value))
       
    #Finally, variable is saved in context.'field' to check values in further steps. (e.g: context.username)
    exec "context.{field} = 'value'".format(field=field, value=value)


@step(u'I clear "{field}" input value')
def fill_in_form_with_value(context, field):
    
    exec "context.page.element_{field}.clear".format(field=field)
