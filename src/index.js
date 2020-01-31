const d3 = require("d3");
const calendar = require("./calendar.js");

const canvas = d3.select("#canvas");

const cellSize = 15;
const yearHeight = cellSize * 7 + 25;

function transformData(data) {
  return data.map(d => {
    d["datetime"] = new Date(d["datetime"]);
    d["time_seconds"] = d["datetime"].getTime();

    return d;
  });
}

d3.json("/strava-activity").then(data => {
  data = transformData(data);
  console.log(data);
  const years = d3
    .nest()
    .key(d => d["datetime"].getUTCFullYear())
    .sortKeys(d3.descending)
    // TODO Adapt to monthly list
    // .key(d => d["datetime"].getMonth())
    // .sortKeys(d3.ascending)
    .entries(data);

  console.log(years);

  const year = canvas
    .selectAll("g")
    .data(years)
    .join("g")
    .attr(
      "transform",
      (d, i) => `translate(40, ${yearHeight * i + cellSize * 1.5})`
    );

  calendar.appendCaption(year);
  calendar.showDayNames(year);
  calendar.displayDays(year);
});
