#!/usr/bin/env python

"""
lucius.py

This script is used to generate color files for various applications that match
the vim color scheme, "Lucius". This script must be run from within Vim!
"""


import os
import sys

import vim


ROOT_DIR = os.path.join(os.environ.get("HOME"), "lucius")
SCHEMES = [
        "LuciusWhite",
        "LuciusWhiteLowContrast",
        "LuciusLight",
        "LuciusLightLowContrast",
        "LuciusDark",
        "LuciusDarkHighContrast",
        "LuciusDarkLowContrast",
        "LuciusBlack",
        "LuciusBlackHighContrast",
        "LuciusBlackLowContrast",
        ]


class Color(object):
    def __init__(self, hex_string):
        if hex_string.startswith("#"):
            hex_string = hex_string[1:]
        self.hex_string = hex_string
        self.r = int(self.hex_string[0:2], 16)
        self.g = int(self.hex_string[2:4], 16)
        self.b = int(self.hex_string[4:6], 16)

    def get_hex0_string(self):
        return "0x%s" % self.hex_string

    def get_hex_string(self):
        return "#%s" % self.hex_string

    def get_rgb_string(self):
        return "%d,%d,%d" % (self.r, self.g, self.b)

    def get_red(self, fraction=False):
        if fraction:
            return self.r / 255.0
        return self.r

    def get_green(self, fraction=False):
        if fraction:
            return self.g / 255.0
        return self.g

    def get_blue(self, fraction=False):
        if fraction:
            return self.b / 255.0
        return self.b



def get_fg(name):
    color = vim.eval("synIDattr(synIDtrans(hlID('%s')), 'fg', 'gui')" % name)
    return Color(color)


def get_bg(name):
    color = vim.eval("synIDattr(synIDtrans(hlID('%s')), 'bg', 'gui')" % name)
    return Color(color)


def is_light_background():
    return vim.eval("&background") == "light"


def get_ansi_colors(mode=None):
    d = {}
    if is_light_background():
        d["ansi0"] = get_fg("Normal")
        d["black"] = get_fg("Normal")
        d["ansi8"] = get_fg("Normal")
        d["black_bold"] = get_fg("Normal")
        d["ansi7"] = get_bg("Normal")
        d["white"] = get_bg("Normal")
        d["ansi15"] = get_bg("Normal")
        d["white_bold"] = get_bg("Normal")
    else:
        d["ansi0"] = get_bg("Normal")
        d["black"] = get_bg("Normal")
        d["ansi8"] = get_bg("Normal")
        d["black_bold"] = get_bg("Normal")
        d["ansi7"] = get_fg("Normal")
        d["white"] = get_fg("Normal")
        d["ansi15"] = get_fg("Normal")
        d["white_bold"] = get_fg("Normal")
    d["ansi1"] = get_fg("ErrorMsg")
    d["red"] = get_fg("ErrorMsg")
    d["ansi9"] = get_fg("ErrorMsg")
    d["red_bold"] = get_fg("ErrorMsg")
    d["ansi2"] = get_fg("Identifier")
    d["green"] = get_fg("Identifier")
    d["ansi10"] = get_fg("Identifier")
    d["green_bold"] = get_fg("Identifier")
    d["ansi3"] = get_fg("Constant")
    d["yellow"] = get_fg("Constant")
    d["ansi11"] = get_fg("Constant")
    d["yellow_bold"] = get_fg("Constant")
    d["ansi4"] = get_fg("Statement")
    d["blue"] = get_fg("Statement")
    d["ansi12"] = get_fg("Statement")
    d["blue_bold"] = get_fg("Statement")
    d["ansi5"] = get_fg("Special")
    d["magenta"] = get_fg("Special")
    d["ansi13"] = get_fg("Special")
    d["magenta_bold"] = get_fg("Special")
    d["ansi6"] = get_fg("PreProc")
    d["cyan"] = get_fg("PreProc")
    d["ansi14"] = get_fg("PreProc")
    d["cyan_bold"] = get_fg("PreProc")

    d["fg"] = get_fg("Normal")
    d["fg_bold"] = get_fg("Normal")
    d["bg"] = get_bg("Normal")
    d["bg_bold"] = get_bg("Normal")
    d["cursor_text"] = get_bg("Normal")
    d["cursor"] = get_bg("Cursor")

    if mode is not None:
        if mode == "rgb":
            for k in d:
                d[k] = d[k].get_rgb_string()
        elif mode == "hex":
            for k in d:
                d[k] = d[k].get_hex_string()
    return d


def write_putty(name):
    template_path = os.path.join(ROOT_DIR, "templates", "putty.txt")
    path = os.path.join(ROOT_DIR, "putty", name + ".reg")
    colors = get_ansi_colors(mode="rgb")
    colors["name"] = name
    template = ""
    with open(template_path, "r") as fd:
        template = fd.read()
    template = template % colors
    with open(path, "w") as fd:
        fd.write(template)


def write_iterm2(name):
    colors = get_ansi_colors()
    path = os.path.join(ROOT_DIR, "iterm2", name + ".itermcolors")
    template_item_path = os.path.join(ROOT_DIR, "templates", "iterm2_entry.txt")
    template_path = os.path.join(ROOT_DIR, "templates", "iterm2.txt")
    template = ""
    template_item = ""
    with open(template_path, "r") as fd:
        template = fd.read()
    with open(template_item_path, "r") as fd:
        template_item = fd.read()
    entries = []
    for i in xrange(16):
        item_name = "Ansi %d Color" % i
        d = dict(
                name=item_name,
                red=colors["ansi%d" % i].get_red(fraction=True),
                green=colors["ansi%d" % i].get_green(fraction=True),
                blue=colors["ansi%d" % i].get_blue(fraction=True),
                )
        entries.append(template_item % d)
    other_colors = {}
    other_colors["Background Color"] = get_bg("Normal")
    other_colors["Bold Color"] = get_fg("Normal")
    other_colors["Cursor Color"] = get_bg("Cursor")
    other_colors["Cursor Text Color"] = get_bg("Normal")
    other_colors["Foreground Color"] = get_fg("Normal")
    other_colors["Selected Text Color"] = get_fg("Normal")
    other_colors["Selection Color"] = get_bg("Visual")
    for c in other_colors:
        d = dict(
                name=c,
                red=other_colors[c].get_red(fraction=True),
                green=other_colors[c].get_green(fraction=True),
                blue=other_colors[c].get_blue(fraction=True),
                )
        entries.append(template_item % d)
    template = template % "".join(entries)
    with open(path, "w") as fd:
        fd.write(template)


def write_xresources(name):
    template_path = os.path.join(ROOT_DIR, "templates", "xresources.txt")
    path = os.path.join(ROOT_DIR, "xresources", name)
    colors = get_ansi_colors(mode="hex")
    template = ""
    with open(template_path, "r") as fd:
        template = fd.read()
    template = template % colors
    with open(path, "w") as fd:
        fd.write(template)


def write_mintty(name):
    template_path = os.path.join(ROOT_DIR, "templates", "mintty.txt")
    path = os.path.join(ROOT_DIR, "mintty", name)
    colors = get_ansi_colors(mode="rgb")
    template = ""
    with open(template_path, "r") as fd:
        template = fd.read()
    template = template % colors
    with open(path, "w") as fd:
        fd.write(template)


def main():
    for scheme in SCHEMES:
        vim.command(scheme)
        write_putty(scheme)
        write_iterm2(scheme)
        write_xresources(scheme)
        write_mintty(scheme)


if __name__ == "__main__":
    main()


# vim: expandtab

