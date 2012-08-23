from __future__ import absolute_import
from __future__ import division
from __future__ import with_statement

import os
import re
import sys


IGNORE_LIST = ["Ignore", "SpellBad", "SpellCap", "SpellRare", "SpellLocal"]

DARK = "LuciusDark"
DARK_DIM = "LuciusDarkDim"
LIGHT = "LuciusLight"

THEMES = [DARK, DARK_DIM, LIGHT]
LIGHT_THEMES = [LIGHT]
DARK_THEMES = [DARK, DARK_DIM]

GIT = os.path.join(os.environ.get("HOME"), "lucius")
GIT_LUCIUS = os.path.join(GIT, "lucius")


class Lucius(object):
    def __init__(self):
        self.file_data = None
        self.colors = dict()
        self.ansi_colors = dict()
        self.load_file_data()
        self.load_dict()
        self.add_ansi_definitions()

    def load_file_data(self):
        with open(os.path.join(GIT, "vimfiles/colors/lucius.vim")) as fd:
            self.file_data = fd.read()

    def load_dict(self):
        self.colors = dict()
        sections = self.file_data.split('" # ')
        for s in sections:
            if s.startswith("%s {{{" % DARK):
                colors = dict()
                self.load_color_definitions(s, colors)
                self.colors[DARK] = colors
            elif s.startswith("%s {{{" % DARK_DIM):
                colors = dict()
                self.load_color_definitions(s, colors)
                self.colors[DARK_DIM] = colors
            elif s.startswith("%s {{{" % LIGHT):
                colors = dict()
                self.load_color_definitions(s, colors)
                self.colors[LIGHT] = colors
            else:
                pass

    def load_color_definitions(self, section, section_dict):
        name_re = re.compile("hi (\w+) ")
        guifg_re = re.compile("guifg=#*(\w+)")
        guibg_re = re.compile("guibg=#*(\w+)")
        for line in section.splitlines():
            if line.strip().startswith("hi "):
                name = name_re.findall(line)
                if name is None or len(name) == 0:
                    raise Exception("Bad hi definition: %s" % line)
                else:
                    name = name[0]
                if name in IGNORE_LIST:
                    continue
                fg = guifg_re.findall(line)
                if fg is None or len(fg) == 0:
                    raise Exception("Bad fg definition: %s" % line)
                else:
                    fg = fg[0]
                bg = guibg_re.findall(line)
                if bg is None or len(bg) == 0:
                    raise Exception("Bad bg definition: %s" % line)
                else:
                    bg = bg[0]
                section_dict[name] = dict(fg=fg, bg=bg)
            elif line.strip().startswith('" }}}'):
                return

    def add_ansi_definitions(self):
        self.ansi_colors = dict()
        for theme in THEMES:
            d = dict()
            self.ansi_colors[theme] = d
            if theme in LIGHT_THEMES:
                d["ansi0"] = self.get_fg(theme, "Normal")
                d["black"] = self.get_fg(theme, "Normal")
                d["ansi8"] = self.get_fg(theme, "Normal")
                d["black_bold"] = self.get_fg(theme, "Normal")
            else:
                d["ansi0"] = self.get_bg(theme, "Normal")
                d["black"] = self.get_bg(theme, "Normal")
                d["ansi8"] = self.get_bg(theme, "Normal")
                d["black_bold"] = self.get_bg(theme, "Normal")
            d["ansi1"] = self.get_fg(theme, "ErrorMsg")
            d["red"] = self.get_fg(theme, "ErrorMsg")
            d["ansi9"] = self.get_fg(theme, "ErrorMsg")
            d["red_bold"] = self.get_fg(theme, "ErrorMsg")
            d["ansi2"] = self.get_fg(theme, "Identifier")
            d["green"] = self.get_fg(theme, "Identifier")
            d["ansi10"] = self.get_fg(theme, "Identifier")
            d["green_bold"] = self.get_fg(theme, "Identifier")
            d["ansi3"] = self.get_fg(theme, "Constant")
            d["yellow"] = self.get_fg(theme, "Constant")
            d["ansi11"] = self.get_fg(theme, "Constant")
            d["yellow_bold"] = self.get_fg(theme, "Constant")
            d["ansi4"] = self.get_fg(theme, "Statement")
            d["blue"] = self.get_fg(theme, "Statement")
            d["ansi12"] = self.get_fg(theme, "Statement")
            d["blue_bold"] = self.get_fg(theme, "Statement")
            d["ansi5"] = self.get_fg(theme, "Special")
            d["magenta"] = self.get_fg(theme, "Special")
            d["ansi13"] = self.get_fg(theme, "Special")
            d["magenta_bold"] = self.get_fg(theme, "Special")
            d["ansi6"] = self.get_fg(theme, "PreProc")
            d["cyan"] = self.get_fg(theme, "PreProc")
            d["ansi14"] = self.get_fg(theme, "PreProc")
            d["cyan_bold"] = self.get_fg(theme, "PreProc")
            if theme in LIGHT_THEMES:
                d["ansi7"] = self.get_bg(theme, "Normal")
                d["white"] = self.get_bg(theme, "Normal")
                d["ansi15"] = self.get_bg(theme, "Normal")
                d["white_bold"] = self.get_bg(theme, "Normal")
            else:
                d["ansi7"] = self.get_fg(theme, "Normal")
                d["white"] = self.get_fg(theme, "Normal")
                d["ansi15"] = self.get_fg(theme, "Normal")
                d["white_bold"] = self.get_fg(theme, "Normal")

    def get_bg(self, theme, name, replace=True):
        return self._get_color(theme, name, "bg", replace=replace)

    def get_fg(self, theme, name, replace=True):
        return self._get_color(theme, name, "fg", replace=replace)

    def get_bg_rgb(self, theme, name):
        hex_color = self._get_color(theme, name, "bg")
        return self.hex_to_rgb(hex_color)

    def get_fg_rgb(self, theme, name):
        hex_color = self._get_color(theme, name, "fg")
        return self.hex_to_rgb(hex_color)

    def get_ansi(self, theme, name):
        return self.ansi_colors[theme][name]

    def get_ansi_rgb(self, theme, name):
        return self.hex_to_rgb(self.ansi_colors[theme][name])

    def hex_to_rgb(self, hex_color):
        rh, gh, bh = [hex_color[0:2], hex_color[2:4], hex_color[4:6]]
        r, g, b = int(rh, 16), int(gh, 16), int(bh, 16)
        return r, g, b

    def _get_color(self, theme, name, c, replace=True):
        color = None
        theme_dict = self.colors.get(theme)
        if theme_dict:
            color = theme_dict.get(name, None)
            if color:
                color = color.get(c, None)
                if replace:
                    if color == "bg":
                        color = self._get_color(theme, "Normal", "bg")
                    elif color == "fg":
                        color = self._get_color(theme, "Normal", "fg")
                    elif color == "NONE":
                        color = self._get_color(theme, "Normal", c)
        if not color:
            sys.stderr.write("Could not find color for %s, %s, %s\n" % (theme, name, c))
            return None
        return color

    def write_all(self):
        self.write_putty()
        self.write_iterm2()

    def write_putty(self):
        def srgb(rgb):
            return ",".join([str(c) for c in rgb])
        putty_dir = os.path.join(GIT_LUCIUS, "putty")
        if not os.path.exists(putty_dir):
            os.mkdir(putty_dir)
        for theme in THEMES:
            d = dict()
            d.update(self.ansi_colors[theme])
            d["fg"] = self.get_fg(theme, "Normal")
            d["fg_bold"] = self.get_fg(theme, "Normal")
            d["bg"] = self.get_bg(theme, "Normal")
            d["bg_bold"] = self.get_bg(theme, "Normal")
            d["cursor_text"] = self.get_bg(theme, "Normal")
            d["cursor"] = self.get_bg(theme, "Cursor")
            for k in d:
                d[k] = srgb(self.hex_to_rgb(d[k]))
            d["name"] = theme
            file_data = _PUTTY % d
            with open(os.path.join(putty_dir, theme + ".reg"), "w") as fd:
                fd.write(file_data)

    def write_iterm2(self):
        iterm_dir = os.path.join(GIT_LUCIUS, "iterm2")
        if not os.path.exists(iterm_dir):
            os.mkdir(iterm_dir)
        for theme in THEMES:
            entries = []
            for i in range(16):
                r, g, b = self.get_ansi_rgb(theme, "ansi%d" % i)
                entry = _ITERM_ENTRY
                name = "Ansi %d Color" % i
                d = dict(name=name, red=r/255.0, green=g/255.0, blue=b/255.0)
                entry = entry % d
                entries.append(entry)
            color_map = dict()
            color_map["Background Color"] = self.get_bg_rgb(theme, "Normal")
            color_map["Bold Color"] = self.get_fg_rgb(theme, "Normal")
            color_map["Cursor Color"] = self.get_bg_rgb(theme, "Cursor")
            color_map["Cursor Text Color"] = self.get_bg_rgb(theme, "Normal")
            color_map["Foreground Color"] = self.get_fg_rgb(theme, "Normal")
            color_map["Selected Text Color"] = self.get_fg_rgb(theme, "Normal")
            color_map["Selection Color"] = self.get_bg_rgb(theme, "Visual")
            for k in color_map:
                r, g, b = color_map[k]
                entry = _ITERM_ENTRY
                d = dict(name=k, red=r/255.0, green=g/255.0, blue=b/255.0)
                entry = entry % d
                entries.append(entry)
            file_data = _ITERM % "\n".join(entries)
            with open(os.path.join(iterm_dir, theme + ".itermcolors"), "w") as fd:
                fd.write(file_data)

    def write_vs2008(self):
        iterm_dir = os.path.join(GIT_LUCIUS, "vs2008")
        if not os.path.exists(iterm_dir):
            os.mkdir(iterm_dir)
        for theme in THEMES:
            entries = []

    def get_vs_abgr_dict(self, theme):
        def abgr(c):
            if c is None:
                return None
            return "0x00" + c[4:6] + c[2:4] + c[0:2]
        default = "0x02000000"
        normal_fg = abgr(self.get_fg(theme, "Normal"))
        normal_bg = abgr(self.get_bg(theme, "Normal"))
        theme_colors = self.colors[theme]
        d = dict()
        for color in theme_colors:
            fg = self.get_fg(theme, color, replace=False)
            bg = self.get_bg(theme, color, replace=False)
            if fg == "fg":
                fg = default
            elif fg == "NONE":
                fg = default
            elif fg == "bg":
                fg = normal_bg
            else:
                fg = abgr(fg)
            if bg == "bg":
                bg = default
            elif bg == "NONE":
                bg = default
            elif bg == "fg":
                bg = normal_fg
            else:
                bg = abgr(bg)
            if fg:
                d[color + "_fg"] = fg
            if bg:
                d[color + "_bg"] = bg

        return d



