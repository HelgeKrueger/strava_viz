<template>
  <div style="position:relative; width: 600px;">
    <div class="activity-overview-map"></div>
    <div class="activity-overview-info" v-if="info">
      Name: {{ info['name']}}
      <br />
      Distance: {{ info['distance_km'] }} km
      <br />
      Moving Time: {{ formatTime(info['moving_time']) }}
      <br />
      Average Speed: {{ info['average_speed']}} km/h
      <br />
      Average Heartrate: {{ info['average_heartrate']}}
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
  width: 300px;
  height: 300px;
}
</style>