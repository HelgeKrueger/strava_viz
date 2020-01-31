test("verifying how date works", () => {
    const dateThursday = new Date(1580394593000);
    const dateSunday = new Date(1569177377000);

    expect(dateThursday.getUTCDay()).toBe(4);
    expect(dateSunday.getUTCDay()).toBe(0);
});