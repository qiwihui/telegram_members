import config
import utils

accounts = config.TELEGRAM_ACCOUNTS[:1]

clients = utils.login(accounts)
client = clients[0]

groups = utils.get_groups(client)

print("Choose a group to scrape members from:")
for idx, g in enumerate(groups):
    print(f"{idx}, {g.title}")

g_index = input("Enter a Number: ")
target_group = groups[int(g_index)]

print("Fetching Members and save to file")

utils.save_members(client, target_group, "members.csv")

client.disconnect()
print("Members scraped successfully.")
