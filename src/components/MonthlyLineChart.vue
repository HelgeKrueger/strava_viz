<template>
  <div class="line-chart">
    <svg class="line-chart-svg" />
  </div>
</template>

<script>
const d3 = require("d3");
import LineChart from "../graph/LineChart.js";
export default {
  name: "MonthlyLineChart",
  props: ["display_variable", "filter_activity_type", "raw_data"],
  watch: {
    display_variable: function() {
      this.updateGraph();
    },
    filter_activity_type: function() {
      this.updateGraph();
    },
    raw_data: function() {
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
      const canvas = d3.select(this.$el).select("svg");
      const data_index = this.get_total_display_variable();
      const maxY = this.get_max_value(data_index);

      let lineChart = new LineChart({
        width: parseInt(canvas.style("width"), 10),
        height: parseInt(canvas.style("height"), 10),
        marginX: 50,
        marginY: 50,
        selector: canvas
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

<style scoped>
svg.line-chart-svg {
  width: 100%;
  height: 100%;
}
div.line-chart {
  width: 100%;
  height: 100%;
}
</style>