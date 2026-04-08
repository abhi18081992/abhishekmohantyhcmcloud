import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://www.abhishekmohantyhcmcloud.com',
  markdown: {
    shikiConfig: {
      theme: 'one-dark-pro',
      wrap: true,
    },
  },
  build: {
    format: 'directory',
  },
});

// rebuild trigger
