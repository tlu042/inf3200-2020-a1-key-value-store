fuser -k 8000/tcp
fuser -k 8001/tcp
fuser -k 8002/tcp
fuser -k 8003/tcp

# python3 node.py -p 8000 &
# sleep .05
# python3 node.py -p 8001 -e localhost:8000 &
# sleep .05
# python3 node.py -p 8002 -e localhost:8000 &
# sleep .05
# python3 node.py -p 8003 -e localhost:8000 &

python3 node.py -p 8000 &
python3 node.py -p 8001 &
python3 node.py -p 8002 &
python3 node.py -p 8003 &
