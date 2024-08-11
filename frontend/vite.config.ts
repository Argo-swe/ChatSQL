import { fileURLToPath, URL } from 'node:url';
import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vite';
import istanbul from 'vite-plugin-istanbul';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
     vue(),
+    istanbul({
+      include: ["src/**/*", "src/**/*.vue"],
+      exclude: ['node_modules', 'tests/', 'cypress/'],
+      extension: ['.js', '.ts', '.vue'],
+      requireEnv: false
+    })
+  ],
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
