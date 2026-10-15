import time
from client import ask_server, ATM_ID

print("1. Redeem a made-up token (local forged command):")
print("  ", ask_server({"atm_id": ATM_ID, "action": "redeem_token", "token": "fake123"}))

print("2. Replay a real token:")
t = ask_server({"atm_id": ATM_ID, "action": "request_token", "amount": 100})["token"]
print("   first use :", ask_server({"atm_id": ATM_ID, "action": "redeem_token", "token": t}))
print("   second use:", ask_server({"atm_id": ATM_ID, "action": "redeem_token", "token": t}))

print("3. Unknown ATM:")
print("  ", ask_server({"atm_id": "ATM-999", "action": "request_token", "amount": 100}))

print("4. Excessive amount:")
print("  ", ask_server({"atm_id": ATM_ID, "action": "request_token", "amount": 999999}))

print("5. Expired token (waiting 31s)...")
t = ask_server({"atm_id": ATM_ID, "action": "request_token", "amount": 100})["token"]
time.sleep(31)
print("  ", ask_server({"atm_id": ATM_ID, "action": "redeem_token", "token": t}))
