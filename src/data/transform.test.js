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
