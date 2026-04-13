import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // Generate manifestation for Django static files
    manifest: true,
    outDir: '../frontend/projects/static/dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: 'src/main.jsx'
      },
      output: {
        // Keeps names stable for easy inclusion in django templates
        entryFileNames: `assets/[name].js`,
        chunkFileNames: `assets/[name].js`,
        assetFileNames: `assets/[name].[ext]`
      }
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
