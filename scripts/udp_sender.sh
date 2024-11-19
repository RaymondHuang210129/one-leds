ip=$1
port=$2
count=$3
red=$4
blue=$5
green=$6

color="\x${red}\x${green}\x${blue}"

printf -v place_holder '%*s' "$count"
payload="$(printf '%s\n' "${place_holder// /${color}}")"

echo ${payload}

echo -n "${payload}" | nc -4u -w0 ${ip} ${port}
