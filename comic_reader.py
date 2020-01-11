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
    return "https://" + cmdlist[0] + cmdlist[1] + cmdlist[2]


def download_image(url):
    file_name = "images/" + url.replace(":", "")
    folder_name = file_name[:file_name.rfind("/")]
    file_exists = os.path.isfile(file_name)
    folder_exists = os.path.isdir(folder_name)
    if not file_exists:
        if not folder_exists:
            os.makedirs(folder_name)
        urllib.request.urlretrieve(url, file_name)
    return file_name

#
# def download_images_recur(url, accum_page_number=0, flag=True, dict={}):
#     '''
#     tail recursively download all images
#     :param url: url for comic
#     :param accum_page_number: the page number to download
#     :param flag: was last page not a double?
#     :param dict: a dictionary of all page numbers to their file names
#     :return: a dictionary of all page numbers to their file names
#     '''
#     try:
#         current_url = url + "/" + str(accum_page_number) + ".jpg"
#         current_file = download_image(current_url)
#         print(current_file)
#         dict[accum_page_number] = current_file
#         return download_images(url, accum_page_number+1, True)
#     except (urllib.error.HTTPError, urllib.error.URLError):
#         try:
#             current_url = url + "/" + str(accum_page_number) + ".png"
#             current_file = download_image(current_url)
#             print(current_file)
#             dict[accum_page_number] = current_file
#             return download_images(url, accum_page_number+1, True)
#         except (urllib.error.HTTPError, urllib.error.URLError):
#             if flag:
#                 dict[accum_page_number] = None
#                 return download_images(url, accum_page_number+1, False)
#             else:
#                 print("reached end")
#                 return dict
#


def download_images(url, dict=[], double_flag=True, done_flag=True, page_num=0, image_type=".jpg"):
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
