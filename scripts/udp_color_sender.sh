#!/bin/bash

ip="$1"
port="$2"
count="$3"
red="$4"
green="$5"
blue="$6"

color="$( echo -e $(printf "\x%s\x%s\x%s" "$red" "$green" "$blue" 2> /dev/null))"
printf -v place_holder '%*s' "${count}"
payload="$(printf '%s' "${place_holder// /${color}}")"
echo "${payload}" | nc -4u -w0 ${ip} ${port}
