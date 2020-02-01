import { format, add } from "date-fns";

const d3 = require("d3");

function yearMonth(d) {
  const date = d["datetime"];
  return format(date, "yyyy-MM");
}

function transformMonthData(entries) {
  entries = entries.sort(d => d["time_seconds"]);
  return entries.reduce(
    (acc, x) => {
      const last = acc[acc.length - 1];
      acc.push([x["datetime"].getDate(), last[1] + x["distance_km"]]);
      return acc;
    },
    [[0, 0]]
  );
}

export class Aggregator {
  constructor(data, options = {}, now = new Date()) {
    this.now = now;

    let yearMonths = d3
      .nest()
      .key(yearMonth)
      .sortKeys(d3.descending)
      .entries(data);

    this.yearMonths = yearMonths.map(entry => {
      entry.values = transformMonthData(entry.values);
      return entry;
    });
  }

  valuesForMonth(date) {
    const key = format(date, "yyyy-MM");
    const result = this.yearMonths.find(x => {
      return x.key === key;
    });

    return result ? result.values : [[0, 0]];
  }

  get currentMonth() {
    return this.valuesForMonth(this.now);
  }

  get lastMonth() {
    return this.valuesForMonth(add(this.now, { months: -1 }));
  }

  get lastYear() {
    return d3
      .range(-2, -13, -1)
      .map(s => this.valuesForMonth(add(this.now, { months: s })));
  }
}
