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
    price = fields.Float(required=True, error_messages={
        'required': 'price is required.',
        'null': 'price cannot be null.',
        'invalid': 'invalid price.'
    })
    subscribe_date = fields.String( required=True, error_messages={
        'required': 'subscribe date is required.',
        'null': 'subscribe date cannot be null.',
        'invalid': 'invalid subscribe date.'
    })
    period = fields.Integer(required=True, error_messages={
        'required': 'period is required.',
        'null': 'period cannot be null.',
        'invalid': 'invalid period.'
    })
