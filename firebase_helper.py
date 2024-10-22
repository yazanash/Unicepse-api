import os

import firebase_admin
from firebase_admin import credentials, messaging, storage
from flask import json
import decrypt
#
#
# mega_helper.get_service_account()
# print("file got")
decrypt.decrypt_file()
cred = credentials.Certificate(os.getenv('DECRYPT_FILE'))
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
        android=messaging.AndroidConfig(
            priority='high',
            notification=messaging.AndroidNotification(
                sound='default'
            ),
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    sound='default',
                    content_available=True
                )
            ),
            headers={
                'apns-priority': '10'
                    }
        )
    )
    response = messaging.send(message)
    return {'message_id': response}
