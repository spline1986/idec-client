#!/usr/bin/env python3

import api
import os
from api import base
from api import exchange
from api import fecho
from api import idec_filter
from bottle import Request, post, redirect, request, route, run, static_file
from bottle import template
from math import floor

@route("/")
def index():
    "Index page function."
    api.load_config()
    messages = []
    for message in base.read_last_messages():
        msgid, msg = message[0], message[1:][0]
        msg[2] = api.formatted_time(msg[2])
        msg[8:] = api.short_body(msg[8:], msgid)
        msg.insert(0, msgid)
        messages.append(msg)
    return template("tpl/{}/index.tpl".format(api.config["template"]),
                    echoareas=api.config["echoareas"], messages=messages,
                    fechoareas=api.config["fechoareas"],
                    template=api.config["template"])


@route("/new")
def newmessages():
    "New messages page function."
    api.load_config()
    with open("newmessages.txt") as new:
        msgids = new.read().split()
    messages = []
    for msgid in msgids:
        msg = base.read_message(msgid).split("\n")
        msg.insert(0, msgid)
        msg[3] = api.formatted_time(msg[3])
        messages.append(msg)
    files = []
    with open("newfiles.txt") as new:
        for line in new.read().split("\n"):
            if len(line) > 0:
                f = line.split(":")
                files.append([f[0], f[1], ":".join(f[2:])])
    files.sort(key = lambda x: x[0])
    return template("tpl/{}/new.tpl".format(api.config["template"]),
                    echoareas=api.config["echoareas"], messages=messages,
                    files=files, fechoareas=api.config["fechoareas"],
                    template=api.config["template"])


def check_pages(pages):
    if int(pages) < pages:
        pages = int(pages) + 1
    else:
        pages = int(pages)
    return pages


def check_echoarea(echoarea):
    for echo in api.config["echoareas"]:
        if echo[0] == echoarea:
            echoarea = echo
            break
    else:
        echoarea = [echoarea, ""]
    return echoarea


@route("/<e1>.<e2>")
@route("/<e1>.<e2>/<page>")
def echo_reader(e1, e2, page=False):
    "Echoarea reader function."
    api.load_config()
    echoarea = "{}.{}".format(e1, e2)
    pages = check_pages(base.echoarea_count(echoarea) / 25)
    if not page:
        page = pages
    else:
        page = int(page)
    messages = []
    for msg in base.read_messages_by_page(echoarea, page, 25):
        msg[3] = api.formatted_time(msg[3])
        messages.append(msg)
    echoarea = check_echoarea(echoarea)
    return template("tpl/{}/echoarea.tpl".format(api.config["template"]),
                    echo=echoarea, echoareas=api.config["echoareas"],
                    fechoareas=api.config["fechoareas"], messages=messages,
                    pages=pages, page=page, paginator_path="",
                    template=api.config["template"])


@route("/list/<e1>.<e2>")
@route("/list/<e1>.<e2>/<page>")
def messages_list(e1, e2, page=False):
    "Echoarea messages list function"
    api.load_config()
    echoarea = "{}.{}".format(e1, e2)
    pages = check_pages(base.echoarea_count(echoarea) / 50)
    if not page:
        page = pages
    else:
        page = int(page)
    messages = []
    for msg in base.read_messages_list(echoarea, page, 50):
        msg[4] = api.list_formatted_time(msg[4])
        messages.append(msg)
    echoarea = check_echoarea(echoarea)
    return template("tpl/{}/list.tpl".format(api.config["template"]),
                    echo=echoarea, echoareas=api.config["echoareas"],
                    fechoareas=api.config["fechoareas"], messages=messages,
                    pages=pages, page=page, paginator_path="list/",
                    template=api.config["template"])


