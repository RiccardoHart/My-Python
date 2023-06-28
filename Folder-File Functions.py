import os
import re

'''
Functions:
 1. list_dirs_files            list all files and subdirs recursively starting with input path
 2. count_file_types           for input dir list return list and count of each file extension
 3. clean_filenames_in_dir     for each file od specific types in folder, clean the name 
 4. clean_name                 for input file or dir name return cleaned name 
 5. append_info_to_subdirs_in_dir     for all subdirs, clean mane and append info string {#...#}
 6. append_dir_info
 7. unappend_dir_info 
'''

'''
1. LIST_DIRS_FOLDERS
params: full path to directory, max depth to walk from here, collate sub-dirs, or files, or both 
return sorted list of files and/or sub-dirs - sorting is directory depth, files, sub-dirs
'''
def list_dirs_files(my_path, max_dir_depth=-1, dirs_files='both'):
    results = []                               # empty list to hold results
    for my_dir in os.walk(my_path):            # walk through passed directory structure
        dir, subdirs, files = my_dir           # returns tuple (directory, list of sub-directories, list of files)
        dir_depth = dir.count(chr(92)) - my_path.count(chr(92))  # relative folder depth (needed for sort)
        results.append((dir_depth, dir))       # results (folder) - tuple(depth, dir)
        # now get each file in this directory and append (depth, full path.name) to results
        for file in files:
            results.append((dir_depth, os.path.join(dir, file)))
    # returns list of tuples: (depth, full path.name)
    return results

# ----------------------------------------------------------------------------------------------------------------------
def list_dirs_files2(my_file_path, max_folder_depth=-1, dirs_files='both'):
    results = []                               # empty list to hold results
    for my_dir in os.walk(my_file_path):       # walk through passed directory structure
        root, subdirs, files = my_dir          # returns tuple (root directory, list of sub-directories, list of files)
        folder_depth = root.count(chr(92)) - my_file_path.count(chr(92))  # relative folder depth
        if max_folder_depth < 0 or folder_depth <= max_folder_depth:   # not exceeded max folder depth if specified
            if dirs_files != 'files':          # not files only => folder details required
                file_exts = set()              # empty set for file extensions in sub-dir
                for file in files:             # loop through files in current directory
                    set.add(file_exts, os.path.splitext(file)[1])   # add unique ext to set
                file_types = []                # empty dictionary for file types in sub-dir
                for ext in file_exts:          # for each unique ext in set
                    count = 0                  # initialize ext count
                    for file in files:         # loop through files again
                        if os.path.splitext(file)[1] == ext:    # if current ext in set
                            count += 1                          # increment ext count
                    file_types.append((ext, count))             # add (ext, count) to file_types dictionary
                # for folder item add depth, parent folder, skip filename, no. sub-dirs, no. files, dict [ext, count]
                results.append((folder_depth, root, "", "D", len(subdirs), len(files), file_types))
            if dirs_files != 'folders':        # not folder details only => file details required
                for file in files:             # for each file in current directory add file details
                    results.append((folder_depth, root, file, "F", "", "", ""))
    # return sorted(results, key=lambda item: f'({item[0]}{item[1]})')
    return results
'''
2. COUNT_FILE_TYPES
for folder referenced in my_path, count no. of files of each file extension type
'''
def count_file_types(my_path):
    results = dict()                                         # create empty dictionary
    dir_items = os.listdir(my_path)                          # us os.listdir to get all items in folder
    for dir_item in dir_items:                               # for each item
        if os.path.isfile(os.path.join(my_path, dir_item)):  # if it is a file and not a sub-directory
            ext = os.path.splitext(dir_item)[1]              # get extension
            if ext in results:                               # if this .ext already in dict, add 1 to count
                results[ext] = results[ext] + 1
            else:
                results[ext] = 1                             # create new dict item, count = 1
    return sorted(results.items(), key=lambda item: item[1], reverse=True) # return dictionary [(.txt: 3; .pdf: 4)] etc.
# ----------------------------------------------------------------------------------------------------------------------

'''
3. CLEAN_FILE_NAMES_IN_DIR
for each file in supplied folder that is one of the specified types call clean_name(filename)
'''
def clean_filenames_in_dir(my_path):
    valid_exts =[".pdf", ".mobi", ".epub", ".mp3", ".flac", ".m4a", ".m4b"]
    dir_items = os.listdir(my_path)                          # use os.listdir to get all items in folder
    for dir_item in dir_items:                               # for each item that is a file
        if os.path.isfile(os.path.join(my_path, dir_item)):
            filename, ext = os.path.splitext(dir_item)       # get extension
            if ext in valid_exts:                            # if one of the specified type
                cleaned_filename = clean_name(filename)      # call function to clean filename
                print(filename, "====", cleaned_filename)
