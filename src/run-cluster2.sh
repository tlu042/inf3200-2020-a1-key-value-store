if [[ $# -lt 2 ]]; then
	echo "Usage: $0 <num_hosts> <port> [create_computers=0]"
	exit
fi

port=$2

if [[ $3 == 0 ]]; then 
	computers=($(/share/apps/ifi/available-nodes.sh | grep compute | shuf | head -n $1))
	rm node_list.txt
	rm node_list_ports.txt
	for computer in ${computers[@]}; do
		echo $computer >> node_list.txt
		echo $computer:$port >> node_list_ports.txt
		echo Node $computer:$port starting...
		ssh -f $computer python3 $(pwd)/node.py -p $port &> /dev/null
	done
else
	readarray -t computers < node_list.txt
	for computer in ${computers[@]}; do
		echo Node $computer:$port starting...
		ssh -f $computer python3 $(pwd)/node.py -p $port &> /dev/null
	done
fi

sleep 10
