// examples/pom-example/pages/LoginPage.ts

import { Locator, Page, expect } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.usernameInput = page.getByLabel('Username');
    this.passwordInput = page.getByLabel('Password');
    this.loginButton = page.getByRole('button', { name: 'Log In' });
    this.errorMessage = page.locator('.error-message'); // Adjust selector as needed
  }

  async goto() {
    await this.page.goto('http://localhost:3000/login');
  }

  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async expectToBeLoggedIn() {
    await expect(this.page).toHaveURL(/.*dashboard/); // Assuming successful login redirects to /dashboard
  }

  async expectLoginError(message: string) {
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toHaveText(message);
  }
}