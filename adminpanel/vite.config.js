import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'https://hearty-learning-production-d991.up.railway.app',
        changeOrigin: true,
      },
      '/media': {
        target: 'https://hearty-learning-production-d991.up.railway.app',
        changeOrigin: true,
      },
    },
  },
})
