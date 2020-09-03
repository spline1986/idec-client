import json
import re
import time
from os import path, makedirs

config = {}


def load_config():
    "Load config json-file to config variable."
    global config
    try:
        with open("config.json") as f:
            config = json.loads(f.read())
        if not "node" in config:
            config["node"] = ""
        if not "auth" in config:
            config["auth"] = ""
        if not "depth" in config:
            config["depth"] = 0
        if not "fdepth" in config:
            config["fdepth"] = 0
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
    with open("config.json", "w") as f:
        f.write(json.dumps(config, sort_keys=True, indent=4, ensure_ascii=False))


def formatted_time(timestamp):
    "Return formatted time by unix timestamp."
    return time.strftime("%d.%m.%Y %H:%M UTC", time.gmtime(int(timestamp)))


def list_formatted_time(timestamp):
    "Return date by unix timestamp."
    return time.strftime("%d.%m.%Y", time.gmtime(int(timestamp)))


def save_counts(counts):
    "Save counts to file."
    with open("counts.json", "w") as f:
        f.write(json.dumps(counts, sort_keys=True, indent=4))


def calculate_depth(local, remote):
    "Calculate request depth."
    depth = 0
    new_echoarea = False
    for echoarea in remote:
        try:
            if remote[echoarea] > local[echoarea]:
                tdepth = remote[echoarea] - local[echoarea]
                if tdepth > depth:
                    depth = tdepth
        except KeyError:
            new_echoarea = True
    if new_echoarea and depth < config["depth"]:
        depth = config["depth"]
    return depth


def calculate_counts(remote):
    "Calculate counts for echoareas and fileechoareas."
    try:
        with open("counts.json") as f:
            local = json.loads(f.read())
        depth = calculate_depth(local["echoareas"], remote["echoareas"])
        fdepth = calculate_depth(local["fechoareas"], remote["fechoareas"])
        if depth == 0:
            depth = -1
        if fdepth == 0:
            fdepth = -1
        return depth, fdepth
    except json.JSONDecodeError:
        return config["depth"], config["fdepth"]
    except FileNotFoundError:
        save_counts(remote)
        return config["depth"], config["fdepth"]


def body_render(body):
    "Render message body to html."
    body = body.strip()
    body = body.replace("<", "&lt;").replace(">", "&gt;")
    rr = re.compile("((^|\n)(PS|P.S|ps|ЗЫ|З.Ы|\/\/|#).*)")
    body = rr.sub(r"<span class='comment'>\1</span>", body)
    rr = re.compile("((http|https|ftp):\/\/[a-z_0-9\-.:]+(\/[^ \t<>\n\r]+)?\/?)")
    body = rr.sub(r"<a target='_blank' href='\1'>\1</a>", body)
    rr = re.compile("(ii:\/\/)([a-z0-9_!.-]{1,60}\.[a-z0-9_!.-]{1,59}[a-z0-9_!-])")
    body = rr.sub(r"<a href='/\2'>ii://\2</a>", body)
    rr = re.compile("(ii:\/\/)([a-z0-9A-Z]{20})")
    body = rr.sub(r"<a href='/\2'>ii://\2</a>", body)
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
    "Initials by To field."
    to = to.split()
    if len(to) == 1:
        return to[0]
    else:
        i = ""
        for word in to:
            i = i + word[0]
        return i


def quoter(text, fr):
    "Qute message."
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
    "Build short message body for main page."
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
