<template>
  <div>
    <div class="welcome-container">
      <div class="calendar-welcome activity-box">
        <h1>Welcome</h1>

        <CalendarWelcome v-bind:data="calendarData" @updateIds="updateIds" />
      </div>

      <div class="activity-box">
        <h2>Rides</h2>
        <div class="chart-container">
          <MonthlyLineChart
            display_variable="distance"
            v-bind:raw_data="monthlyData"
            filter_activity_type="ride"
          />
        </div>
      </div>
      <div class="activity-box">
        <h2>Runs</h2>
        <div class="chart-container">
          <MonthlyLineChart
            display_variable="distance"
            v-bind:raw_data="monthlyData"
            filter_activity_type="run"
          />
        </div>
      </div>
      <div class="activity-box">
        <h2>Heartrate</h2>
        <div class="chart-container">
          <AverageChart display_variable="heartrate" v-bind:raw_data="activities" />
        </div>
      </div>
      <div class="activity-box activities" v-for="id in activityIds" v-bind:key="id">
        <ActivityOverview v-bind:activityId="id" />
      </div>
    </div>
  </div>
</template>

<script>
import { transformData } from "../data/transform";
const d3 = require("d3");

import ActivityOverview from "./ActivityOverview.vue";
import AverageChart from "./AverageChart.vue";
import MonthlyLineChart from "./MonthlyLineChart.vue";
import CalendarWelcome from "./CalendarWelcome.vue";

export default {
  name: "Welcome",
  data: function() {
    return {
      monthlyData: {},
      activityIds: {},
      calendarData: {},
      activities: {}
    };
  },
  mounted: function() {
    d3.json("/api/monthly_data").then(data => {
      this.monthlyData = data;
    });

    d3.json("/api/activities").then(data => {
      this.activities = data;
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
  components: {
    ActivityOverview,
    AverageChart,
    MonthlyLineChart,
    CalendarWelcome
  }
};
</script>

<style>
h1 {
  text-align: center;
}
h2 {
  text-align: center;
}
.welcome-container {
  display: flex;
  flex-wrap: wrap;
  background-color: lightgray;
  height: calc(100vh - 100px);
  overflow: scroll;
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
.activity-box {
  width: 400px;
  height: 300px;
  background-color: white;
  box-shadow: 0 4px 1px 0 darkgray;
  margin: 5px;
}

.chart-container {
  height: calc(100% - 70px);
  width: 90%;
}

.activities {
  width: 800px;
}
</style>