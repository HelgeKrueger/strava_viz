const d3 = require("d3");

const formatDay = d =>
  ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"][d.getUTCDay()];
const cellSize = 15;
const countDay = d => d.getUTCDay();
const timeWeek = d3.utcSunday;

function appendCaption(year) {
  year
    .append("text")
    .attr("x", -5)
    .attr("y", -20)
    .attr("text-anchor", "end")
    .attr("font-size", 16)
    .attr("font-weight", 550)
    .attr("transform", "rotate(270)")
    .text(d => d.key);
}

function showDayNames(year) {
  year
    .append("g")
    .attr("text-anchor", "end")
    .selectAll("text")
    .data(d3.range(7).map(i => new Date(1999, 0, i)))
    .join("text")
    .attr("x", 5)
    .attr("y", d => (countDay(d) + 0.5) * cellSize)
    .attr("dy", "0.31em")
    .text(formatDay);
}

function determineColor(d) {
  if (d["activity_type"] == "ride") {
    return "blue";
  }

  if (d["activity_type"] == "run") {
    return "red";
  }

  return "black";
}

function fixDay(day) {
  day = day - 1;
  if (day < 0) {
    return 6;
  }
  return day
}

function displayDays(year) {
  year
    .append("g")
    .selectAll("rect")
    .data(d => d.values)
    .join("rect")
    .attr("width", cellSize - 1.5)
    .attr("height", cellSize - 1.5)
    .attr(
      "x",
      (d, i) =>
        timeWeek.count(d3.utcYear(d.datetime), d.datetime) * cellSize + 10
    )
    .attr("y", d => fixDay(countDay(d.datetime)) * cellSize + 0.5)
    .attr("fill", determineColor);
}

module.exports = {
  appendCaption,
  showDayNames,
  displayDays
};
