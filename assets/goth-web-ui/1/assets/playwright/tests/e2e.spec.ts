import { expect, test } from "@playwright/test";

test("homepage renders", async ({ page }) => {
  const [cssResponse] = await Promise.all([
    page.waitForResponse(
      (response) =>
        response.url().includes("/assets/app.css") && response.status() === 200
    ),
    page.goto("/"),
  ]);
  expect(cssResponse.ok()).toBeTruthy();
  await expect(page.getByTestId("page-title")).toBeVisible();
});

test("htmx interaction updates fragment", async ({ page }) => {
  await page.goto("/");
  await page.getByTestId("htmx-button").click();
  await expect(page.getByTestId("htmx-target")).toContainText("Updated");
});
