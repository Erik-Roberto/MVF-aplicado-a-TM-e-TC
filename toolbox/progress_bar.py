import colorama

colorama.init()

GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
BLUE = colorama.Fore.BLUE
YELLOW = colorama.Fore.YELLOW


def progress_bar(color = GREEN):
    def inner(foo):
        def wrapper(*args, **kwargs):
            progress, total = foo(*args, **kwargs)
            percent = 100 * (progress / total)
            bar = "█"*int(percent) + "-"*(100 - int(percent))
            if percent == 100:
                print(color + f"\r|{bar}| {percent: .2f}%", end="\n")
            else:
                print(color + f"\r|{bar}| {percent: .2f}%", end="\r")
        return wrapper
    return inner


def pb(progress, total,color=GREEN):
    percent = 100 * (progress / total)
    bar = "█"*int(percent) + "-"*(100 - int(percent))
    if percent == 100:
        print(color + f"\r|{bar}| {percent: .2f}%", end="\n")
    else:
        print(color + f"\r|{bar}| {percent: .2f}%", end="\r")

def disable_color():
    colorama.Style.RESET_ALL