<template>
  <svg class="canvas" />
</template>

<script>
import { buildCalendar } from "../calendar.js";

const d3 = require("d3");

function transformData(data) {
  return data.map(d => {
    d["datetime"] = new Date(d["datetime"]);
    d["time_seconds"] = d["datetime"].getTime();

    return d;
  });
}

export default {
  name: "Calendar",
  mounted() {
    const canvas = d3.select("svg.canvas");

    d3.json("/strava-activity").then(data => {
      data = transformData(data);

      buildCalendar(canvas, data);
    });
  }
};
</script>

<style>
svg {
  width: 100%;
  height: 2000px;
}
</style>
