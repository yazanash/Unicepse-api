from marshmallow import Schema, fields, ValidationError


class HandShakeBaseSchema(Schema):
    pid = fields.String(required=True, error_messages={
        'required': 'player id is required.',
        'null': 'player cannot be null.',
        'invalid': 'invalid player id.'
    })
    uid = fields.String(required=True, error_messages={
        'required': 'user id is required.',
        'null': 'user id cannot be null.',
        'invalid': 'invalid user id.'
    })
    gym_id = fields.String(required=True, error_messages={
        'required': 'gym id is required.',
        'null': 'gym id cannot be null.',
        'invalid': 'invalid gym id.'
    })