import argparse
import signal
import threading
import socket
import socketserver
import json
import re
import http.client
from hashlib import sha1
from http.server import BaseHTTPRequestHandler, HTTPServer

object_store = {}


class NodeHttpHandler(BaseHTTPRequestHandler):
    def send_whole_response(self, code, content, content_type="text/plain"):

        if isinstance(content, str):
            content = content.encode("utf-8")
            if not content_type:
                content_type = "text/plain"
            if content_type.startswith("text/"):
                content_type += "; charset=utf-8"
        elif isinstance(content, bytes):
            if not content_type:
                content_type = "application/octet-stream"
        elif isinstance(content, object):
            content = json.dumps(content, indent=2)
            content += "\n"
            content = content.encode("utf-8")
            content_type = "application/json"

        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.send_header('Content-length', len(content))
        self.end_headers()
        self.wfile.write(content)

    def extract_key_from_path(self, path):
        return re.sub(r'/storage/?(\w+)', r'\1', path)

    def do_PUT(self):
        content_length = int(self.headers.get('content-length', 0))
        value = self.rfile.read(content_length)

        if self.path.startswith("/storage"):

            key = self.extract_key_from_path(self.path)

            object_store[key] = value

            # Send OK response
            self.send_whole_response(200, "Value stored for " + key)

        elif self.path.startswith("/join"):
            status, neighbors = self.server.find_neighbors(value)
            self.send_whole_response(status, neighbors)

        elif self.path.startswith("/update"):
            status = self.server.update_neighbors(value)
            self.send_whole_response(status, None)

    def do_GET(self):
        if self.path.startswith("/storage"):
            key = self.extract_key_from_path(self.path)

            if key in object_store:
                self.send_whole_response(200, object_store[key])
            else:
                self.send_whole_response(200, self.ask_neighbor(key))

        elif self.path.startswith("/neighbors"):
            self.send_whole_response(
                200, {"successor": self.server.successor, "predecessor": self.server.predecessor})

        else:
            self.send_whole_response(404, "Unknown path: " + self.path)

    def ask_neighbor(self, key):
        neighbor = self.server.successor[1]
        print(neighbor)
        conn = http.client.HTTPConnection(self.server.successor[1].decode())
        conn.request("GET", "/storage/" + key)
        resp = conn.getresponse()
        headers = resp.getheaders()
        if resp.status != 200:
            value = None
        else:
            value = resp.read()
        contenttype = "text/plain"
        for h, hv in headers:
            if h == "Content-type":
                contenttype = hv
        if contenttype == "text/plain":
            value = value.decode("utf-8")
        conn.close()

        return value


