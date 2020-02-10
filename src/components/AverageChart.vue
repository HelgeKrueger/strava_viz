<template>
  <div class="line-chart">
    <svg class="line-chart-svg" />
  </div>
</template>

<script>
const d3 = require("d3");
import LineChart from "../graph/LineChart.js";
export default {
  name: "AverageChart",
  props: ["display_variable", "raw_data"],
  watch: {
    display_variable: function() {
      this.updateGraph();
    },
    raw_data: function() {
      this.updateGraph();
    }
  },
  methods: {
    get_total_display_variable: function() {
      const name_map = {
        heartrate: "average_heartrate"
      };
      return name_map[this.display_variable];
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
      const item_count = 30;

      const data_index = this.get_total_display_variable();
      // const maxY = this.get_max_value(data_index);

      let lineChart = new LineChart({
        width: parseInt(canvas.style("width"), 10),
        height: parseInt(canvas.style("height"), 10),
        marginX: 50,
        marginY: 50,
        selector: canvas
      })
        .clean()
        .withXRange(0, item_count)
        .withYRange(0, 205)
        .drawAxes();

      let options = {
        opacity: 1,
        xValue: d => d["index"],
        yValue: d => d[data_index]
      };

      console.log(this.raw_data, data_index);

      const data = this.raw_data.slice(0, item_count).map((d, idx) => {
        d["index"] = item_count - idx - 1;
        return d;
      });

      const run_data = data.filter(d => d["activity_type"] == "run");
      const ride_data = data.filter(d => d["activity_type"] == "ride");

      lineChart.plotLine(ride_data, options);
      options["color"] = "red";
      lineChart.plotLine(run_data, options);
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