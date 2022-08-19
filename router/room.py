from typing import List,Optional
import random,uuid
from fastapi import APIRouter,Depends,WebSocket,Request,HTTPException,Response,Cookie,WebSocketDisconnect
from Room import Room,User,gameList,disconnectQueue
import asyncio
import datetime

router = APIRouter()

async def waitForTimeout(room_):
    await asyncio.sleep(600)
    await manager.rooms.remove(room_)

class ConnectionManager:
    def __init__(self):
        self.rooms: List[Room] = []

    async def connect(self, websocket: WebSocket,room_,uuid,name):
        await websocket.accept()
        find = False
        for u in room_.users :
            if u.uuid == uuid:
                u.websocket = websocket
                find = True
                break
        if not find:
            newuser = User(uuid,name)
            newuser.websocket = websocket
            room_.users.append(newuser)

        for task in disconnectQueue:
            if task["room_id"] == room_.room_id:
                task["task"].cancel()
                disconnectQueue.remove(task)
                break

        data={"event":"users_changed","data":[uu.serialize() for uu in room_.users]}
        await self.broadcastRoom(room_,data)
        await manager.broadcastRoom(room_,{"event": "userJoin"})

    async def disconnect(self, websocket: WebSocket,room_):
        for u in room_.users :
            if u.websocket == websocket:
                u.websocket=None
                break
        data={"event":"users_changed","data":[uu.serialize() for uu in room_.users]}
        await self.broadcastRoom(room_,data)
        await manager.broadcastRoom(room_,{"event": "userLeave"})
        temp = True
        for u in room_.users :
            if u.websocket != None:
                temp = False
                break
        if temp :
            task={
                "task":asyncio.create_task(waitForTimeout(room_)),
                "room_id":room_.room_id
            }
            disconnectQueue.append(task)

    async def broadcastRoom(self, room_, data):
        for u in room_.users :
            if u.websocket!=None:
                await u.websocket.send_json(data)
    def getRoom(self,room_id):
        for room_ in self.rooms:
            if room_.room_id == room_id:
                # print(room_)
                return room_
        return None

manager = ConnectionManager()


@router.get("/getRooms")
async def getRooms():
    ls = []
    for room in manager.rooms:
        if room.isPublic:
            data = {
                "room_id":room.room_id,
                "data": room.raw_data,
                "user_count":len(room.users),
            }
            ls.append(data)
    return {"rooms":ls}

@router.post("/create")
async def createRoom(data : dict,request: Request):
    room_id = str(uuid.uuid4())[:8]
    newRoom=None
    newRoom=Room(room_id,data)
    print(F"{newRoom} {room_id}")
    print(newRoom.users)
    leader = User(request.headers["Authorization"][7:],"")
    leader.leader=True
    newRoom.users.append(leader)
    manager.rooms.append(newRoom)
    print(newRoom.users)
    print(F"Room #{room_id} : 房間已建立!")

    return {"room_id":room_id}

@router.get("/{room_id}")
async def roomData(room_id) :
    room_ = manager.getRoom(room_id)
    if room_ is None:
        return {"error": "房間已關閉，請重新創建!"}
    return room_.serialize()


@router.post("/{room_id}/changeName")
async def changeName(data : dict,request: Request,room_id) :
    r = manager.getRoom(room_id)
    if r is None:
        return {"error": "房間已關閉，請重新創建!"}
    for u in r.users :
        if u.uuid==request.headers["Authorization"][7:]:
            u.name = data["name"]
            break
    await manager.broadcastRoom(r,{"event":"users_changed","data":[uu.serialize() for uu in r.users]})
    return {"detail":"OK"}

@router.post("/{room_id}/select")
async def select(data : dict,request: Request,room_id) :
    r = manager.getRoom(room_id)
    if r is None:
        return {"error": "房間已關閉，請重新創建!"}
    if r.playing:
        for u in r.users :
            if u.uuid==request.headers["Authorization"][7:]:
                if u.current_select == "":
                    u.current_select = data["song_id"]
                    u.ans_time = datetime.datetime.now()
                    await manager.broadcastRoom(r,{"event":"users_changed","data":[uu.serialize() for uu in r.users]})
                    break
    return {"detail":"OK"}

@router.get("/{room_id}/start")
async def start(request: Request,room_id) :
    r = manager.getRoom(room_id)
    if r is None:
        return {"error": "房間已關閉，請重新創建!"}
    if r.isStart==True:
        return {"detail":"OK"}
    for u in r.users :
        if u.uuid==request.headers["Authorization"][7:]:
            if u.leader == True:
                game={
                    "task":asyncio.create_task(gameStart(room_id)),
                    "room_id":room_id
                }
                gameList.append(game)
                break
    return {"detail":"OK"}

