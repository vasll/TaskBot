""" Utility file to upload files to google drive with TaskBot """
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
import config


def get_gdrive_v3_service(json_key_file: str):
    """ Gets a google drive v3 service from a .json key file"""
    credentials = service_account.Credentials.from_service_account_file(json_key_file)
    scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=scoped_credentials)
    return service


def upload_file_to_gdrive(file: str, upload_file_name: str, parent_folder_id: str) -> dict | None:
    """ Uploads a file to google drive """
    service = get_gdrive_v3_service(config.service_account_file_path)

    uploaded_file = service.files().create(
        body={'name': upload_file_name, 'parents': [parent_folder_id]},
        media_body=MediaFileUpload(file, resumable=True)
    ).execute()

    return uploaded_file