# ----------------------------------------------------------------------------------------------------------------------

'''
3.1 CLEAN_SUB_DIR_NAMES_IN_DIR
for each file in supplied folder that is one of the specified types call clean_name(filename)
'''
def clean_sub_dir_names_in_dir(my_path):
    dir_items = os.listdir(my_path)                          # use os.listdir to get all items in folder
    for dir_item in dir_items:                               # for each item that is a file
        if os.path.isdir(os.path.join(my_path, dir_item)):

            cleaned_dir = clean_name(dir_item)      # call function to clean filename
            if cleaned_dir != dir_item:
                os.rename(os.path.join(my_path, dir_item),os.path.join(my_path, cleaned_dir))            # change name
                print(dir_item, "====", cleaned_dir)
# ----------------------------------------------------------------------------------------------------------------------


'''
4. CLEAN_NAME
input filename (without ext) or folder name; return cleaned name
perform various cleaning actions and return cleaned filename
*  use regex to find and replace target sub-strings, regardless of case
*  replace underscores with space
*  remove leading and trailing spaces
'''
def clean_name(file_or_dir_name):
    cleaned_name = re.sub('sanet.st', '', file_or_dir_name, flags=re.IGNORECASE)
    cleaned_name = re.sub('_', ' ', cleaned_name)
    return cleaned_name.strip()
# ----------------------------------------------------------------------------------------------------------------------

'''
5. APPEND_INFO_TO_SUBDIRS_IN_DIR
for all sub-dirs in input dir clean, append ext info and rename
'''
def append_info_to_subdirs_in_dir(my_path, action='append'):
    dir_items = os.listdir(my_path)                          # use os.listdir to get all items in folder
    for dir_item in dir_items:                               # loop through items in folder
        this_dir = os.path.join(my_path, dir_item)           # this sub-dir, full path
        if os.path.isdir(this_dir):                          # for dir items only
            # clean any existing appendages and get refreshed info appendage
            my_path_cleaned, new_append = append_dir_info(this_dir)
            if action == 'append':                           # refresh / create appended info?
                new_dir_name = my_path_cleaned+new_append    # cleaned dir + new append info
            else:                                            # just clean
                new_dir_name = my_path_cleaned               # cleaned dir

            if new_dir_name != this_dir:                     # if result is modified directory
                os.rename(this_dir, new_dir_name)            # change name
                print(new_dir_name)
# ----------------------------------------------------------------------------------------------------------------------

'''
6. APPEND_DIR_INFO
for input dir, add structured list of subdir count, file count, file ext counts:
e.g. 'my folder {#d=41 f=20 pdf=6 m4b=5 rar=2 mp3=2 avi=1 json=1 mp4=1 azw3=1 mkv=1#}'
'''
def append_dir_info(my_path):
    file_count, dir_count =(0, 0)                       # initialise subdir, file count
    for item in os.listdir(my_path):                    #
        if os.path.isdir(os.path.join(my_path, item)):  # if file
            file_count += 1                             # count files
        else:
            dir_count += 1                              # count subdirs

    file_exts = count_file_types(my_path)               # get dictionary of file extensions & counts
    my_path_cleaned = unappend_dir_info(my_path)  # remove any {#...#} info

    s = f'd={file_count } f={dir_count} '               # construct e.g d=41 f=20 counts
    for ext, count in file_exts:                        # for each extension
        s = s + f'{ext[1:]}={count} '                   # append extension and count
    s = ' {#' + s[:-1] + '#}'                           # append {# ... #} labels
    return (my_path_cleaned,s)                          # return input dir path with appended {#...#} string

# ----------------------------------------------------------------------------------------------------------------------

'''
7. UNAPPEND_DIR_INFO
Remove trailing {#...#} text in parameter string
Input dir name, output dir name with any dir info removed
'''
def unappend_dir_info(my_path):
    pattern = r' {#.*\#\}$'                           # locate text between " {# ... #}"
    return re.sub(pattern, "", my_path)

# ----------------------------------------------------------------------------------------------------------------------

'''
7. ORPHANED_FILE_TO_DIR
Remove trailing {#...#} text in parameter string
Input dir name, output dir name with any dir info removed
'''
def orphaned_file_to_dir(my_path):
    these_file_types = [".mp3", ".flac", ".m4a", ".m4b"]

    for dir_item in os.listdir(my_path):                                  # each file in folder
        if os.path.isfile(os.path.join(my_path, dir_item)):                 # files in folder
            name, ext = os.path.splitext(dir_item)                   # split name, ext
            if any(ext in file_type for file_type in these_file_types):    # files supporting tags
                file_path = (os.path.join(my_path, dir_item))
                new_file_name = file_name_from_tags(my_path,name,ext)   # construct file name
                if new_file_name == '':
                    new_file_path = file_path
                new_folder = os.path.join(my_path, new_file_name)
                if not os.path.exists(new_folder):
                    os.mkdir(new_folder)
                os.rename(file_path, os.path.join(new_folder, new_file_name + ext))

