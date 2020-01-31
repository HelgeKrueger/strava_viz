<template>
  <div>
    <h1>Monthly overview</h1>
    <svg class="canvas" />
  </div>
</template>

<script>
import { transformData } from "../data/transform.js";

const d3 = require("d3");

const padTwoDigits = x => (x < 10 ? `0${x}` : `${x}`);

function yearMonth(d) {
  const date = d["datetime"];
  return `${date.getUTCFullYear()}-${padTwoDigits(date.getMonth())}`;
}

function transformMonthData(entries) {
  entries = entries.sort(d => d["time_seconds"]);
  return entries.reduce(
    (acc, x) => {
      const last = acc[acc.length - 1];
      acc.push([x["datetime"].getDate(), last[1] + x["distance_km"]]);
      return acc;
    },
    [[0, 0]]
  );
}

export default {
  name: "Monthly",
  mounted() {
    d3.json("/strava-activity").then(data => {
      data = transformData(data);

      let yearMonths = d3
        .nest()
        .key(yearMonth)
        .sortKeys(d3.descending)
        .entries(data);

      yearMonths = yearMonths.map(entry => {
        entry.values = transformMonthData(entry.values);
        return entry;
      });

      const canvas = d3.select("svg.canvas");

      const xScale = d3
        .scaleLinear()
        .domain([0, 31])
        .range([100, 900]);
      const xAxis = d3.axisBottom(xScale);
      canvas
        .append("g")
        .attr("transform", "translate(0, 500)")
        .call(xAxis);

      const yScale = d3
        .scaleLinear()
        .domain([0, 300])
        .range([500, 100]);
      const yAxis = d3.axisLeft(yScale);
      canvas
        .append("g")
        .attr("transform", "translate(100, 0)")
        .call(yAxis);

      const line = d3
        .line()
        .x(d => xScale(d[0]))
        .y(d => yScale(d[1]));

      canvas
        .append("g")
        .append("path")
        .datum(yearMonths[0].values)
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("d", line);

      console.log(yearMonths[0]);
    });
  }
};
</script>

<style>
.canvas {
  width: 1000px;
  height: 1000px;
}
</style>