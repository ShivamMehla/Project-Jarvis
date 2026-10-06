import datetime as dt
from sys import exit
import subprocess as sp
from json import loads
import time

def main():
    while True:
        user = input("Ask Anything: ").strip().lower()
        output = handle_commands(user)
        print(output)

    
def handle_commands(u):
    if "time" in u or "date" in u:
        return get_time(u)
    elif "date" in u:
        return get_date()
    elif "open" in u:
        return open_app(u)
    elif "exit" in u:
        exit(0)
    else:
        return "I didn't get it."


def get_time(u):
    if "time" in u and "date" in u:
        return dt.datetime.now().strftime("Today is %d-%m-%Y and it's %I:%M %p right now.\n" 
        "Date: %d-%m-%Y\n" \
        "Time: %I:%M %p")
    elif "time" in u:
        return dt.datetime.now().strftime("It's %I:%M %p right now.")
    elif "date" in u:
        return dt.datetime.now().strftime("Today is %d-%m-%Y")


def get_date():
    current_date = dt.datetime.now().str

def open_app(a):
    _, name = a.split(" ", maxsplit=1)
    result = sp.run(["powershell.exe", "-Command", "ConvertTo-Json(Get-StartApps)"], capture_output=True, text=True)
    apps = loads(result.stdout)

    app_dict = {}
    for app in apps:
        app_dict[app["Name"].lower()] = app["AppID"]
    if name in app_dict:
        result = sp.Popen(["powershell.exe", "-Command", f"explorer.exe shell:AppsFolder\\{app_dict[name]}"])
        return f"Opening {name}"        
    else:
        result = sp.run(["powershell.exe", "-Command", f"convertto-json(get-command {name})"], capture_output=True, text=True)
        if result.stdout:
            command = loads(result.stdout)
            sp.Popen(command["Path"])
            return f"Opening {name}"
        else:
            return f"I am not able to find any app with name {name} in your system."
    
if __name__ == "__main__":
    main()