@route("/<msgid>")
def message_reader(msgid):
    "Message reader function."
    api.load_config()
    msg = base.read_message(msgid)
    if msg :
        msg = msg.split("\n")
        msg[2] = api.formatted_time(msg[2])
    return template("tpl/{}/message.tpl".format(api.config["template"]),
                    echoareas=api.config["echoareas"], msgid=msgid,
                    fechoareas=api.config["fechoareas"], message=msg,
                    template=api.config["template"])


@route("/new_message/<echoarea>")
def new_message(echoarea):
    "New message function."
    api.load_config()
    if idec_filter.is_echoarea(echoarea):
        return template("tpl/{}/new_message.tpl".format(api.config["template"]),
                        echoareas=api.config["echoareas"], echo=echoarea,
                        fechoareas=api.config["fechoareas"], body="", subj="",
                        repto="", to="All", template=api.config["template"])


@route("/reply/<echoarea>/<msgid>")
def new_message(echoarea, msgid):
    "Reply function."
    api.load_config()
    if idec_filter.is_echoarea(echoarea) and idec_filter.is_msgid(msgid):
        msg = base.read_message(msgid).split("\n")
        fr = msg[3]
        initials = api.initials(msg[3])
        subj = msg[6]
        if not subj.startswith("Re: "):
            subj = "Re: " + subj
        msg = api.quoter(msg[8:], initials)
        return template("tpl/{}/new_message.tpl".format(api.config["template"]),
                        echoareas=api.config["echoareas"], echo=echoarea,
                        fechoareas=api.config["fechoareas"],
                        body="\n".join(msg), subj=subj, to=fr, repto=msgid,
                        template=api.config["template"])


@route("/fecho/<fechoarea>")
def fechoarea(fechoarea):
    "Fileechoarea function."
    api.load_config()
    files = []
    for f in fecho.read_fechoarea(fechoarea):
        files.append(f[1].split(":"))
    files.sort(key=lambda x: x[1].lower())
    return template("tpl/{}/fechoarea.tpl".format(api.config["template"]),
                    echoareas=api.config["echoareas"],
                    fechoareas=api.config["fechoareas"],
                    fechoarea=fechoarea, files=files,
                    template=api.config["template"])


@route("/send_file")
def send_file():
    "Send file function."
    api.load_config()
    return template("tpl/{}/send_file.tpl".format(api.config["template"]),
                    echoareas=api.config["echoareas"],
                    fechoareas=api.config["fechoareas"],
                    template=api.config["template"])


@route("/settings")
def settings():
    "Settings function."
    api.load_config()
    templates = os.listdir("tpl")
    templates.sort()
    remote_echolist = list(exchange.download_echolist(api.config["node"]))
    remote_fecholist = list(exchange.download_fecholist(api.config["node"]))
    return template("tpl/{}/settings.tpl".format(api.config["template"]),
                    config=api.config, templates=templates,
                    remote_echolist=remote_echolist,
                    remote_fecholist=remote_fecholist)


@route("/search")
def search():
    "Search function."
    api.load_config()
    return template("tpl/{}/search.tpl".format(api.config["template"]),
                    template=api.config["template"],
                    echoareas=api.config["echoareas"],
                    fechoareas=api.config["fechoareas"],
                    messages=False, echoarea=False, text=False)


@post("/search_result")
def search_result():
    "Search results function."
    api.load_config()
    echoarea = request.forms.getunicode("echoarea")
    text = request.forms.getunicode("text")
    result = base.search(echoarea, text)
    messages = []
    for message in result:
        msgid, msg = message[0], message[1:][0]
        msg[2] = api.formatted_time(msg[2])
        msg[8:] = api.short_body(msg[8:], msgid)
        messages.append([msgid, msg])
    return template("tpl/{}/search.tpl".format(api.config["template"]),
                    echoareas=api.config["echoareas"], messages=messages,
                    fechoareas=api.config["fechoareas"],
                    template=api.config["template"], echoarea=echoarea,
                    text=text)


@route("/file/<fechoarea>/<filename>")
def file(fechoarea, filename):
    "File function."
    api.load_config()
    response =  static_file(filename,
                            root="fecho/{}".format(fechoarea))
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
    return response


