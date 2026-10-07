import datetime as dt
from sys import exit
import subprocess as sp
import json

def main():
    while True:
        user = input("Ask Anything: ").strip().lower()
        command = identify_commands(user)
        command_data = handle_commands(command, user)
        output = execute_command(command_data)
        print(output)

    
def identify_commands(user):
    if "time" in user or "date" in user:
        return "get_time"
    elif "open" in user:
        return "open_app"
    elif "exit" in user:
        exit(0)
    else:
        return "unknown"


def handle_commands(command, user):
    if command == "get_time":
        command_data = {"command": command, "argument": user}
    elif command == "open_app":
        if " " not in user:
            command_data = {"command": command, "argument": None}
        else:
            _, name = user.split(" ", maxsplit=1)
            command_data = {"command": command, "argument": name}
    else:
        command_data = {"command": command, "argument": None}
    return command_data


def execute_command(cd):
    if cd["command"] == "unknown":
        return "I didn't get it."
    if cd["command"] == "open_app" and cd["argument"] is None:
        return "Which app do you want me to open?"
    
    commands = {"get_time": get_time, "open_app": open_app}
    return commands[cd["command"]](cd["argument"])


def get_time(u):
    if "time" in u and "date" in u:
        return dt.datetime.now().strftime("Today is %d-%m-%Y and it's %I:%M %p right now.\n" 
        "Date: %d-%m-%Y\n" \
        "Time: %I:%M %p")
    elif "time" in u:
        return dt.datetime.now().strftime("It's %I:%M %p right now.")
    elif "date" in u:
        return dt.datetime.now().strftime("Today is %d-%m-%Y")


def open_app(name):
    result = sp.run(["powershell.exe", "-Command", "ConvertTo-Json(Get-StartApps)"], capture_output=True, text=True)
    apps = json.loads(result.stdout)

    app_dict = {}
    for app in apps:
        app_dict[app["Name"].lower()] = app["AppID"]
    if name in app_dict:
        result = sp.Popen(["powershell.exe", "-Command", f"explorer.exe shell:AppsFolder\\{app_dict[name]}"])
        return f"Opening {name}"        
    else:
        result = sp.run(["powershell.exe", "-Command", f"convertto-json(get-command {name})"], capture_output=True, text=True)
        if result.stdout:
            command = json.loads(result.stdout)
            sp.Popen(command["Path"])
            return f"Opening {name}"
        else:
            return f"I am not able to find any app with name {name} in your system."

    
if __name__ == "__main__":
    main()