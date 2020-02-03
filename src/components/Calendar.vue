<template>
  <svg class="canvas" />
</template>

<script>
import { buildCalendar } from "../calendar.js";
import { transformData } from "../data/transform.js";

const d3 = require("d3");

export default {
  name: "Calendar",
  mounted() {
    const canvas = d3.select("svg.canvas");

    d3.json("/api/activities").then(data => {
      data = transformData(data);

      buildCalendar(canvas, data);
    });
  }
};
</script>

<style>
</style>
