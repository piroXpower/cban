from pyrogram import Client

app = Client("my_account")


async def main():
    async with app:
        print(await app.get_me())


app.run(main())
