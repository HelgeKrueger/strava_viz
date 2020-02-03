<template>
  <div>
    <h1>Monthly overview</h1>
    <svg class="canvas" />
  </div>
</template>

<script>
const d3 = require("d3");

export default {
  name: "Monthly",
  mounted() {
    d3.json("/api/monthly_data").then(data => {
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

      plotLine(data.currentMonth, 1);
      plotLine(data.lastYear[0], 0.6);

      data.lastYear.slice(1).forEach(d => {
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
