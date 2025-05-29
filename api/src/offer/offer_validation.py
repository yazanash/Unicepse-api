from marshmallow import Schema, fields, ValidationError


class OfferBaseSchema(Schema):
    offer_name = fields.String(required=True, error_messages={
        'required': 'offer name is required.',
        'null': 'offer name cannot be null.',
        'invalid': 'invalid offer name.'
    })
    offer_percent = fields.Float(required=True, error_messages={
        'required': 'offer percent is required.',
        'null': 'offer percent cannot be null.',
        'invalid': 'invalid offer percent.'
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
