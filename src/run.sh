fuser -k 8000/tcp
fuser -k 8001/tcp
fuser -k 8002/tcp
fuser -k 8003/tcp
# fuser -k 8004/tcp
# fuser -k 8005/tcp
# fuser -k 8006/tcp
# fuser -k 8007/tcp
# fuser -k 8008/tcp
# fuser -k 8009/tcp
# fuser -k 8010/tcp
# fuser -k 8011/tcp
# fuser -k 8012/tcp
# fuser -k 8013/tcp
# fuser -k 8014/tcp
# fuser -k 8015/tcp
# fuser -k 8016/tcp

python3 node.py -p 8000 &
sleep .05
python3 node.py -p 8001 -e localhost:8000 &
sleep .05
python3 node.py -p 8002 -e localhost:8000 &
sleep .05
python3 node.py -p 8003 -e localhost:8000 &

# python3 node.py -p 8000 &
# python3 node.py -p 8001 &
# python3 node.py -p 8002 &
# python3 node.py -p 8003 &
# python3 node.py -p 8004 &
# python3 node.py -p 8005 &
# python3 node.py -p 8006 &
# python3 node.py -p 8007 &
# python3 node.py -p 8008 &
# python3 node.py -p 8009 &
# python3 node.py -p 8010 &
# python3 node.py -p 8011 &
# python3 node.py -p 8012 &
# python3 node.py -p 8013 &
# python3 node.py -p 8014 &
# python3 node.py -p 8015 &
# python3 node.py -p 8016 &
