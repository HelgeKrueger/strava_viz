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

      const minDate = data[0]["datetime"];
      const maxDate = data[data.length - 1]["datetime"];

      const maxDistance = d3.max(data.map(d => d["distance_km"]));
      const minDistance = d3.min(data.map(d => d["distance_km"]));

      const xAxis = d3
        .scaleLinear()
        .domain([minDistance, maxDistance])
        .range([0, 1000]);

      const yAxis = d3
        .scaleTime()
        .domain([minDate, maxDate])
        .range([0, 1000]);

      canvas
        .append("g")
        .attr("transform", "translate(50, 50)")
        .call(d3.axisLeft(yAxis));

      canvas
        .append("g")
        .attr("transform", "translate(50, 50)")
        .call(d3.axisTop(xAxis));
      canvas
        .append("g")
        .attr("transform", "translate(50, 50)")
        .selectAll("rect")
        .data(data)
        .join("rect")
        .attr("x", () => 0)
        .attr("y", d => yAxis(d["datetime"]))
        .attr("height", 1)
        .attr("width", d => xAxis(d["distance_km"]));
    });
  }
};
</script>
<style>
svg {
  width: 1100px;
  height: 1100px;
}
</style>
