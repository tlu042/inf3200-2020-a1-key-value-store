#!/usr/bin/env python3

import argparse
import json
import random
import threading
import string
import time
import unittest
import uuid


def do_request(host_port, method, url, body=None, accept_statuses=[200]):
    def describe_request():
        return "%s %s%s" % (method, host_port, url)

    conn = None
    try:
        conn = httplib.HTTPConnection(host_port)
        try:
            conn.request(method, url, body)
            r = conn.getresponse()
        except Exception as e:
            raise Exception(describe_request()
                    + " --- "
                    + describe_exception(e))

        status = r.status
        if status not in accept_statuses:
            raise Exception(describe_request() + " --- unexpected status %d" % (r.status))

        headers = r.getheaders()
        body = r.read()

    finally:
        if conn:
            conn.close()

    content_type = search_header_tuple(headers, "Content-type")
    if content_type == "application/json":
        try:
            body = json.loads(body)
        except Exception as e:
            raise Exception(describe_request()
                    + " --- "
                    + describe_exception(e)
                    + " --- Body start: "
                    + body[:30])

    if content_type == "text/plain" and sys.version_info[0] >= 3:
        body = body.decode()

    r2 = Response()
    r2.status = status
    r2.headers = headers
    r2.body = body

    return r2


def retrieve_nodes_from_file():
    nodes = []
    with open("node_list.txt", "r") as f:
        for node in f:
            nodes.append(node)
    return nodes


def nodes_join_network(nodes):
    t1 = time.time()
    for node in nodes:
        do_request(node, "POST", "/join?nprime=" + nodes[0])
        # time.sleep(0.5)
    t2 = time.time()
    return t1 - t2


def sim_crash(node):
    do_request(node, "POST", "/sim-crash")


def sim_recover(node):
    do_request(node, "POST", "/sim-recover")


def main():
    nodes = retrieve_nodes_from_file()
    time = nodes_join_network(nodes)
    print("Time", time)


if __name__ == "__main__":
    main()
