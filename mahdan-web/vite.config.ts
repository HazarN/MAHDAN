import react from '@vitejs/plugin-react';
import { defineConfig, loadEnv } from 'vite';

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const dotenv = loadEnv(mode, process.cwd());

  const PORT: number = parseInt(dotenv.VITE_PORT as string) || 3333;

  return {
    plugins: [react()],
    server: { port: PORT },
  };
});
