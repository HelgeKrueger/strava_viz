import { Aggregator } from "./aggregator.js";
import { parseISO, add } from "date-fns";

const now = parseISO("2020-02-10");

test("aggregator", () => {
  const raw_data = [
    {
      datetime: parseISO("2019-06-28"),
      distance_km: 250
    },
    {
      datetime: parseISO("2020-01-28"),
      distance_km: 4
    },
    {
      datetime: parseISO("2020-02-02"),
      distance_km: 10
    },
    {
      datetime: parseISO("2020-02-08"),
      distance_km: 1
    }
  ];

  const aggregator = new Aggregator(raw_data, {}, now);
  const currentMonth = aggregator.currentMonth;
  const lastMonth = aggregator.lastMonth;
  const lastYear = aggregator.lastYear;

  expect(currentMonth.length).toBe(3);
  expect(currentMonth[1]).toEqual([2, 10]);
  expect(currentMonth[2]).toEqual([8, 11]);

  expect(lastMonth.length).toBe(2);
  expect(lastMonth[1]).toEqual([28, 4]);

  expect(lastYear.length).toBe(11);
});
