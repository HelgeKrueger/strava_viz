<template>
  <div>
    <div class="plotOptions">
      <select v-model="filter_activity_type" value="Both">
        <option selected="selected" value="both">Both</option>
        <option value="ride">Rides</option>
        <option value="run">Runs</option>
      </select>
    </div>
    <svg class="canvas" />
  </div>
</template>

<script>
import { transformData } from "../data/transform.js";
import { determineColor } from "../calendar.js";

const d3 = require("d3");

function renderHistoric(data, filter_activity_type) {
  let filter = {};

  if (filter_activity_type !== "both") {
    filter.filter = filter_activity_type.toLowerCase();
  }

  data = transformData(data, filter);

  const canvas = d3.select("svg.canvas");

  canvas.selectAll("*").remove();

  const minDate = data[0]["datetime"];
  const maxDate = data[data.length - 1]["datetime"];

  const distances = data.map(d => d["distance_km"]);
  const maxDistance = d3.max(distances);
  const minDistance = d3.min(distances);

  const xAxis = d3
    .scaleLinear()
    .domain([minDistance, maxDistance])
    .range([0, 1000]);

  const yAxis = d3
    .scaleTime()
    .domain([minDate, maxDate])
    .range([0, 2000]);

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
    .attr("width", d => xAxis(d["distance_km"]))
    .attr("fill", determineColor);
}

export default {
  name: "Aggregated",
  data: () => {
    return {
      filter_activity_type: "both",
      data: []
    };
  },
  mounted() {
    d3.json("/api/activities").then(data => {
      this.data = data;
      renderHistoric(data, this.filter_activity_type);
    });
  },
  watch: {
    filter_activity_type: function() {
      renderHistoric(this.data, this.filter_activity_type);
    }
  }
};
</script>
<style scoped>
svg.canvas {
  width: 1100px;
  height: 2100px;
}

div.plotOptions {
  margin: 20px;
}
</style>
