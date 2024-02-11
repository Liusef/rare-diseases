import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({command, mode}) => {
  const env = loadEnv(mode, process.cwd(), '');
  return {
    server: {
      proxy: {
        "/api": {
          target: env.VITE_APP_PROXY_HOST,
          changeOrigin: true,
          secure: false,
        },
      },
    },
    plugins: [react()],
  };
})
