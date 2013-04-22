#!/usr/bin/env python
#
# pat.py - the pat mail notification daemon worker process

from gi.repository import Gio
from collections import Counter
from time import gmtime, strftime
import os
import re
import subprocess
import time

# Global tick counter
jiffies = 0

## Environment variables and derivitives.
WORKING_DIR = os.getenv('PAT_WORKING_DIR', '~/.pat')
MAIL_DIR = os.getenv('PAT_MAILDIR', '~/Maildir')
POLL_TIME = float(os.getenv('PAT_POLL_TIME', 120))
LOG = os.getenv('PAT_LOG', None)
CACHE = WORKING_DIR + '/cache'
DEBUG = os.getenv('PAT_DEBUG', None)

# Write a message to log log file. Entries in the log file appear in the form:
#   [<timestamp>] <message>
def log(message):
    if (LOG != None):
        f = open(LOG, 'a')
        f.write('[' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '] '
                + message + '\n')
        f.close()

# Write a debugging message to log file if PAT_DEBUGGING envrionment variable is
# set. Debugging entires appear in the log as:
#   [<timestamp>] [DEBUG] <message>
#
# @param message string.
def debug(message):
    if (DEBUG != None):
        log('[DEBUG ' + jiffies + '] ' + message)

# Show a desktop notification, in the form:
#   <b><title></b> <title>
#
# @param title notification title.
# @param message notification message.
def notify(title, message):
    notify = Gio.DBusProxy.new_sync(Gio.bus_get_sync(Gio.BusType.SESSION, None),
                                    0, None, 'org.freedesktop.Notifications',
                                    '/org/freedesktop/Notifications',
                                    'org.freedesktop.Notifications', None)
    log(title + ': ' + message)
    notify.Notify('(susssasa{sv}i)', 'pat', 3, 'emblem-mail',
                  title, message,
                  [], {}, 10000)

# Get the name of the given message Maildir. If it is the base maildir,
# return None.
#
# @return string containing maildir name, or None if top dir.
def get_message_dir(m):
    dir = os.path.dirname(os.path.dirname(m))
    if dir == MAIL_DIR:
        return None
    else:
        return re.sub('^\.', '', os.path.split(dir)[-1])

# Show a new message notification.
#
# @param m file path to new message.
def notify_message(m):
    for l in open(m):
        if re.search('^From:\s+', l, flags=re.IGNORECASE):
            sender = re.sub('^From:\s+', '', l, flags=re.IGNORECASE).strip()
            dir = os.path.dirname(os.path.dirname(m))
            if dir == MAIL_DIR:
                notify('New mail', sender)
            else:
                dir = re.sub('^\.', '', os.path.split(dir)[-1])
                notify('[' + dir + ']', sender)
            return

# Show a new messages notification in the format:
#   New mail (<num) : <box1> (<count>), <box2> (<count)...
#
# @param M list structure containing file paths to new messages.
def notify_messages(M):
    D = Counter([get_message_dir(x) for x in M]).most_common(3)
    summary = ''
    for d in D:
        if d[0] == None:
            summary += 'Inbox (' + str(d[1]) + '), '
        else:
            summary += d[0] + ' (' + str(d[1]) + '), '
    summary = summary[:-2]
    if len(D) < len(M):
        summary += '...'
    notify('New mail (' + str(len(M)) + ')', summary)

# Send desktop notification for new mail.
#
# @param M list structure containing file paths to new messages.
def notify_new_mail(M):
    if len(M) == 1:
        notify_message(M[0])
    elif len(M) >= 2:
        notify_messages(M)

# Get the contents of a directory.
#
# @param d path to directory
# @return a list structure containing file paths to directory contents.
def files_in_dir(d):
    f = []
    p = subprocess.Popen(['find', d, '-type', 'f'], stdout=subprocess.PIPE)
    for l in iter(p.stdout.readline, ''):
        f.append(l.rstrip())
    return f

# The email cache file is compared against the parameter list, removing any
# shared items. This leaves a list of items that are unique to the parameter.
#
# @param M a list structure containing file paths to new messages.
# @return list of file paths that are unique to param M.
def strip_cached_mail(M):
    M_cache = []
    try:
        f = open(CACHE, 'r')
        M_cache = [x.strip() for x in f.readlines()]
        f.close
        return [x for x in M if x not in M_cache]
    except IOError:
        return M

# Cache a list of file paths to new messages to cache file.
#
# @param M list structure containing file paths to new messages.
def cache_mail_files(M):
    f = open(CACHE, 'w')
    for m in M:
        f.write(str(m) + '\n')
    f.close()
    os.chmod(CACHE, 0600) # bMake sure we keep our 600 mod.

# Perform a polling operation on the maildir and display a notification if
# necessary.
def poll_maildir():
    B = []
    M = []
    p = subprocess.Popen(['find', MAIL_DIR, '-type', 'd',
                          '-name', '*new'], stdout=subprocess.PIPE)
    for l in iter(p.stdout.readline, ''):
        B.append(l.rstrip())
    for b in B:
        M.extend(files_in_dir(b))
    notify_new_mail(strip_cached_mail(M))
    cache_mail_files(M)


log('starting session (' + str(os.getpid()) + ')')
while True:   # Main loop.
    debug('polling \'' + MAIL_DIR + '\'')
    poll_maildir()
    time.sleep(POLL_TIME)
    jiffies += 1
