import os
import subprocess

def save_query(save, name, wires, br, length, start, end, display):
    save = os.getenv("HOME") + "/.config/sootty/save/" + save
    print(save)
    with open(save, 'w') as wf:
        wf.truncate(0)
        if name:
            wf.write("sootty -f \"" + name + "\"")
        if wires:
            wf.write(" -w \"" + wires + "\"")
        if br:
            wf.write(" -b \"" + br + "\"")
        if length:
            wf.write(" -l \"" + length + "\"")
        if start:
            wf.write(" -s \"" + start + "\"")
        if end:
            wf.write(" -e \"" + end + "\"")
        if display:
            wf.write(" -d")

def reload_query(reload):
    with open(reload, 'r') as rf:
        cmd  = rf.readline()
        process = subprocess.run(cmd, shell=True)

def is_save_file(filename):
    if filename.endswith(".txt"):
        return True
    else:
        return False