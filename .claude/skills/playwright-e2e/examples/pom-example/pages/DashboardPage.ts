// examples/pom-example/pages/DashboardPage.ts

import { Locator, Page, expect } from '@playwright/test';

export class DashboardPage {
  readonly page: Page;
  readonly welcomeMessage: Locator;
  readonly logoutButton: Locator;
  readonly dashboardHeading: Locator;

  constructor(page: Page) {
    this.page = page;
    this.welcomeMessage = page.getByText('Welcome,');
    this.logoutButton = page.getByRole('button', { name: 'Log Out' });
    this.dashboardHeading = page.getByRole('heading', { name: 'Dashboard' });
  }

  async goto() {
    await this.page.goto('http://localhost:3000/dashboard');
  }

  async expectWelcomeMessage(username: string) {
    await expect(this.welcomeMessage).toHaveText(`Welcome, ${username}!`);
  }

  async logout() {
    await this.logoutButton.click();
  }

  async expectToBeOnDashboard() {
    await expect(this.page).toHaveURL(/.*dashboard/);
    await expect(this.dashboardHeading).toBeVisible();
  }
}