_PUTTY = """\
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions\%(name)s]
"Colour0"="%(fg)s"
"Colour1"="%(fg_bold)s"
"Colour2"="%(bg)s"
"Colour3"="%(bg_bold)s"
"Colour4"="%(cursor_text)s"
"Colour5"="%(cursor)s"
"Colour6"="%(black)s"
"Colour7"="%(black_bold)s"
"Colour8"="%(red)s"
"Colour9"="%(red_bold)s"
"Colour10"="%(green)s"
"Colour11"="%(green_bold)s"
"Colour12"="%(yellow)s"
"Colour13"="%(yellow_bold)s"
"Colour14"="%(blue)s"
"Colour15"="%(blue_bold)s"
"Colour16"="%(magenta)s"
"Colour17"="%(magenta_bold)s"
"Colour18"="%(cyan)s"
"Colour19"="%(cyan_bold)s"
"Colour20"="%(white)s"
"Colour21"="%(white_bold)s"
"""


_ITERM = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
%s
</dict>
</plist>
"""


_ITERM_ENTRY = """\
    <key>%(name)s</key>
    <dict>
        <key>Blue Component</key>
        <real>%(blue)f</real>
        <key>Green Component</key>
        <real>%(green)f</real>
        <key>Red Component</key>
        <real>%(red)f</real>
    </dict>"""


_VS2008 = """\
<UserSettings>
    <ApplicationIdentity version="9.0"/>
    <ToolsOptions>
        <ToolsOptionsCategory name="Environment" RegisteredName="Environment"/>
    </ToolsOptions>
    <Category name="Environment_Group" RegisteredName="Environment_Group">
        <Category name="Environment_FontsAndColors" Category="{1EDA5DD4-927A-43a7-810E-7FD247D0DA1D}" Package="{DA9FB551-C724-11d0-AE1F-00A0C90FFFC3}" RegisteredName="Environment_FontsAndColors" PackageName="Visual Studio Environment Package">
            <PropertyValue name="Version">2</PropertyValue>
            <FontsAndColors Version="2.0">
                <Categories>
                    <Category GUID="{358463D0-D084-400F-997E-A34FC570BC72}" FontIsDefault="Yes">
                        <Items>
                            <Item Name="Text" Foreground="0x003A3A3A" Background="0x02000000" BoldFont="No"/>
                            <Item Name="SelectedText" Foreground="0x02000000" Background="0x02000000" BoldFont="No"/>
                            <Item Name="ChangedText" Foreground="0x000000FF" Background="0x02000000" BoldFont="No"/>
                        </Items>
                    </Category>
                    <Category GUID="{40660F54-80FA-4375-89A3-8D06AA954EBA}" FontName="Consolas" FontSize="8" CharSet="0" FontIsDefault="No">
                        <Items>
                            <Item Name="Plain Text" Foreground="0x003A3A3A" Background="0x00EEEEEE" BoldFont="No"/>
                            <Item Name="Selected Text" Foreground="0x003A3A3A" Background="0x00FFD7AF" BoldFont="No"/>
                            <Item Name="Inactive Selected Text" Foreground="0x003A3A3A" Background="0x00AFAFAF" BoldFont="No"/>
                        </Items>
                    </Category>
                    <Category GUID="{47724E70-AF55-48FB-A928-BB161C1D0C05}" FontName="Consolas" FontSize="10" CharSet="0" FontIsDefault="No">
                        <Items/>
                    </Category>
                    <Category GUID="{5C48B2CB-0366-4FBF-9786-0BB37E945687}" FontName="Consolas" FontSize="8" CharSet="0" FontIsDefault="No">
                        <Items>
                            <Item Name="Plain Text" Foreground="0x003A3A3A" Background="0x00EEEEEE" BoldFont="No"/>
                            <Item Name="Selected Text" Foreground="0x003A3A3A" Background="0x00FFD7AF" BoldFont="No"/>
                            <Item Name="Inactive Selected Text" Foreground="0x003A3A3A" Background="0x00AFAFAF" BoldFont="No"/>
                            <Item Name="Current list location" Foreground="0x00A3DBFF" Background="0x01000007" BoldFont="No"/>
                        </Items>
                    </Category>
                    <Category GUID="{6BB65C5A-2F31-4BDE-9F48-8A38DC0C63E7}" FontName="Consolas" FontSize="8" CharSet="0" FontIsDefault="No">
                        <Items>
                            <Item Name="Plain Text" Foreground="0x003A3A3A" Background="0x00EEEEEE" BoldFont="No"/>
                            <Item Name="Selected Text" Foreground="0x003A3A3A" Background="0x00FFD7AF" BoldFont="No"/>
                            <Item Name="Inactive Selected Text" Foreground="0x003A3A3A" Background="0x00AFAFAF" BoldFont="No"/>
                        </Items>
                    </Category>
                    <Category GUID="{8259ACED-490A-41B3-A0FB-64C842CCDC80}" FontIsDefault="Yes">
                        <Items>
                            <Item Name="Text" Foreground="0x003A3A3A" Background="0x02000000" BoldFont="No"/>
                            <Item Name="SelectedText" Foreground="0x02000000" Background="0x02000000" BoldFont="No"/>
                            <Item Name="ChangedText" Foreground="0x000000FF" Background="0x02000000" BoldFont="No"/>
                        </Items>
                    </Category>
                    <Category GUID="{9973EFDF-317D-431C-8BC1-5E88CBFD4F7F}" FontName="Consolas" FontSize="8" CharSet="0" FontIsDefault="No">
                        <Items>
                            <Item Name="Plain Text" Foreground="0x003A3A3A" Background="0x00EEEEEE" BoldFont="No"/>
                            <Item Name="Selected Text" Foreground="0x003A3A3A" Background="0x00FFD7AF" BoldFont="No"/>
                            <Item Name="Inactive Selected Text" Foreground="0x003A3A3A" Background="0x00AFAFAF" BoldFont="No"/>
                            <Item Name="Current list location" Foreground="0x00A3DBFF" Background="0x01000007" BoldFont="No"/>
                        </Items>
                    </Category>
                    <Category GUID="{9E632E6E-D786-4F9A-8D3E-B9398836C784}" FontName="Consolas" FontSize="8" CharSet="0" FontIsDefault="No">
                        <Items>
                            <Item Name="Plain Text" Foreground="0x003A3A3A" Background="0x00EEEEEE" BoldFont="No"/>
                            <Item Name="Selected Text" Foreground="0x003A3A3A" Background="0x00FFD7AF" BoldFont="No"/>
                            <Item Name="Inactive Selected Text" Foreground="0x003A3A3A" Background="0x00AFAFAF" BoldFont="No"/>
                        </Items>
                    </Category>
                    <Category GUID="{A27B4E24-A735-4D1D-B8E7-9716E1E3D8E0}" FontName="Consolas" FontSize="10" CharSet="0" FontIsDefault="No">
                        <Items>
                            <Item Name="Plain Text" Foreground="%(Normal_fg)s" Background="%(Normal_bg)s" BoldFont="No"/>
                            <Item Name="Selected Text" Foreground="%(Normal_bg)s" Background="%(Visual_bg)s" BoldFont="No"/>
                            <Item Name="Inactive Selected Text" Foreground="%(Normal_bg)s" Background="0x00AFAFAF" BoldFont="No"/>
                            <Item Name="Indicator Margin" Foreground="0x02000000" Background="%(SignColumn_bg)s" BoldFont="No"/>
                            <Item Name="Line Numbers" Foreground="0x009E9E9E" Background="0x00DADADA" BoldFont="No"/>
                            <Item Name="Visible White Space" Foreground="0x00D7AFAF" Background="0x02000000" BoldFont="No"/>
                            <Item Name="Bookmark" Foreground="0x02000000" Background="0x00FFD7AF" BoldFont="No"/>
                            <Item Name="Brace Matching (Highlight)" Foreground="0x003A3A3A" Background="0x02000000" BoldFont="Yes"/>
                            <Item Name="Brace Matching (Rectangle)" Foreground="0x02000000" Background="0x00D7D75F" BoldFont="No"/>
                            <Item Name="Comment" Foreground="0x00808080" Background="0x02000000" BoldFont="No"/>
                            <Item Name="CSS Comment" Foreground="0x00808080" Background="0x02000000" BoldFont="No"/>
                            <Item Name="CSS Keyword" Foreground="0x00875F00" Background="0x02000000" BoldFont="No"/>
                            <Item Name="CSS Property Value" Foreground="0x00875F00" Background="0x02000000" BoldFont="No"/>
                            <Item Name="CSS String Value" Foreground="0x00875F00" Background="0x02000000" BoldFont="No"/>
                            <Item Name="HTML Attribute Value" Foreground="0x00875F00" Background="0x02000000" BoldFont="No"/>
                            <Item Name="HTML Comment" Foreground="0x00808080" Background="0x02000000" BoldFont="No"/>
                            <Item Name="HTML Operator" Foreground="0x00875F00" Background="0x02000000" BoldFont="No"/>
                            <Item Name="HTML Tag Delimiter" Foreground="0x00875F00" Background="0x02000000" BoldFont="No"/>
                            <Item Name="Identifier" Foreground="0x003A3A3A" Background="0x02000000" BoldFont="No"/>
                            <Item Name="Keyword" Foreground="0x00875F00" Background="0x02000000" BoldFont="No"/>
                            <Item Name="Number" Foreground="0x00005FAF" Background="0x02000000" BoldFont="No"/>
                            <Item Name="Preprocessor Keyword" Foreground="0x00878700" Background="0x02000000" BoldFont="No"/>
                            <Item Name="String" Foreground="0x00005FAF" Background="0x02000000" BoldFont="No"/>
                            <Item Name="String(C# @ Verbatim)" Foreground="0x00005FAF" Background="0x02000000" BoldFont="No"/>
                            <Item Name="User Keywords" Foreground="0x00AF5F00" Background="0x02000000" BoldFont="No"/>
                            <Item Name="User Types" Foreground="0x00AF5F00" Background="0x02000000" BoldFont="No"/>
                            <Item Name="User Types(Delegates)" Foreground="0x00AF5F00" Background="0x02000000" BoldFont="No"/>
                            <Item Name="User Types(Enums)" Foreground="0x00AF5F00" Background="0x02000000" BoldFont="No"/>
                            <Item Name="User Types(Interfaces)" Foreground="0x00AF5F00" Background="0x02000000" BoldFont="No"/>
                            <Item Name="User Types(Value types)" Foreground="0x00AF5F00" Background="0x02000000" BoldFont="No"/>
                            <Item Name="VB XML Comment" Foreground="0x00808080" Background="0x02000000" BoldFont="No"/>
                            <Item Name="XAML Comment" Foreground="0x00808080" Background="0x02000000" BoldFont="No"/>
                            <Item Name="XML Comment" Foreground="0x00808080" Background="0x02000000" BoldFont="No"/>
                            <Item Name="XML Doc Comment" Foreground="0x00870087" Background="0x02000000" BoldFont="No"/>
                        </Items>
                    </Category>
                    <Category GUID="{A7EE6BEE-D0AA-4B2F-AD9D-748276A725F6}" FontIsDefault="Yes">
                        <Items>
                            <Item Name="Text" Foreground="0x003A3A3A" Background="0x02000000" BoldFont="No"/>
                            <Item Name="SelectedText" Foreground="0x02000000" Background="0x02000000" BoldFont="No"/>
                            <Item Name="ChangedText" Foreground="0x000000FF" Background="0x02000000" BoldFont="No"/>
                        </Items>
                    </Category>
                    <Category GUID="{CE2ECED5-C21C-464C-9B45-15E10E9F9EF9}" FontName="Consolas" FontSize="8" CharSet="0" FontIsDefault="No">
                        <Items>
                            <Item Name="Plain Text" Foreground="0x003A3A3A" Background="0x00EEEEEE" BoldFont="No"/>
                            <Item Name="Selected Text" Foreground="0x003A3A3A" Background="0x00FFD7AF" BoldFont="No"/>
                            <Item Name="Inactive Selected Text" Foreground="0x003A3A3A" Background="0x00AFAFAF" BoldFont="No"/>
                        </Items>
                    </Category>
                    <Category GUID="{EE1BE240-4E81-4BEB-8EEA-54322B6B1BF5}" FontName="Consolas" FontSize="8" CharSet="0" FontIsDefault="No">
                        <Items>
                            <Item Name="Plain Text" Foreground="0x003A3A3A" Background="0x00EEEEEE" BoldFont="No"/>
                            <Item Name="Selected Text" Foreground="0x003A3A3A" Background="0x00FFD7AF" BoldFont="No"/>
                            <Item Name="Inactive Selected Text" Foreground="0x003A3A3A" Background="0x00AFAFAF" BoldFont="No"/>
                        </Items>
                    </Category>
                </Categories>
            </FontsAndColors>
        </Category>
    </Category>
</UserSettings>

"""

