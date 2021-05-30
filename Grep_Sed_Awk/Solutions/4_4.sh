#!/bin/bash
if [ $# -lt 2 ]; then
	echo "give proper no. of arguments!!"
	exit 1
fi

array=("$@")
source_dir=${array[0]}
cd $source_dir 2>/dev/null
if [ $? != 0 ]
then
	echo "wrong source directory given!"
	exit 1
fi

if [ $# -eq 2 ] && [ $2 != "all" ]; then

	for ((i=1;i<$#;i++))
	do
		type=$(echo ${array[i]} | tr [:lower:] [:upper:])
		mkdir $type 2> /dev/null
	done
	files=(`ls`)
	z=`ls | wc -w `
	for ((i=0;i<z;i++))
	do
		if [ ! -f ${files[i]} ]; then
			continue
		fi
		grep -q '.*\...*' <<< ${files[i]}
		y=$?
		if [ $y -eq 0 ];then
			extension=$(cut -d '.' -f 2- <<< ${files[i]} | tr [:lower:] [:upper:])
		    echo $extension
	        mv ${files[i]} ./$extension
	        # echo "mv ${files[i]} ./$extension"
	    else 
	    	continue
	    fi
	done 
elif [ $# -eq 2 ] && [ $2 = "all" ];then
	files=(`ls`)
	z=`ls | wc -w `
	for ((i=0;i<z;i++))
	do
		if [ ! -f ${files[i]} ]; then
			continue
		fi
		grep -q '.*\...*' <<< ${files[i]}
		y=$?
		if [ $y -eq 0 ];then
			extension=$(cut -d '.' -f 2- <<< ${files[i]} | tr [:lower:] [:upper:])
		    echo $extension
		    mkdir $extension 2> /dev/null
	        mv ${files[i]} ./$extension
	        #echo "mv ${files[i]} ./$extension"
	    else 
	    	continue
	    fi
	done 

fi 