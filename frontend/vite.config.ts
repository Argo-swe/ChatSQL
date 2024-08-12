import vue from '@vitejs/plugin-vue';
import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import istanbul from 'vite-plugin-istanbul';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    istanbul({
      include: 'src/*',
      exclude: ['node_modules', 'test/', 'cypress/'],
      extension: ['.js', '.ts', '.vue'],
      requireEnv: true
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://host.docker.internal:8000',
        changeOrigin: true
      }
    }
  }
});
