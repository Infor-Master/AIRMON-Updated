<template>
  <div>
    <div>
      <b-navbar toggleable="lg" type="dark" variant="dark" fixed="top">
        <b-navbar-brand href="/#/devices">AIRMON</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse is-nav id="nav-collapse">
          <b-navbar-nav>
            <b-nav-item href="/#/devices">Dispositivos</b-nav-item>
            <b-nav-item href="/#/admin">Admin</b-nav-item>
            <b-nav-item href="/#/logout">Logout</b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
    <div>
      <b-card bg-variant="light" class="bCard">
        <form class="device" @submit.prevent="handlerAddDevice">
          <h3>Add Device</h3>
          <div class="DeviceForm">
            <div class="form-group">
              <label>Device Name</label>
              <input
                required
                v-model="devname"
                class="form-control form-control-lg"
                type="text"
                placeholder="Device Name"
              />
            </div>
            <div class="form-group">
              <label>Device Key</label>
              <input
                required
                v-model="devtoken"
                class="form-control form-control-lg"
                type="text"
                placeholder="Device Key"
              />
            </div>
            <button type="submit" class="btn btn-dark btn-lg btn-block">
              Create Device
            </button>
          </div>
          <p>{{ addmessage }}</p>
        </form>
      </b-card>
      <b-card bg-variant="light" class="bCard">
        <form class="device" @submit.prevent="handlerRemoveDevice">
          <h3>Remove Device</h3>
          <div class="DeviceForm">
            <div class="form-group">
              <b-form-select
                v-model="devRemove"
                :options="devoptions"
                size="sm"
                class="mr-sm-2"
              />
            </div>
            <button type="submit" class="btn btn-dark btn-lg btn-block">
              Remove Device
            </button>
          </div>
          <p>{{ remmessage }}</p>
        </form>
      </b-card>
    </div>
  </div>
</template>

<script>
import settings from "../../configs.json";
import VueJwtDecode from "vue-jwt-decode";
export default {
  data() {
    return {
      addmessage: "",
      remmessage: "",
      devname: this.devname,
      devtoken: this.devtoken,
      devRemove: null,
      devoptions: [],
    };
  },
  methods: {
    handlerAddDevice() {
      this.message = "";
      this.axios({
        method: "post",
        url: "/device",
        baseURL:
          settings.backend.protocol + settings.URL + settings.backend.path,
        data: {
          key: this.devtoken,
          name: this.devname,
        },
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
        },
      })
        .then((response) => {
          this.addmessage = response.data.message;
          this.getDevices()
        })
        .catch((error) => {
          this.addmessage = error.status + " - " + error.statusText;
        });
    },
    handlerRemoveDevice() {
      this.message = "";
      this.axios({
        method: "delete",
        url: "/device",
        baseURL:
          settings.backend.protocol + settings.URL + settings.backend.path,
        data: this.devRemove.device,
        headers: {
          Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
        },
      })
        .then((response) => {
          this.remmessage = response.data.message;
          this.getDevices()
        })
        .catch((error) => {
          this.remmessage = error.status + " - " + error.statusText;
        });
    },
    getDevices() {
      try {
        this.jwtDecoded = VueJwtDecode.decode(
          sessionStorage.getItem("session_token")
        );
        this.axios({
          method: "get",
          url: `/device`,
          baseURL:
            settings.backend.protocol + settings.URL + settings.backend.path,
          data: {},
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
          },
        })
          .then((response) => {
            this.devoptions = [];
            for (var i in response.data.data) {
              this.devoptions.push({
                value: {
                  id: response.data.data[i].ID,
                  device: response.data.data[i],
                },
                text: response.data.data[i].Name,
              });
            }
          })
          .catch((error) => {
            this.remmessage =
              error.status + " - " + error.statusText;
          });
      } catch (error) {
        this.remmessage = error.status + " - " + error.statusText;
      }
    },
  },
  mounted() {
    this.getDevices();
  },
  created() {},
  watch: {
  },
};
</script>

<style></style>
