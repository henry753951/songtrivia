<style lang="scss">
.area{
    position:fixed;
    z-index: -50;
    background: #4e54c8;  
    background: -webkit-linear-gradient(to left, #8f94fb, #4e54c8);  
    width: 100%;
    height:100vh;
    
   
}

.circles{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.circles li{
    position: absolute;
    display: block;
    list-style: none;
    width: 20px;
    height: 20px;
    background: rgba(255, 255, 255, 0.2);
    animation: animate 25s linear infinite;
    bottom: -150px;
    
}

.circles li:nth-child(1){
    left: 25%;
    width: 80px;
    height: 80px;
    animation-delay: 0s;
}


.circles li:nth-child(2){
    left: 10%;
    width: 20px;
    height: 20px;
    animation-delay: 2s;
    animation-duration: 12s;
}

.circles li:nth-child(3){
    left: 70%;
    width: 20px;
    height: 20px;
    animation-delay: 4s;
}

.circles li:nth-child(4){
    left: 40%;
    width: 60px;
    height: 60px;
    animation-delay: 0s;
    animation-duration: 18s;
}

.circles li:nth-child(5){
    left: 65%;
    width: 20px;
    height: 20px;
    animation-delay: 0s;
}

.circles li:nth-child(6){
    left: 75%;
    width: 110px;
    height: 110px;
    animation-delay: 3s;
}

.circles li:nth-child(7){
    left: 35%;
    width: 150px;
    height: 150px;
    animation-delay: 7s;
}

.circles li:nth-child(8){
    left: 50%;
    width: 25px;
    height: 25px;
    animation-delay: 15s;
    animation-duration: 45s;
}

.circles li:nth-child(9){
    left: 20%;
    width: 15px;
    height: 15px;
    animation-delay: 2s;
    animation-duration: 35s;
}

.circles li:nth-child(10){
    left: 85%;
    width: 150px;
    height: 150px;
    animation-delay: 0s;
    animation-duration: 11s;
}



@keyframes animate {

    0%{
        transform: translateY(0) rotate(0deg);
        opacity: 1;
        border-radius: 0;
    }

    100%{
        transform: translateY(-1000px) rotate(720deg);
        opacity: 0;
        border-radius: 50%;
    }

}

.nav-bar{
  backdrop-filter: blur(10px);
  background:rgba(247, 247, 247, 0.1);
}
</style>
<template>
  <div class="area" >
      <ul class="circles">
              <li></li>
              <li></li>
              <li></li>
              <li></li>
              <li></li>
              <li></li>
              <li></li>
              <li></li>
              <li></li>
              <li></li>
      </ul>
  </div >

  <template v-if="isIOSMsg">
    <div
      class="modal"
      style="display : block;"
      tabindex="30"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-body" align="center">
            <p>iOS裝置需要授權播放音訊</p>
            <button type="button" @click="audio.play();init();" class="btn btn-dark m-3">授權</button>
          </div>
        </div>
      </div>
    </div>
  </template>


  <div class="d-flex flex-column" style="min-height:100vh;height: 100vh;padding-bottom: 9rem;">
    <div class="nav-bar">
      <div class="d-flex justify-content-between container pt-2 pb-3 flex-wrap no-540">
        <div class="d-flex gap-3 align-items-center">
          <router-link :to="{ name: 'Home' }" class="navbar-brand text-light">Eagle 猜歌小遊戲</router-link>
          <span @click="copyURL()" style="cursor: pointer;" class="badge rounded-pill bg-dark"><div class="text-light">房間 #{{$route.params.room_id}} <i class="fa-solid fa-arrow-up-right-from-square"></i></div></span>
        </div>
        <div class="d-flex align-items-center sm-nav-w-100">
          <button @click="playerListVisibility=true" class="btn btn-outline-light me-auto player-list-switch text-nowrap"><div class="d-flex align-items-center gap-1"><i class="fa-solid fa-user-group"></i>列表</div></button>
          <div class="d-flex gap-2 align-items-center ms-1">
            <input class="name-input" v-model="playerName">
            <button class="btn btn-outline-light text-nowrap circle-btn" @click="changePlayerName"><i class="fa-solid fa-check"></i></button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="room!=null" class="w-100 container mt-2 no-540" >
      <div class="progress w-100" v-if="room!=null">
        <div class="progress-bar text-white" :style="{width: `${room.playing ? ((Math.round(Now.diff(this.$moment.unix(room.start_datetime))/100)/10)/room.timePerRound)*100 : 100 }%`}" role="progressbar" :aria-valuenow="((Math.round(Now.diff(this.$moment.unix(room.start_datetime))/100)/10)/room.timePerRound)*100" aria-valuemin="0" aria-valuemax="100">{{room.playing ? Math.round(Now.diff(this.$moment.unix(room.start_datetime))/1000) : (room.isStart ? '請稍等' : '等待回合開始')}}</div>
      </div>
    </div>

    <div class="container pt-2 mt-2 pb-3 no-540 game-body">
      <template v-if="room!=null">
        <div class="row h-100">
          <div class="col-md-5 col-lg-3 player-list-box active h-100">
            <div class="player-list h-100">
              <p>玩家清單</p>
              <div class="h-100" style="position:relative">
                <ul class="list-group player-list-group" style="overflow-y: scroll;overflow-x: hidden;">
                  <li class="list-group-item player" v-for="user in this.room.users" :key="user" :class="{'wrong':user.old_score==user.score&&!room.playing&&room.isStart&&!room.isEnd,'correct':user.old_score!=user.score&&!room.playing&&room.isStart&&!room.isEnd}">
                    <div class="d-flex">
                      <span v-if="user.connected" style="color:green"><i class="fa-solid fa-circle"></i></span> 
                      <span v-else style="color:red"><i class="fa-solid fa-circle"></i></span> 
                      <div class="me-auto ms-1 d-flex align-items-center">
                        <span>{{user.name}}</span> <span v-show="user.leader" class="badge bg-secondary ms-1">房主</span>
                      </div>
                      
                      <div class="pe-3">
                        <number
                          :from="user.old_score"
                          :to="user.score"
                          :duration="1"
                          easing="Power1.easeOut"/>
                      </div>
                    </div>
                    <!-- <div style="position:fixed;right:-60px;transform:translateY(-2em);z-index: 9999;">
                      <div class="speech-bubble p-2">0123</div>
                    </div> -->

                  </li>
                </ul>
              </div>
            </div>
          </div>

          <transition
            enter-active-class="animate__animated animate__zoomIn animate__faster"
            leave-active-class="animate__animated animate__zoomOut animate__faster"
          >
            <div class="col-md-4 player-list-box player-list-sm w-100" v-if="playerListVisibility">
              <div class="player-list">
                <div @click="playerListVisibility=false" style="cursor: pointer;" class="close-btn d-flex align-items-center justify-content-center"><i class="fa-solid fa-xmark"></i></div>
                <p>玩家清單</p>
                <ul class="list-group" style="height:50vh;overflow-y: scroll;overflow-x: hidden;">
                  <li class="list-group-item player" v-for="user in this.room.users" :key="user" :class="{'wrong':user.old_score==user.score&&!room.playing&&room.isStart&&!room.isEnd,'correct':user.old_score!=user.score&&!room.playing&&room.isStart&&!room.isEnd}">
                    <div class="d-flex">
                      <span v-if="user.connected" style="color:green"><i class="fa-solid fa-circle"></i></span> 
                      <span v-else style="color:red"><i class="fa-solid fa-circle"></i></span> 
                      <div class="me-auto ms-1 d-flex align-items-center">
                        <span>{{user.name}}</span> <span v-show="user.leader" class="badge bg-secondary ms-1">房主</span>
                      </div>
                      
                      <div class="pe-3">
                        <number
                          :from="user.old_score"
                          :to="user.score"
                          :duration="1"
                          easing="Power1.easeOut"/>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </transition>

          <div class="w-100 col d-flex flex-column">
            <div class="pt-2 pb-2">
              <div class="np-card p-4 d-flex align-items-center" v-if="room != null">
                <div>                
                  <img :src="room.raw_data.artwork" width="90" height="90" class="me-3">
                </div>
                <div class="d-flex gap-3 w-100 align-items-center flex-wrap">
                  <div class="d-flex flex-column  me-auto">{{room.raw_data.rawName}}<small>{{room.raw_data.name}}</small></div>
                  <div class="me-3">
                    <span class="text-nowrap">
                      回合 : 
                      <template v-if="room.isStart">{{room.current_round}}/{{room.total_round}}</template>
                      <template v-else-if="room.isEnd">遊戲結束</template>
                      <template v-else>等待房主開始</template>
                    </span>
                    <div class="d-flex gap-1">
                      <button class="btn btn-primary w-100 mt-3" v-show="room.isStart==false&&getUser()!=null&&getUser().leader" @click="startGame()">開始</button>
                      <button class="btn btn-primary w-100 mt-3" v-show="getUser()!=null&&getUser().leader" @click="SyncSetting();showRoomSetting=!showRoomSetting;showListChangeModal=false">設定</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="d-flex flex-column gap-3 mb-3">
              <a @click="select(song_selection.id)" class="btn" :class="
              {
                'btn-danger':getUser().current_select==song_selection.id&&endRound&&song_selection.id!=room.current_song.id,
                'btn-success':endRound&&song_selection.id==room.current_song.id,
                'btn-primary':getUser().current_select==song_selection.id&&!endRound,
                'btn-light':getUser().current_select!=song_selection.id&&!(endRound&&song_selection.id==room.current_song.id),
              }
              " v-for="song_selection in room.current_song_selections" :key="song_selection">
              <div style="position: absolute;" v-show="((Math.round(Now.diff(this.$moment.unix(room.start_datetime))/100)/10)/room.timePerRound)*100 >= 75"><i class="fa-solid fa-user-group"></i> {{getSelectionCount(song_selection.id)}}</div>
              <div class="ms-5 me-5">{{song_selection.attributes.name}} </div>
              </a>
            </div>
            <div class="mt-auto chat-box p-2 text-white d-flex flex-column mb-5" style="overflow-y: scroll;" ref="chatBox">
              <div class="mt-auto pb-4">              
                <div v-for="msg in chatMsgList" :key="msg">
                  {{msg.name}} : {{msg.msg}}
                </div>
              </div>

            </div>
          </div>

          <div class="song-list-box active h-100" style="width: 400px;">
            <div class="song-list h-100">
              <p class="ps-3 pe-3">歌曲紀錄</p>
              <ul class="list-group song-list-group" style="overflow-y: scroll;overflow-x: hidden">
                <li class="pt-1 pb-1 song-card ps-3 pe-3" v-for="song in this.room.historySongs" :key="song">
                  <div class="d-flex align-items-center ">
                    <img style="height:60px;border-radius: 10px;" class="me-2" :src="song.attributes.artwork.url.replace(/{h}/i, '500').replace(/{w}/i, '500')">
                    <div class="d-flex flex-column">

                      <div class="text-truncate d-inline-block" style="width: 260px;">
                        <a class="item-link" target="_blank" :href="song.attributes.url">{{song.attributes.name}}</a>
                      </div>
                      <div class="text-truncate d-inline-block" style="width: 260px;">
                        <small style="font-size:xx-small">{{song.attributes.artistName}} - {{song.attributes.albumName}}</small>
                      </div>

                    </div>  
                  </div>
                </li>
              </ul>
            </div>
          </div>

        </div>
      </template>
    </div>
  </div>

  <div class="bottom-bar p-2">
    <div class="container no-540 d-flex gap-3 align-items-center">
      <va-button color="#2550C0" class="me-auto" @click="showVolumeSetting=!showVolumeSetting"><i class="fa-solid fa-volume-high"></i></va-button>
      <input class="chat-input" placeholder="你的訊息" v-model="message.text" @keypress.enter="sendMessage('text')">
      <va-button flat size="small" style="width:min-content" @click="sendMessage('text')"><i class="fa-solid fa-share text-white"></i></va-button>
      <va-button gradient color="warning"><i class="fa-solid fa-face-grin-wide"></i></va-button>
    </div> 
  </div>


  <template>
    <va-modal
      v-model="showVolumeSetting"
      :mobile-fullscreen="false"
    >
      <template #content>
        <label for="volume" class="form-label">音量</label>
        <va-slider style="width:30vw" v-model="volume" :max="1.0" :step="0.01" @change="audio.volume = this.volume" />
      </template>
    </va-modal>
  </template>
  <template v-if="room!=null">
    <va-modal
      v-model="room.isEnd"
      :mobile-fullscreen="false"
    >
      <template #content>
        <h3>遊戲結束</h3>
        <ul class="list-group">
          <li class="list-group-item" v-for="user in this.room.users" :key="user">
            <div class="d-flex">
              <span v-if="user.connected" style="color:green"><i class="fa-solid fa-circle"></i></span> 
              <span v-else style="color:red"><i class="fa-solid fa-circle"></i></span> 
              <div class="me-auto ms-1 d-flex align-items-center">
                <span>{{user.name}}</span> <span v-show="user.leader" class="badge bg-secondary ms-1">房主</span>
              </div>
              
              <div class="pe-3">
                {{Math.round(user.score)}}
              </div>
            </div>
          </li>
        </ul>
        <button class="btn btn-primary w-100 mt-3" v-show="getUser()!=null&&getUser().leader" @click="reset()">重置</button>
      </template>
    </va-modal>
  </template>

  <template v-if="room!=null">
    <va-modal
      v-model="showRoomSetting"
    >
      <template #content>
        <va-modal v-model="showListChangeModal">
          <template #content>

            <div>
              <template v-if="loadPlayList.tempPlaylistInfo==null">
                <div class="pb-2">
                  <select class="form-select" aria-label="Default select example" @change="fastSelect(loadPlayList.fastSelect)" v-model="loadPlayList.fastSelect">
                    <option value="None" selected>快速導入</option>
                    <option :value="item.value" v-for="item in loadPlayList.DefaultPlaylist" :key="item.value">{{item.name}}</option>
                    <option disabled="disabled">----歷史紀錄----</option>
                    <option :value="item.value" v-for="item in loadPlayList.historyPlaylist" :key="item.value">{{item.name}}</option>
                  </select>
                </div>
                <div class="pb-2">
                  <p>Apple Music 播放列表ID (pl.xxxxxxxxxxxxxxxxxx)</p>
                  <input type="text" v-model="loadPlayList.id" class="w-100 form-control">
                </div>
                <va-button :loading="loadPlayList.loadingPlaylist" class="w-100" color="#2550C0" @click="get_playlist_info">讀取</va-button>
              </template>
              <template v-else>
                <va-card-content>
                  <div class="d-flex">
                    <img :src="loadPlayList.tempPlaylistInfo.artwork" width="90" height="90" class="me-3" style="border-radius:15px">
                    <div class="d-flex flex-column justify-content-center">
                      <p>{{loadPlayList.tempPlaylistInfo.rawName}}</p>
                      <small>{{loadPlayList.tempPlaylistInfo.name}}</small>
                    </div>
                  </div>
                </va-card-content>
                <div class="d-flex gap-2">
                  <va-button class="w-100" outline @click="loadPlayList.tempPlaylistInfo=null">取消</va-button>
                  <va-button class="w-100" color="#2550C0" @click="roomSettings.raw_data=loadPlayList.tempPlaylistInfo;showListChangeModal=false;loadPlayList.tempPlaylistInfo=null">選取</va-button>
                </div>
              </template>
            </div>
          </template>
        </va-modal>
        <h3>房間設定</h3>
        <div class="p-2 d-flex flex-column gap-3">
          <va-card square outlined class="my-3">
            <va-card-content>
              <div class="d-flex">
                <img :src="roomSettings.raw_data.artwork" width="90" height="90" class="me-3" style="border-radius:15px">
                <div class="d-flex flex-column justify-content-center">
                  <p>{{roomSettings.raw_data.rawName}}</p>
                  <small>{{roomSettings.raw_data.name}}</small>
                </div>
                <div class="ms-auto mt-auto">
                  <va-button color="#2550C0" @click="showListChangeModal=true">更換</va-button>
                </div>
              </div>
            </va-card-content>
          </va-card>
          <div class="d-flex justify-content-between align-items-center py-2">
            <span style="width:25vw">公開房間</span>
            <va-switch v-model="roomSettings.isPublic" />
          </div>
          <div class="d-flex justify-content-between align-items-center">
            <span style="width:25vw">回合數</span>
            <va-counter class="my-1"
              v-model="roomSettings.total_round"
              messages="遊戲總回和數"
              :min="1"
              outline
              buttons
            />
          </div>
          <div class="d-flex justify-content-between align-items-center">
            <span style="width:25vw">作答時間</span>
            <va-counter class="my-1"
              v-model="roomSettings.timePerRound"
              :min="0"
              messages="單位秒"
              outline
              buttons
            />
          </div>
          <div class="d-flex justify-content-between align-items-center">
            <span style="width:25vw">選項數量</span>
            <va-counter class="my-1"
              v-model="roomSettings.songSelectionsCount"
              buttons
              :min="1"
              messages="建議4個，過多過少可能會影響遊戲"
              :flat="false"
            />
          </div>
          <div class="d-flex flex-wrap gap-2 mt-3">
            <va-button class="w-100" color="primary" @click="saveRoomSettings()">保存</va-button>
            <va-button class="w-100" color="danger" gradient  @click="reset()">重置遊戲</va-button>
            <va-button class="w-100" flat  @click="showRoomSetting=false">關閉視窗</va-button>
          </div>
        </div>
      </template>
    </va-modal>
  </template>

</template>

<script>
import "@/assets/scss/style.scss"
var crypto_ = require('crypto');
var ws;
export default {
  name: 'Home',
  data(){
    return {
      loadPlayList:{
        id:"",
        fastSelect:"",
        loadingPlaylist:false,
        tempPlaylistInfo:null,
        historyPlaylist:localStorage.getItem('historyPlaylist') == undefined ? [] : JSON.parse(localStorage.getItem('historyPlaylist')),
        DefaultPlaylist:[
          {
            value:"pl.dc16cb58902342cba9711cbcd9bf284",
            name:"JPOP Now"
          },
          {
            value:"pl.370b1f4caa54400cbbb36e0585f10565",
            name:"Top 25 Taipei"
          },
          {
            value:"pl.2f5fcebf9ad247098e445d27011aecc4",
            name:"今日熱門-日本流行樂"
          },
          {
            value:"pl.5ee8333dbe944d9f9151e97d92d1ead9",
            name:"a-list-歐美流行樂"
          },
          {
            value:"pl.beb783da7712481fbeed35be144bd48c",
            name:"a-list-國語流行樂"
          },
          {
            value:"pl.48229b41bbfc47d7af39dae8e8b5276e",
            name:"a-list-韓國流行樂"
          },
          {
            value:"pl.6d8228f57b864a4296dc02d9761a0d9b",
            name:"熱播金曲-國語流行樂"
          },
          {
            value:"pl.3c940066ea8d47adb2d317c492a981fe",
            name:"卡拉永遠ok-國語"
          },

        ],
      },
      showListChangeModal:false,
      showRoomSetting:false,
      showVolumeSetting:false,
      playerListVisibility: false,
      disabledSelect:false,
      isIOSMsg:false,
      endRound:false,
      Now:this.$moment(),
      audio:new Audio(),
      volume:0.3,
      loading:true,
      room:null,
      playerName:localStorage.getItem("playerName")==null ? "Guest1234" : localStorage.getItem("playerName"),
      message:{
        emotion:"",
        text:"",
      },
      chatMsgList:[],
      roomSettings:{
        timePerRound:10,
        total_round: 10,
        songSelectionsCount:4,
        raw_data:undefined,
        isPublic:true,
      }

    }
  },
  beforeUnmount(){
      this.audio.pause();
      if(ws != undefined ) ws.close();
      clearInterval(this.interval);
  },
  mounted(){
    this.init_(),
    this.interval = setInterval(() => {
      if(this.room!=null)
        if(this.room.playing)
          if(Math.round(this.Now.diff(this.$moment.unix(this.room.start_datetime))/100)/10<=10)
            this.Now = this.getNow()
    }, 10)
  },
  methods:{
    fastSelect(key){
      if(key!="None")
        this.loadPlayList.id = key
    },
    get_playlist_info(){
        this.loadPlayList.loadingPlaylist = true;
        fetch("//" + window.location.hostname +`/api/playlist/${this.loadPlayList.id}`, {
          headers: {
            "content-type": "application/json",
          },
          cache: "no-cache",
        }).then((res) => res.json())
          .then((data) => {
            this.loadPlayList.tempPlaylistInfo=data.data
            this.loadPlayList.loadingPlaylist=false
            
            var found = this.loadPlayList.DefaultPlaylist.find(element => element.value == this.loadPlayList.id)
            if(found) return
            var savedData = localStorage.getItem('historyPlaylist') == undefined ? [] : JSON.parse(localStorage.getItem('historyPlaylist'))

            savedData.push(
              {
                name:this.loadPlayList.tempPlaylistInfo.name,
                value:this.loadPlayList.id,
              }
            )
            this.loadPlayList.historyPlaylist=savedData
            localStorage.setItem("historyPlaylist",JSON.stringify(savedData))
            
          })
          .catch((error) => {
            console.log(error);
            this.$vaToast.init({ message: '找不到歌單或發生錯誤', color: 'danger' })
            this.loadPlayList.loadingPlaylist=false
          });
    },
    SyncSetting(){
      this.roomSettings.timePerRound=this.room.timePerRound
      this.roomSettings.total_round=this.room.total_round
      this.roomSettings.song_selections_count=this.room.song_selections_count
      this.roomSettings.isPublic=this.room.isPublic
      this.roomSettings.raw_data=this.room.raw_data
    },
    saveRoomSettings(){
        fetch("//" + window.location.hostname +`/api/room/${this.$route.params.room_id}/changeSetting`, {
          body: JSON.stringify(this.roomSettings),
          headers: {
            "content-type": "application/json",
            "Authorization":"Bearer " + this.getToken()
          },
          cache: "no-cache",
          method:"POST"
        }).then((res) => res.json())
          .then((data) => {
            this.$vaToast.init({ message: '成功變更設定', color: 'success' })
          })
          .catch((error) => {});
    },
    sendMessage(type){
      var data = {
        hash: this.getUser().hash,
        type:type,
        data: this.message,
      }
      if(ws == undefined ) return
      ws.send(JSON.stringify({data:data,event:"sendMsg"}))
      if(type=="text") this.message.text = ""
    },
    getSelectionCount(id){
      var count = 0
      this.room.users.forEach(element => {
        if(element.current_select==id)
        count++
      });
      return count
    },
    copyURL(){
      navigator.clipboard.writeText(window.location.href).then(function() {
        alert('已複製連結');
      }, function() {});
    },
    reset(){
        fetch("//" + window.location.hostname +`/api/room/${this.$route.params.room_id}/reset`, {
          headers: {
            "content-type": "application/json",
            "Authorization":"Bearer " + this.getToken()
          },
          method: "POST",
          cache: "no-cache",
        }).then((res) => res.json())
          .then((data) => {
            if("error" in data){
              this.$vaToast.init({ message: data.error, color: 'danger' })
            }
          })
    },
    select(song_id){
        if(this.disabledSelect)
          return
        this.disabledSelect = true
        fetch("//" + window.location.hostname +`/api/room/${this.$route.params.room_id}/select`, {
          body: JSON.stringify({song_id:song_id}),
          headers: {
            "content-type": "application/json",
            "Authorization":"Bearer " + this.getToken()
          },
          method: "POST",
          cache: "no-cache",
        }).then((res) => res.json())
          .then((data) => {
            if("error" in data){
              this.$vaToast.init({ message: data.error, color: 'danger' })
            }
          })
    },
    getUser(){
      if(this.room!=null){
        var user = this.room.users.find(element => element.hash == crypto_.createHash('sha256').update(this.getToken()).digest("hex"))
        return user
      }
      return null
    },
    getUserByHash(hash){
      if(this.room!=null){
        var user = this.room.users.find(element => element.hash == hash)
        return user
      }
      return null
    },
    audioLoad() {
      this.audio.autoplay = true;
      this.audio.currentTime = 0;
      var url = this.room.current_song.attributes.previews[0].url;
      this.audio.src = url;
      this.audio.volume = this.volume;    
      this.audio.play()
    },
    init_(){
        var _iOSDevice = navigator.userAgent.match(/(iPad|iPhone|iPod)/g)
        this.isIOSMsg = _iOSDevice
        if(_iOSDevice){
          this.audio.src = "data:audio/mpeg;base64,SUQzBAAAAAABEVRYWFgAAAAtAAADY29tbWVudABCaWdTb3VuZEJhbmsuY29tIC8gTGFTb25vdGhlcXVlLm9yZwBURU5DAAAAHQAAA1N3aXRjaCBQbHVzIMKpIE5DSCBTb2Z0d2FyZQBUSVQyAAAABgAAAzIyMzUAVFNTRQAAAA8AAANMYXZmNTcuODMuMTAwAAAAAAAAAAAAAAD/80DEAAAAA0gAAAAATEFNRTMuMTAwVVVVVVVVVVVVVUxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQsRbAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVf/zQMSkAAADSAAAAABVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV";
        }else{
          this.init()
        }
    },
    async init(){
        this.isIOSMsg=false;
        this.loading=true;
        await fetch("//" + window.location.hostname +`/api/room/${this.$route.params.room_id}`, {
          headers: {
            "content-type": "application/json",
            "Authorization":"Bearer " + this.getToken()
          },
          cache: "no-cache",
        }).then((res) => res.json())
          .then((data) => {
            if(!("error" in data)){
              this.room = data
              console.log(data)
              this.connect()
              if(!data.isEnd)
                this.audioLoad()
            }else{
              alert("房間不存在")
              this.$router.push({ name: 'Home'})
            }
          })
          .catch((error) => {
            console.log(error)
            this.loading=false
          });
        await new Promise(r => setTimeout(r, 1500));
        this.changePlayerName()
    },
    connect(){
      const v = this;
      ws = new WebSocket((window.location.hostname == 'api.' ? '' : '' + window.location.hostname == "127.0.0.1" ? "ws://" : "wss://") + window.location.hostname + `/api/room/ws/${this.$route.params.room_id}/${this.getToken()}`);
      ws.onmessage = function(event) {
        var data = JSON.parse(event.data)
        switch(data.event){
          case "users_changed":{
            v.room.users = data.data
            break;
          }
          case "userJoin":{
            v.chatMsgList.push({name: '系統', msg:'一位玩家加入了遊戲'})
            let obj = v.$refs.chatBox
            obj.scroll({ top: obj.scrollHeight, behavior: "smooth"})
            break;
          }
          case "userLeave":{
            v.chatMsgList.push({name: '系統', msg:'一位玩家離開了遊戲'})
            let obj = v.$refs.chatBox
            obj.scroll({ top: obj.scrollHeight, behavior: "smooth"})
            break;
          }
          case "nextRound":{
            v.room = data.data
            v.disabledSelect = false
            v.endRound=false
            v.audioLoad()
            break;
          }
          case "endRound":{
            v.room = data.data
            v.endRound=true
            break;
          }
          case "endGame":{
            v.room = data.data
            break;
          }
          case "reset":{
            v.room = data.data
            v.endRound=true
            v.audio.pause();
            break;
          }
          case "updateStatus":{
            v.room = data.data
            break;
          }
          case "UserMessage":{
            var user = v.getUserByHash(data.data.hash)
            if(user == undefined) break
            if(data.data.type=='text')
            v.chatMsgList.push({name: user.name, msg:data.data.data.text})
            let obj = v.$refs.chatBox
            obj.scroll({ top: obj.scrollHeight, behavior: "smooth"})
            break;
          }
        }
        console.log(data)
      };
    },
    getToken(){
      function uuidv4() {
        return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
          (crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
        );
      }
      var token=localStorage.getItem("token")
      if(token==null){
        localStorage.setItem("token",uuidv4())
      }
      token=localStorage.getItem("token")
      return token
    },
    changePlayerName(){
        localStorage.setItem("playerName",this.playerName)
        fetch("//" + window.location.hostname +`/api/room/${this.$route.params.room_id}/changeName`, {
          body: JSON.stringify({name:this.playerName}),
          headers: {
            "content-type": "application/json",
            "Authorization":"Bearer " + this.getToken()
          },
          method: "POST",
          cache: "no-cache",
        }).then((res) => res.json())
          .then((data) => {
            if("error" in data){
              this.$vaToast.init({ message: data.error, color: 'danger' })
            }
          })
          .catch((error) => {
            console.log(error)
          });
    },
    startGame(){
        fetch("//" + window.location.hostname +`/api/room/${this.$route.params.room_id}/start`, {
          headers: {
            "content-type": "application/json",
            "Authorization":"Bearer " + this.getToken()
          },
          method: "GET",
          cache: "no-cache",
        }).then((res) => res.json())
          .then((data) => {
            if("error" in data){
              this.$vaToast.init({ message: data.error, color: 'danger' })
            }
          })
          .catch((error) => {
            console.log(error)
          });
    },    
    getNow(){
      return this.$moment()
    },
  },
  computed:{

  },
}
</script>
