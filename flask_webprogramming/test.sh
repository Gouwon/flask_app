list=$(pip3 list)

echo ">>>>>> \n ${list}"

echo pwd

echo $1, $2

case "$2" in
'')
    echo "!!!";;
js)
    echo "@@@";;
esac

cd $(dirname "$0")
pwd
ls -la

. ./start.sh

