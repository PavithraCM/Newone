#!/bin/bash
SRVPORT=4499
while true; do
    cat <<EOF | nc -l -p $SRVPORT -q 1
HTTP/1.1 200 OK
Content-Type: text/plain

$(/usr/games/fortune | /usr/games/cowsay)
EOF
done



