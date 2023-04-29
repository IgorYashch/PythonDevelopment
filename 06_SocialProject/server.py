import asyncio
from collections import defaultdict

from cowsay import cowsay, list_cows

clients = {}  # peername : cow, queue


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info("peername"))
    print(me)

    clients[me] = [None, asyncio.Queue()]
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me][1].get())

    login = None
    quit = False

    while not reader.at_eof() and not quit:
        done, pending = await asyncio.wait(
            [send, receive], return_when=asyncio.FIRST_COMPLETED
        )
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                result = q.result().decode().strip()

                if result == "quit":
                    quit = True
                    writer.write(f"2Goodbye!".encode())
                    break

                elif result == "cows":
                    used_cows = set(cow for cow, _ in clients.values() if cow)
                    available_cows = set(list_cows()) - used_cows
                    await clients[me][1].put(
                        f"0Available cows: {', '.join(available_cows)}"
                    )

                elif result == "cows complete":
                    used_cows = set(cow for cow, _ in clients.values() if cow)
                    available_cows = set(list_cows()) - used_cows
                    await clients[me][1].put(f"1{' '.join(available_cows)}")

                elif result.startswith("login"):
                    _, cowname = result.split()
                    used_cows = set(cow for cow, _ in clients.values() if cow)
                    if cowname in used_cows:
                        await clients[me][1].put("0Name already in use")
                    elif cowname in list_cows():
                        clients[me][0] = cowname
                        await clients[me][1].put(f"0You logged as {cowname}")
                        login = cowname
                    else:
                        await clients[me][1].put("0Unknown cowname")

                elif result == "who":
                    used_cows = [cow for cow, _ in clients.values() if cow]
                    await clients[me][1].put(
                        f"0Authorized cows: {', '.join(used_cows) or 'there is no logged cows'}"
                    )

                elif result == "who complete":
                    used_cows = [cow for cow, _ in clients.values() if cow]
                    await clients[me][1].put(f"1{' '.join(used_cows)}")

                elif login:
                    if result.startswith("say"):
                        _, name, msg = result.split(maxsplit=2)
                        for to, (cowname, _) in clients.items():
                            if cowname == name:
                                await clients[to][1].put("0" + cowsay(msg, cow=login))
                    elif result.startswith("yield"):
                        _, msg = result.split(maxsplit=1)
                        for cow, queue in clients.values():
                            if login != cow:
                                await queue.put("0" + cowsay(msg, cow=login))
                else:
                    await clients[me][1].put(
                        f"0You are not authorized. Please use: login <cowname>"
                    )

            elif q is receive:
                receive = asyncio.create_task(clients[me][1].get())
                result = q.result()
                writer.write(f"{result}\n".encode())

            await writer.drain()

    send.cancel()
    receive.cancel()
    print(me, "end")

    del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
