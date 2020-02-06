<template>
  <div>
    <h1>Welcome</h1>
    <svg id="calendar-welcome" />
    <div class="activities">
      <ActivityOverview v-for="id in activityIds" v-bind:key="id" v-bind:activityId="id" />
    </div>
    <div class="monthly-activity">
      <div class="monthly-run">
        <h2>Rides</h2>
        <MonthlyLineChart
          display_variable="distance"
          v-bind:raw_data="monthlyData"
          filter_activity_type="ride"
        />
      </div>
      <div class="monthly-run">
        <h2>Runs</h2>
        <MonthlyLineChart
          display_variable="distance"
          v-bind:raw_data="monthlyData"
          filter_activity_type="run"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { transformData } from "../data/transform";
const d3 = require("d3");

import ActivityOverview from "./ActivityOverview.vue";
import MonthlyLineChart from "./MonthlyLineChart.vue";

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
  data: function() {
    return {
      monthlyData: {},
      activityIds: {}
    };
  },
  mounted: function() {
    const svg = d3.select("svg");
    const cellSize = 15;
    const cellSpacing = 20;

    d3.json("/api/monthly_data").then(data => {
      this.monthlyData = data;
    });

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
        .attr("fill", determineColor)
        .on("click", d => {
          this.activityIds = d["ids"];
        });

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
        .attr("fill", determineColor)
        .on("click", d => {
          this.activityIds = d["ids"];
        });
      console.log(data);
    });
  },
  components: { ActivityOverview, MonthlyLineChart }
};
</script>

<style>
#calendar-welcome {
  width: 500px;
  height: 175px;
}

@media (min-width: 800px) {
  .monthly-activity {
    position: absolute;
    top: 100px;
    right: 10px;
  }
}
.monthly-run {
  width: 400px;
  height: 300px;
}

.monthly-ride {
  width: 400px;
  height: 300px;
}
</style>