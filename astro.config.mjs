import { defineConfig } from 'astro/config'; 
 
export default defineConfig({ 
  site: 'https://www.abhishekmohantyhcmcloud.com', 
  markdown: { 
    allowDangerousHtml: true, 
    shikiConfig: { 
      theme: 'one-dark-pro', 
      wrap: true, 
    }, 
  }, 
  build: { 
    format: 'directory', 
  }, 
}); 
