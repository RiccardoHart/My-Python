import os
import re
'''
'''
def list_dirs_files(my_file_path, max_folder_depth=-1, folders_files="both"):
    results = []                               # empty list to hold results
    for my_dir in os.walk(my_file_path):       # walk through passed directory structure
        root, subdirs, files = my_dir          # returns tuple (root directory, list of sub-directories, list of files)
        folder_depth = root.count(chr(92)) - my_file_path.count(chr(92))  # relative folder depth
        if max_folder_depth < 0 or folder_depth <= max_folder_depth:   # not exceeded max folder depth if specified
            if folders_files != 'files':       # folder details required
                file_exts = set()              # empty set for file extensions in sub-dir
                for file in files:             # add unique ext to set
                    set.add(file_exts, os.path.splitext(file)[1])
                file_types = []
                for ext in file_exts:
                    count = 0
                    for file in files:
                        if os.path.splitext(file)[1] == ext:
                            count += 1
                    file_types.append((ext, count))
                results.append((folder_depth, root, "", "D", len(subdirs), len(files), file_types))
            if folders_files != 'folders':     # file details required
                for file in files:             # for each file in current directory add file details
                     results.append((folder_depth, root, file, "F", "", "", ""))
    return sorted(results, key=lambda item: f'({item[0]}{item[1]})')
# ----------------------------------------------------------------------------------------------------------------------
'''
 simplified directory walk. os.walk returns tuples of (dir, list of sub-dirs, list of files)
 in results() save (dir depth, dir name), then (dir depth, file name)
 this gives a list of top dir/files; sub-dirs/files
 sort by (dir depth) + (dir name / file name) to return hierarchical and alphabetic order
'''
def list_dirs_files2(my_path, max_dir_depth=-1, dirs_files="both"):
    results = []                               # empty list to hold results
    for my_dir in os.walk(my_path):            # walk through passed directory structure
        dir, subdirs, files = my_dir           # returns tuple (directory, list of sub-directories, list of files)
        dir_depth = dir.count(chr(92)) - my_path.count(chr(92)) # relative folder depth (needed for sort)
        results.append((dir_depth, dir))       # results (folder) - tuple(depth, dir)
        # now get each file in this directory and append (depth, full path.name) to results
        for file in files:                     # add unique ext to set
            results.append((dir_depth, os.path.join(dir, file)))

    return sorted(results, key=lambda item: f'({item[0]}{item[1]})')
# ----------------------------------------------------------------------------------------------------------------------


'''
input - file path; for each file in this folder create a dictionary to hold number of each file extension
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
    return results                                           # return dictionary [(.txt: 3; .pdf: 4)] etc.
# ----------------------------------------------------------------------------------------------------------------------


# dir_walk = list_dirs_files2(r'D:\logs')
# for item in dir_walk:
#     print(item)

'''CLEAN_FILE_NAMES_IN_FOLDER
input filename only, perform various cleaning actions and return cleaned filename
    use regex to find and replace target sub-strings, regardless of case
    replace underscores with space
    remove leading and trailing spaces
'''
def clean_filenames_in_folder(my_path):
    valid_exts =[".pdf", ".mobi", ".epub", ".mp3", ".flac", ".m4a", ".m4b"]
    dir_items = os.listdir(my_path)                          # use os.listdir to get all items in folder
    for dir_item in dir_items:
        if os.path.isfile(os.path.join(my_path, dir_item)):
            filename, ext = os.path.splitext(dir_item)
            if ext in valid_exts:
                cleaned_filename = clean_filename(filename)
                print(filename, "====", cleaned_filename)
# ----------------------------------------------------------------------------------------------------------------------


'''CLEAN_FILENAME
input filename (without ext), perform various cleaning actions and return cleaned filename
    use regex to find and replace target sub-strings, regardless of case
    replace underscores with space
    remove leading and trailing spaces
'''
def clean_filename(raw_filename):
    cleaned_filename = re.sub('sanet.st', '', raw_filename, flags=re.IGNORECASE)
    cleaned_filename = re.sub('_', ' ', cleaned_filename)
    return cleaned_filename.strip()
# ----------------------------------------------------------------------------------------------------------------------

'''CLEAN_APPEND_SUBDIRS_IN_FOLDER
for all sub-dirs in input folder clean, append ext info and rename
'''
def clean_append_subdirs_in_folder(my_path):
    dir_items = os.listdir(my_path)                          # use os.listdir to get all items in folder
    for dir_item in dir_items:                               # loop through items in folder
        if os.path.isdir(os.path.join(my_path, dir_item)):  # for dir items only
            new_dir_name = os.path.join(my_path, clean_append_folder(os.path.join(my_path, dir_item)))
            os.replace(os.path.join(my_path, dir_item), new_dir_name)
    return new_dir_name

# ----------------------------------------------------------------------------------------------------------------------


'''CLEAN_APPEND_FOLDER
for single dir, clean dir name the add structured list of subdir count, file count, dile ext counts:
e.g. 'my folder {#d=41 f=20 pdf=6 m4b=5 rar=2 mp3=2 avi=1 json=1 mp4=1 azw3=1 mkv=1#}'
'''
def clean_append_folder(dir_path):
    cleaned_dir_path = re.sub('sanet.st', '', dir_path, flags=re.IGNORECASE)    # replace sanet.st
    cleaned_dir_path = re.sub('_', ' ', cleaned_dir_path)                       # replace underscores
    count_dirs, count_files =(0, 0)                                             # initialise subdir, file count
    for item in os.listdir(dir_path):                                           #
        if os.path.isdir(os.path.join(dir_path, item)):                         # if file
            count_files += 1                                                    # count files
        else:
            count_dirs += 1                                                     # count subdirs
    file_types = count_file_types(dir_path)
#   sort by extensions alphabetically
    file_types_sorted = sorted(file_types.items(), key = lambda item: item[1], reverse=True)
    s = f'd={count_dirs} f={count_files} '               # construct d=41 f=20 counts
    for ext, count in file_types_sorted:                 # for each extension
        s = s + f'{ext[1:]}={count} '                    # append extension and count
    s = ' {#' + s[:-1] + '#}'                            # append {# ... #} labels
    return cleaned_dir_path.strip() + s                  # remove leading/trailing spaces and return
# ----------------------------------------------------------------------------------------------------------------------



my_path = r'D:\testwalk'
clean_append_subdirs_in_folder(my_path)











