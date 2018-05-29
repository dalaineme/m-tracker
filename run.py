#! run.py
# -*- coding: utf-8 -*-
"""Entry point of the app

Runs the app in debug mode
"""
from api.server import APP
APP.run(debug=True)