@route("/s/fetch")
def fetch():
    "Fetch mail from uplink."
    api.load_config()
    exchange.send_mail(api.config["node"], api.config["auth"])
    open("newmessages.txt", "w")
    echoareas = [echo[0] for echo in api.config["echoareas"]]
    fechoareas = [fecho[0] for fecho in api.config["fechoareas"]]
    counts, fcounts = exchange.download_counts(api.config["node"], echoareas,
                                               fechoareas)
    remote = {"echoareas": counts, "fechoareas": fcounts}
    depth, fdepth = api.calculate_counts(remote)
    if depth >= 0:
        if api.config["echoareas"]:
            exchange.download_mail(api.config["node"], echoareas, depth)
    else:
        print("new messages not found")
    open("newfiles.txt", "w")
    if fdepth >= 0:
        if api.config["fechoareas"]:
            exchange.download_filemail(api.config["node"], fechoareas, fdepth)
    else:
        print("new files not found")
    api.save_counts(remote)
    redirect("/new")


@post("/s/save_message")
def save_message():
    "Save out message."
    api.load_config()
    to = request.forms.getunicode("to")
    subj = request.forms.getunicode("subj")
    if subj == "":
        subj = "No subject"
    repto = request.forms.getunicode("repto")
    if not repto == "":
        body = "@repto:{}\n".format(repto)
    else:
        body = ""
    body += request.forms.getunicode("body")
    echo = request.forms.getunicode("echo")
    if idec_filter.is_echoarea(echo):
        base.save_out(echo, to, subj, body)
        redirect("/s/saved")
    else:
        redirect("/")


@route("/s/saved")
def saved():
    "Saved page function."
    api.load_config()
    return template("tpl/{}/saved.tpl".format(api.config["template"]),
                    echoareas=api.config["echoareas"],
                    fechoareas=api.config["fechoareas"],
                    body="", template=api.config["template"])


@post("/s/send_file")
def s_send_file():
    "Send file function."
    api.load_config()
    fechoarea = request.forms.getunicode("fechoarea")
    f = request.files.get("file")
    dsc = request.forms.get("description")
    exchange.send_file(api.config["node"], api.config["auth"],
                       fechoarea, dsc, f)
    redirect("/s/sended")


@route("/s/sended")
def sended():
    "Sended file function."
    api.load_config()
    return template("tpl/{}/sended.tpl".format(api.config["template"]),
                    echoareas=api.config["echoareas"],
                    fechoareas=api.config["fechoareas"],
                    body="", template=api.config["template"])


def build_arealist(areas):
    "Build arealist by settings field."
    areas = areas.strip().replace("\r", "")
    for area in areas.split("\n"):
        echo = area.split(":")
        if len(echo) == 1:
            echo.append("")
        yield echo


@post("/s/save_settings")
def save_settings():
    "Save settings function."
    api.load_config()
    settings = {}
    settings["node"] = request.forms.getunicode("node")
    settings["auth"] = request.forms.getunicode("auth")
    settings["template"] = request.forms.getunicode("template")
    if request.forms.get("nodeecholist"):
        echoareas = request.forms.getunicode("nodeechoareas")
    else:
        echoareas = request.forms.getunicode("echoareas")
    settings["echoareas"] = list(build_arealist(echoareas))
    if request.forms.get("nodefecholist"):
        fechoareas = request.forms.getunicode("nodefechoareas")
    else:
        fechoareas = request.forms.getunicode("fechoareas")
    settings["fechoareas"] = list(build_arealist(fechoareas))
    api.config = settings
    api.save_config()
    redirect("/settings")


@route("/files/<filename>")
def style(filename):
    "Static files of template."
    api.load_config()
    return static_file(filename, root="tpl/{}".format(api.config["template"]))

Request.MEMFILE_MAX = 1024000
print(open("logo.txt").read())
base.check_base()
run(port=62222)
