
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // Uncomment and update the line below if deploying to GitHub Pages with a repository name (not username.github.io)
  // base: '/your-repository-name/',
  define: {
    'process.env.API_KEY': JSON.stringify(process.env.API_KEY || '')
  },
  build: {
    outDir: 'dist',
    sourcemap: false
  }
});
