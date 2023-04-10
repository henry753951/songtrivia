import datetime
import hashlib
import asyncio

gameList = []
disconnectQueue = []


class Room:
    room_id: int
    isPublic = True
    playing = False
    isStart = False
    isEnd = False
    current_round = 0
    total_round = 10
    song_selections_count = 4

    timePerRound = 10
    start_datetime = None

    current_song = {}
    current_song_selections = []
    raw_data = {}
    users = []
    songs = []
    picklist = []
    historySongs = []

    def __init__(self, room_id, raw_data):
        self.room_id = room_id
        self.raw_data = raw_data
        self.songs = raw_data["songs"]["data"]
        self.picklist = raw_data["songs"]["data"]
        self.users = []
        self.historySongs = []

    def __str__(self):
        return str(self.room_id)

    def __repr__(self):
        return self.__str__()

    def reset(self):
        self.picklist = []
        self.current_song = {}
        self.current_song_selections = []
        self.playing = False
        self.isStart = False
        self.isEnd = False
        self.current_round = 0
        for user in self.users:
            user.current_select = ""
            user.old_score = 0
            user.score = 0
        for game in gameList:
            if game["room_id"] == self.room_id:
                game["task"].cancel()

    def serialize(self):
        start_datetime = None
        if self.start_datetime is not None:
            start_datetime = self.start_datetime.timestamp()

        return {
            "isPublic": self.isPublic,
            "playing": self.playing,
            "room_id": self.room_id,
            "isStart": self.isStart,
            "isEnd": self.isEnd,
            "current_round": self.current_round,
            "total_round": self.total_round,
            "timePerRound": self.timePerRound,
            "start_datetime": start_datetime,
            "current_song": self.current_song,
            "current_song_selections": self.current_song_selections,
            "raw_data": self.raw_data,
            "users": [u.serialize() for u in self.users],
            "songs": self.songs,
            "historySongs": list(reversed(self.historySongs)),
        }


class User:
    uuid: str
    ans_time = datetime.datetime.now()
    current_select = None
    name = ""
    leader = False
    score = 0
    old_score = 0
    websocket = None

    def __init__(self, uuid, name):
        self.uuid = uuid
        self.name = name

    def __str__(self):
        return str(self.uuid)

    def __repr__(self):
        return self.__str__()

    def serialize(self):
        x = bytes(self.uuid, "utf-8")
        return {
            "hash": str(hashlib.sha256(x).hexdigest()),
            "name": self.name,
            "leader": self.leader,
            "current_select": self.current_select,
            "score": self.score,
            "old_score": self.old_score,
            "connected": True if self.websocket != None else False,
        }
