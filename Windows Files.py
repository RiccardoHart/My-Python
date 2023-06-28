import ntpath
import os
from datetime import datetime
from iptcinfo3 import IPTCInfo
from pathlib import Path

from stat import *

my_file_path = r'D:\Logs\#Stefano Maiorana - Santiago de Murcia Entre dos almas\test.flac'
#my_file_path = r'D:\Logs\#Stefano Maiorana - Santiago de Murcia Entre dos almas'
# ntpath values - Windows variant of os.path info)
path_exists = ntpath.exists(my_file_path)        # Item exists
format_path = ntpath.normpath(my_file_path)      # Path reformatted: "D:\\" => "D:\"
lcase_path = ntpath.normpath(my_file_path)       # All characters in lowercase; forward slashes => back slashes
isfile = ntpath.isfile(my_file_path)             # Item is a file
isdir = ntpath.isdir(my_file_path)               # Item is a folder
split = ntpath.split(my_file_path)               # Tuple: ParentPath, FileName.ext
folder_name = ntpath.dirname(my_file_path)       # Tuple item 1: Parent Folder
basename = ntpath.basename(my_file_path)         # Tuple item 2: FileName.ext or deepest folder
drive, *rest = ntpath.splitdrive(my_file_path)   # Tuple: item 1 drive letter (e.g. "D:")
ext = ntpath.splitext(my_file_path)              # Extension (e.g. ".txt"
getatime = f"{datetime.fromtimestamp(ntpath.getatime(my_file_path)):%d-%b-%Y %H:%M.%f}"  # Last access
getmtime = f"{datetime.fromtimestamp(ntpath.getmtime(my_file_path)):%d-%b-%Y %H:%M.%f}"  # Last Modified
getctime = f"{datetime.fromtimestamp(ntpath.getctime(my_file_path)):%d-%b-%Y %H:%M.%f}"  # Created
getsize = ntpath.getsize(my_file_path)                                                   # Size in bytes
status = os.stat(my_file_path)
permissions = (status.st_mode)
read_access = os.access(my_file_path, os.R_OK)
write_access = os.access(my_file_path, os.W_OK)
same_stat = ntpath.samestat(status, status)
attributes = IPTCInfo(my_file_path)
mp3tag_file = ext in ["mp3", "flac", "mp4", "m4a", "m4b"]
ebook_file = ext in ["epub", "mobi", "azw", "azw3", "azw4"]



'''
os.mkdir(path)
os.mkdirs(path)
os.path.join(path1, path2)
os.remove('file_path')	                Removes the specified file.
os.unlink('file_path')	                Removes the specified file. Useful in UNIX environment.
pathlib.Path("file_path").unlink()	    Delete the file or symbolic link in the mentioned path
os.rmdir('empty_dir_path')	            Removes the empty folder.
pathlib.Path(empty_dir_path).rmdir()	Unlink and delete the empty folder.
shutil.rmtree('dir_path')	            Delete a directory and the files contained in it.
'''

results= {}                                                 # Initialise dictionary
# fstring f'{varname =}' returns "varname = value"
results[f"{basename=}".split("=")[0]] = basename
results[f"{basename = }".split("=")[0]] = basename
results[f"{dirname = }".split("=")[0]] = dirname
results[f"{fspath = }".split("=")[0]] = fspath
results[f"{abspath = }".split("=")[0]] = abspath
results[f"{exists = }".split("=")[0]] = exists
results[f"{lexists = }".split("=")[0]] = lexists
results[f"{expanduser = }".split("=")[0]] = expanduser
results[f"{split = }".split("=")[0]] = split
# results[f"{os_splitdrive = }".split("=")[0]] = basename
# results[f"{drive = }".split("=")[0]] = drive
# results[f"{split = }".split("=")[0]] = split
# results[f"{getatime = }".split("=")[0]] = getatime
# results[f"{getmtime = }".split("=")[0]] = getmtime
# results[f"{getctime = }".split("=")[0]] = getctime
# results[f"{getsize = }".split("=")[0]] = getsize
# results[f"{isabs = }".split("=")[0]] = isabs
# results[f"{isfile = }".split("=")[0]] = isfile
# results[f"{isdir = }".split("=")[0]] = isdir
# results[f"{normcase = }".split("=")[0]] = normcase
# results[f"{normpath = }".split("=")[0]] = normpath
# results[f"{sep = }".split("=")[0]] = sep
# results[f"{ext = }".split("=")[0]] = ext
# results[f"{mp3tag_file = }".split("=")[0]] = mp3tag
# results[f"{ebook_file = }".split("=")[0]] = ebook
# results[f"{path_stem = }".split("=")[0]] = stem
# results[stat.st_mode.split("=")[0]] = stat

