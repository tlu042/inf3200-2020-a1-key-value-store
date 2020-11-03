#!/usr/bin/env python3

import argparse
import json
import random
import threading
import string
import time
import unittest
import uuid
import http.client as httplib
import sys

def describe_exception(e):
    return "%s: %s" % (type(e).__name__, e)


class Response(object): pass


def search_header_tuple(headers, header_name):
    if sys.version_info[0] <= 2:
        header_name = header_name.lower()
    elif sys.version_info[0] >= 3:
        pass

    for key, value in headers:
        if key == header_name:
            return value
    return None


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
    with open("node_list_copy.txt", "r") as f:
        for node in f:
            nodes.append(node.strip())
    return nodes


def nodes_join_network(nodes):
    t1 = time.time()
    prev = nodes[0]
    for node in nodes[1::]:
        do_request(node, "POST", f"/join?nprime={prev}")
        prev = node
    t2 = time.time()
    return t2 - t1

def nodes_leave_network(size, nodes):
    remove_nodes = random.sample(nodes, k=size)
    t1 = time.time()
    for node in remove_nodes:
        do_request(node, "POST", "/leave")
    t2 = time.time()
    for node in nodes:
        if node not in remove_nodes:
            return t2 - t1, node


def sim_crash(node):
    do_request(node, "POST", "/sim-crash")


def sim_recover(node):
    do_request(node, "POST", "/sim-recover")


def get_neighbours(node):
    conn = httplib.HTTPConnection(node)
    conn.request("GET", "/neighbors")
    resp = conn.getresponse()
    if resp.status != 200:
        neighbors = []
    else:
        body = resp.read()
        neighbors = json.loads(body)
    conn.close()
    return neighbors


def walk_neighbours(start_nodes):
    to_visit = start_nodes
    visited = set()
    while to_visit:
        next_node = to_visit.pop()
        visited.add(next_node)
        neighbors = get_neighbours(next_node)
        for neighbor in neighbors:
            if neighbor not in visited:
                to_visit.append(neighbor)
    return visited


def main():
    nodes = retrieve_nodes_from_file()
    
    time = nodes_join_network(nodes)
    print("Join time", time)

    walked_nodes = set([nodes[0]])
    walked_nodes |= walk_neighbours([nodes[0]])
    walked_nodes = list(walked_nodes)
    print("%d nodes registered: %s" % (len(walked_nodes), ", ".join(walked_nodes)))

    time, node = nodes_leave_network(25, nodes)
    print("Leave time", time)

    walked_nodes = set([node])
    walked_nodes |= walk_neighbours([node])
    walked_nodes = list(walked_nodes)
    print("%d nodes registered: %s" % (len(walked_nodes), ", ".join(walked_nodes)))

if __name__ == "__main__":
    main()
