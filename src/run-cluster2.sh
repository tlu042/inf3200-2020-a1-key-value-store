if [[ $# -lt 2 ]]; then
	echo "Usage: $0 <num_hosts> <port>"
	exit
fi

port=$2

computers=($(/share/apps/ifi/available-nodes.sh | grep compute | shuf | head -n $1))

entry=${computers[0]}
unset computers[0]

echo Starting initial node: $entry:$port
ssh -f $entry python3 $(pwd)/node.py -p $port &> /dev/null

for computer in ${computers[@]}; do
	echo Node $computer:$port starting...
	ssh -f $computer python3 $(pwd)/node.py -p $port &> /dev/null
done
