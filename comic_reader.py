import sys
import os
import urllib.request

from viewer import Viewer



"""
Advertisementless comic reader
AT
20191223

usage:

comic_reader.py
    -d
    --domain <domain specifically for images (i.whatever.net)>
    -p
    --path <path after domain (/galleries/)>
    -n
    --number <comic number>

"""


def parseargs(cmds):
    """
    simple sysargv parsing
    :param cmds: args when called
    :return: list of relevant args
    """
    domain = ""
    path = ""
    number = ""
    ltr = False
    for i in range (0, len(cmds)-1):
        if cmds[i] == "-d" or cmds[i] == "--domain":
            domain = cmds[i+1]
        if cmds[i] == "-p" or cmds[i] == "--path":
            path = cmds[i+1]
        if cmds[i] == "-n" or cmds[i] == "--number":
            number = str(cmds[i+1])
    return [domain, path, number]


def url_builder(cmdlist):
    """
    make a url out of 3 cmds
    :param cmdlist: list of commands
    :return: url
    """
    return "https://" + cmdlist[0] + cmdlist[1] + cmdlist[2]


def download_image(url):
    """
    download a single image
    :param url: image to download
    :return: name of file
    """
    file_name = "images/" + url.replace(":", "")
    folder_name = file_name[:file_name.rfind("/")]
    file_exists = os.path.isfile(file_name)
    folder_exists = os.path.isdir(folder_name)
    if not file_exists:
        if not folder_exists:
            os.makedirs(folder_name)
        urllib.request.urlretrieve(url, file_name)
    return file_name


def download_images(url, dict=[], double_flag=True, done_flag=True, page_num=0, image_type=".jpg"):
    """
    download images sequentially
    :param url: base url
    :param dict: array of images
    :param double_flag: was last a double?
    :param done_flag: are we not done?
    :param page_num: number at end of url
    :param image_type: png or jpg?
    :return: array of images
    """
    while done_flag:
        try:
            current_url = url + "/" + str(page_num) + image_type
            current_file = download_image(current_url)
            print(current_file)
            dict += [current_file]
            page_num += 1
            double_flag = True
        except (urllib.error.HTTPError, urllib.error.URLError):
            try:
                if image_type == ".jpg":
                    image_type = ".png"
                else:
                    image_type = ".jpg"
                current_url = url + "/" + str(page_num) + image_type
                current_file = download_image(current_url)
                print(current_file)
                dict += [current_file]
                page_num += 1
                double_flag = True
            except (urllib.error.HTTPError, urllib.error.URLError):
                if double_flag:
                    dict += [None]
                    page_num += 1
                    double_flag = False
                else:
                    done_flag = False
                    print("reached end")
    return dict


def main():
    page_dict = download_images(url_builder(parseargs(sys.argv)))
    viewer = Viewer(page_dict, 400)
    viewer.start()


main()
