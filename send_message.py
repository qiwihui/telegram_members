from telethon.errors.rpcerrorlist import PeerFloodError
import sys
import random
import utils
import config
import asyncio

input_file = sys.argv[1]
users = utils.load_user(input_file)

accounts = config.TELEGRAM_ACCOUNTS[:1]
clients = utils.login(accounts)
# client = clients[0]


async def worker(client, queue):
    while True:
        # print("Waiting {} seconds".format(config.SLEEP_TIME))
        # await asyncio.sleep(config.SLEEP_TIME)
        (user, message) = await queue.get()

        receiver = await utils.get_user(user, client)

        try:
            print("Sending Message to: ", user["name"])
            await client.send_message(receiver, message.format(user["name"]))
        except PeerFloodError:
            # too much requests at the same time
            print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
            # client.disconnect()
            # sys.exit()
        except Exception as e:
            print("Error:", e)
            print("Trying to continue...")
        queue.task_done()


async def main():
    queue = asyncio.Queue()
    for user in users:
        message = random.choice(config.MESSAGES_TEMPLATE)
        queue.put_nowait((user, message))

    tasks = []
    for client in clients:
        task = asyncio.create_task(worker(client, queue))
        tasks.append(task)
    # wait queue
    await queue.join()

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

    for client in clients:
        await client.disconnect()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print("Done. Message sent to all users.")
