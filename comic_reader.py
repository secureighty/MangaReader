import sys
from downloader import Downloader
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


def main():
    downloader = Downloader(parseargs(sys.argv))
    downloader.download()
    viewer = Viewer(downloader.page_arr, 400)
    viewer.start()


main()
