# 外觀版本紀錄（Design Changelog）

版本規則見 `docs/06-design-versions.md`。每個版本對應 git tag `design-vX.Y.Z`。

## design-v1.2.0 — 2026-09-10

**主題：合併另一個 AI 推送的「醫學圖解與 3D 素材庫」，並加上顯示開關。**

新增（來自遠端 `main`，由 CI bot 產生）
- `public/medical-visuals/`：52 篇文章各 6 個靜態圖（封面 1600/800/480、SVG＋WebP 圖卡、OG 分享圖）、47 組 GLB 3D 模型與預覽、膝屈曲 MP4；`src/data/medical-visuals.json` 資料表。
- `MedicalVisual.astro`／`MedicalModel.astro`：文章頁「醫學圖解」區塊（三點解說、注意事項、可下載圖卡、按下按鈕才載入的 `@google/model-viewer` 3D 檢視器）。
- `/medical-visuals/` 圖庫索引頁。

本版整合調整
- `src/data/site.js` 新增 `MEDICAL_VISUALS` 開關：`covers`（3D 渲染圖作為無照片文章的封面，預設開）、`section`（醫學圖解區塊位置，預設 `'after'`＝內文之後；原整合為內文之前）、`galleryIndexable`（預設 false：圖庫頁 noindex 並排除於 sitemap，待醫師審閱通過再開）。
- 封面優先順序統一為：frontmatter 真實照片 → GPT 生成圖（`src/assets/generated/`）→ 3D 醫學示意圖 → 分類幾何封面。
- 所有 3D 素材維持原標記 `clinician-review-pending`（尚待醫師審閱），前台顯示「示意草稿・尚待醫師審閱」。

注意
- `.github/workflows/medical-visuals.yml` 會在 `main` 上的文章、ArticleCard、ArticleLayout 等檔案變動時重建素材並由 bot 自動 commit 到 `main`；推送前請先 `git pull`。

## design-v1.1.0 — 2026-09-10

**主題：整合 SVG 視覺素材包與醫學解說圖，建立生成圖片放置區。**

新增
- 首頁 Hero 背景改用 `decor/hero-flow.svg`（桌機）／`decor/hero-flow-mobile.svg`（手機）；醫師照片後方改為 `decor/portrait-halo.svg` 光環。
- 首頁專欄區與門診區之間加入 `decor/section-wave.svg` 分隔曲線。
- 門診區塊背景 `decor/clinic-panel.svg`；頁尾背景 `decor/footer-flow.svg`。
- 四張治療卡與治療頁標題加入治療圖示（`treatments/*.svg`）。
- 「從問題開始找資訊」八格加入主題圖示（`topics/*.svg`）；主題頁與「可能相關的治療」列同步顯示圖示。
- 首頁專欄區的分類 chip 改為三張分類磁磚（`categories/*.svg` 插畫＋名稱＋說明）；分類列表頁標題右側顯示分類插畫。
- 6 張醫學解說圖（`public/medical/*.svg`）以 `<figure>` 嵌入 5 篇文章：ACL 與落地機制（2 張）、場邊 ABCDE、超音波導引、體操手腕生長板、運動性腦震盪。
- `src/assets/generated/` 放置區與 `src/lib/generated.ts` 自動偵測：放入文章封面／治療主圖／分類橫幅／裝飾背景即自動啟用，SVG 為備援。
- `<meta name="design-version">` 與 `DESIGN_VERSION` 常數。

變更
- `CategoryCover` 仍作為無封面文章的幾何備援（移除封面上的分類文字，避免與 chip 重複）。
- `.prose .figure` 樣式（深色資訊圖表邊框與圖說）。

未變更
- 色彩 token、字體、版面寬度、選單結構、門診／醫師資料。

## design-v1.0.0 — 2026-09-09

**第一版本。** Astro 7 靜態網站：Design System（teal 主色、amber 輔助色、Noto Sans TC）、首頁六區、關於頁、四個治療頁（11 段結構）、專欄（52 篇）、主題入口、門診頁、404、SEO／sitemap／JSON-LD、手機底部 CTA。
