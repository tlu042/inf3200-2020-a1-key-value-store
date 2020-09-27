if [[ $# -lt 2 ]]; then
	echo "Usage: $0 <max_nodes> <port>"
	exit
fi

max_nodes=$1
port=$2

for ((nodes = 1; nodes <= max_nodes; nodes++)); do
	echo -e "Benchmarking on $nodes nodes.\n"
	./run-cluster.sh $nodes $port 1
	echo -e "\nKilling nodes..."
	./cleanup.sh &> /dev/null
	echo -e "Nodes killed!\n"
done
	
