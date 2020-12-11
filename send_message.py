from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import sys
import random
import time
import utils
import config

input_file = sys.argv[1]
users = utils.load_user(input_file)

accounts = config.TELEGRAM_ACCOUNTS[:1]
clients = utils.login(accounts)
client = clients[0]


for user in users:
    receiver = utils.get_user(user, client)
    message = random.choice(config.MESSAGES_TEMPLATE)

    try:
        print("Sending Message to: ", user["name"])
        client.send_message(receiver, message.format(user["name"]))

        print("Waiting {} seconds".format(config.SLEEP_TIME))
        time.sleep(config.SLEEP_TIME)
    except PeerFloodError:
        # too much requests at the same time
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        client.disconnect()
        sys.exit()
    except Exception as e:
        print("Error:", e)
        print("Trying to continue...")
        continue

client.disconnect()
print("Done. Message sent to all users.")
