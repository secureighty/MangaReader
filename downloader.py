import os
import urllib.request
from random import choice

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
]


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
        req = urllib.request.Request(url, headers={'User-Agent': choice(user_agents)})
        response = urllib.request.urlopen(req).read()
        file_obj = open(file_name, "wb")
        file_obj.write(response)
        file_obj.close()
    return file_name


def download_images(url):
    """
    download images sequentially
    :param url: base url
    :return: array of images
    """
    arr = []
    double_flag = True
    done_flag = True
    page_num = 0
    image_type = ".jpg"
    while done_flag:
        try:
            current_url = url + "/" + str(page_num) + image_type
            current_file = download_image(current_url)
            print(current_file)
            arr += [current_file]
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
                arr += [current_file]
                page_num += 1
                double_flag = True
            except (urllib.error.HTTPError, urllib.error.URLError):
                if double_flag:
                    page_num += 1
                    double_flag = False
                else:
                    done_flag = False
                    print("reached end")
    return arr


class Downloader:
    def __init__(self, cmdlist):
        self.cmdlist = cmdlist
        self.page_arr = None

    def download(self):
        self.page_arr = download_images(self.url_builder())

    def url_builder(self):
        """
        make a url out of 3 cmds
        :param cmdlist: list of commands
        :return: url
        """
        return "https://" + self.cmdlist[0] + self.cmdlist[1] + self.cmdlist[2]

