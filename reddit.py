import asyncpraw


class CacheData:
    def __init__(self):
        self.__storage = {}
        self.__active = {}

    async def add_meme(self, links: list, chat_id) -> None:
        self.__storage[chat_id] = links

    async def add_user(self, chat_id: int, channel: int, active: bool, time: int) -> None:
        self.__active[chat_id] = {
            "channel": channel,
            "active": active,
            "between_posts": time
        }
        self.__storage[chat_id] = []

    async def get_storage(self) -> dict:
        return self.__storage

    async def get_user(self, chat_id) -> dict:
        return self.__active[chat_id]

    async def get_groups(self) -> list:
        data = []
        for i in self.__active.values():
            if i["active"] is True:
                data.append(i["channel"])
        return data

    async def change_status(self, chat_id: int, channel: int):
        if self.__active[chat_id]["channel"] == channel:
            self.__active[chat_id]["active"] = False
        else:
            raise ValueError("incorrect user")


class RedditInit:
    def __init__(self, user_id, secret, agent="default"):
        self.__id = user_id
        self.__secret = secret
        self.__agent = agent

    async def connect(self):
        reddit = asyncpraw.Reddit(
            client_id=self.__id,
            client_secret=self.__secret,
            user_agent=self.__agent
        )
        return reddit


class GetMemes:
    def __init__(self, reddit):
        self.__reddit = reddit
        self.__data = []

    async def load(self) -> list:
        sub = await self.__reddit.subreddit("memes")
        async for meme in sub.new(limit=1):
            self.__data.append((meme.url, meme.title))
            await self.__reddit.close()
        return self.__data
