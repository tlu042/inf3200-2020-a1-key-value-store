kill -9 $(sudo lsof -t  -i:8000)
kill -9 $(sudo lsof -t  -i:8001)
kill -9 $(sudo lsof -t  -i:8002)
kill -9 $(sudo lsof -t  -i:8005)
kill -9 $(sudo lsof -t  -i:8004)

python node.py -p 8000 &
python node.py -p 8001 -e localhost:8000 &
python node.py -p 8002 -e localhost:8001 &

