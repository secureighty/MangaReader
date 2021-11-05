import os
import requests
from random import choice

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
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
        req = requests.get(url, headers={'User-Agent': choice(user_agents)})
        if req.status_code == 404:
            raise FileNotFoundError
        response = req.content
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
        except (FileNotFoundError):
            try:
                if image_type == ".jpg":
                    image_type = ".png"
                else:
                    image_type = ".jpg"
                current_url = url + "/" + str(page_num) + image_type
                print("trying:"+current_url)
                current_file = download_image(current_url)
                print(current_file)
                arr += [current_file]
                page_num += 1
                double_flag = True
            except (FileNotFoundError):
                if double_flag:
                    page_num += 1
                    double_flag = False
                else:
                    done_flag = False
                    print("reached end")
    return arr


class Downloader:
    def __init__(self, cmddict):
        self.cmddict = cmddict
        self.page_arr = None

    def download(self):
        self.page_arr = download_images(self.url_builder())

    def url_builder(self):
        """
        make a url out of 3 cmds
        :param cmdlist: list of commands
        :return: url
        """
        return "https://" + self.cmddict.get("domain") + self.cmddict.get("path") + str(self.cmddict.get("number"))
