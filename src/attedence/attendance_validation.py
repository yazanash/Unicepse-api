from marshmallow import Schema, fields


class AttendanceBaseSchema(Schema):
    aid = fields.Integer(required=True, error_messages={
        'required': 'attendance id is required.',
        'null': 'attendance id cannot be null.',
        'invalid': 'invalid attendance id.'
    })
    date = fields.DateTime(required=True, error_messages={
        'required': 'date is required.',
        'null': 'date cannot be null.',
        'invalid': 'invalid date.'
    })
    login_time = fields.DateTime(required=True, error_messages={
        'required': 'login time is required.',
        'null': 'login time cannot be null.',
        'invalid': 'invalid login time.'
    })
    logout_time = fields.DateTime(required=True, error_messages={
        'required': 'logout time is required.',
        'null': 'logout time cannot be null.',
        'invalid': 'invalid logout time.'
    })
    pid = fields.Integer(required=True, error_messages={
        'required': 'player id is required.',
        'null': 'player id cannot be null.',
        'invalid': 'invalid player id.'
    })
    sid = fields.Integer(required=True, error_messages={
        'required': 'subscription id is required.',
        'null': 'subscription id cannot be null.',
        'invalid': 'invalid subscription id.'
    })
    gym_id = fields.String(required=True, error_messages={
        'required': 'gym_id is required.',
        'null': 'gym_id cannot be null.',
        'invalid': 'invalid gym_id.'
    })
