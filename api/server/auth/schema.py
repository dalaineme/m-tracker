#! /api/server/auth/schema.py
# -*- coding: utf-8 -*-
"""Contains the schema for the auth endpoint

Marshmallow validation with wtforms
"""

from marshmallow import Schema, fields
from marshmallow_validators.wtforms import from_wtforms
from wtforms.validators import Length, Regexp

PASS_REG = r"^(?=.*\d)(?=.*[a-zA-Z]).{8,20}$"


class UserSchema(Schema):
    """User schema"""
    is_admin = fields.Str(dump_only=True)
    first_name = fields.Str(
        required=True,
        validate=from_wtforms(
            [
                Length(
                    min=3,
                    max=15,
                    message="First name should be between 3 and 15 characters"
                ),
                Regexp(
                    '^[^±!@£$%^&*_+§¡€#¢§¶•ªº«\\/<>?:;|=.,]{1,20}$',
                    message="Invalid first name"
                ),
            ]
        )
    )
    last_name = fields.Str(
        required=True,
        validate=from_wtforms(
            [
                Length(min=3, max=15,
                       message="Last name should be between 3 and 15"),
                Regexp(
                    '^[^±!@£$%^&*_+§¡€#¢§¶•ªº«\\/<>?:;|=.,]{1,20}$',
                    message="Invalid last name"
                ),
            ]
        )
    )
    email = fields.Email(
        required=True,
        validate=from_wtforms(
            [Length(min=8, max=50,
                    message="Email should be between 8 and 50")]
        )
    )
    password = fields.Str(
        required=True,
        validate=from_wtforms(
            [
                Length(min=8, max=20,
                       message="Password should be between 8 and 20"),
                Regexp(
                    PASS_REG,
                    message="Weak password"
                ),
            ]
        )
    )
