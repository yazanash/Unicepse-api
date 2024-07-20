from marshmallow import Schema, fields, ValidationError


class UserBaseSchema(Schema):
    email = fields.Email(required=True, error_messages={
        'required': 'email is required.',
        'null': 'email cannot be null.',
        'invalid': 'invalid email.'
    })


class UserSchema(UserBaseSchema):
    otp = fields.Integer(required=True, error_messages={
        'required': 'otp is required.',
        'null': 'otp cannot be null.',
        'invalid': 'invalid otp.'
    })
    notify_token = fields.String(required=True, error_messages={
        'required': 'notify_token is required.',
        'null': 'notify_token cannot be null.',
        'invalid': 'notify_token otp.'
    })
