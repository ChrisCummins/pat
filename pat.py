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

## Environment variables and derivitives.
WORKING_DIR = os.getenv('PAT_WORKING_DIR', '~/.local/share/pat')
MAIL_DIR = os.getenv('PAT_MAILDIR', '~/Maildir')
POLL_TIME = float(os.getenv('PAT_POLL_TIME', 120))
LOG = os.getenv('PAT_LOG', None)
CACHE = WORKING_DIR + '/cache'
DEBUG = os.getenv('PAT_DEBUG', None)

# Write a message to log.
def log(message):
    if (LOG != None):
        f = open(LOG, 'a')
        f.write('[' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '] '
                + message + '\n')
        f.close()

def debug(message):
    if (DEBUG != None):
        log('[DEBUG] ' + message)

# Send a desktop notification.
def notify(title, message):
    d = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    notify = Gio.DBusProxy.new_sync(d, 0, None,
                                    'org.freedesktop.Notifications',
                                    '/org/freedesktop/Notifications',
                                    'org.freedesktop.Notifications', None)
    log(title + ': ' + message)
    notify.Notify('(susssasa{sv}i)', 'pat', 3, 'emblem-mail',
                  title, message,
                  [], {}, 10000)

# Return the name of the given message Maildir. If it is the base maildir,
# return None.
def get_message_dir(m):
    dir = os.path.dirname(os.path.dirname(m))
    if dir == MAIL_DIR:
        return None
    else:
        return re.sub('^\.', '', os.path.split(dir)[-1])

# Show a new message notification.
def notify_message(m):
    for l in open(m):
        if re.search('^From:\s+', l, flags=re.IGNORECASE):
            sender = re.sub('^From:\s+', '', l, flags=re.IGNORECASE).strip()
            dir = os.path.dirname(os.path.dirname(m))
            if dir == MAIL_DIR:
                notify('New mail', sender)
            else:
                dir = re.sub('^\.', '', os.path.split(dir)[-1])
                notify('New mail [' + dir + ']', sender)

# Show a new messages notification.
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

def notify_new_mail(M):
    if len(M) == 1:
        notify_message(M[0])
    elif len(M) >= 2:
        notify_messages(M)

def files_in_dir(d):
    f = []
    p = subprocess.Popen(['find', d, '-type', 'f'], stdout=subprocess.PIPE)
    for l in iter(p.stdout.readline, ''):
        f.append(l.rstrip())
    return f

def strip_cached_mail(M):
    M_cache = []
    try:
        f = open(CACHE, 'r')
        M_cache = [x.strip() for x in f.readlines()]
        f.close
        return [x for x in M if x not in M_cache]
    except IOError:
        return M_cache

def cache_mail_files(M):
    f = open(CACHE, 'w')
    for m in M:
        f.write(str(m) + '\n')
    f.close()
    os.chmod(CACHE, 0600) # Make sure we keep our 600 mod.

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

log('started session (' + str(os.getpid()) + ')')
while True:
    debug('polling \'' + MAIL_DIR + '\'')
    poll_maildir()
    time.sleep(POLL_TIME)
