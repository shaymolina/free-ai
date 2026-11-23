import { defineConfig, devices } from '@playwright/test';

const PORT = 4317;

export default defineConfig({
  testDir: 'test/e2e',
  fullyParallel: true,
  reporter: 'list',
  use: { baseURL: `http://127.0.0.1:${PORT}`, trace: 'off' },
  webServer: {
    command: `node ../../server.js`,
    env: { PORT: String(PORT), DATA_DIR: 'node_modules/.cache/e2e-data' },
    url: `http://127.0.0.1:${PORT}/privacy`,
    reuseExistingServer: false,
    timeout: 30_000,
  },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'] } },
  ],
});
