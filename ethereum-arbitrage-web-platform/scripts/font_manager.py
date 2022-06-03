class FontColor:
    PURPLE = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[93m"
    YELLOW = "\033[91m"
    NORMAL = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def tag(name):
    return f"{FontColor.BOLD}\n[{name}]{FontColor.NORMAL}"


def highlight(address):
    return f"{FontColor.BOLD}{FontColor.BLUE}{address}{FontColor.NORMAL}"


def underline(text):
    return f"{FontColor.UNDERLINE}{text}{FontColor.NORMAL}"


def purple(text):
    return f"{FontColor.PURPLE}{text}{FontColor.NORMAL}"


def green(text):
    return f"{FontColor.GREEN}{text}{FontColor.NORMAL}"


def yellow(text):
    return f"{FontColor.YELLOW}{text}{FontColor.NORMAL}"


def cyan(text):
    return f"{FontColor.CYAN}{text}{FontColor.NORMAL}"


def red(text):
    return f"{FontColor.RED}{text}{FontColor.NORMAL}"
