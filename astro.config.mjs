import { defineConfig } from 'astro/config'; 
import rehypeRaw from 'rehype-raw'; 
 
export default defineConfig({ 
  site: 'https://www.abhishekmohantyhcmcloud.com', 
  markdown: { 
    allowDangerousHtml: true, 
    rehypePlugins: [rehypeRaw], 
    shikiConfig: { theme: 'one-dark-pro', wrap: true }, 
  }, 
  build: { format: 'directory' }, 
}); 
