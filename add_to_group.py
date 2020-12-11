import sys
import time
import traceback
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import utils
import config


input_file = sys.argv[1]
users = utils.load_user(input_file)

accounts = config.TELEGRAM_ACCOUNTS[:1]
clients = utils.login(accounts)
client = clients[0]
groups = utils.get_groups(client)

print("Choose a group to add user to:")
for idx, g in enumerate(groups):
    print(f"{idx}, {g.title}")

g_index = input("Enter a Number: ")
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

for user in users:
    try:
        print("Adding {}".format(user["id"]))
        user_to_add = utils.get_user(user, client)
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("Waiting 60 Seconds...")
        time.sleep(config.SLEEP_TIME)
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue

client.disconnect()
print("Done. Add all users to target group.")