<template>
  <div>
    <div>
      <b-navbar toggleable="lg" type="dark" variant="dark" fixed="top">
        <b-navbar-brand href="/#/devices">AIRMON</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
        <b-collapse is-nav id="nav-collapse">
            <b-navbar-nav>
                <b-nav-item href="/#/devices">Dispositivos</b-nav-item>
                <b-nav-item href="/#/logout">Logout</b-nav-item>
            </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
    <div>
      <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
      <datatable
        title="Leituras Sensores"
        :columns="columns"
        :rows="data"
        :clickable="false"
        :printable="false"
        :perPage="[10, 20, 50, 100]"
        :defaultPerPage=20
      >
      </datatable>
    </div>
  </div>
</template>

<script>
import settings from "../../configs.json";
import VueJwtDecode from "vue-jwt-decode";
import DataTable from "vue-materialize-datatable";

export default {
  components: {
    "datatable": DataTable
  },
  data() {
    return {
      limit: this.$route.params.limit,
      offset: this.$route.params.offset,
      device: {},
      data: [],
      columns: [{
        label: "Time",
        field: "CreatedAt",
        numeric: false,
        html: false
      },{
        label: "O3 (ppm)",
        field: "O3_PPM",
        numeric: true,
        html: false
      },{
        label: "CO2 (ppm)",
        field: "CO2_PPM",
        numeric: true,
        html: false
      },{
        label: "NO2 (ppm)",
        field: "NO2_PPM",
        numeric: true,
        html: false
      },{
        label: "CH2O (ppm)",
        field: "CH2O_PPM",
        numeric: true,
        html: false
      },{
        label: "Temperatura (ºC)",
        field: "Temp_C",
        numeric: true,
        html: false
      },{
        label: "Humidade (%)",
        field: "Hum_100",
        numeric: true,
        html: false
      }]
    };
  },
  methods: {
    getDevice() {
      try {
        this.jwtDecoded = VueJwtDecode.decode(
          sessionStorage.getItem("session_token")
        );
        this.axios({
          method: "get",
          url: `/device/`+this.$route.params.id,
          baseURL:
            settings.backend.protocol + settings.URL + settings.backend.path,
          data: {},
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
          },
        })
          .then((response) => {
            this.devices = response.data.data;
            this.getData();
          })
          .catch((error) => {
            this.message =
              error.status + " - " + error.statusText;
          });
      } catch (error) {
        this.message =
          error.status + " - " + error.statusText;
      }
    },
    getData() {
      try {
        this.jwtDecoded = VueJwtDecode.decode(
          sessionStorage.getItem("session_token")
        );
        this.axios({
          method: "get",
          url: `/data/`+this.$route.params.id+`/`+this.limit+`/`+this.offset,
          baseURL:
            settings.backend.protocol + settings.URL + settings.backend.path,
          data: {},
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("session_token")}`,
          },
        })
          .then((response) => {
            console.log(response)
            this.data = [];
            for (var i in response.data.data) {
              this.data.push(response.data.data[i]);
            }
          })
          .catch((error) => {
            this.message =
              error.status + " - " + error.statusText;
          });
      } catch (error) {
        this.message =
          error.status + " - " + error.statusText;
      }
    },
    deviceHandler(id) {
      this.$router.push("/devices/" + id);
    },
  },
  mounted() {
    this.getDevice();
  },
  created() {},
  watch: {},
};
</script>

<style>
.bCard {
  width: auto;
  margin: auto;
  padding: 20px;
}
html,
body {
  margin: 0px;
  padding: 0px;
  background-color: rgb(221, 221, 221);
}
</style>
