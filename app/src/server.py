#!/usr/bin/env python3
import os
import socket
import selectors
import types
import logging

sel = selectors.DefaultSelector()
HOST = ''
PORT = 9999

# def get_module_logging(mod_name):
#     """
#     To use this, do logging = get_module_logging(__name__)
#     """
#     logger = logging.getlogging(mod_name)
#     handler = logger.StreamHandler()
#     formatter = logger.Formatter(
#         '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)
#     logger.setLevel(logging.DEBUG)
#     return logger

logging.basicConfig(level=logging.DEBUG)


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    logging.info(f"accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            logging.info(f"closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            logging.info(f"From {data.addr}: {repr(data.outb)}")
            # print("From ", data.addr, ": ", repr(data.outb))
            # print("echoing", repr(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


# if len(sys.argv) != 3:
#     print("usage:", sys.argv[0], "<host> <port>")
#     sys.exit(1)

# host, port = sys.argv[1], int(sys.argv[2])
host, port = HOST, PORT
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
logging.info(f"listening on ({host}, {port})")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

print("TESTING")

try:
    while True:
        try:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
        except ConnectionResetError:
            logging.info("Client closed the connection")
except KeyboardInterrupt:
    logging.info("caught keyboard interrupt, exiting")
finally:
    sel.close()
