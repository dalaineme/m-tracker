#! run.py
# -*- coding: utf-8 -*-
"""Entry point of the app
Runs the app in specified exported mode
"""

# import the APP used to instanciate flask
from api.server import APP

# run the app

if __name__ == '__main__':
    # PORT = int(os.environ.get('PORT', 5000))
    APP.run()
