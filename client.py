#!/usr/bin/env python3

import api
from api import base
from api import exchange
from api import fecho
from api import idec_filter
from bottle import post, redirect, request, route, run, static_file, template
from math import floor


@route("/")
def index():
    "Index page function."
    api.load_config()
    messages = []
    counts = {}
    for echoarea in api.config["echoareas"]:
        msg = base.read_last_message(echoarea[0])
        if msg:
            msg[2] = api.formatted_time(msg[2])
            messages.append(msg)
            counts[msg[1]] = base.echoarea_count(msg[1])
    return template("tpl/{}/index.tpl".format(api.config["template"]),
                    echoareas=api.config["echoareas"], messages=messages,
                    fechoareas=api.config["fechoareas"], counts=counts,
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
    files.sort(key = lambda x: x[1])
    return template("tpl/{}/new.tpl".format(api.config["template"]),
                    echoareas=api.config["echoareas"], messages=messages,
                    files=files, fechoareas=api.config["fechoareas"],
                    template=api.config["template"])


@route("/<e1>.<e2>")
@route("/<e1>.<e2>/<page>")
def echo_reader(e1, e2, page=False):
    "Echoarea reader function."
    api.load_config()
    echoarea = "{}.{}".format(e1, e2)
    messages = []
    pages = floor(base.echoarea_count(echoarea) / 50) + 2
    if not page:
        page = pages - 1
    for msg in base.read_messages_by_page(echoarea, int(page), 50):
        msg[3] = api.formatted_time(msg[3])
        messages.append(msg)
    for echo in api.config["echoareas"]:
        if echo[0] == echoarea:
            echoarea = echo
            break
    else:
        echoarea = [echoarea, ""]
    return template("tpl/{}/echoarea.tpl".format(api.config["template"]),
                    echo=echoarea, echoareas=api.config["echoareas"],
                    fechoareas=api.config["fechoareas"], messages=messages,
                    pages=pages, page=int(page),
                    template=api.config["template"])


@route("/<msgid>")
def message_reader(msgid):
    api.load_config()
    msg = base.read_message(msgid).split("\n")
    msg[2] = api.formatted_time(msg[2])
    return template("tpl/{}/message.tpl".format(api.config["template"]),
                    echoareas=api.config["echoareas"], msgid=msgid,
                    fechoareas=api.config["fechoareas"], message=msg,
                    template=api.config["template"])


@route("/new_message/<echoarea>")
def new_message(echoarea):
    api.load_config()
    if idec_filter.is_echoarea(echoarea):
        return template("tpl/{}/new_message.tpl".format(api.config["template"]),
                        echoareas=api.config["echoareas"], echo=echoarea,
                        fechoareas=api.config["fechoareas"], body="", subj="",
                        to="All", template=api.config["template"])


@route("/reply/<echoarea>/<msgid>")
def new_message(echoarea, msgid):
    api.load_config()
    if idec_filter.is_echoarea(echoarea) and idec_filter.is_msgid(msgid):
        msg = base.read_message(msgid).split("\n")
        fr = msg[3]
        initials = api.initials(msg[3])
        subj = msg[6]
        msg = api.quoter(msg[8:], initials)
        return template("tpl/{}/new_message.tpl".format(api.config["template"]),
                        echoareas=api.config["echoareas"], echo=echoarea,
                        fechoareas=api.config["fechoareas"],
                        body="\n".join(msg), subj=subj, to=fr,
                        template=api.config["template"])


@route("/fecho/<fechoarea>")
def fechoarea(fechoarea):
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


@route("/settings")
def settings():
    api.load_config()
    return template("tpl/{}/settings.tpl".format(api.config["template"]),
                    config=api.config)


@route("/file/<fechoarea>/<filename>")
def file(fechoarea, filename):
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
    if api.config["echoareas"]:
        echoareas = [echo[0] for echo in api.config["echoareas"]]
        exchange.download_mail(api.config["node"], echoareas, 200)
    open("newfiles.txt", "w")
    if api.config["fechoareas"]:
        fechoareas = [fecho[0] for fecho in api.config["fechoareas"]]
        exchange.download_filemail(api.config["node"], fechoareas, 200)
    redirect("/new")


@post("/s/save_message")
def save_message():
    api.load_config()
    to = request.forms.getunicode("to")
    subj = request.forms.getunicode("subj")
    if subj == "":
        subj = "No subject"
    body = request.forms.getunicode("body")
    echo = request.forms.getunicode("echo")
    if idec_filter.is_echoarea(echo):
        base.save_out(echo, to, subj, body)
        redirect("/s/saved")
    else:
        redirect("/")


@route("/s/saved")
def saved():
    api.load_config()
    return template("tpl/{}/saved.tpl".format(api.config["template"]),
                    echoareas=api.config["echoareas"],
                    fechoareas=api.config["fechoareas"],
                    body="", template=api.config["template"])


@route("/files/<filename>")
def style(filename):
    "Static files of template."
    api.load_config()
    response =  static_file(filename,
                            root="tpl/{}".format(api.config["template"]))
    return response


print(open("logo.txt", "r").read())
api.check_base()
run(host="localhost", port=4242)
