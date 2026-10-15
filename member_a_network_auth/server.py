import socket, threading, logging, secrets, time
from common import send_msg, recv_msg

HOST, PORT = "127.0.0.1", 5000
REGISTERED_ATMS = {"ATM-001", "ATM-002"}
TOKEN_TTL = 30
MAX_AMOUNT = 20000

issued = {}
lock = threading.Lock()

logging.basicConfig(filename="audit.log", level=logging.INFO,
                    format="%(asctime)s %(message)s")

def deny(reason):
    return {"status": "denied", "reason": reason}

def handle_request_token(req, atm_id):
    amount = req.get("amount")
    if not isinstance(amount, int) or not (0 < amount <= MAX_AMOUNT):
        logging.info(f"DENY token request {atm_id}: bad amount {amount}")
        return deny("invalid amount")
    token = secrets.token_urlsafe(32)
    with lock:
        issued[token] = {"atm_id": atm_id, "amount": amount,
                         "expires": time.time() + TOKEN_TTL, "used": False}
    logging.info(f"ISSUED token to {atm_id} for amount {amount}")
    return {"status": "ok", "token": token, "ttl": TOKEN_TTL}

def handle_redeem(req, atm_id):
    token = req.get("token")
    with lock:
        rec = issued.get(token)
        if rec is None:
            reason = "invalid token"
        elif rec["atm_id"] != atm_id:
            reason = "token belongs to another ATM"
        elif rec["used"]:
            reason = "token already used (replay)"
        elif time.time() > rec["expires"]:
            reason = "token expired"
        else:
            rec["used"] = True
            logging.info(f"APPROVED dispense {rec['amount']} for {atm_id}")
            return {"status": "ok", "amount": rec["amount"]}
    logging.info(f"DENY redeem {atm_id}: {reason}")
    return deny(reason)

def handle_client(conn, addr):
    conn.settimeout(30)
    try:
        while True:
            req = recv_msg(conn)
            atm_id = req.get("atm_id")
            action = req.get("action")
            if atm_id not in REGISTERED_ATMS:
                logging.info(f"REJECT unknown ATM {atm_id} from {addr}")
                send_msg(conn, deny("unknown device"))
            elif action == "request_token":
                send_msg(conn, handle_request_token(req, atm_id))
            elif action == "redeem_token":
                send_msg(conn, handle_redeem(req, atm_id))
            else:
                send_msg(conn, deny("unknown action"))
    except (ConnectionError, socket.timeout, ValueError) as e:
        logging.info(f"DISCONNECT {addr}: {e}")
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVER] Central Banking Cloud listening on {HOST}:{PORT}", flush=True)
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
