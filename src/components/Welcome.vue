<template>
  <div>
    <h1>Welcome</h1>
    <svg id="calendar-welcome" />
  </div>
</template>

<script>
import { transformData } from "../data/transform";
const d3 = require("d3");

const formatYearMonth = d => {
  const year = d["datetime"].getUTCFullYear();
  const month = d["datetime"].getMonth() + 1;
  if (month < 10) {
    return `${year}-0${month}`;
  }
  return `${year}-${month}`;
};

function determineColor(d) {
  if (d["ride_distance"] > 0) {
    return "blue";
  }
  if (d["run_distance"] > 0) {
    return "red";
  }

  return "lightgray";
}

export default {
  name: "Welcome",
  mounted: () => {
    const svg = d3.select("svg");
    const cellSize = 15;
    const cellSpacing = 20;

    d3.json("/api/current_and_last_month").then(data => {
      const lastMonth = data.last_month;
      const currentMonth = data.current_month;
      const dayNames = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"];
      const monthNames = ["Januar", "Februar"];
      svg
        .append("g")
        .attr("transform", "translate(0, 20)")
        .attr("text-anchor", "end")
        .selectAll("text")
        .data(d3.range(7))
        .join("text")
        .attr("x", 30)
        .attr("y", d => (d + 0.7) * cellSpacing)
        .text(d => dayNames[d]);

      svg
        .append("g")
        .attr("transform", "translate(120, 0)")
        .attr("text-anchor", "end")
        .selectAll("text")
        .data(d3.range(2))
        .join("text")
        .attr("x", d => 120 * d)
        .attr("y", 15)
        .text(d => monthNames[d]);

      svg
        .append("g")
        .attr("transform", "translate(40, 20)")
        .selectAll("rect")
        .data(lastMonth)
        .join("rect")
        .attr("width", cellSize)
        .attr("height", cellSize)
        .attr("x", d => d["week"] * cellSpacing)
        .attr("y", d => d["weekday"] * cellSpacing)
        .attr("fill", determineColor);

      svg
        .append("g")
        .attr("transform", "translate(160, 20)")
        .selectAll("rect")
        .data(currentMonth)
        .join("rect")
        .attr("width", cellSize)
        .attr("height", cellSize)
        .attr("x", d => d["week"] * cellSpacing)
        .attr("y", d => d["weekday"] * cellSpacing)
        .attr("fill", determineColor);
      console.log(data);
    });
  }
};
</script>
