#!/usr/bin/env bash
#/**
# * Created by Hoang Tran (hoangtq)
# * Copyright (c) 2021 ai face. All rights reserved.
# **/

function check_file {
	if [ ! -e "$1" ]; then
		echo "The file '$1' does not exist."
		return 1
	else
	  echo "The file '$1' exists!"
	fi
}

function create_folder() {

  if [ -d $1 ]; then
		echo "$1 exists!"
		return 0
	fi

	mkdir -p "${1}"

	if [ $? -ne 0 ]; then
		echo "Couldn't create $1"
		exit 3
	else
		echo "Created $1"
	fi
}

function create_file() {
    if ! [[ -f $1 ]]; then
        touch $1
    fi
}

pathToFile=$1
fileName=$2

check_file "${pathToFile}/${fileName}"

if [ $? -ne 0 ]; then
  create_folder "${pathToFile}"

  if [ $? -ne 0 ]; then
		echo "Couldn't create '${pathToFile}'"
		exit 1
	else
	  # tạo folder thành công
		create_file "${pathToFile}/${fileName}"
    if [ $? -ne 0 ]; then
      echo "Couldn't create '${fileName}'"
      exit 3
    else
      echo "Created '${fileName}'"
    fi
	fi
fi

exit 0
