# 程皓醫師個人專業網站

聯新國際醫院運動醫學科 程皓醫師的個人專業網站。以 [Astro 7](https://astro.build) 建置的靜態網站：SEO 友善、零 JS 為主（僅選單互動）、內建圖片最佳化與 sitemap。

> 內容原則：只使用本機素材中可查證的資料；治療頁為一般衛教資訊並明確標示需經醫師評估；缺漏資料以 TODO 標示（見 `docs/05-todo-for-owner.md`），不自行捏造。

## 需求

- Node.js **22.12 以上**（本機已為 v24）
- npm

## 本機啟動

```bash
cd website
npm install
npm run dev          # http://localhost:4321
```

## 建置 production

```bash
cd website
npm run build        # 輸出至 website/dist/（純靜態檔案）
npm run preview      # 本機預覽 dist
```

`dist/` 可直接部署到任何靜態主機（Cloudflare Pages、Netlify、Vercel、GitHub Pages、S3、Nginx…）。

上線前請設定正式網域：修改 `src/data/site.js` 的 `SITE_URL`（或以環境變數 `SITE_URL=https://... npm run build`）。canonical、Open Graph、sitemap、robots.txt 皆依此產生。

## 其他指令

```bash
npm run check          # astro check（型別／模板檢查）
npm run import-assets  # 從上層原始素材重新匯入並最佳化照片（不會改動原始檔）
```

## 專案結構

```
website/
├── astro.config.mjs          # site、sitemap、響應式圖片設定
├── src/
│   ├── data/                 # ★ 集中管理的資料（改這裡，不必改頁面）
│   │   ├── site.js           #   網站名稱、SITE_URL、預設描述
│   │   ├── doctor.ts         #   醫師資料：現職、學經歷、證照、理念引言、社群
│   │   ├── clinics.ts        #   門診院所、時段、電話、掛號連結、就診須知
│   │   ├── treatments.ts     #   四個治療頁的全部內容（11 段結構）
│   │   ├── categories.ts     #   專欄三分類
│   │   ├── topics.ts         #   「從問題開始找」主題 → 文章 tag 對應
│   │   └── nav.ts            #   桌機／手機／footer 選單
│   ├── content/articles/     # ★ 專欄文章（Markdown + frontmatter），新增一篇＝新增一個 .md
│   ├── content.config.ts     #   文章 schema
│   ├── assets/photos/        #   醫師照片（由 import-assets 產生）
│   ├── assets/articles/      #   文章封面（由 import-assets 產生）
│   ├── components/           #   Header、Footer、卡片、FAQ、Callout…
│   ├── layouts/              #   BaseLayout（SEO head）、ArticleLayout
│   ├── pages/                #   路由
│   ├── lib/                  #   文章查詢、JSON-LD 產生
│   └── styles/global.css     #   Design tokens 與基礎樣式
├── scripts/import-assets.mjs #   照片匯入／縮圖腳本（來源對照表在檔內）
└── docs/                     #   盤點、設計、資料使用說明、待確認清單
```

## 常見維護

### 更新門診時間
編輯 `src/data/clinics.ts` 的 `schedule` 與 `lastConfirmed`，重新 build。首頁、門診頁、治療頁尾、footer、JSON-LD 會一起更新。

### 新增文章
在 `src/content/articles/` 新增 `your-slug.md`：

```md
---
title: 文章標題
description: 120 字內摘要（用於列表與 meta description）
category: sports-injury | weight-management | training
tags: [knee, shoulder, back, ankle-foot, tendon, muscle, sports-injury, weight, training]
pubDate: 2026-01-01        # 原始社群發布日期
updatedDate: 2026-09-09    # 網站更新日期
featured: false            # true 會出現在首頁精選
cover: ../../assets/articles/xxx.jpg   # 選用；無則使用分類視覺封面
coverAlt: 圖片說明
sources:
  - platform: Facebook | Threads | Blog | Instagram
    date: 2026-01-01
    url: https://...       # 選用
    note: 原文開頭或標題
---

內文（Markdown）。可用 <div class="supplement">…</div> 標示非原文的補充說明。
```

### 修改治療頁
編輯 `src/data/treatments.ts` 對應項目；頁面版型由 `src/pages/[treatment].astro` 統一產生。

### 更新醫師資料
編輯 `src/data/doctor.ts`。

## 文件

- `docs/01-content-inventory.md` 本機素材盤點與照片分級
- `docs/02-sitemap-and-design.md` Sitemap、頁面架構、Design direction
- `docs/03-design-system.md` Design System 摘要
- `docs/04-data-usage.md` 本機資料如何被整理／使用
- `docs/05-todo-for-owner.md` 尚待確認的內容清單
