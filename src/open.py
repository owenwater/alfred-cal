#!/usr/bin/python
# encoding: utf-8

import subprocess

applescript_name_tem = "open_%s.scpt"
arg_tem = {
    "calendar": "%s %s %s",
    "fantastical": "%s-%s-%s",
    "busycal": "%s-%s-%s"
}

def open_cal(arg):
    arg = arg.strip()
    if arg.endswith(".json"):
        open_file(arg)
    else:
        from workflow import Workflow
        wf = Workflow()
        
        default_software = 'calendar'
        software = wf.settings.get('software', default_software)
        file_name = applescript_name_tem %(software)

        year, month, day = arg.split()
        script_arg = arg_tem[software] %(year, month, day)

        execute_osascript(file_name, script_arg)

def execute_osascript(file, arg):
    subprocess.call(['osascript', file, arg])

def open_file(file):
    subprocess.call(['open', file])

if __name__ == "__main__":
    import sys
    open_cal(' '.join(sys.argv[1:]))
