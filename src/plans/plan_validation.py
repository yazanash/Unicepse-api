from marshmallow import Schema, fields, ValidationError


class PlanBaseSchema(Schema):
    plan_name = fields.String(required=True, error_messages={
        'required': 'plan is required.',
        'null': 'plan cannot be null.',
        'invalid': 'invalid plan.'
    })
    price = fields.Float(required=True, error_messages={
        'required': 'price is required.',
        'null': 'price cannot be null.',
        'invalid': 'invalid price.'
    })
    description = fields.String(required=True, error_messages={
        'required': 'description is required.',
        'null': 'description cannot be null.',
        'invalid': 'invalid description.'
    })
    period = fields.Integer(required=True, error_messages={
        'required': 'period is required.',
        'null': 'period cannot be null.',
        'invalid': 'invalid period.'
    })
