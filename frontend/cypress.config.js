import coverageTask from '@cypress/code-coverage/task';
import { defineConfig } from 'cypress';

export default defineConfig({
  component: {
    devServer: {
      framework: 'vue',
      bundler: 'vite'
    },
    setupNodeEvents(on, config) {
      coverageTask(on, config);
      return config;
    },
    specPattern: 'tests/component/**/*.{js,ts,jsx,tsx}'
  },
  e2e: {
    baseUrl: 'http://localhost:5173',
    specPattern: 'tests/e2e/**/*.{js,ts,jsx,tsx}'
  }
});
