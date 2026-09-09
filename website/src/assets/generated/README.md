# 生成圖片放置區（GPT Image 產出後直接放入即生效）

本資料夾由 `src/lib/generated.ts` 自動掃描；放入符合命名的圖片後重新 `npm run build`，
對應頁面會自動改用生成圖，原本的 SVG／幾何封面成為備援。**不需要修改任何程式或 frontmatter。**

| 子資料夾 | 檔名規則 | 建議尺寸 | 用途 | 備援 |
|---|---|---|---|---|
| `articles/` | `{文章 slug}.webp` | 1600×900（16:9，主體置中 55%） | 文章封面（列表卡片、文章頁、OG） | 分類幾何封面 |
| `treatments/` | `prolotherapy.webp`、`prp.webp`、`bma.webp`、`weight-management.webp` | 1200×900（4:3） | 治療頁主圖 | 治療 SVG 圖示 |
| `categories/` | `sports-injury.webp`、`weight-management.webp`、`training.webp` | 1800×600（3:1） | 分類列表頁橫幅、首頁專欄區 | 分類 SVG 插畫 |
| `decor/` | `home-hero-desktop.webp`、`home-hero-mobile.webp`、`home-portrait-surround.webp`、`home-section-divider.webp`、`home-clinic-backdrop.webp`、`home-footer-backdrop.webp` | 依 `design/image-production/supplemental.json` | 首頁／全站裝飾背景 | `public/visual-kit/decor/*.svg` |

- 支援 `.webp`、`.png`、`.jpg`、`.avif`；建議以 WebP 交付。
- 文章 slug 即 `src/content/articles/` 的檔名（不含 `.md`）。
- 若文章 frontmatter 已有 `cover`（真實照片），仍以 frontmatter 為優先。
- 提示詞與逐張規格：`design/image-production/`（`QUEUE.md`、`spec.json`、`articles-01/02.json`、`supplemental.json`）；對應表：`design/image-production/PLACEMENT.md`。
- BMA 治療圖已生成但放在 `treatments/_hold/bma.webp`，服務確認前不要移到 `treatments/bma.webp`（見 `docs/05-todo-for-owner.md` B1）。
- 目前已放入：文章封面 52、治療主圖 3（葡萄糖／PRP／體重管理）、分類橫幅 3、裝飾背景 6。生成紀錄見 `design/image-production/GENERATION.md`。
