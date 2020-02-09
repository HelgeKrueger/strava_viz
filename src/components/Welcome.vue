<template>
  <div>
    <div class="welcome-container">
      <div class="calendar-welcome">
        <h1>Welcome</h1>

        <CalendarWelcome v-bind:data="calendarData" @updateIds="updateIds" />
      </div>

      <div class="monthly-run">
        <h2>Rides</h2>
        <div class="chart-container">
          <MonthlyLineChart
            display_variable="distance"
            v-bind:raw_data="monthlyData"
            filter_activity_type="ride"
          />
        </div>
      </div>
      <div class="monthly-run">
        <h2>Runs</h2>
        <div class="chart-container">
          <MonthlyLineChart
            display_variable="distance"
            v-bind:raw_data="monthlyData"
            filter_activity_type="run"
          />
        </div>
      </div>
      <div class="activities">
        <ActivityOverview v-for="id in activityIds" v-bind:key="id" v-bind:activityId="id" />
      </div>
    </div>
  </div>
</template>

<script>
import { transformData } from "../data/transform";
const d3 = require("d3");

import ActivityOverview from "./ActivityOverview.vue";
import MonthlyLineChart from "./MonthlyLineChart.vue";
import CalendarWelcome from "./CalendarWelcome.vue";

export default {
  name: "Welcome",
  data: function() {
    return {
      monthlyData: {},
      activityIds: {},
      calendarData: {}
    };
  },
  mounted: function() {
    d3.json("/api/monthly_data").then(data => {
      this.monthlyData = data;
    });

    d3.json("/api/current_and_last_month").then(data => {
      this.calendarData = data;
    });
  },
  methods: {
    updateIds: function(ids) {
      console.log(ids);
      this.activityIds = ids;
    }
  },
  components: { ActivityOverview, MonthlyLineChart, CalendarWelcome }
};
</script>

<style>
.welcome-container {
  display: flex;
  flex-wrap: wrap;
}
.calendar-welcome {
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

.chart-container {
  height: calc(100% - 70px);
  width: 90%;
}

.monthly-ride {
  width: 400px;
  height: 300px;
}
</style>