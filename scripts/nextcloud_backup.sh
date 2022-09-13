#!/bin/bash

# assumes that python b2 module is installed and user is authenticated

nextcloud_user=""

password=""

bucket=""

backup="nextcloud_backup_$(date +%Y_%m_%d).tar.gz.enc"

tar czf - -C / var/www/nextcloud/data/${nextcloud_user}/files | \
openssl enc -aes-256-cbc -pbkdf2 -pass pass:${password} -out /tmp/${backup}

python3 -m b2 upload-file ${bucket} /tmp/${backup} ${backup}

rm /tmp/${backup}