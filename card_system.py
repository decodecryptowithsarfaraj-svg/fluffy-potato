import random
import json
import time

DB = "cards.json"


# ---------- File Handling ----------
def load_cards():
    try:
        with open(DB, "r") as f:
            return json.load(f)
    except:
        return []

def save_cards(cards):
    with open(DB, "w") as f:
        json.dump(cards, f)


# ---------- Generators ----------
def gen_card_number():
    return "".join(str(random.randint(0, 9)) for _ in range(16))

def gen_cvv():
    return str(random.randint(100, 999))


# ---------- Features ----------
def create_card():
    cards = load_cards()

    nickname = input("Card name: ")
    limit = int(input("Spending limit: "))
    expiry_days = int(input("Expiry days: "))
    block_int = input("Block international? (y/n): ") == "y"

    card = {
        "number": gen_card_number(),
        "cvv": gen_cvv(),
        "limit": limit,
        "spent": 0,
        "expiry": time.time() + (expiry_days * 86400),
        "block_int": block_int,
        "nickname": nickname
    }

    cards.append(card)
    save_cards(cards)

    print("\n✅ Card Created!")
    print("Number:", card["number"])
    print("CVV:", card["cvv"], "\n")


def view_cards():
    cards = load_cards()

    if not cards:
        print("No cards found\n")
        return

    for c in cards:
        remaining = int(c["limit"] - c["spent"])
        print(f"{c['nickname']} | {c['number']} | Remaining: {remaining}")
    print()


def make_payment():
    cards = load_cards()

    number = input("Card number: ")
    amount = int(input("Amount: "))
    international = input("International? (y/n): ") == "y"

    for c in cards:
        if c["number"] == number:

            # Expiry check
            if time.time() > c["expiry"]:
                print("❌ Card expired\n")
                return

            # Limit check
            if c["spent"] + amount > c["limit"]:
                print("❌ Limit exceeded\n")
                return

            # International check
            if c["block_int"] and international:
                print("❌ International blocked\n")
                return

            c["spent"] += amount
            save_cards(cards)

            print("✅ Payment success")
            print("Remaining:", c["limit"] - c["spent"], "\n")
            return

    print("❌ Card not found\n")


# ---------- Menu ----------
while True:
    print("==== Virtual Card System ====")
    print("1. Create Card")
    print("2. View Cards")
    print("3. Pay")
    print("4. Exit")

    ch = input("Choose: ")

    if ch == "1":
        create_card()
    elif ch == "2":
        view_cards()
    elif ch == "3":
        make_payment()
    elif ch == "4":
        break
    else:
        print("Invalid\n")