
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/Cloud-Based-Assignment-Submission-Portal/',
  server: { port: 5173 },
  preview: { port: 4173 },
});
