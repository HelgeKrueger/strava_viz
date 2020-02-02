<template>
  <div>
    <h1>Monthly overview</h1>
    <svg class="canvas" />
  </div>
</template>

<script>
import { transformData } from "../data/transform.js";
import { Aggregator } from "../data/aggregator.js";

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

      const aggregator = new Aggregator(data);

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

      const plotLine = (data, opacity) => {
        canvas
          .append("g")
          .append("path")
          .datum(data)
          .attr("fill", "none")
          .attr("stroke", "steelblue")
          .attr("stroke-width", 3)
          .attr("stroke-linejoin", "round")
          .attr("stroke-linecap", "round")
          .attr("stroke-opacity", opacity)
          .attr("d", line);
      };

      plotLine(aggregator.currentMonth, 1);
      plotLine(aggregator.lastMonth, 0.6);

      aggregator.lastYear.forEach(d => {
        plotLine(d, 0.2);
      });
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
