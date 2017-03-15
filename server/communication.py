#!/usr/bin/env python3
"""
    Module for translate data
    pickle.dumps - serializing data
    pickle.loaded - loading data
    struct.pack - Return a bytes object containing the values v1, v2, ...
                  packed according to the format string fmt. The arguments must
                  match the values required by the format exactly.

                  "L" - unsigned long
    socket.htonl - Convert 32-bit positive integers from host to network byte
                   order. On machines where the host byte order is the same as
                   network byte order, this is a no-op; otherwise, it performs
                   a 4-byte swap operation.
"""
import pickle
import socket
import struct

marshall = pickle.dumps
unmarshall = pickle.loads


def send(channel, *args):
    buf = marshall(args)
    value = socket.htonl(len(buf))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buf)


def receive(channel):

    size = struct.calcsize("L")
    size = channel.recv(size)
    try:
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error:
        return ''

    buf = ""

    while len(buf) < size:
        buf = channel.recv(size - len(buf))

    return unmarshall(buf)[0]
