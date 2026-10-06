import datetime as dt
from sys import exit
import subprocess as sp

def main():
    while True:
        user = input("Ask Anything: ").strip().lower()
        output = handle_commands(user)
        print(output)

    
def handle_commands(u):
    if "time" in u:
        return get_time()
    elif "exit" in u:
        exit(0)
    else:
        return "I didn't get it."


def get_time():
    current_time = dt.datetime.now().strftime("It's %I:%M %p right now")
    return current_time


if __name__ == "__main__":
    main()