for key, value in results.items():
    print(key, value)

# print(f"{npath_basename = }")
# print(f"{npath_dirname = }")
# print(f"{os_fspath = }")
# print(f"{npath_abspath = }")
# print(f"{npath_exists = }")
# print(f"{npath_lexists = }")
# print(f"{npath_expanduser = }")
# print(f"{npath_split = }")
# print(f"{os_splitdrive = }")
# print(f"{drive = }")
# print(f"{npath_splitext = }")
# print(f"{npath_getatime = }")
# print(f"{npath_getmtime = }")
# print(f"{npath_getctime = }")
# print(f"{npath_getsize = }")
# print(f"{npath_isabs = }")
# print(f"{npath_isfile = }")
# print(f"{npath_isdir = }")
# print(f"{npath_normcase = }")
# print(f"{npath_normpath = }")
# print(f"{os.sep = }")
# print(f"{ext = }")
# print(f"{mp3tag_file = }")
# print(f"{ebook_file = }")
# print(f"{path_stem = }")
# print(stat.st_mode)


# def get_tags(a_file):
#     from tinytag import TinyTag
#     tag = TinyTag.get(a_file)
#     if tag.albumartist
"""
    print('Title; %s' % tag.title)
    print('Artist: %s.' % tag.artist)
    print('Album Artist: %s.' % tag.albumartist)
    print('It is %f seconds long.' % tag.duration)
    print(tag.album)  # album as string
    print(tag.albumartist)  # album artist as string
    print(tag.artist)  # artist name as string
    print(tag.audio_offset)  # number of bytes before audio data begins
    print(tag.bitdepth)  # bit depth for lossless audio
    print(tag.bitrate)  # bitrate in kBits/s
    print(tag.comment)  # file comment as string
    print(tag.composer)  # composer as string
    print(tag.disc)  # disc number
    print(tag.disc_total)  # the total number of discs
    print(tag.duration)  # duration of the song in seconds
    print(tag.filesize)  # file size in bytes
    print(tag.genre)  # genre as string
    print(tag.samplerate)  # samples per second
    print(tag.title)  # title of the song
    print(tag.track)  # track number as string
    print(tag.track_total)  # total number of tracks as string
    print(tag.year)  # year or date as string
"""
    # return tag

# Python's built-in module for encoding and decoding JSON data
import json
# Python's built-in module for opening and reading URLs
from urllib.request import urlopen

# sample ISBN for testing: 1593276036

while True:

    # create getting started variables
    api = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
    isbn = input("Enter 10 digit ISBN: ").strip()

    # send a request and get a JSON response
    resp = urlopen(api + isbn)
    # parse JSON into Python as a dictionary
    book_data = json.load(resp)

    # create additional variables for easy querying
    volume_info = book_data["items"][0]["volumeInfo"]
    author = volume_info["authors"]
    # practice with conditional expressions!
    prettify_author = author if len(author) > 1 else author[0]

    # display title, author, page count, publication date
    # fstrings require Python 3.6 or higher
    # \n adds a new line for easier reading
    print(f"\nTitle: {volume_info['title']}")
    print(f"Author: {prettify_author}")
    print(f"Page Count: {volume_info['pageCount']}")
    print(f"Publication Date: {volume_info['publishedDate']}")
    print("\n***\n")

    # ask user if they would like to enter another isbn
    user_update = input("Would you like to enter another ISBN? y or n ").lower().strip()

    if user_update != "y":
        print("May the Zen of Python be with you. Have a nice day!")
        break # as the name suggests, the break statement breaks out of the while loop




