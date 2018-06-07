#! /bin/sh

read -p "Path to the directory containing SimulaQron directory:" path

echo "Preparing environment:"

echo "Extending PYTHONPATH with '$path' ..."
export PYTHONPATH=$path:$PYTHONPATH

echo "Setting NETSIM to '$path/SimulaQron'"
export NETSIM=$path/SimulaQron
