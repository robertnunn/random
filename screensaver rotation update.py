"""
written using python 3.6.3

I have a giant folder full of images that I'd like to use as my screensaver. I'd like to only see the latest <num_pics>
 images. This script takes three things from the end user:
    source: the source directory of images
    destination: the directory containing the latest <num_pics> images
    num_pics: how many images to keep in the <destination> folder

"""

import os
import time
from shutil import copy2

source = r'<source folder here>'
destination = r'<destination>'
num_pics = 1000
# excluded_extensions is here if you want to do blacklisting instead of whitelisting
excluded_extensions = ['.mp4',
                       '.html',
                       '.webm',
                       '.gifv',
                       '.gif',
                       ]
included_extensions = ['.jpg',
                       '.jpeg',
                       '.png',
                       ]


def get_name_modtime(dir):  # returns a list of tuples, each having a filename and the last time it was modified
    os.chdir(dir)
    return [(x[0], time.ctime(x[1].st_mtime)) for x in sorted([(fn, os.stat(fn)) for fn in os.listdir('.')], key=lambda x: x[1].st_mtime)]


full_pic_list = get_name_modtime(source)
ss_rot = get_name_modtime(destination)
pics = []
print("before filtering pics ", len(full_pic_list))

# this loop checks every file in <source> and if it matches the included extensions, adds the data to the final pic list
for i in full_pic_list:
    ext = i[0][i[0].find('.'):]
    if ext in included_extensions:
        pics.append(i)

print("pics ", len(pics))
print("ss_rot ",len(ss_rot))

# using sets to remove files from the pics list that are already there
pics_set = set(pics[-num_pics:])
ss_rot_set = set(ss_rot)
update_list = pics_set.difference(ss_rot_set)

print("update list len ", len(update_list))
# copy new files to <destination>, don't recopy old files
for i in update_list:
    print(i)
    copy2(source + "\\" + i[0], destination)

print(len(pics_set))
# get the list of files in <destination> AFTER the new ones have been copied
new_ss_rot_list = get_name_modtime(destination)
print("new list ", len(new_ss_rot_list))

# remove older files that are no longer in the latest <num_pics>
if len(new_ss_rot_list):
    del_list = new_ss_rot_list[:-num_pics]
    os.chdir(destination)
    for i in del_list:
        print(i)
        os.remove(i[0])
