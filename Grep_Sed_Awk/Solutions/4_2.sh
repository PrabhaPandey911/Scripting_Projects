#!/bin/bash
echo -n Password:
read -s paswrd
x=${#paswrd}
echo -e "\n"
grep -q '.*[0-9].*' <<< $paswrd
y=$?
grep -q '.*[@#$%&*+-=].*' <<< $paswrd
z=$?

if [ $x -lt 8 ] || [ $y -ne 0 ] || [ $z -ne 0 ];then
	echo "Weak Password!!"
	exit 0
else
	echo "Strong Password!!"
	exit 0
fi
exit 0
