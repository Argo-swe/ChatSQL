import coverageTask from '@cypress/code-coverage/task';
import { defineConfig } from 'cypress';

export default defineConfig({
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
