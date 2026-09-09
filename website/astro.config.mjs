// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { SITE_URL, MEDICAL_VISUALS } from './src/data/site.js';

export default defineConfig({
  // TODO：正式網域確認後請更新 src/data/site.ts 的 SITE_URL（canonical、sitemap、OG 皆依此產生）
  site: SITE_URL,
  trailingSlash: 'always',
  output: 'static',
  integrations: [
    sitemap({
      // 醫學圖解圖庫頁在醫師審閱通過前不列入 sitemap（與頁面 noindex 一致）
      filter: (page) => MEDICAL_VISUALS.galleryIndexable || !page.includes('/medical-visuals/'),
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
