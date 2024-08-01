from marshmallow import Schema, fields, ValidationError


class GymBaseSchema(Schema):
    id = fields.Int(required=True, error_messages={
        'required': 'gym id is required.',
        'null': 'gym id cannot be null.',
        'invalid': 'invalid gym id.'
    })
    gym_name = fields.String(required=True, error_messages={
        'required': 'gym name is required.',
        'null': 'gym name cannot be null.',
        'invalid': 'invalid gym name.'
    })
    owner_name = fields.String(required=True, error_messages={
        'required': 'owner name is required.',
        'null': 'owner name cannot be null.',
        'invalid': 'invalid owner name.'
    })
    phone_number = fields.String(required=True, error_messages={
        'required': 'phone number is required.',
        'null': 'phone number cannot be null.',
        'invalid': 'invalid phone number.'
    })
    telephone = fields.String(required=True, error_messages={
        'required': 'telephone is required.',
        'null': 'telephone cannot be null.',
        'invalid': 'invalid telephone.'
    })
    logo = fields.Url(required=True, error_messages={
        'required': 'logo url is required.',
        'null': 'logo url cannot be null.',
        'invalid': 'invalid logo url.'
    })
    address = fields.String(required=True, error_messages={
        'required': 'address is required.',
        'null': 'address cannot be null.',
        'invalid': 'invalid address.'
    })
