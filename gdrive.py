import os
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive
from pprint import pprint
import json

GDRIVE_CREDENTIALS_PATH = 'client_secrets.json'

class Gdrive():
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.metadata']

        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(GDRIVE_CREDENTIALS_PATH, SCOPES)
        self.drive = GoogleDrive(gauth)

    def list_files(self, payload=None):
        return self.drive.ListFile(payload).GetList()

    def find_photos_folder(self, title):
        return self.drive.ListFile({'q': "title='%s'" % title}).GetList()[0]['id']

    def list_folder_by_parent(self, parent):
        filelist = []
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % parent}).GetList()
        for f in file_list:
            if f['mimeType'] == 'application/vnd.google-apps.folder':  # if folder
                filelist.append({"id": f['id'], "title": f['title'], "list": self.list_folder_by_parent(f['id'])})
            else:
                filelist.append({"title": f['title'], "title1": f['alternateLink'], "id": f['id'], 'type': f['mimeType']})
        return filelist

    def list_folder_by_id(self, folder_id):
        filelist = []
        file_list = self.drive.ListFile({'q': "'%s' in id and trashed=false" % folder_id}).GetList()
        for f in file_list:
            if f['mimeType'] == 'application/vnd.google-apps.folder':  # if folder
                filelist.append({"id": f['id'], "title": f['title'], "list": self.list_folder_by_parent(f['id'])})
            else:
                filelist.append({"title": f['title'], "title1": f['alternateLink'], "id": f['id'], 'type': f['mimeType']})
        return filelist

    def download_image(self, image_id, image_name, path):
        f = self.drive.CreateFile({'id': image_id})
        return f.GetContentFile(os.path.join(path, image_name))


    def create(self):
        f = self.drive.CreateFile({'title': 'Hello.txt'})
        f.Upload()


if __name__ == '__main__':
    q = {'q': "title='test'"}
    my_drive = Gdrive()
    pprint(my_drive.list_files())
