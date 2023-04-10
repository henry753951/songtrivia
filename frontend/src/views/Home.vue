<style lang="scss">
	.area {
		position: fixed;
		z-index: -50;
		background: #4e54c8;
		background: -webkit-linear-gradient(to left, #8f94fb, #4e54c8);
		width: 100%;
		height: 100vh;
	}

	.circles {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		overflow: hidden;
	}

	.circles li {
		position: absolute;
		display: block;
		list-style: none;
		width: 20px;
		height: 20px;
		background: rgba(255, 255, 255, 0.2);
		animation: animate 25s linear infinite;
		bottom: -150px;
	}

	.circles li:nth-child(1) {
		left: 25%;
		width: 80px;
		height: 80px;
		animation-delay: 0s;
	}

	.circles li:nth-child(2) {
		left: 10%;
		width: 20px;
		height: 20px;
		animation-delay: 2s;
		animation-duration: 12s;
	}

	.circles li:nth-child(3) {
		left: 70%;
		width: 20px;
		height: 20px;
		animation-delay: 4s;
	}

	.circles li:nth-child(4) {
		left: 40%;
		width: 60px;
		height: 60px;
		animation-delay: 0s;
		animation-duration: 18s;
	}

	.circles li:nth-child(5) {
		left: 65%;
		width: 20px;
		height: 20px;
		animation-delay: 0s;
	}

	.circles li:nth-child(6) {
		left: 75%;
		width: 110px;
		height: 110px;
		animation-delay: 3s;
	}

	.circles li:nth-child(7) {
		left: 35%;
		width: 150px;
		height: 150px;
		animation-delay: 7s;
	}

	.circles li:nth-child(8) {
		left: 50%;
		width: 25px;
		height: 25px;
		animation-delay: 15s;
		animation-duration: 45s;
	}

	.circles li:nth-child(9) {
		left: 20%;
		width: 15px;
		height: 15px;
		animation-delay: 2s;
		animation-duration: 35s;
	}

	.circles li:nth-child(10) {
		left: 85%;
		width: 150px;
		height: 150px;
		animation-delay: 0s;
		animation-duration: 11s;
	}

	@keyframes animate {
		0% {
			transform: translateY(0) rotate(0deg);
			opacity: 1;
			border-radius: 0;
		}

		100% {
			transform: translateY(-1000px) rotate(720deg);
			opacity: 0;
			border-radius: 50%;
		}
	}

	.nav-bar {
		backdrop-filter: blur(10px);
		background: rgba(247, 247, 247, 0.1);
	}
</style>
<template>
	<div class="area">
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
	</div>

	<template v-if="page == 'home'">
		<div
			class="w-100 d-flex justify-content-center align-items-center flex-column"
			style="height: 100vh; background-color: azure">
			<h3>Eagle 猜歌小遊戲</h3>
			<div class="d-flex">
				<button class="btn btn-primary" @click="page = 'create'">
					建立房間
				</button>
				<p class="m-4">或</p>
				<button
					class="btn btn-dark"
					@click="
						page = 'room_list';
						get_rooms();
					">
					尋找房間
				</button>
			</div>
		</div>
	</template>
	<template v-if="page == 'room_list'">
		<div class="w-100" style="height: 100vh; background-color: azure">
			<div class="container pt-3">
				<button class="btn btn-dark w-100 mb-2" @click="page = 'home'">
					返回
				</button>
				<button class="btn btn-dark w-100" @click="get_rooms()">刷新</button>
			</div>
			<div class="d-flex flex-wrap gap-3 container pt-4 pb-4">
				<div class="card p-3" v-for="room in rooms" :key="room.room_id">
					<div class="d-flex align-items-center justify-content-center">
						<img
							:src="room.data.artwork"
							width="180"
							height="180"
							class="me-3" />
						<div>
							<h4>
								<i class="fa-solid fa-arrow-up-right-from-square"></i> #{{
									room.room_id
								}}
							</h4>
							<p>{{ room.data.name }}</p>
							<p>
								<i class="fa-solid fa-user-group"></i> {{ room.user_count }}
							</p>
							<router-link
								class="btn btn-dark w-100 mt-3"
								:to="{ name: 'Room', params: { room_id: room.room_id } }"
								>進入房間</router-link
							>
						</div>
					</div>
				</div>
			</div>
		</div>
	</template>
	<template v-if="page == 'create'">
		<div class="container pt-3">
			<va-card>
				<va-card-title>建立房間</va-card-title>
				<va-card-content>
					<div>
						<div
							class="pb-2 d-flex gap-3 justify-content-between align-items-center">
							<va-button outline class="mr-4 mb-2" @click="page = 'home'"
								>返回</va-button
							>
							<va-button-group>
								<va-button @click="mode = 'manual'">手動選取歌單</va-button>
								<va-button @click="mode = 'fast'">快速導入歌單</va-button>
							</va-button-group>
						</div>
						<template v-if="mode == 'fast'">
							<div class="pb-2">
								<select
									class="form-select"
									aria-label="Default select example"
									@change="fastSelect(this.key)"
									v-model="key">
									<option value="None" selected>快速導入</option>
									<option v-for="pl in playlists" :value="pl.value">
										{{ pl.name }}
									</option>
									<option value="pl.370b1f4caa54400cbbb36e0585f10565">
										Top 25 Taipei
									</option>
									<option value="pl.2f5fcebf9ad247098e445d27011aecc4">
										今日熱門-日本流行樂
									</option>
									<option value="pl.5ee8333dbe944d9f9151e97d92d1ead9">
										a-list-歐美流行樂
									</option>
									<option value="pl.beb783da7712481fbeed35be144bd48c">
										a-list-國語流行樂
									</option>
									<option value="pl.48229b41bbfc47d7af39dae8e8b5276e">
										a-list-韓國流行樂
									</option>
									<option value="pl.6d8228f57b864a4296dc02d9761a0d9b">
										熱播金曲-國語流行樂
									</option>
									<option value="pl.3c940066ea8d47adb2d317c492a981fe">
										卡拉永遠ok-國語
									</option>
								</select>
							</div>
							<button
								class="btn btn-dark w-100 mt-3"
								@click="get_playlist_info"
								:disabled="loading">
								讀取
							</button>
						</template>
						<template v-else-if="mode == 'manual'">
							<div class="pb-2">
								<p>Apple Music 網址暫放處</p>
								<input
									type="text"
									placeholder="給你方便訪網址的，可不必填寫。"
									class="w-100 form-control" />
								<p>Apple Music 播放列表ID (pl.xxxxxxxxxxxxxxxxxx)</p>
								<input type="text" v-model="id" class="w-100 form-control" />
							</div>
							<button
								class="btn btn-dark w-100 mt-3"
								@click="get_playlist_info"
								:disabled="loading">
								讀取
							</button>
						</template>
					</div>
					<div
						v-if="playlist_info.name != ''"
						class="p-3 d-flex align-items-center flex-wrap justify-content-center">
						<img
							:src="playlist_info.artworkImg"
							width="300"
							height="300"
							class="me-3" />
						<div>
							<h3>{{ playlist_info.name }}</h3>
							<p>{{ playlist_info.description }}</p>
							<p>數量:{{ playlist_info.count }}</p>
							<button
								class="btn btn-dark w-100 mt-3"
								@click="CreateRoom"
								:disabled="loading">
								建立房間
							</button>
						</div>
					</div>
				</va-card-content>
			</va-card>
		</div>
	</template>
