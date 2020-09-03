"""
Module contains functions:
- is_msgid(msgid) -> bool
- is_echoarea(echoarea) -> bool
- is_fileechoarea(fileechoarea) -> bool
- is_filename(filename) -> bool
"""
import re


def is_msgid(msgid):
    "Checks if msgid is correct."
    return re.match("[0-9a-zA-Z]{20}", msgid)


def is_echoarea(echoarea):
    "Checks if echoarea name is correct."
    return re.match("[0-9a-z_\-\.]{1,60}\.[0-9a-z_\-\.]{1,60}", echoarea)


def is_fileechoarea(fileechoarea):
    "Checks if fileechoarea name is correct."
    if fileechoarea == "indexes":
        return false
    else:
        return re.match("[0-9a-z_\-\.]{3,120}", fileechoarea)


def is_filename(filename):
    "Check if filename is correct."
    return re.match("[0-9a-zA-Z_\-\.]{5,120}", filename)
