#!/bin/sh

mode="${1}"
shift
case $mode in
"-p" | "--postal")
    python ./check_all_by_postal_code.py ${@}
    ;;
*)
    echo "Use -p"
    ;;
esac