</template>

<style lang="scss" scoped>
	.card {
		background-color: white;
	}
</style>

<script>
	export default {
		name: "Home",
		data() {
			return {
				mode: "fast",
				key: "None",
				page: "home",
				loading: false,
				rooms: [],
				id: "",
				playlists: [],
				playlist_info: {
					artworkImg: "",
					name: "",
					description: "",
					count: 0,
					data: null,
				},
				rawData: null,
			};
		},
		mounted() {},
		methods: {
			fastSelect(key) {
				if (key != "None") this.id = key;
			},
			get_rooms() {
				fetch("//" + window.location.hostname + `/api/room/getRooms`, {
					headers: {
						"content-type": "application/json",
					},
					cache: "no-cache",
				})
					.then((res) => res.json())
					.then((data) => {
						this.rooms = data.rooms;
					});
			},
			get_playlist() {
				fetch("//" + window.location.hostname + `/api/playlists`, {
					headers: {
						"content-type": "application/json",
					},
					cache: "no-cache",
				})
					.then((res) => res.json())
					.then((data) => {
						this.playlists = data.playlists;
					});
			},
			get_playlist_info() {
				// window.location.hostname == 'api.' ? '' : '' + window.location.hostname
				this.loading = true;
				fetch("//" + window.location.hostname + `/api/playlist/${this.id}`, {
					headers: {
						"content-type": "application/json",
					},
					cache: "no-cache",
				})
					.then((res) => res.json())
					.then((data) => {
						this.playlist_info.artworkImg = data.data.artwork;
						this.playlist_info.name = data.data.rawName;
						this.playlist_info.description = data.data.description.short;
						this.loading = false;
						this.playlist_info.data = data.data;
						this.playlist_info.count = data.data.songs.data.length;
						this.rawData = data.data;
					})
					.catch((error) => {
						console.log(error);
						this.loading = false;
					});
			},
			CreateRoom() {
				this.loading = true;
				fetch("//" + window.location.hostname + "/api/room/create", {
					body: JSON.stringify(this.rawData),
					headers: {
						"content-type": "application/json",
						Authorization: "Bearer " + this.getToken(),
					},
					cache: "no-cache",
					method: "POST",
				})
					.then((res) => res.json())
					.then((data) => {
						this.$router.push({
							name: "Room",
							params: { room_id: data.room_id },
						});
					})
					.catch((error) => {
						console.log(error);
						this.loading = false;
					});
			},
			getToken() {
				function uuidv4() {
					return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, (c) =>
						(
							c ^
							(crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (c / 4)))
						).toString(16)
					);
				}
				var token = localStorage.getItem("token");
				if (token == null) {
					localStorage.setItem("token", uuidv4());
				}
				token = localStorage.getItem("token");
				return token;
			},
		},
		computed: {},
	};
</script>
