#! /api/server/__init__.py
# -*- coding: utf-8 -*-

"""This module instanciates flask
"""

from flask import Flask, jsonify

APP = Flask(__name__)


@APP.route('/')
def index():
    """Home route"""
    return jsonify({'message': 'working'})
