import json
import struct

def send_msg(sock, obj):
    data = json.dumps(obj).encode("utf-8")
    sock.sendall(struct.pack("!I", len(data)) + data)

def _recv_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("connection closed")
        buf += chunk
    return buf

def recv_msg(sock, max_size=65536):
    (length,) = struct.unpack("!I", _recv_exact(sock, 4))
    if length > max_size:
        raise ValueError("message too large")
    return json.loads(_recv_exact(sock, length).decode("utf-8"))
