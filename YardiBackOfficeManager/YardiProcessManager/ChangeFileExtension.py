import glob, os
folder = 'C:\\Users\\Brandon\\tf_files\\grapes'
for filename in glob.iglob(os.path.join(folder, '*.tmp')):
    print("Change extension from .tmp to .jpg")
    os.rename(filename, filename[:-4] + '.jpg')
