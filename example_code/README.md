Client code for INF-3200 Assignment 1
==================================================

This is a simple Python script to check your node's API.


Test client: `client.py`
--------------------------------------------------

The client will walk your network using the `/neighbours` call, and then it will
perform a few simple checks to see if it can PUT and GET values using the
`/storage/<KEY>` call.

To use:

1. Start your network
2. Run the client code, giving it a node host:port to start with.

        python3 client.py localhost:8000


Dummy node: `dummynode.py`
--------------------------------------------------

This is skeleton code for a node, mainly just to test the client code. 

If you want to run it, use -p to set the port number, and then give it a list of
neighbours to report.

Example:

    python3 node.py -p 8000 localhost:8001 localhost:8002 &
    python3 node.py -p 8001 localhost:8000 localhost:8002 &
    python3 node.py -p 8002 localhost:8000 localhost:8001 &

    python3 client.py localhost:8000

The dummy node stores values sent to it and it reports the neighbours given on
its command line, but it doesn't actually communicate with the neighbours.
