import socket
from common import send_msg, recv_msg

HOST, PORT = "127.0.0.1", 5000
ATM_ID = "ATM-001"

def ask_server(payload):
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            send_msg(sock, payload)
            return recv_msg(sock)
    except (OSError, ConnectionError, ValueError):
        return None

def open_drawer(amount):
    print(f"[ATM] >>> CASH DRAWER OPEN: dispensing {amount}")

def dispense(amount):
    reply = ask_server({"atm_id": ATM_ID, "action": "request_token", "amount": amount})
    if not reply or reply.get("status") != "ok":
        print(f"[ATM] DENIED at token request: {reply and reply.get('reason') or 'server unreachable'}")
        return False
    check = ask_server({"atm_id": ATM_ID, "action": "redeem_token", "token": reply["token"]})
    if not check or check.get("status") != "ok":
        print(f"[ATM] DENIED at verification: {check and check.get('reason') or 'server unreachable'}")
        return False
    open_drawer(check["amount"])
    return True

if __name__ == "__main__":
    dispense(500)
