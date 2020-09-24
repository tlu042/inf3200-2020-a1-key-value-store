kill -9 $(sudo lsof -t  -i:8000)
kill -9 $(sudo lsof -t  -i:8001)
kill -9 $(sudo lsof -t  -i:8002)
kill -9 $(sudo lsof -t  -i:8003)
kill -9 $(sudo lsof -t  -i:8004)
kill -9 $(sudo lsof -t  -i:8005)
kill -9 $(sudo lsof -t  -i:8006)
kill -9 $(sudo lsof -t  -i:8007)
kill -9 $(sudo lsof -t  -i:8008)
kill -9 $(sudo lsof -t  -i:8009)
kill -9 $(sudo lsof -t  -i:8010)
kill -9 $(sudo lsof -t  -i:8011)

python3 node.py -p 8000 &
sleep .05
python3 node.py -p 8001 -e localhost:8000 &
sleep .05
python3 node.py -p 8002 -e localhost:8001 &
sleep .05
python3 node.py -p 8003 -e localhost:8002 &
sleep .05
python3 node.py -p 8004 -e localhost:8003 &
sleep .05
python3 node.py -p 8005 -e localhost:8004 &
sleep .05
python3 node.py -p 8006 -e localhost:8005 &
sleep .05
python3 node.py -p 8007 -e localhost:8006 &
sleep .05
python3 node.py -p 8008 -e localhost:8007 &
sleep .05
python3 node.py -p 8009 -e localhost:8008 &
sleep .05
python3 node.py -p 8010 -e localhost:8009 &
sleep .05
python3 node.py -p 8011 -e localhost:8010