# ----------------------------------------------------------------------------------------------------------------------

'''
7. UNAPPEND_DIR_INFO
Remove trailing {#...#} text in parameter string
Input dir name, output dir name with any dir info removed
'''
def file_name_from_tags(my_path, name, ext):        # Full path, file name, extension
    from tinytag import TinyTag
    t = TinyTag.get(os.path.join(my_path, name + ext))             # Get tags for file
    artist = select_string(t.albumartist, t.artist)          # Preferentially select album artist over artist
    album = select_string(t.album, t.title)                # Preferentially select album over title
    if artist+album == '':
        file_name = name
    else:
        file_name = artist + ' - ' + album
    invalid = r'<>:":/\|?*'
    for char in invalid:
        file_name = file_name.replace(char, '')
    return file_name

# ========================================================================================================
'''
select string given 2 strings return blank if both blank, otherwise str1 if not blank, otherwise str2
'''
def select_string(str1, str2):
    if not str1 and not str2:
        return ''
    elif str1:
        return str1
    else:
        return str2

'''
Testing ...
Functions:
 2. test_count_file_types           for input dir list return list and count of each file extension
 3. clean_filenames_in_folder  for each file od specific types in folder, clean the name 
 4. clean_name                 for input file or dir name return cleaned name 
 5. append_info_to_subdirs_in_dir     for all subdirs, clean mane and append info string {#...#}
 6. append_dir_info
 7. unappend_dir_info 
'''

def test_list_dirs_files(my_path):            # list all files and subdirs recursively starting with input path

    l = list_dirs_files2(my_path, max_folder_depth=3)    # (my_file_path, max_folder_depth=-1,
    for i in l:                                          #  dirs_files='both'/'folders'/'files')
        idepth, ipath, iname, itype, isubdirs, ifiles, ifile_types = i
        if itype == 'D':
            print(f'{ipath} Sub-dirs={isubdirs}; Files={ifiles}')
        else:
            print(f'   {iname}')

# test_list_dirs_files(r'D:\logs')

def appendx(my_dir):
    append_info_to_subdirs_in_dir(my_dir,action='clean')
def append(my_dir):
    append_info_to_subdirs_in_dir(my_dir)


'''
1. LIST_DIRS_FOLDERS
params: full path to directory, max depth to walk from here, collate sub-dirs, or files, or both 
return sorted list of files and/or sub-dirs - sorting is directory depth, files, sub-dirs
'''
def list_dirs_files3(my_path, ext_list=[], max_dir_depth=-1, dirs_files='both'):
    results = []  # empty list to hold results
    for dir_item in os.walk(my_path):  # walk through passed directory structure
        dir, subdirs, files = dir_item  # returns tuple (directory, list of sub-directories, list of files)
        dir_depth = dir.count(chr(92)) - my_path.count(chr(92))  # relative folder depth (needed for sort)
        if max_dir_depth < 0 or dir_depth <= max_dir_depth:  # not exceeded max folder depth if specified

            if dirs_files != 'files':  # not files only => folder details required
                for sub_dir in subdirs:
                    results.append(os.path.join(dir, sub_dir))  # results (folder) - tuple(depth, dir)
        # now get each file in this directory and append (depth, full path.name) to results
            if dirs_files != 'dirs':  # not files only => folder details required
                for file in files:
                    results.append(os.path.join(dir, file))
    # returns list of tuples: (depth, full path.name)
    return results


# ----------------------------------------------------------------------------------------------------------------------

l=list_dirs_files3(my_path=r'H:\#4 Magazines',max_dir_depth=-1,dirs_files='both')
valid_exts = ["",".pdf", ".mobi", ".epub", ".mp3", ".flac", ".m4a", ".m4b"]

for i in l:
    root, name = os.path.split(i)
    name, ext = os.path.splitext(name)
    if ext in valid_exts:
        new_name = clean_name(name)
        if new_name != name:
            count=+1
            new_path = os.path.join(root, new_name + ext)
            # os.replace(i, new_path)
            print(f'{count}. {i} ')
            print(f'{name}{ext} => {new_name}{ext} ')


# ======
# appendx(r'D:\logs')

#clean_sub_dir_names_in_dir(r'D:\logs')

# test_list_dirs_files(r'D:\logs')

# orphaned_file_to_dir(r'D:\logs')
