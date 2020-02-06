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

    <div class="canvas">
      <MonthlyLineChart
        v-bind:display_variable="display_variable"
        v-bind:raw_data="raw_data"
        v-bind:filter_activity_type="filter_activity_type"
      />
    </div>
  </div>
</template>

<script>
import MonthlyLineChart from "./MonthlyLineChart.vue";

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
    });
  },
  components: { MonthlyLineChart }
};
</script>

<style>
.canvas {
  width: 100%;
  height: calc(100vh - 200px);
  overflow-y: scroll;
}
</style>
