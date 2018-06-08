#! /api/server/request/schema.py
# -*- coding: utf-8 -*-
"""Contains the schema for the request endpoint
Marshmallow validation with wtforms
"""

from marshmallow import Schema, fields, post_load
from marshmallow_validators.wtforms import from_wtforms
from wtforms.validators import Length
from api.server.models import Request


class RequestSchema(Schema):
    """Request schema"""
    request_id = fields.Str(dump_only=True)
    title = fields.Str(
        required=True,
        validate=from_wtforms(
            [
                Length(
                    min=20,
                    max=100,
                    message="Request title should be between 20 to 50 characters"
                ),
            ]
        )
    )
    description = fields.Str(
        required=True,
        validate=from_wtforms(
            [
                Length(min=50, max=500,
                       message="Description should be between 50 to 500 characters"),
            ]
        )
    )
    email = fields.Email()

    @post_load
    def make_user(self, data):  # pylint: disable=R0201
        """Receives dictionary of deserialized data"""
        return Request(**data)


class ModifyRequestSchema(Schema):
    """Request schema"""
    title = fields.Str(
        required=True,
        validate=from_wtforms(
            [
                Length(
                    min=20,
                    max=100,
                    message="Request title should be between 20 to 50 characters"
                ),
            ]
        )
    )
    description = fields.Str(
        required=True,
        validate=from_wtforms(
            [
                Length(min=50, max=500,
                       message="Description should be between 50 to 500 characters"),
            ]
        )
    )
