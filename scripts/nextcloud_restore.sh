#!/bin/bash

nextcloud_user=""

password=""

bucket=""

backup=$(python3 -m b2 ls ${bucket} | sort -nr | head -n 1)

python3 -m b2 download-file-by-name ${bucket} ${backup} /tmp/${backup}

openssl enc -d -aes-256-cbc -pbkdf2 -pass pass:${password} -in /tmp/${backup} | \
tar xzkf - -C /

rm /tmp/${backup}