#!/usr/bin/env bash

echo '# HELP node_reboot_required Node reboot is required for software updates.'
echo '# TYPE node_reboot_required gauge'

NEXTLINE=0
FIND=""

for I in $(file /boot/vmlinuz*)
do
  if [ ${NEXTLINE} -eq 1 ]
  then
    FIND="${I}"
    NEXTLINE=0
  else
    if [ "${I}" = "version" ]
    then
      NEXTLINE=1
    fi
  fi
done

if [ ! "${FIND}" = "" ]
then
  CURRENT_KERNEL=$(uname -r)
  if [ ! "${CURRENT_KERNEL}" = "${FIND}" ]
  then
    echo "node_reboot_required{current_kernel=\"${CURRENT_KERNEL}\",new_kernel=\"${FIND}\"} 1"
    exit 0
  fi
fi

echo "node_reboot_required{current_kernel=\"${CURRENT_KERNEL}\"} 0"
