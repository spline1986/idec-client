import api
import base64
import hashlib
import os
from shutil import copyfile


def fechoarea_count(fechoarea):
    "Return files count in fileechoarea."
    try:
        return len(open(f"fecho/{fechoarea}.txt", "r").read().strip().split("\n"))
    except FileNotFoundError:
        return 0


def read_fechoarea(fechoarea):
    "Return fileechoarea index."
    try:
        for line in open(f"fecho/{fechoarea}.txt").read().strip().split("\n"):
            yield [fechoarea, line]
    except FileNotFoundError:
        return []


def save_file(fecho, frow, out):
    "Save file and metainformation to base."
    file_size = 0
    block_size = 8192
    if not os.path.exists(f"fecho/{fecho}"):
        os.mkdir(f"fecho/{fecho}")
    f = open("fecho/{0}/{1}".format(fecho, frow[1]), "wb")
    while True:
        buffer = out.read(block_size)
        if not buffer:
            break
        file_size += len(buffer)
        f.write(buffer)
    f.close()
    open(f"fecho/{fecho}.txt", "a").write(":".join(frow) + "\n")
    open("newfiles.txt", "a").write("{}:{}:{}\n".format(fecho, frow[1], frow[4]))


def get_file_hashs(fileechoarea):
    "Return fids of fileechoarea."
    files = []
    try:
        files = open("fecho/{}".format(fileechoarea)).read().split("\n")
    except FileNotFoundError:
        None
    return [f.split(":")[0] for f in files]
