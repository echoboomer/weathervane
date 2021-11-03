from termcolor import colored

# Colorize function.


def errcolor(i, cond):
    if i != cond:
        return colored(i, "red")
    else:
        return colored(i, "green")