def file_to_folder(a_path):
    import os
    import ntpath
    these_file_types = ["mp3", "flac", "m4a", "m4b"]

    for a_file in os.listdir(a_path):                                  # each file in folder
        if ntpath.isfile(ntpath.join(a_path, a_file)):                 # files in folder
            name, ext = ntpath.splitext(os.path.join(a_path, a_file))  # split name, ext
            if any(ext[1:] in file_type for file_type in these_file_types):    # files supporting tags
                file_name = file_name_from_tags(ntpath.join(a_path, a_file))   # construct file name
                if file_name != '':
                    new_folder = ntpath.normpath(ntpath.join(a_path, file_name))
                    if not ntpath.exists(new_folder):
                        os.mkdir(new_folder)
                    new_a_file = file_name + ntpath.splitext(a_file)[1]
                    os.rename(ntpath.join(a_path, a_file), ntpath.join(new_folder, new_a_file))
                    # print(f'Current Path/File: {a_path} {a_file}, New Name:,{new_a_path}')

def clean_file_names(a_path):
    import os
    import ntpath

    for a_file in os.listdir(a_path):                                  # each file in folder
        if ntpath.isfile(ntpath.join(a_path, a_file)):                 # files in folder
            name, ext = ntpath.splitext(os.path.join(a_path, a_file))  # split name, ext
            file_name = clean_file_name(name)
            print(f'Original Name: {name} \n Cleaned Name: {file_name}')

                    # print(f'Current Path/File: {a_path} {a_file}, New Name:,{new_a_path}')
'''
Get tags. Function to get mp3 tags and return a suggested file name based on artist and album if found.
Input: full path /name of file. Return suggested file name.
'''

def file_name_from_tags(a_file):        # Full path/file name
    from tinytag import TinyTag
    t = TinyTag.get(a_file)             # Get tags for file
    if t.albumartist is not None:
        artist = t.albumartist          # Preferentially select album artist over artist
    else:
        artist = t.artist
    if t.album is not None:
        album = t.album                 # Preferentially select album over title
    else:
        album = t.title

    if artist is not None and artist != '' and album is not None and album != '':
        file_name = artist + " - " + album
    else:
        file_name = ""
    invalid = '<>:":/\|?*'
    for char in invalid:
        file_name = file_name.replace(char,'')
    return file_name.replace('/','-')                    # Returns just file name (no path or ext)


def clean_file_name(file_name):
    replace_with_space = '_.'
    for char in replace_with_space:
        file_name = file_name.replace(char, ' ')

    file_name = file_name.replace('  ', ' ')
    file_name = file_name.strip()
    return file_name


# # Loop through given folder for specified file types
# my_dir=r"D:/Logs"
# file_to_folder(my_dir)

# Loop through given folder for specified file types
my_dir=r"D:/Logs/Extracted"
clean_file_names(my_dir)



from pathlib import Path
from enquiries import choose, confirm

def dir_chooser(c_dir=getcwd(),selected_dirs=None,multiple=True) :
    '''
        This function shows a file chooser to select single or
        multiple directories.
    '''
    selected_dirs = selected_dirs if selected_dirs else set([])

    dirs = { item for item in listdir(c_dir) if isdir(join(c_dir, item)) }
    dirs = { item for item in dirs if join(c_dir,item) not in selected_dirs and item[0] != "." } # Remove item[0] != "." if you want to show hidde

    options = [ "Select This directory" ]
    options.extend(dirs)
    options.append("⬅")

    info = f"You have selected : \n {','.join(selected_dirs)} \n" if len(selected_dirs) > 0 else "\n"
    choise = choose(f"{info}You are in {c_dir}", options)

    if choise == options[0] :
        selected_dirs.add(c_dir)

        if multiple and confirm("Do you want to select more folders?") :
            return get_folders(Path(c_dir).parent,selected_dirs,multiple)

        return selected_dirs

    if choise == options[-1] :
        return get_folders(Path(c_dir).parent,selected_dirs,multiple)

    return get_folders(join(c_dir,choise),selected_dirs,multiple)






