#!/bin/sh

export PATH=/bin:/usr/bin:/opt/rocks/bin

ME=`id -un`

if [ x$ME = xroot ]
then
	echo "Do not run $0 as root"
	exit
fi

AN=`/share/apps/ifi/available-nodes.sh; echo uvcluster`
TN=`hostname -s`

for N in `echo $AN | sed -e "s/$TN//"`
do
        ssh $N "killall -s 9 -u $ME" &
done
wait
