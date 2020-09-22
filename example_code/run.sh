kill -9 $(sudo lsof -t  -i:8000)
kill -9 $(sudo lsof -t  -i:8001)
kill -9 $(sudo lsof -t  -i:8002)

python3 dummynode.py -p 8000 localhost:8001 localhost:8002 &
python3 dummynode.py -p 8001 localhost:8002 localhost:8000 &
python3 dummynode.py -p 8002 localhost:8000 localhost:8001