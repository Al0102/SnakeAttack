"""
Helpers for visual customization like text colour and emphasis.
"""
from enum import Enum


class Style(Enum):
    RESET = 0
    BOLD = 1
    DIM = 2
    ITALIC = 3
    UNDERLINE = 4
    # <-Usually only for Windows Powershell->
    SLOW_BLINK = 5
    RAPID_BLINK = 6
    STRIKE = 9
    # <------------------------------------->
    NORMAL_INTENSITY = 22
    NOT_ITALIC = 23
    NOT_UNDERLINED = 24
    NOT_BLINKING = 25
    # Foreground Colours
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    # Background Colours
    BACKGROUND_BLACK = 40
    BACKGROUND_RED = 41
    BACKGROUND_GREEN = 42
    BACKGROUND_YELLOW = 43
    BACKGROUND_BLUE = 44
    BACKGROUND_MAGENTA = 45
    BACKGROUND_CYAN = 46
    BACKGROUND_WHITE = 47


def get_styles():
    """
    Return a dictionary of available styles and their ANSI escape sequences.

    :postcondition: get a dictionary of available styles and their ANSI escape sequences
    :postcondition: the key-value pairs have the form <name>: <sequence> and both are strings
    :return: a dictionary representing the available styles and their ANSI escape sequences.

    >>> get_styles() == {
    ...     "reset": "\\033[0m",
    ...     "bold": "\\033[1m",
    ...     "dim": "\\033[2m",
    ...     "italic": "\\033[3m",
    ...     "underline": "\\033[4m",
    ...     "slow_blink": "\\033[5m",
    ...     "rapid_blink": "\\033[6m",
    ...     "strike": "\\033[9m",
    ...     "normal_intensity": "\\033[22m",
    ...     "not_italic": "\\033[23m",
    ...     "not_underlined": "\\033[24m",
    ...     "not_blinking": "\\033[25m",
    ...     "black": "\\033[30m",
    ...     "red": "\\033[31m",
    ...     "green": "\\033[32m",
    ...     "yellow": "\\033[33m",
    ...     "blue": "\\033[34m",
    ...     "magenta": "\\033[35m",
    ...     "cyan": "\\033[36m",
    ...     "white": "\\033[37m",
    ...     "background_black": "\\033[40m",
    ...     "background_red": "\\033[41m",
    ...     "background_green": "\\033[42m",
    ...     "background_yellow": "\\033[43m",
    ...     "background_blue": "\\033[44m",
    ...     "background_magenta": "\\033[45m",
    ...     "background_cyan": "\\033[46m",
    ...     "background_white": "\\033[47m"}
    True
    """
    return {
        Style.RESET: "\033[0m",
        Style.BOLD: "\033[1m",
        Style.DIM: "\033[2m",
        Style.ITALIC: "\033[3m",
        Style.UNDERLINE: "\033[4m",
        # <-Usually only for Windows Powershell->
        Style.SLOW_BLINK: "\033[5m",
        Style.RAPID_BLINK: "\033[6m",
        Style.STRIKE: "\033[9m",
        # <------------------------------------->
        Style.NORMAL_INTENSITY: "\033[22m",
        Style.NOT_ITALIC: "\033[23m",
        Style.NOT_UNDERLINED: "\033[24m",
        Style.NOT_BLINKING: "\033[25m",
        # Foreground Colours
        Style.BLACK: "\033[30m",
        Style.RED: "\033[31m",
        Style.GREEN: "\033[32m",
        Style.YELLOW: "\033[33m",
        Style.BLUE: "\033[34m",
        Style.MAGENTA: "\033[35m",
        Style.CYAN: "\033[36m",
        Style.WHITE: "\033[37m",
        # Background Colours
        Style.BACKGROUND_BLACK: "\033[40m",
        Style.BACKGROUND_RED: "\033[41m",
        Style.BACKGROUND_GREEN: "\033[42m",
        Style.BACKGROUND_YELLOW: "\033[43m",
        Style.BACKGROUND_BLUE: "\033[44m",
        Style.BACKGROUND_MAGENTA: "\033[45m",
        Style.BACKGROUND_CYAN: "\033[46m",
        Style.BACKGROUND_WHITE: "\033[47m"
    }


def style(text, *styles, reset=True):
    """
    Return <text> with the style <type> prepended to it.

    The optional <reset> will append the ANSI reset code to <text>

    :param text: a string representing the text to style
    :param reset: a boolean representing whether to reset the styling after <text>
    :param styles: Styles or strings representing the styles to apply to <text>
    :precondition: text must be a string representing the text to style
    :precondition: reset a boolean representing whether to reset the styling after <text>
    :precondition: types must be made up of strings found in get_styles()
    :postcondition: prepend and/or append ANSI codes to style the text when printing
    :return: a string representing the styled <text> with appropriate ANSI codes prepended/appended to it

    >>> style("This is red", Style.RED)
    '\\x1b[31mThis is red\\x1b[0m'
    >>> style("This is bold and blue", Style.BOLD, Style.BLUE)
    '\\x1b[1m\\x1b[34mThis is bold and blue\\x1b[0m'
    >>> style("This is bold and blue and not reset", Style.BOLD, Style.BLUE, reset=False)
    '\\x1b[1m\\x1b[34mThis is bold and blue and not reset'
    """
    codes = "".join(map(
        lambda name: get_styles()[name if type(name) == Style else Style[name.upper()]],
        styles))
    new_text = codes + text
    if reset:
        new_text += get_styles()[Style.RESET]
    return new_text


def reset_style():
    """
    Reset the text style being printed.

    :postcondition: print the reset escape code
    :postcondition: no newline will be printed

    >>> reset_style()
    \\x1b[0m
    """
    print(get_styles()[Style.RESET], end="", flush=True)


def main():
    """
    Drive the program.
    """
    print(style("This is RED", Style.RED), " --> but not this.")
    print(style("Unless...", Style.BOLD, Style.ITALIC))
    print(style("This is GREEN", Style.GREEN, reset=False), " --> reset is False.")

    print("RESET")
    reset_style()

    print(style("Under where?", Style.UNDERLINE))
    print(style("BACKGROUND AND TEXT", Style.BACKGROUND_YELLOW, Style.BLACK))

    input(style("Remember to blink", Style.RAPID_BLINK))
    input(style("But not too fast", Style.SLOW_BLINK))
    print(style("My eyes hurt and it's hard to see...", Style.DIM))

    print(style("I have one last secret...", Style.STRIKE))


if __name__ == '__main__':
    main()
