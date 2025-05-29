from marshmallow import Schema, fields, ValidationError


class LicenseBaseSchema(Schema):
    gym_id = fields.String(required=True, error_messages={
        'required': 'gym id is required.',
        'null': 'gym id cannot be null.',
        'invalid': 'invalid gym id.'
    })
    plan_id = fields.String(required=True, error_messages={
        'required': 'plan id is required.',
        'null': 'plan cannot be null.',
        'invalid': 'invalid plan id.'
    })

    subscribe_date = fields.DateTime( required=True, error_messages={
        'required': 'subscribe date is required.',
        'null': 'subscribe date cannot be null.',
        'invalid': 'invalid subscribe date.'
    })

