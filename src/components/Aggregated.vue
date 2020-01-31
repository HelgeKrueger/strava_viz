<template>
  <svg class="canvas" />
</template>

<script>
import { transformData } from "../data/transform.js";

const d3 = require("d3");

console.log(d3);

export default {
  name: "Aggregated",
  mounted() {
    const canvas = d3.select("svg.canvas");
    d3.json("/strava-activity").then(data => {
      data = transformData(data);

      const minDate = data[0]["time_seconds"];
      const maxDate = data[data.length - 1]["time_seconds"];

      const maxDistance = d3.max(data.map(d => d["distance_meter"]));
      const minDistance = d3.min(data.map(d => d["distance_meter"]));

      const xAxis = d3
        .scaleLinear()
        .domain([minDistance, maxDistance])
        .range([0, 1000]);

      const y = d3
        .scaleLinear()
        .domain([minDate, maxDate])
        .range([0, 1000]);

      canvas.append("g").call(y);
      canvas
        .append("g")
        .selectAll("rect")
        .data(data)
        .join("rect")
        .attr("x", () => 0)
        .attr("y", d => y(d["time_seconds"]))
        .attr("height", 1)
        .attr("width", d => xAxis(d["distance_meter"]));
    });
  }
};
</script>
<style>
svg {
  width: 1000px;
  height: 1000px;
}
</style>
