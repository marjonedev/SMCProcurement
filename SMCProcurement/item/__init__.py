# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint

blueprint = Blueprint(
    'item_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)