class ThreadingHttpServer(HTTPServer, socketserver.ThreadingMixIn):
    def __init__(self, *args, entry_node=None):
        super().__init__(*args)
        self.address = f"{self.server_address[0]}:{self.server_address[1]}"
        self.key = self.hash_value(self.address.encode())
        self.successor = None
        self.predecessor = None
        if entry_node:
            self.join_ring(entry_node)
        print(
            f"{self.address} got successor {self.successor} and predecessor {self.predecessor} and own key {self.key}")

    def update_neighbors(self, new_node):
        key = self.hash_value(new_node)
        new_node = new_node.decode()

        if self.key < key:
            if (key > self.predecessor[0]) or (self.predecessor[0] > self.key):
                self.predecessor = (key, new_node)
        elif self.key > key:
            if (key < self.successor[0]) or (self.successor[0] < self.key):
                self.successor = (key, new_node)
        else:
            return - 1

        return 200

    def request(self, method, client, path, value=None):
        conn = http.client.HTTPConnection(client)
        conn.request(method, path, value)
        resp = conn.getresponse()
        headers = resp.getheaders()
        conn.close()
        return resp, headers

    def join_ring(self, node):
        resp, headers = self.request(
            "PUT", node, "/join", self.address)
        if resp.status != 200:
            print("Failed to join ring")
        else:
            value = resp.read()
        print("\n\n\n\n\n-----------------\n\n\n\n\n")
        # contenttype = "application/json"
        # for h, hv in headers:
        #     if h == "Content-type":
        #         contenttype = hv
        # if contenttype == "text/plain":
        #     raise NotImplementedError()
        # elif contenttype == "application/json":
        #     print(value)
        print("------------------------------------")
        print(value)
        print("------------------------------------")
        neighbors = json.loads(value.decode())
        self.successor = neighbors["successor"]
        self.predecessor = neighbors["predecessor"]

    def find_neighbors(self, new_node):
        neighbors = {}
        status = 200
        key = self.hash_value(new_node)
        new_node = new_node.decode()

        # If single node
        if not (self.successor or self.predecessor):
            self.successor = (key, new_node)
            self.predecessor = (key, new_node)
            neighbors["predecessor"] = (self.key, self.address)
            neighbors["successor"] = (self.key, self.address)
            neighbors = json.dumps(neighbors, indent=2)
            return status, neighbors

        if key < self.key:
            if (key > self.predecessor[0]) or (self.predecessor[0] > self.key):
                neighbors["successor"] = (self.key, self.address)
                neighbors["predecessor"] = self.predecessor
                self.request(
                    "PUT", self.predecessor[1], "/update", new_node)
                self.predecessor = (key, new_node)
                neighbors = json.dumps(neighbors, indent=2)
                status = 200

            else:
                resp, headers = self.request(
                    "PUT", self.predecessor[1], "/join", new_node)
                status = resp.status
                if resp.status != 200:
                    print("Failed to find neighbors")
                else:
                    value = resp.read()
                print("\n\n\n\n\n\n self.successor > key < self.key \n\n\n\n\n\n")
                # contenttype = "application/json"
                # for h, hv in headers:
                #     if h == "Content-type":
                #         contenttype = hv
                # if contenttype == "text/plain":
                #     raise NotImplementedError()
                # elif contenttype == "application/json":
                #     neighbors = value
                neighbors = value

        # key > self.key
        else:
            if (key < self.successor[0]) or (self.successor[0] < self.key):
                neighbors["successor"] = self.successor
                neighbors["predecessor"] = (self.key, self.address)
                self.request(
                    "PUT", self.successor[1], "/update", new_node)
                self.successor = (key, new_node)
                neighbors = json.dumps(neighbors, indent=2)
                status = 200

            else:
                resp, headers = self.request(
                    "PUT", self.successor[1], "/join", new_node)
                status = resp.status
                if resp.status != 200:
                    print("Failed to find neighbors")
                else:
                    value = resp.read()
                print("\n\n\n\n\n\n self.successor < key > self.key \n\n\n\n\n\n")
                # contenttype = "application/json"
                # for h, hv in headers:
                #     if h == "Content-type":
                #         contenttype = hv
                # if contenttype == "text/plain":
                #     raise NotImplementedError()
                # elif contenttype == "application/json":
                #     neighbors = value
                neighbors = value

        return status, neighbors

    def hash_value(self, value):
        m = sha1()
        m.update(value)
        return m.hexdigest()


def arg_parser():
    PORT_DEFAULT = 8000
    DIE_AFTER_SECONDS_DEFAULT = 20 * 60
    parser = argparse.ArgumentParser(prog="node", description="DHT Node")

    parser.add_argument("-p", "--port", type=int, default=PORT_DEFAULT,
                        help="port number to listen on, default %d" % PORT_DEFAULT)

    parser.add_argument("--die-after-seconds", type=float,
                        default=DIE_AFTER_SECONDS_DEFAULT,
                        help="kill server after so many seconds have elapsed, " +
                        "in case we forget or fail to kill it, " +
                        "default %d (%d minutes)" % (DIE_AFTER_SECONDS_DEFAULT, DIE_AFTER_SECONDS_DEFAULT/60))

    parser.add_argument("-e", "--entry", type=str, help="Entry node")

    return parser


def run_server(args):
    server = ThreadingHttpServer(
        ('', args.port), NodeHttpHandler, entry_node=args.entry)

    def server_main():
        print("Starting server on port {}. Entry: {}".format(
            args.port, args.entry))
        server.serve_forever()
        print("Server has shut down")

    def shutdown_server_on_signal(signum, frame):
        print("We get signal (%s). Asking server to shut down" % signum)
        server.shutdown()

    # Start server in a new thread, because server HTTPServer.serve_forever()
    # and HTTPServer.shutdown() must be called from separate threads
    thread = threading.Thread(target=server_main)
    thread.daemon = True
    thread.start()

    # Shut down on kill (SIGTERM) and Ctrl-C (SIGINT)
    signal.signal(signal.SIGTERM, shutdown_server_on_signal)
    signal.signal(signal.SIGINT, shutdown_server_on_signal)

    # Wait on server thread, until timeout has elapsed
    #
    # Note: The timeout parameter here is also important for catching OS
    # signals, so do not remove it.
    #
    # Having a timeout to check for keeps the waiting thread active enough to
    # check for signals too. Without it, the waiting thread will block so
    # completely that it won't respond to Ctrl-C or SIGTERM. You'll only be
    # able to kill it with kill -9.
    thread.join(args.die_after_seconds)
    if thread.is_alive():
        print("Reached %.3f second timeout. Asking server to shut down" %
              args.die_after_seconds)
        server.shutdown()

    print("Exited cleanly")


if __name__ == "__main__":

    parser = arg_parser()
    args = parser.parse_args()
    run_server(args)
