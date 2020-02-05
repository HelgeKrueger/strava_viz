<template>
  <div>
    <h1>Welcome</h1>
    <svg id="calendar-welcome" />
  </div>
</template>

<script>
import { transformData } from "../data/transform";
const d3 = require("d3");

const formatYearMonth = d => {
  const year = d["datetime"].getUTCFullYear();
  const month = d["datetime"].getMonth() + 1;
  if (month < 10) {
    return `${year}-0${month}`;
  }
  return `${year}-${month}`;
};

export default {
  name: "Welcome",
  mounted: () => {
    d3.json("/api/activities").then(data => {
      data = transformData(data);
      const years = d3
        .nest()
        .key(formatYearMonth)
        .sortKeys(d3.descending)
        // TODO Adapt to monthly list
        // .key(d => d["datetime"].getMonth())
        // .sortKeys(d3.ascending)
        .entries(data);
      console.log(years[0]);
      console.log(years[1]);
    });
  }
};
</script>
