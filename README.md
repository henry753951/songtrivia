# Eagle 猜歌遊戲
song trivia multiplayer.   

  遊戲網址 : [https://songtrivia.henry0725.tk](https://songtrivia.nukapp.tk)
 * 多人同樂，房間系統
 * Apple Music 來源 (可匯入自己的歌單)
 * 簡易後端，無資料庫  
 
### Screenshots
 ![image](https://user-images.githubusercontent.com/31657781/185310665-3b325438-6cec-4c3d-975a-3bef3cbf3306.png)
 ![image](https://user-images.githubusercontent.com/31657781/185310987-36b3418c-58a0-4b0c-b0db-0956fa3fd9a2.png)

- - -
### 目錄結構
```
├── main.py   #Host web server
├── router.py 
├── router
└── frontend  # vue 專案目錄
```
### Docker 部屬

```
docker build -t songtrivia .
```

```
docker run -d --name {容器名稱} -p {容器對映端口}:80 songtrivia
```

### Using
Go to `https://hostname:{容器對映端口}`
and play for fun
