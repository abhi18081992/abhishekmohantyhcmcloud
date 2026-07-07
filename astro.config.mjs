import { defineConfig } from 'astro/config'; 
 
export default defineConfig({ 
  site: 'https://www.abhishekmohantyhcmcloud.com', 
  markdown: { 
    allowDangerousHtml: true, 
    shikiConfig: { theme: 'github-light', wrap: true }, 
  }, 
  build: { format: 'directory' }, 
}); 
