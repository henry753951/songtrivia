from typing import List
from bs4 import BeautifulSoup
import uvicorn,aiohttp,json
import re,uuid,asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,Depends
from fastapi.staticfiles import StaticFiles
from router import router as api_router
from fastapi.responses import RedirectResponse



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




async def request(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        return await response.text()


app.mount("/app", StaticFiles(directory="dist"), name="static")


@app.get("/")
async def home():
    return RedirectResponse("/app/index.html")

@app.get("/api/song/{song_id}")
async def songInfo(song_id : str):
    r=await request(F"https://itunes.apple.com/tw/lookup?id={song_id}")
    return {"song_id":song_id,"data":json.loads(r)["results"][0]}


@app.get("/api/playlist/{id}")
async def songInfo(id : str):
    
    # try:
        r=await request(F"https://tools.applemediaservices.com/playlist/{id}?country=tw")
        soup = BeautifulSoup(r,"html.parser")
        data = soup.find_all('script')
        p = re.compile('(?<=var RLOCKUP = )(.*)(?=;)')
        m = p.search(data[1].string).group(1)
        jsonData = json.loads(m)
        img=""
        try:
            img=jsonData['product']['data']['attributes']['artwork']["url"].replace("{w}","600").replace("{h}","600")
        except:
            pass
        model={
            "name":jsonData['product']['data']['attributes']['curatorName'],
            "rawName":jsonData['product']['data']['attributes']['name'],
            "artwork":img,
            "description":jsonData['product']['data']['attributes']['description'],
            "url":jsonData['product']['data']['attributes']['url'],
            "songs":jsonData['product']['data']['relationships']['tracks']
            }
        return {"playlist_id":id,"data":model,"code":"200"}
    # except:
    #     return {"playlist_id":id,"data":"error","code":"400"}





app.include_router(api_router, prefix="/api")

@app.on_event('startup')
async def startup():
    print("Server is running...")
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=80, reload=True)