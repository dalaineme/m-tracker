#! run.py
# -*- coding: utf-8 -*-
"""Entry point of the app
Runs the app in specified exported mode
"""

# import the APP used to instanciate flask
from api.server import APP

# run the app
# APP.run()
APP.run(host='0.0.0.0')
