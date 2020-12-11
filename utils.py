import csv
from typing import List, Dict, Optional
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, Channel, InputPeerUser


def login(accounts: List[Dict]) -> List[TelegramClient]:
    clients = []
    for account in accounts:
        api_id = account["app_id"]
        api_hash = account["app_hash"]
        phone = account["phone"]
        client = TelegramClient(phone, api_id, api_hash)
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(phone)
            client.sign_in(phone, input(f"Enter the code for {phone}: "))

        clients.append(client)
    return clients


def get_groups(client: TelegramClient):
    chats = []
    last_date = None
    chunk_size = 200
    groups = []

    result = client(
        GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0,
        )
    )

    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue

    return groups


def get_members(client: TelegramClient, target_group: Channel, aggressive: bool = True) -> List:
    all_participants = []
    all_participants = client.get_participants(target_group, aggressive=aggressive)
    return all_participants


def save_members(client: TelegramClient, target_group: Channel, file_path: str = "members.csv"):
    all_participants = get_members(client, target_group)
    with open(file_path, "w", encoding="UTF-8") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(["username", "user_id", "access_hash", "name", "group", "group_id"])
        for user in all_participants:
            username = user.username or ""
            first_name = user.first_name or ""
            last_name = user.last_name or ""
            name = (first_name + " " + last_name).strip()
            writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])


def load_user(input_file):
    users = []
    with open(input_file, encoding="UTF-8") as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user["username"] = row[0]
            user["id"] = int(row[1])
            user["access_hash"] = int(row[2])
            user["name"] = row[3]
            users.append(user)
    return users


def get_user(user: Dict, client: Optional[TelegramClient] = None):
    if user["username"] == "" or client is None:
        receiver = InputPeerUser(user["id"], user["access_hash"])
    else:
        receiver = client.get_input_entity(user["username"])

    return receiver