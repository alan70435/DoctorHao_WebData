// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { SITE_URL } from './src/data/site.js';

export default defineConfig({
  // TODO：正式網域確認後請更新 src/data/site.ts 的 SITE_URL（canonical、sitemap、OG 皆依此產生）
  site: SITE_URL,
  trailingSlash: 'always',
  output: 'static',
  integrations: [
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
    }),
  ],
  image: {
    // 響應式圖片：自動產生 srcset/sizes，並注入必要的 CSS
    layout: 'constrained',
    responsiveStyles: true,
  },
  build: {
    inlineStylesheets: 'auto',
  },
  prefetch: {
    prefetchAll: false,
    defaultStrategy: 'hover',
  },
});
