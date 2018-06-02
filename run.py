#! run.py
# -*- coding: utf-8 -*-
"""Entry point of the app
Runs the app in specified exported mode
"""
import os

# import the APP used to instanciate flask
from api.server import APP

# run the app

if __name__ == '__main__':
    APP.debug = True
    port = int(os.environ.get('PORT', 5000))
    APP.run(host='0.0.0.0', port=port)
