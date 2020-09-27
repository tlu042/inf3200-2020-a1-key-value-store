if [[ $# -lt 2 ]]; then
	echo "Usage: $0 <num_hosts> <port> [benchmark (default=0)]"
	exit
fi

port=$2

computers=($(/share/apps/ifi/available-nodes.sh | grep compute | shuf | head -n $1))

entry=${computers[0]}
unset computers[0]

echo Starting initial node: $entry:$port
ssh -f $entry python3 $(pwd)/node.py -p $port &> /dev/null
wait

for computer in ${computers[@]}; do
	echo Node $computer:$port joining $entry:$port
	ssh -f $computer python3 $(pwd)/node.py -p $port -e $entry:$port &> /dev/null
	wait
done

if [[ "$3" == "1" ]]; then
	sleep 2
	python3 client.py $entry.local:$port
fi
