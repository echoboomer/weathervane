from termcolor import colored

# Colorize function.
def color(i, cond):
  if i != cond:
    return(colored(i, 'red'))
  else:
    return(colored(i, 'green'))
