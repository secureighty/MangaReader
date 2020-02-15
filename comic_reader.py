import sys
from downloader import Downloader
from viewer import Viewer
import yaml
import os



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
    -c
    --config <config_file_location/config_file_name.yaml>

"""


def parseargs(cmds):
    """
    simple sysargv parsing
    :param cmds: args when called
    :return: list of relevant args
    """
    if len(cmds) < 2:
        return pull_from_config()
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
        if cmds[i] == "-c" or cmds[i] == "--config":
            return pull_from_config(cmds[i+1])
    return {"domain": domain, "path": path, "number": number}


def pull_from_config(file_location="config.yaml"):
    if os.path.isfile(file_location):
        with open(file_location) as file:
            return yaml.load(file, Loader=yaml.FullLoader)
    else:
        print("Missing config file. Add a valid Config.yaml or use arguments.")


def main():
    downloader = Downloader(parseargs(sys.argv))
    downloader.download()
    viewer = Viewer(downloader.page_arr, 400)
    viewer.start()


main()
