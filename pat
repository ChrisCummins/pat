#!/bin/bash

usage() {
    echo 'Usage: pat [--help] [--version] [--status] [--start]'
    echo '           [--stop | --kill]'
    echo ''
    echo 'Pat is an email notification daemon. It polls on a local Maildir'
    echo 'filesystem and displays desktop notifications when new mail has been'
    echo 'received. Settings are made in the ~/.config/patrc configuration'
    echo 'file.'
}

version() {
    echo 'pat version 0.0.1'
}

start_pat() {
    if [ -f $LOCK ]; then
	ps cax | grep $(cat $LOCK) &>/dev/null
	if [ $? -eq 0 ]; then
	    echo "unable to start, existing session ($(cat $LOCK | head -n1))" >&2
	    exit 1
	else
	    echo "removing dead lock '$LOCK'"
	    rm -f $LOCK
	fi
    fi

    if [ ! -f $CACHE ]; then
	touch $CACHE
	chmod 600 $CACHE
    fi

    $PAT &
    pid=$!
    echo $pid > $LOCK
    echo "pat started ($pid)"
    exit 0
}

kill_pat() {
    if [ -f $LOCK ]; then
	kill $(cat $LOCK) &>/dev/null
	if [ $? -eq 0 ]; then
	    echo "pat closed ($(cat $LOCK))"
	    rm -f $LOCK
	else
	    echo "no pat session found" >&2
	    rm -f $LOCK
	    exit 1
	fi
    else
	echo "no pat session found" >&2
	exit 1
    fi

    exit 0
}

status() {
    if [ -f $LOCK ]; then
	ps cax | grep $(cat $LOCK) &>/dev/null
	if [ $? -eq 0 ]; then
	    echo "pat running ($(cat $LOCK))"
	else
	    echo "pat not running (dead process $(cat $LOCK))"
	fi
    else
	echo "pat not running"
    fi

    exit 0
}

test -n "$PAT_DEBUG" && set -x
PATRC=~/.config/patrc
PAT=~/.local/share/pat/pat.py

# Parse non-functional arguments first.
for arg in $@; do
    case $arg in
	"--help")
            usage
            exit 0
	    ;;
	"--version")
	    version
	    exit 0
	    ;;
    esac
done

# Sanity checks and envrionment setup.
if [ ! -f $PAT ]; then
    echo "missing executable file '$PAT'!"
    exit 1
fi

if [ -f $PATRC ]; then
    . $PATRC
else
    echo "missing environment file '$PATRC'!"
    exit 1
fi

if [ -z $PAT_WORKING_DIR ]; then
    echo "no working directory (PAT_WORKING_DIR)"
    exit 1
fi

LOCK=$PAT_WORKING_DIR/lock
CACHE=$PAT_WORKING_DIR/cache

# Parse arguments.
for arg in $@; do
    case $arg in
	"--start")
	    start_pat
	    ;;
	"--kill" | "--stop")
	    kill_pat
	    ;;
	"--status")
	    status
	    ;;
	*)
	    echo "unkown option '$arg'" >&2
	    echo ""
	    usage
	    exit 1
    esac
done

# Default behaviour.
start_pat
