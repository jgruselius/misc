#!/usr/bin/env python

# Author:      Joel Gruselius 2018-10
# Description: Create a reminder entry in Reminder.app
# Usage:       <description>... @ <date and time>
# Example:     reminders Don't forget to do that @ Friday 16:30
# Requires:    https://github.com/bear/parsedatetime
# References:  https://gist.github.com/renfredxh/7836327
#              https://gist.github.com/n8henrie/c3a5bf270b8200e33591

import subprocess as sub
import sys
from datetime import datetime
import parsedatetime

# A apple script that creates a new reminder given a name date and time 
HELP = """Create reminders in the macOS Reminders app from the command line.
    usage: reminders <description>... @ <date and time>
    example: reminders Don't forget to do that @ Friday 16:30"""

OSASCRIPT = ('<<END\n'
'on run argv\n'
'    set dateString to date (item 2 of argv & " " & item 3 of argv)\n'
'    tell application "Reminders"\n'
'        make new reminder with properties {name:item 1 of argv, remind me date:dateString}\n'
'    end tell\n'
'end run\n'
'END')

def parse_date_time(text):
    cal = parsedatetime.Calendar()
    time_struct, status = cal.parse(text)
    if status != 0:
        # Convert to datetime object:
        dt = datetime(*time_struct[:6])
    else:
        raise ValueError("Could not parse date and time.")
    return dt


def new_reminder(remind_datetime, name):
    # Locale complicates things a litte:
    #timestr = remind_datetime.strftime("%I:%M:00%p")
    #datestr = remind_datetime.strftime("%m/%d/%Y")
    timestr = remind_datetime.strftime("%H:%M:00")
    datestr = remind_datetime.strftime("%Y-%m-%d")
    # Execute applescript via shell to create a new reminder.
    command = 'osascript - "{n}" {d} {t} {osa}'.format(n=name, d=datestr, 
                                                       t=timestr, osa=OSASCRIPT)
    sub.check_call(command, shell=True, stdout=sub.DEVNULL, stderr=sub.DEVNULL)


def main(args):
    # Specify a reminder date and time using "@":
    arg_str = " ".join(args)
    rem = [s.strip() for s in arg_str.split("@")]
    if(len(rem) < 2):
        raise ValueError("No time of reminder given.")
    dt = parse_date_time(rem[1])
    try:
        new_reminder(dt, rem[0])
    except sub.CalledProcessError as e:
        raise OSError("An error occured when calling the osascript")

    # Confirm that reminder:
    print("A new reminder was created:")
    print("\t{0}: {1}".format(dt.strftime("%Y-%m-%d %H:%M"), rem[0]))


if __name__ == "__main__":
    # Skip argparse until more options are added...
    # p = argparse.ArgumentParser(description="""Create reminders in the macOS
    #     Reminders app from the command line. Example:
    #     <script.py> Don't forget to do that @ Friday 16:30""")
    # p.add_argument("reminder_text", nargs="+",
    #     help="Title of reminder @ time and date of notification")
    # args = p.parse_args()

    args = sys.argv[1:]
    if not len(args) or args[0] == "-h" or args[0] == "--help":
        print(HELP)
    else:
        try:
            main(args)
        except Exception as e:
            sys.exit(e)
