<template>
  <div style="position:relative; width: 600px;">
    <div class="activity-overview-map"></div>
    <div class="activity-overview-info" v-if="info">
      <dl>
        <dt>Name:</dt>
        <dd>
          <a v-bind:href="stravaLink()">{{ info['name']}}</a>
        </dd>
        <dt>Distance:</dt>
        <dd>{{ info['distance_km'].toFixed(1) }} km</dd>
        <dt>Moving Time:</dt>
        <dd>{{ formatTime(info['moving_time']) }}</dd>
        <dt>Average Speed:</dt>
        <dd>{{ info['average_speed_kmh'].toFixed(1)}} km/h</dd>
        <dt>Average Heartrate:</dt>
        <dd>{{ info['average_heartrate']}}</dd>
      </dl>
    </div>
  </div>
</template>

<script>
import { OpenLayerMap } from "../olmap.js";

export default {
  name: "ActivityOverview",
  props: ["activityId"],
  data: function() {
    return {
      openLayerMap: new OpenLayerMap(),
      info: null
    };
  },
  mounted: function() {
    const mapDiv = this.$el.querySelector(".activity-overview-map");
    this.openLayerMap.addToDiv(mapDiv);

    fetch(`/api/activity/${this.activityId}`)
      .then(d => d.json())
      .then(d => {
        this.info = d;
        this.openLayerMap.addPolylines([d]);
      });
  },
  methods: {
    formatTime: hours => {
      const HH = Math.floor(hours);
      let MM = Math.floor((hours - HH) * 60);
      if (MM < 10) {
        MM = `0${MM}`;
      }
      return `${HH}:${MM}`;
    },
    stravaLink: function() {
      return `https://www.strava.com/activities/${this.activityId}`;
    }
  }
};
</script>


<style scoped>
.activity-overview-map {
  width: 300px;
  height: 300px;
}
.activity-overview-info {
  position: absolute;
  top: 0;
  left: 350px;
  width: 350px;
  height: 300px;
}

dt {
  width: 175px;
  font-weight: bold;
  float: left;
}

dd {
  float: left;
  margin-left: 10px;
}
</style>