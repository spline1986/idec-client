import json
import re
import time
from os import path, makedirs

config = {}


def check_dir(directory):
    "Check and create directory."
    if not path.exists(directory):
        makedirs(directory)


def check_file(filename):
    "Check and create file."
    if not path.exists(filename):
        open(filename, "w")


def check_base():
    "Check base and needed files."
    check_dir("echo")
    check_dir("msg")
    check_dir("out")
    check_dir("fecho")
    check_file("config.json")


def load_config():
    "Load config json-file to config variable."
    global config
    try:
        with open("config.json", "r") as config_file:
            config = json.loads(config_file.read())
        if not "node" in config:
            config["node"] = ""
        if not "auth" in config:
            config["auth"] = ""
        if not "depth" in config:
            config["depth"] = 50
        if not "echoareas" in config:
            config["echoareas"] = []
        if not "fechoareas" in config:
            config["fechoareas"] = []
        if not "template" in config:
            config["template"] = "photon"
    except json.JSONDecodeError:
        print("Load config error.")


def save_config():
    "Save config json-file from config variable."
    global config
    with open("config.json", "w") as config_file:
        config_file.write(json.dumps(config, sort_keys=True, indent=4))


def formatted_time(timestamp):
    "Return formatted time by unix timestamp."
    return time.strftime("%d.%m.%Y %H:%M UTC", time.gmtime(int(timestamp)))


def body_render(body):
    body = body.strip()
    body = body.replace("<", "&lt;").replace(">", "&gt;")
    rr = re.compile("((^|\n)(PS|P.S|ps|ЗЫ|З.Ы|\/\/|#).*)")
    body = rr.sub(r"<span class='comment'>\1</span>", body)
    rr = re.compile("((http|https|ftp):\/\/[a-z_0-9\-.:]+(\/[^ \t<>\n\r]+)?\/?)")
    body = rr.sub(r"<span class='url'><a target='_blank' href='\1'><i class='fa fa-link'></i> \1</a></span>", body)
    rr = re.compile("(ii:\/\/)([a-z0-9_!.-]{1,60}\.[a-z0-9_!.-]{1,59}[a-z0-9_!-])")
    body = rr.sub(r"<i class='fa fa-plane iilink'></i>&nbsp;<a class='iilink' href='\2'>\2</a>", body)
    rr = re.compile("(ii:\/\/)([a-z0-9A-Z]{20})")
    body = rr.sub(r"<i class='fa fa-envelope iilink'></i>&nbsp;<a class='iilink' href='\2'>\2</a>", body)
    rr = re.compile("((^|\n)(== ).+)")
    body = rr.sub(r"<b class='title'>\1</b>", body)
    rr = re.compile("((^|\n)----)")
    body = rr.sub(r"<hr>", body)
    rr = re.compile("((^|\n)(\+\+\+).*)")
    body = rr.sub(r"<span class='origin'>\1</span>", body)
    body = "<br>\n".join(body.split("\n"))
    txt = ""; pre = 0
    for line in body.split("\n"):
        rr = re.compile("((^|\n)[a-zA-Zа-яА-Я0-9_-]{0,20}(&gt;){1,20}.+)")
        try:
            count = line[0:rr.match(line).span()[1]].count("&gt;")
        except AttributeError:
            count = 0
        if count > 0:
            if count % 2 == 1:
                line = rr.sub(r"<span class='quote1'>\1</span>", line)
            else:
                line = rr.sub(r"<span class='quote2'>\1</span>", line)
        if line.startswith("====") and pre == 0:
            pre = 1
            txt += "<pre>====\n"
        elif line.startswith("====") and pre == 1:
            pre = 0
            txt += "====</pre>\n"
        elif pre == 1:
            txt += line.replace("<br>", "") + "\n"
        else:
            txt += line + "\n"
    txt = txt.replace("(:[:", "<").replace(":]:)",">")
    return txt


def initials(to):
    to = to.split()
    if len(to) == 1:
        return to[0]
    else:
        i = ""
        for word in to:
            i = i + word[0]
        return i


def quoter(text, fr):
    rr = re.compile(r"[a-zA-Zа-яА-Я0-9_\(\)-]{0,20}>{1,20}")
    for line in text:
        if rr.match(line):
            if line[rr.match(line).span()[1]] == " ":
                quoter = ">"
            else:
                quoter = "> "
            yield (line[:rr.match(line).span()[1]] + quoter +
                   line[rr.match(line).span()[1]:])
        elif line != "":
            yield "{}> {}".format(fr, line)
        else:
            yield ""


def short_body(lines, msgid):
    body = []
    n = 0
    for line in lines:
        words = line.split()
        r = []
        for word in words:
            r.append(word)
            n += 1
            if n == 200:
                r[-1] = r[-1] + "..."
                body.append(" ".join(r))
                body.append("")
                body.append("(:[:a target='_blank' href='/{}':]:)Читать далее(:[:/a:]:)".format(msgid))
                break
        if n == 200:
            break
        body.append(" ".join(r))
    return body
