import os

import firebase_admin
from firebase_admin import credentials, messaging, storage
from flask import json

key = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS_JSON'])
cred = credentials.Certificate(key)
firebase_admin.initialize_app(cred, {
    'storageBucket': os.environ['STORAGE_BUCKET']
})
bucket = storage.bucket()


def send_notification(token, title, body):
    registration_token = token
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=registration_token,
    )
    response = messaging.send(message)
    return {'message_id': response}
