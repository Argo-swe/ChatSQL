import coverageTask from '@cypress/code-coverage/task';
import { defineConfig } from 'cypress';

export default defineConfig({
  env: {
    VITE_VERSION: '1.0.0'
  },
  component: {
    devServer: {
      framework: 'vue',
      bundler: 'vite'
    },
    setupNodeEvents(on, config) {
      coverageTask(on, config); // Add code coverage tasks
      return config;
    },
    specPattern: 'tests/component/**/*.{js,ts,jsx,tsx}'
  }
});
