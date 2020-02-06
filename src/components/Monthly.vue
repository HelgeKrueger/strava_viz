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
        <option value="time">Moving time (hours)</option>
      </select>
    </div>

    <svg class="canvas" />
  </div>
</template>

<script>
const d3 = require("d3");
import LineChart from "../graph/LineChart.js";

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
    },
    filter_activity_type: function() {
      this.updateGraph();
    }
  },
  methods: {
    get_total_display_variable: function() {
      const prefix_map = {
        both: "total",
        ride: "ride",
        run: "run"
      };
      return (
        prefix_map[this.filter_activity_type] + "_" + this.display_variable
      );
    },
    get_max_value: function(data_index) {
      const lastValue = d => d[d.length - 1];
      let maximas = this.raw_data.lastYear.map(
        month => lastValue(month)[data_index]
      );
      maximas.push(lastValue(this.raw_data.currentMonth)[data_index]);

      return Math.max.apply(null, maximas);
    },
    updateGraph: function() {
      const data_index = this.get_total_display_variable();
      const maxY = this.get_max_value(data_index);

      let lineChart = new LineChart({
        width: parseInt(canvas.style("width"), 10),
        height: parseInt(canvas.style("height"), 10),
        marginX: 50,
        marginY: 50,
        selector: d3.select(this.$el).select("svg")
      })
        .clean()
        .withXRange(0, 31)
        .withYRange(0, maxY)
        .drawAxes();

      let options = {
        opacity: 1,
        xValue: d => d["day"],
        yValue: d => d[data_index]
      };

      lineChart.plotLine(this.raw_data.currentMonth, options);

      options["opacity"] = 0.4;
      lineChart.plotLine(this.raw_data.lastYear[0], options);

      options["opacity"] = 0.1;
      this.raw_data.lastYear.slice(1).forEach(
        d => {
          lineChart.plotLine(d, options);
        },
        { lineChart }
      );
    }
  }
};
</script>

<style>
.canvas {
  width: 100%;
  height: calc(100vh - 200px);
  overflow-y: scroll;
}
</style>
