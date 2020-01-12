import os, subprocess

def generate():
    process ="./crunch {0} {1} -f /home/kuskus/Dropbox/ZyBR/crunch-3.6/charset.lst {2} -o /home/kuskus/Dropbox/ZyBR/AES/data/cr_wordlist.txt"
    known = None
    min = int(input("Enter minimum password length(in chars): "))
    max = int(input("Enter maximum password length: "))
    type = input("Type in desired charset: ")
    if min == max:
        known = input("Enter known characters, replace unknown ones with @ symbol (eg.: @@@know@@@@): ")
        process ="./crunch {0} {1} -f /home/kuskus/Dropbox/ZyBR/crunch-3.6/charset.lst {2} -t {3} -o /home/kuskus/Dropbox/ZyBR/AES/data/cr_wordlist.txt"
    subprocess.call(process.format(min, max, type, known), shell = True)