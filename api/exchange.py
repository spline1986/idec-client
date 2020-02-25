import base64
import requests
import sys
import urllib.parse
import urllib.request
from api import base
from api import idec_filter
from api import fecho


def split(l, size=40):
    "Split list to list of lists of 40 items."
    for i in range(0, len(l), size):
        yield l[i:i+size]


def download_index(node, echoareas, depth):
    "Download echoareas index from uplink."
    print("download echoareas index")
    ids = []
    if depth == 0:
        r = urllib.request.Request(
            "{0}u/e/{1}".format(node, "/".join(echoareas))
        )
    else:
        r = urllib.request.Request(
            "{0}u/e/{1}/-{2}:{3}".format(node, "/".join(echoareas),
                                         depth, depth)
        )
    try:
        with urllib.request.urlopen(r) as f:
            raw = f.read().decode("utf-8").split()
            ids = [msgid for msgid in raw if idec_filter.is_msgid(msgid)]
    except urllib.error.URLError:
        print("cannot connect to uplink")
        sys.exit(1)
    return ids


def build_diff(local, remote):
    "Return diff of local and remote index."
    return [i for i in remote if i not in local]


def download_bundle(node, msgids):
    "Download messages bundle from uplink."
    bundle = []
    print("fetch: {0}u/m/{1}".format(node, "/".join(msgids)))
    r = urllib.request.Request("{0}u/m/{1}".format(node, "/".join(msgids)))
    try:
        with urllib.request.urlopen(r) as f:
            bundle = f.read().decode("utf-8").split()
    except urllib.error.URLError:
        print("cannot connect to uplink")
        sys.exit(1)
    return bundle


def download_mail(node, echoareas, depth):
    "Download echomail."
    index = build_diff(list(base.read_local_index(echoareas)),
                       download_index(node, echoareas, depth))
    if len(index) == 0:
        print("new messages not found")
    for s in split(index):
        base.debundle(download_bundle(node, s))


def read_local_fileindex(fechoareas):
    "Read local index of fileechoareas."
    for fechoarea in fechoareas:
        for f in fecho.read_fechoarea(fechoarea):
            yield f


def download_fecho_index(node, fechoareas, depth):
    "Download index of fileechoareas from uplink."
    print("download file echoareas index")
    ids = []
    if depth == 0:
        r = urllib.request.Request(
            "{0}f/e/{1}".format(node, "/".join(fechoareas))
        )
    else:
        r = urllib.request.Request(
            "{0}f/e/{1}/-{2}:{3}".format(node, "/".join(fechoareas),
                                         depth, depth)
        )
    with urllib.request.urlopen(r) as f:
        raw = f.read().decode("utf-8").split("\n")
        fechoarea = ""
        for line in raw:
            if ":" not in line:
                fechoarea = line
            else:
                if len(line) > 0:
                    ids.append([fechoarea, line])
    return ids


def download_file(node, fechoarea, fid):
    "Download file from uplink."
    frow = fid.split(":")
    print("download: {0}f/f/{1}/{2} {3}".format(node, fechoarea,
                                                frow[0], frow[1]))
    r = urllib.request.Request(
        "{0}f/f/{1}/{2}".format(node, fechoarea, frow[0])
    )
    out = urllib.request.urlopen(r)
    fecho.save_file(fechoarea, frow, out)


def download_filemail(node, fileechoareas, depth):
    "Fownload fileecho mail."
    index = build_diff(list(read_local_fileindex(fileechoareas)),
                                download_fecho_index(node, fileechoareas, depth))
    if len(index) == 0:
        print("new files not found")
    for s in index:
        download_file(node, s[0], s[1])


def c_x(r):
    counts = {}
    try:
        with urllib.request.urlopen(r) as f:
            for line in f.read().decode("utf8").split():
                count = line.split(":")
                if len(count) == 2:
                    counts[count[0]] = int(count[1])
    except urllib.error.URLError:
        print("cannot connect to uplink")
    return counts


def download_counts(node, echoareas, fechoareas):
    r = urllib.request.Request("{0}x/c/{1}".format(node, "/".join(echoareas)))
    counts = c_x(r)
    r = urllib.request.Request("{0}f/c/{1}".format(node, "/".join(fechoareas)))
    fcounts = c_x(r)
    return (counts, fcounts)

def send_mail(node, auth):
    "Send outgoing messages to server."
    tossed = list(base.get_tossed_list())
    n = 1
    count = len(tossed)
    for msg in tossed:
        print("send message {}/{}".format(n, count))
        data = {}
        data["pauth"] = auth
        data["tmsg"] = base.get_tossed(msg)
        data = urllib.parse.urlencode(data).encode("utf8")
        req = urllib.request.Request(node + "u/point", data=data)
        urllib.request.urlopen(req)
        base.remove_tossed(msg)
        n += 1


def send_file(node, pauth, fechoarea, dsc, f):
    data = {}
    files = {}
    data["pauth"] = pauth
    data["fecho"] = fechoarea
    data["dsc"] = dsc
    filename = f.filename
    files["file"] = (filename, f.file)
    print("sending {}".format(filename))
    r = requests.post(node + "f/p", data=data, files=files)
    return r.text


def download_echolist(node):
    r = urllib.request.Request("{}/list.txt".format(node))
    try:
        with urllib.request.urlopen(r) as f:
            lines = f.read().decode("utf-8")
            for line in lines.split("\n"):
                if len(line) > 0:
                    yield line.split(":")
    except urllib.error.URLError:
        return []


def download_fecholist(node):
    r = urllib.request.Request("{}/f/list.txt".format(node))
    try:
        with urllib.request.urlopen(r) as f:
            lines = f.read().decode("utf-8")
            for line in lines.split("\n"):
                if len(line) > 0:
                    yield line.split(":")
    except urllib.error.URLError:
        return []
