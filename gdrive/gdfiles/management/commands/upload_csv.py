from django.core.management.base import BaseCommand

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
import httplib2

from gdoauth2.models import DriveCredential


class Command(BaseCommand):
    def handle(self, *args, **options):
        # TODO: specify which credential to use
        credential = DriveCredential.objects.latest('id').credential
        http = credential.authorize(httplib2.Http())
        service = build('drive', 'v2', http=http)
        mime_type = 'text/csv'
        for filename in args:
            print 'uploading', filename
            media_body = MediaFileUpload(
                filename, mimetype=mime_type, resumable=True)
            upload = service.files().insert(
                body=dict(title=filename, mimeType=mime_type),
                media_body=media_body, convert=True).execute()
            print 'File ID: %s' % upload['id']
