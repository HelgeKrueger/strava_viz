import { transformData } from "./transform";

test("transformData", () => {
  const rawData = [
    {
      datetime: "2020-01-31T18:14:31.414Z",
      distance_meter: 1234000
    }
  ];

  const transformed = transformData(rawData);

  expect(transformed[0]["distance_km"]).toBe(1234);
});

test("transformData - filter", () => {
  const rawData = [
    {
      datetime: "2020-01-31T18:14:31.414Z",
      distance_meter: 1234000,
      activity_type: "run"
    },
    {
      datetime: "2020-01-31T18:14:31.414Z",
      distance_meter: 1000,
      activity_type: "ride"
    }
  ];

  const transformed = transformData(rawData, { filter: "ride" });

  expect(transformed.length).toBe(1);
  expect(transformed[0]["distance_km"]).toBe(1);
});
