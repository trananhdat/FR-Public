#!/usr/bin/env bash

#/**
# * Created by Hoang Tran (hoangtq)
# * Copyright (c) 2021 ai face. All rights reserved.
# **/

SOURCE="https://github.com/trananhdat/FR-Public.git"
PROJECT_NAME="FR-Public"
PROJECT_NAME_OLD="FR-Public_Old"
STATUS_OK=0

cd ..

curr_dir=$(pwd)

tmp="tmp-clone"

if [ -d "${tmp}" ]; then
  time=$(date +"%T %d-%m-%Y")
  echo "${time} [I] Folder '${tmp}' exist!"
else
  mkdir -p "${tmp}"
  time=$(date +"%T %d-%m-%Y")
	echo "${time} [I] Created ${tmp}"
fi

cd ${tmp}

git clone "${SOURCE}"


if [ $? -ne ${STATUS_OK} ]; then
  time=$(date +"%T %d-%m-%Y")
  echo "${time} [E] Clone sourcecode fail"
  exit 1
else
  time=$(date +"%T %d-%m-%Y")
  echo "${time} [I] Clone sourcecode done!"
fi

cd ${curr_dir}

mv ${PROJECT_NAME} ${PROJECT_NAME_OLD}

if [ $? -ne ${STATUS_OK} ]; then
  time=$(date +"%T %d-%m-%Y")
  echo "${time} [E] Move sourcecode: '${PROJECT_NAME}' to '${PROJECT_NAME_OLD}' fail"
  exit 1
else
  time=$(date +"%T %d-%m-%Y")
  echo "${time} [I] Move sourcecode '${PROJECT_NAME}' to '${PROJECT_NAME_OLD}' done!"
fi


mv "${tmp}/${PROJECT_NAME}" ${PROJECT_NAME}

if [ $? -ne ${STATUS_OK} ]; then
  time=$(date +"%T %d-%m-%Y")
  echo "${time} [E] Move sourcecode: '${tmp}/${PROJECT_NAME}' to '${PROJECT_NAME_OLD}' fail"

  echo "Reupdate..."
  mv ${PROJECT_NAME_OLD} ${PROJECT_NAME}
  if [ $? -ne ${STATUS_OK} ]; then
    time=$(date +"%T %d-%m-%Y")
    echo "${time} [E] Move sourcecode: '${PROJECT_NAME_OLD}' to '${PROJECT_NAME}' fail"
    exit 1
  else
    time=$(date +"%T %d-%m-%Y")
    echo "${time} [I] Move sourcecode '${PROJECT_NAME_OLD}' to '${PROJECT_NAME}' done!"
  fi
  exit 1
else
  time=$(date +"%T %d-%m-%Y")
  echo "${time} [I] Move sourcecode: '${tmp}/${PROJECT_NAME}' to '${PROJECT_NAME_OLD}' done!"
fi

exit 0
