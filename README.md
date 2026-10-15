# ATM Jackpotting Defense

AI-driven IoT security: defending ATMs from jackpotting using centralized cryptographic authorization.

## Folder structure

```
ATM-defense/
├── README.md
├── .gitignore
├── member_a_network_auth/   # Member A: sockets + centralized token authorization
├── member_b_.../
└── member_c_.../
```

## Member A: Network & Centralized Authorization

The ATM client must obtain a one-time, short-lived token from the central server before the cash drawer opens. If the server is unreachable, the ATM fails closed.

Run (from inside `member_a_network_auth/`):

```
python server.py          # terminal 1: Central Banking Cloud
python client.py          # terminal 2: ATM requests token, drawer opens
python test_attacks.py    # terminal 2: forged / replayed / expired tokens are denied
```

Decisions are written to `audit.log`.
