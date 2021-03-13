#/**
# * Created by Hoang Tran (hoangtq)
# * Copyright (c) 2021 ai face. All rights reserved.
# **/
LOG_PATH="logs"
LOG_FILE="monitor.log"

all: update
update: setup tear-down
	bash scripts/update.sh >> "${LOG_PATH}/${LOG_FILE}"
	echo "" >> "${LOG_PATH}/${LOG_FILE}"
setup:
	bash scripts/file_util.sh "${LOG_PATH}" "${LOG_FILE}"
tear-down:
	echo "" >> "${LOG_PATH}/${LOG_FILE}"