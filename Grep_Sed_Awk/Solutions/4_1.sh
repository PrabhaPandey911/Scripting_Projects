#!/bin/bash
if [ $# -lt 1 ]; then
	echo "give one file name as argument"
	exit 0
fi
if [ $# -eq 1 ]; then
	var=$1
    echo $var
    s=$var
	echo $1
	if [ -f "$s" ]; then
		case $s in 
			*.tar) tar xf "$1" ;;
			*.tar.gz) tar xzf "$1" ;;
			*.tar.bz2) tar xjf "$1" ;; 
			*.bz2) bunzip2 "$1" ;; 
			*.zip) unzip "$1" ;;
			*.tar.xz) tar zxvf "$1" ;;
			*.rar) rar x "$1" ;;
			*.gz) gunzip "$1" ;;
			*.tbz2) tar xjf "$1" ;;
			*.tgz) tar xzf "$1" ;;
			*.xz) xz -d "$1" ;;
			*) echo "contents of '$1' can't be extracted" ;;
	    esac
	else
		echo "$1 is not a file"
	fi 
	exit 0
fi 