"""
THIS MODULE HAS BEEN MADE BY LUDUK AT ningawent@gmail.com
PLEASE CONTACT BEFORE DISTRIBUTING AND OR MODIFYING THIS ON YOUR OWN ACCORD.

I, LUDUK, TAKE NO RESPONSIBILITY FOR ANY MISUES OF THIS MODULE.

also if you don't credit me you're a big meanie
"""

import os

"""
TODO:
1) Add check for Windows terminal, and only then do os.sysem('color').
2) Add check for Python terminal, and not put the color codes there, they don't work anyway.
"""
os.system('color')

"""
Color Printer usage examples:
    ColorPrinter.cprint('Hello!')                                  # normal
    ColorPrinter.cprint('Hello!', fg='g')                          # green
    ColorPrinter.cprint('Hello!', fg='r', bg='w', style='bx')      # bold red blinking on white

    print(ColorPrinter.fmt('Hello!', fg='r'))                      # works the same as ColorPrinter.cprint('Hello', fg='r')

List of colours (for fg and bg):
    k   black
    r   red
    g   green
    y   yellow
    b   blue
    m   magenta
    c   cyan
    w   white
List of styles:
    b   bold
    i   italic
    u   underline
    s   strikethrough
    x   blinking
    r   reverse
    y   fast blinking
    f   faint
    h   hide
"""

class ColorPrinter:
    to_style = "Terminal"

    COLCODE = {
        "Terminal": {
            'k': 0, # black
            'r': 1, # red
            'g': 2, # green
            'y': 3, # yellow
            'b': 4, # blue
            'm': 5, # magenta
            'c': 6, # cyan
            'w': 7  # white
        },

        "HTML": {
            'k': "black", # black
            'r': "red", # red
            'g': "green", # green
            'y': "yellow", # yellow
            'b': "dodgerblue", # blue
            'm': "magenta", # magenta
            'c': "cyan", # cyan
            'w': "white"  # white
        }
    }

    FMTCODE = {
        "Terminal": {
            'b': 1, # bold
            'f': 2, # faint
            'i': 3, # italic
            'u': 4, # underline
            'x': 5, # blinking
            'y': 6, # fast blinking
            'r': 7, # reverse
            'h': 8, # hide
            's': 9, # strikethrough
        },

        "HTML": {
            'b': "font-weight:bold",
            'i': "font-style:italic"
        }
    }

    def fmt(text, fg=None, bg=None, style=None):
        if(ColorPrinter.to_style == "Terminal"):
            props = []
            if isinstance(style, str):
                for letter in style:
                    props.append(ColorPrinter.FMTCODE[ColorPrinter.to_style][letter])
            if isinstance(fg, str):
                props.append(30 + ColorPrinter.COLCODE[ColorPrinter.to_style][fg])
            if isinstance(bg, str):
                props.append(40 + ColorPrinter.COLCODE[ColorPrinter.to_style][bg])

            props = ';'.join([str(x) for x in props])

            if(props):
                return '\x1b[%sm%s\x1b[0m' % (props, text)
            else:
                return text
        elif(ColorPrinter.to_style == "HTML"):
            style_string = ""
            if(isinstance(style, str)):
                for style_letter in style:
                    style_string += ColorPrinter.FMTCODE[ColorPrinter.to_style][style_letter] + "; "

            return "<span style='%s %s %s'>%s</span>" % (
                ("color:" + ColorPrinter.COLCODE[ColorPrinter.to_style][fg] + ";") if isinstance(fg, str) else "",
                ("background:" + ColorPrinter.COLCODE[ColorPrinter.to_style][bg] + ";") if isinstance(bg, str) else "",
                style_string,
                text
                )

    def cprint(text, fg=None, bg=None, style=None):
        print(ColorPrinter.fmt(text, fg, bg, style))
