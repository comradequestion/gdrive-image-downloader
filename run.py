from gdrive import Gdrive
import os
import yaml


out_path = None
folder_name = None
with open('config.yaml', 'r') as conf:
    print(conf)
    c = yaml.load(conf.read(), Loader=yaml.FullLoader)
    out_path = c['out_path']
    folder_name = c['folder_name']

existing_files = os.listdir(out_path)

my_drive = Gdrive()
photo_folder_id = my_drive.find_photos_folder(folder_name)

files = my_drive.list_folder_by_parent(photo_folder_id)

for f in files:
    if 'image' not in f['type']:
        print('%s is not an image, skipping' % f['title'])
        continue
    if f['title'] not in existing_files:
        print('Downloading %s' % f['title'])
        my_drive.download_image(f['id'], f['title'], out_path)
    else:
        print('skipping %s' % f['title'])
