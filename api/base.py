import os
import base64
import sqlite3


con = sqlite3.connect("idec.db")
c = con.cursor()


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
    check_dir("fecho")
    check_dir("out")
    check_file("newmessages.txt")
    check_file("newfiles.txt")
    c.execute("""CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    msgid TEXT,
    tags TEXT,
    echoarea TEXT,
    date INTEGER,
    msgfrom TEXT,
    address TEXT,
    msgto TEXT,
    subject TEXT,
    body TEXT,
    UNIQUE(id));""")
    con.commit()


def echoarea_count(echoarea):
    "Return messages count in echoarea."
    return c.execute("SELECT COUNT(1) FROM messages WHERE echoarea = ?;",
                     (echoarea, )).fetchone()[0]


def read_echoarea(echoarea):
    "Return echoarea index."
    msgids = []
    rows = c.execute("SELECT msgid FROM messages WHERE echoarea = ? " +
                     "ORDER BY id;", (echoarea, )).fetchall()
    for row in rows:
        msgids.append(row[0])
    return msgids


def read_last_message(echoarea):
    "Return last message in echoarea."
    raw = c.execute("SELECT msgid, tags, echoarea, date, msgfrom, address, " +
                    "msgto, subject, body FROM messages WHERE echoarea = ? " +
                    "ORDER BY id DESC LIMIT 1;", (echoarea, )).fetchone()
    if raw:
        message = list(raw)
        message.insert(8, "")
        message[9:] = message[9].split("\n")
        return message[0], message[1:]
    else:
        return "", []


def read_messages_by_page(echoarea, page, onpage):
    rows = c.execute("SELECT msgid, tags, echoarea, date, msgfrom, address, msgto, " +
                    "subject, body FROM messages WHERE echoarea = ? " +
                     "ORDER BY id LIMIT ?, ?;",
                     (echoarea, (page - 1) * onpage, onpage)).fetchall()
    for row in rows:
        yield list(row)


def read_local_index(echoareas):
    "Read local echoareas index."
    for echoarea in echoareas:
        for msgid in read_echoarea(echoarea):
            yield msgid


def read_message(msgid):
    "Return raw message."
    raw = c.execute("SELECT tags, echoarea, date, msgfrom, address, msgto, " +
                    "subject, body FROM messages WHERE msgid = ? ",
                    (msgid, )).fetchone()
    if raw:
        message = list(raw)
        message[2] = str(message[2])
        message.insert(7, "")
        return "\n".join(message)
    else:
        return None


def save_messages(messages):
    "Save message to base."
    for line in messages:
        message = line[1].split("\n")
        c.execute("INSERT INTO messages (msgid, tags, echoarea, date, " +
                  "msgfrom, address, msgto, subject, body) " +
                  "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",
                  (line[0], message[0], message[1], message[2], message[3],
                   message[4], message[5], message[6], "\n".join(message[8:])))
        with open("newmessages.txt", "a") as new:
            new.write(line[0] + "\n")
    con.commit()


def debundle(bundle):
    "Unpack messages bundle."
    bundle = bundle
    messages = []
    for row in bundle:
        vals = row.split(":")
        message = base64.urlsafe_b64decode(vals[1]).decode("utf-8")
        messages.append([vals[0], message])
    save_messages(messages)


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
    msg = msg.replace("\r", "")
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
