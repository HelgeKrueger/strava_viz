<template>
  <div>
    <h1>Monthly overview</h1>

    <div>
      <select v-model="filter_activity_type" value="Both">
        <option selected="selected" value="both">Both</option>
        <option value="ride">Rides</option>
        <option value="run">Runs</option>
      </select>

      <select v-model="display_variable" value="Both">
        <option value="distance">Distance (km)</option>
        <option value="teim">Moving time (hours)</option>
      </select>
    </div>

    <svg class="canvas" />
  </div>
</template>

<script>
const d3 = require("d3");

export default {
  name: "Monthly",
  data: () => {
    return {
      display_variable: "distance",
      filter_activity_type: "both",
      raw_data: null
    };
  },
  mounted() {
    d3.json("/api/monthly_data").then(data => {
      this.raw_data = data;
      this.updateGraph();
    });
  },
  watch: {
    display_variable: function() {
      this.updateGraph();
    }
  },
  methods: {
    updateGraph: function() {
      const canvas = d3.select(this.$el).select("svg");
      canvas.selectAll("*").remove();

      const width = parseInt(canvas.style("width"), 10);
      const height = parseInt(canvas.style("height"), 10);
      const marginX = 50;
      const marginY = 50;

      const data_index = this.display_variable === "distance" ? 1 : 2;
      const max_name =
        this.display_variable === "distance"
          ? "maximal_distance"
          : "maximal_time";

      const maxY = this.raw_data[max_name];

      const xScale = d3
        .scaleLinear()
        .domain([0, 31])
        .range([marginX, width - marginX]);
      const xAxis = d3.axisBottom(xScale);
      canvas
        .append("g")
        .attr("transform", `translate(0, ${height - marginY})`)
        .call(xAxis);

      const yScale = d3
        .scaleLinear()
        .domain([0, maxY])
        .range([height - marginY, marginY]);
      const yAxis = d3.axisLeft(yScale);
      canvas
        .append("g")
        .attr("transform", `translate(${marginX}, 0)`)
        .call(yAxis);

      const line = d3
        .line()
        .x(d => xScale(d[0]))
        .y(d => yScale(d[data_index]));

      const plotLine = (data, opacity) => {
        canvas
          .append("g")
          .append("path")
          .datum(data)
          .attr("fill", "none")
          .attr("stroke", "steelblue")
          .attr("stroke-width", 2)
          .attr("stroke-linejoin", "round")
          .attr("stroke-linecap", "round")
          .attr("stroke-opacity", opacity)
          .attr("d", line);
      };

      plotLine(this.raw_data.currentMonth, 1);
      plotLine(this.raw_data.lastYear[0], 0.4);

      this.raw_data.lastYear.slice(1).forEach(d => {
        plotLine(d, 0.1);
      });
    }
  }
};
</script>

<style>
.canvas {
  width: 100%;
  height: calc(100vh - 200px);
}
</style>
