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
def list_dirs_files2(my_path, max_dir_depth=-1, dirs_files='both'):
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
            new_dir_name = clean_append_folder(os.path.join(my_path, dir_item))
            print(new_dir_name)



# ----------------------------------------------------------------------------------------------------------------------


'''CLEAN_APPEND_FOLDER
for single dir, clean dir name the add structured list of subdir count, file count, dile ext counts:
e.g. 'my folder {#d=41 f=20 pdf=6 m4b=5 rar=2 mp3=2 avi=1 json=1 mp4=1 azw3=1 mkv=1#}'
'''
def clean_append_folder(dir_path):
    dir_root, dir_name = os.path.split(dir_path)
    cleaned_dir_name = re.sub('sanet.st', '', dir_name, flags=re.IGNORECASE)    # replace sanet.st
    cleaned_dir_name = re.sub('_', ' ', cleaned_dir_name)                       # replace underscores
    cleaned_dir_name = unappend_dir_info(cleaned_dir_name)                      # remove any {#...#} info
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
    cleaned_dir_name = cleaned_dir_name.strip() + s                  # remove leading/trailing spaces and return

    new_dir_path = os.path.join(dir_root, cleaned_dir_name)
    print(new_dir_path)
    if new_dir_path != dir_path:
        print("hello1")
        os.rename(dir_path, os.path.join(dir_root, new_dir_path))
    print("hello2")
    return(new_dir_path)
# ----------------------------------------------------------------------------------------------------------------------


'''UNAPPEND_DIR_INFO_IN_FOLDER
for all sub-dirs in input folder clean, append ext info and rename
'''
def unappend_dir_info_in_folder(my_path):
    dir_items = os.listdir(my_path)                          # use os.listdir to get all items in folder
    for dir_item in dir_items:                               # loop through items in folder
        if os.path.isdir(os.path.join(my_path, dir_item)):  # for dir items only
            new_dir_name = os.path.join(my_path, clean_append_folder(os.path.join(my_path, dir_item)))
    return new_dir_name

# ----------------------------------------------------------------------------------------------------------------------

'''UNAPPEND_DIR_INFO
for all sub-dirs in input folder clean, append ext info and rename
     '          10        20       30        40        50        60        70   '
     '12345678901234567890123456789012345678901234567890123456789012345678901234567890'
text = 'logs {#d=41 f=20 pdf=6 m4b=5 rar=2 mp3=2 avi=1 json=1 mp4=1 azw3=1 mkv=1#}
'''
def unappend_dir_info(my_dir):
    pattern = r' {#.*\#\}$'                           # locate test between " {# ... #}"
    new_dir=re.sub(pattern, "", my_dir)
    return new_dir



#
# print(re.sub(text, comp_pattern, ""))
# for match in matches:
#     s, e =match.span()
#     print(match, text[s:e+1])
#
# my_path = r'D:\testwalk'
# my_path = r'D:\logs {#d=41 f=20 pdf=6 m4b=5 rar=2 mp3=2 avi=1 json=1 mp4=1 azw3=1 mkv=1#}'
# unappend_dir_info(my_path)



def test_unappend_dir_info_in_folder():
    my_dir = r'D:\testwalk'
    result = unappend_dir_info_in_folder(my_dir)
    print(result)

def test_unappend_dir_info_in_folder():
    my_dir = r'D:\testwalk'
    result = unappend_dir_info_in_folder(my_dir)
    print(result)

def test_clean_append_subdirs_in_folder():
    my_dir = r'D:\testwalk'
    clean_append_subdirs_in_folder(my_dir)


def test_clean_append_folder():
    my_dir = r'D:\testwalk'
    clean_append_folder(my_dir)


test_clean_append_subdirs_in_folder()

def list_dirs_files(my_file_path, max_folder_depth=-1, folders_files="both"):
    import os
    results = []                                # empty list to hold results
    for my_dir in os.walk(my_file_path):       # walk through passed directory structure
        root, subdirs, files = my_dir          # returns tuple (root directory, list of sub-directories, list of files)
        folder_depth = root.count(chr(92)) - my_file_path.count(chr(92))  # relative folder depth
        if max_folder_depth < 0 or folder_depth <= max_folder_depth:   # not exceeded max folder depth if specified
            if folders_files != 'files':       # folder details required
                # results.append(f'{folder_depth} {root} [{len(subdirs)}, {len(files)}]')    # add current folder & relative depth to results
                results.append((folder_depth, root, len(subdirs), len(files)))
            if folders_files != 'folders':     # file details required
                for file in files:             # for each file in current directory add file details
                    # results.append(f'{folder_depth} {os.path.join(root, file)}')
                    results.append((folder_depth, os.path, root, file))

    return sorted(results, key=lambda item: f'({item[0]}{item[1]})')


def clean_filename(filename):
    import re
    filename_lower = filename.lower
    cleaned_filename = re.sub('sanet.st', '', filename, flags=re.IGNORECASE)
    cleaned_filename = re.sub('_', ' ', cleaned_filename)
    return cleaned_filename.strip()


for item in list_dirs_files(r'D:\testwalk', folders_files='files', max_folder_depth=0):
    if os.path.isfile(item[1]):
        print(' ' * 2 * (item[0]+2), clean_filename(os.path.basename((item[1]))))
    else:
        print(' ' * 2 * (item[0]), (item[1]), item[2], item[3])