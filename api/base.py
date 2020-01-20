import os
import base64


def check_file(filename):
    "Check file exists and create if not."
    if not os.path.exists(filename):
        open(filename, "w")


def check_dir(dirname):
    "Check directory exists and create if not."
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def check_base():
    "Check base and needed files."
    check_dir("echo")
    check_dir("msg")
    check_dir("fecho")


def echoarea_count(echoarea):
    "Return messages count in echoarea."
    return len(read_echoarea(echoarea))


def read_echoarea(echoarea):
    "Return echoarea index."
    try:
        with open(f"echo/{echoarea}") as echofile:
            return echofile.read().strip().split("\n")
    except FileNotFoundError:
        return []


def read_last_message(echoarea):
    "Return last message in echoarea."
    try:
        with open(f"echo/{echoarea}") as echofile:
            msgid = echofile.read().split()[-1]
    except FileNotFoundError:
        return "", []
    try:
        with open(f"msg/{msgid}") as msgfile:
            return msgid, msgfile.read().split("\n")
    except FileNotFoundError:
        return "", []


def read_messages_by_page(echoarea, page, onpage):
    msgids = read_echoarea(echoarea)
    page -= 1
    msgids = msgids[page * onpage:(page + 1) * onpage]
    for msgid in msgids:
        message = read_message(msgid).split("\n")
        message.insert(0, msgid)
        yield message


def read_local_index(echoareas):
    "Read local echoareas index."
    for echoarea in echoareas:
        for msgid in read_echoarea(echoarea):
            yield msgid


def read_message(msgid):
    "Return raw message."
    try:
        with open(f"msg/{msgid}") as msgfile:
            return msgfile.read()
    except FileNotFoundError:
        return None


def save_message(echoarea, msgid, message):
    "Save message to base."
    with open(f"echo/{echoarea}", "a") as echofile:
        echofile.write(f"{msgid}\n")
    with open(f"msg/{msgid}", "w") as msgfile:
        msgfile.write(message)
    with open("newmessages.txt", "a") as new:
        new.write(msgid + "\n")


def debundle(echoarea, bundle):
    "Unpack messages bundle."
    bundle = bundle.split()
    for row in bundle:
        vals = row.split(":")
        message = base64.urlsafe_b64decode(vals[1]).decode("utf-8")
        save_message(echoarea, vals[0], message)


def next_out():
    try:
        with open("out/last") as last:
            n = int(last.read())
        with open("out/last", "w") as last:
            last.write(str(n+1))
        return "{:0>5d}".format(n)
    except FileNotFoundError:
        with open("out/last", "w") as last:
            last.write("1")
        return "00000"


def save_out(echoarea, to, subj, body):
    "Save outgoing message to base."
    msg = "\n".join([echoarea, to, subj, "", body])
    filename = next_out()
    with open("out/{}.txt".format(filename), "w") as out:
        out.write(msg)
    encoded = base64.b64encode(msg.encode())
    with open("out/{}.toss".format(filename), "w") as toss:
        toss.write(encoded.decode())


def get_tossed_list():
    "Return filenames of tossed messages."
    files = os.listdir("out/")
    files.sort()
    for f in files:
        if f.endswith(".toss"):
            yield f


def get_tossed(i):
    "Return tossed message."
    with open("out/{}".format(i)) as tossed:
        return tossed.read()


def remove_tossed(i):
    "Remove tossed message."
    os.remove("out/{}".format(i))
