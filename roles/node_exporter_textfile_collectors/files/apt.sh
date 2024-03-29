#!/usr/bin/env bash
#
# Description: Expose metrics from apt updates.
#
# Author: Ben Kochie <superq@gmail.com>

upgrades="$(/usr/bin/apt-get --just-print dist-upgrade \
  | /usr/bin/awk -F'[()]' \
      '/^Inst/ { sub("^[^ ]+ ", "", $2); gsub(" ","",$2);
                 sub("\\[", " ", $2); sub("\\]", "", $2); print $2 }' \
  | /usr/bin/sort \
  | /usr/bin/uniq -c \
  | /usr/bin/awk '{ gsub(/\\\\/, "\\\\", $2); gsub(/"/, "\\\"", $2);
           gsub(/\[/, "", $3); gsub(/\]/, "", $3);
           print "apt_upgrades_pending{origin=\"" $2 "\",arch=\"" $NF "\"} " $1}'
)"

autoremove="$(/usr/bin/apt-get --just-print autoremove \
  | /usr/bin/awk '/^Remv/{a++}END{printf "apt_autoremove_pending %d", a}'
)"

echo '# HELP apt_upgrades_pending Apt package pending updates by origin.'
echo '# TYPE apt_upgrades_pending gauge'
if [[ -n "${upgrades}" ]] ; then
  echo "${upgrades}"
else
  echo 'apt_upgrades_pending{origin="",arch=""} 0'
fi

echo '# HELP apt_autoremove_pending Apt package pending autoremove.'
echo '# TYPE apt_autoremove_pending gauge'
echo "${autoremove}"