@router.post("/{room_id}/reset")
async def reset(room_id,request : Request) :
    r = manager.getRoom(room_id)
    if r is None:
        return {"error": "房間已關閉，請重新創建!"}
    for u in r.users :
        if u.uuid==request.headers["Authorization"][7:]:
            if u.leader == True:
                r.reset()
                await manager.broadcastRoom(r,{"event": "reset","data":r.serialize()})
                break
    return {"detail":"OK"}
@router.post("/{room_id}/changeSetting")
async def changeSetting(room_id,request : Request, data : dict) :
    r = manager.getRoom(room_id)
    if r is None:
        return {"error": "房間已關閉，請重新創建!"}
    for u in r.users :
        if u.uuid==request.headers["Authorization"][7:]:
            if u.leader == True:
                r.timePerRound=data["timePerRound"]
                r.total_round=data["total_round"]
                r.song_selections_count=data["songSelectionsCount"]
                r.raw_data=data["raw_data"]
                r.isPublic=data["isPublic"]
                r.songs = data["raw_data"]["songs"]["data"] 
                r.picklist = data["raw_data"]["songs"]["data"] 
                await manager.broadcastRoom(r,{"event": "updateStatus","data":r.serialize()})
                break
    return {"detail":"OK"}

@router.websocket("/ws/{id}/{token}")
async def websocket_endpoint(websocket: WebSocket,id,token):
    room_ = manager.getRoom(id)
    if room_ is None:
        return {"error": ""}
    print(F'Room #{id}: Accepting client connection... {token}')
    await manager.connect(websocket,room_ ,token,"")
    
    print(F"All rooms")
    for r in manager.rooms:
        print(r.room_id)
        print(r.users)
        print("======")
    try:
        while True:
            data = await websocket.receive_json()
            if data["event"] == "sendMsg":
                room_ = manager.getRoom(id)
                await manager.broadcastRoom(room_,{"event": "UserMessage","data":data['data']})
            print(data)

    
    except WebSocketDisconnect:
        await manager.disconnect(websocket,room_)


async def gameStart(room_id):
    room_ = manager.getRoom(room_id)
    room_.current_round=0
    room_.current_time=0
    room_.current_song_selections=[]
    room_.current_song=None
    room_.picklist = room_.songs
    room_.isStart=True
    while True:
        if room_.current_round != 0:
            await asyncio.sleep(4)
        if room_.current_round >= room_.total_round:
            room_.isEnd = True
            await manager.broadcastRoom(room_,{"event": "endGame","data":room_.serialize()})
            break
        room_.current_round+=1
        room_.current_time=0
        room_.current_song_selections=[]
        if len(room_.picklist)==0:
            room_.isEnd = True
            await manager.broadcastRoom(room_,{"event": "endGame","data":room_.serialize()})
            break

        try:
            room_.current_song=random.choice(room_.picklist)
            for song in room_.picklist:
                if song["id"]==room_.current_song["id"]:
                    room_.picklist.remove(song)
                    break
            for song in room_.songs:
                if song["id"]==room_.current_song["id"]:
                    room_.songs.remove(song)
                    break
            t=random.sample(room_.songs,room_.song_selections_count-1)
            room_.songs.append(room_.current_song)
            room_.current_song_selections=t
            
        except Exception as e:
            print(e)
            room_.isEnd = True
            await manager.broadcastRoom(room_,{"event": "endGame","data":room_.serialize()})
            break
        room_.current_song_selections.append(room_.current_song)
        random.shuffle(room_.current_song_selections)

        room_.start_datetime = datetime.datetime.now() #計時開始
        room_.playing=True
        for user in room_.users:
            user.current_select=""
        await manager.broadcastRoom(room_,{"event": "nextRound","data":room_.serialize()})
        while (datetime.datetime.now()-room_.start_datetime).total_seconds() < room_.timePerRound:
            await asyncio.sleep(1)
        room_.playing=False

        for user in room_.users:
            if user.current_select==room_.current_song["id"]:
                ratio =1 if (user.ans_time-room_.start_datetime).total_seconds()/room_.timePerRound >= 1 else (user.ans_time-room_.start_datetime).total_seconds()/room_.timePerRound   
                user.old_score=user.score
                user.score+=500*(1-ratio)
        room_.users=sorted(room_.users, key = lambda user : user.score,reverse = True)
        room_.historySongs.append(room_.current_song)
        if len(room_.historySongs)>50:
            room_.historySongs.pop(0)
        await manager.broadcastRoom(room_,{"event": "endRound","data":room_.serialize()})
        for user in room_.users:
            user.old_score=user.score

        
        

