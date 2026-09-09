# 03｜Design System 摘要

所有 token 定義於 `src/styles/global.css` 的 `:root`。

## 色彩

| 角色 | Token | 值 | 對比（白底） |
|---|---|---|---|
| 主品牌色（CTA、連結、標號） | `--c-brand-700` | `#0F5C6E` | 7.6:1 |
| 品牌深色（Footer、CTA 區） | `--c-brand-900` | `#0B3F4C` | — |
| 品牌 hover／eyebrow | `--c-brand-600` | `#15707F` | 5.6:1 |
| 品牌淺色（chip、底色） | `--c-brand-100` / `--c-brand-50` | `#DCEEF1` / `#F1F8F9` | — |
| 溫暖輔助（文字級） | `--c-warm-700` | `#A8521A` | 5.9:1 |
| 溫暖輔助（強調） | `--c-warm-500` | `#E0862E` | 僅用於非文字 |
| 溫暖淺底 | `--c-warm-100` / `--c-warm-50` | `#FBEFE3` / `#FDF7F0` | — |
| 主要文字 | `--c-ink` | `#1B2430` | 15:1 |
| 內文 | `--c-text` | `#2B3440` | 12:1 |
| 次要文字 | `--c-muted` | `#5B6672` | 6.3:1 |
| 分隔線 | `--c-line` | `#E3E8EC` | — |
| 淺灰面 | `--c-surface` | `#F7F9FA` | — |

分類色：運動傷害及疼痛＝teal（brand-700）、體重控制及減重＝amber（warm-700）、運動訓練＝green `#26684B`。淺底分別為 brand-100、warm-100、`#E3F2EA`。

全站經 axe-core（WCAG 2.1 AA + best-practice）檢查，文字對比皆達 4.5:1 以上。

## 字體

- 家族：`Noto Sans TC Variable`（@fontsource 自架，依 unicode-range 分包，僅載入用到的字集）→ PingFang TC → Microsoft JhengHei → system-ui。
- 字級：`--fs-xs` 13px、`--fs-sm` 15px、`--fs-base` 17px、`--fs-md` 19px、`--fs-lg` 22px、`--fs-xl` 28px、`--fs-2xl` 34px、`--fs-3xl` 44px；H1/H2 以 `clamp()` 隨視窗縮放。
- 行高：內文 1.85、標題 1.3。
- 文章欄寬：`--measure: 44em`（約 720px），標題 `text-wrap: balance`。
- 字重：內文 400、次標 600、標題 700。

## 間距與形狀

- 4px 基準：`--sp-1`(4) … `--sp-24`(96)。
- 容器：1200px；窄版（文章）860px。
- 圓角：按鈕 10px、卡片 14px、大圖 20px、chip pill。
- 陰影：`--shadow-sm/md/lg`，低飽和、單層為主。
- 過渡：160ms，`prefers-reduced-motion` 時關閉。

## 元件

| 元件 | 檔案 | 說明 |
|---|---|---|
| Button | `.btn`, `.btn--secondary`, `.btn--ghost`, `--lg/--sm/--block` | 主 CTA 為實心 brand-700；次要為外框 |
| Chip | `.chip`, `.chip--teal/amber/green` | 分類標籤 |
| Card | `.card`, `.card--link` | 統一邊框與 hover 提升 |
| Callout | `Callout.astro` | brand／warm／neutral 三種語氣，用於提醒與免責 |
| FAQ | `Faq.astro` | 原生 `<details>`，可選 FAQPage JSON-LD |
| DoctorQuote | `DoctorQuote.astro` | 醫師原話引用，附來源日期 |
| SectionHead | `SectionHead.astro` | eyebrow + 標題 + lede，可帶右側動作 |
| ArticleCard | `ArticleCard.astro` | default／compact 兩種；無封面時使用 `CategoryCover` |
| CategoryCover | `CategoryCover.astro` | 依分類色與 slug 種子產生的幾何線條封面，取代 stock photo |
| TreatmentCard | `TreatmentCard.astro` | 首頁四大治療入口 |
| ClinicCard / ClinicSection | `ClinicCard.astro`, `ClinicSection.astro` | 院所卡與共用門診區塊 |
| TopicGrid | `TopicGrid.astro` | 「從問題開始找」八格入口 |
| Header | `Header.astro` | 桌機一層選單＋專欄 dropdown（滑鼠／鍵盤／觸控）、手機 hamburger 分組選單、Esc 關閉 |
| MobileCtaBar | `MobileCtaBar.astro` | 手機底部固定「查看門診」（門診頁不顯示） |
| Breadcrumb | `Breadcrumb.astro` | 搭配 BreadcrumbList JSON-LD |

## 版面模板

- `BaseLayout`：title／description／canonical／OG／Twitter／JSON-LD（WebSite ＋ 頁面提供者）、skip link、Header、Footer、手機 CTA。
- `ArticleLayout`：Breadcrumb、分類 chip、H1、導言、meta（作者／原始發布／網站更新／閱讀時間）、封面、`.prose` 內文、免責、原始來源、相關主題、作者卡、相關文章、門診 CTA；Article JSON-LD 含 author／datePublished／dateModified。
- 治療頁（`[treatment].astro`）：11 段固定結構＋側邊目錄（桌機 sticky）＋「程皓醫師曾這樣說」＋ FAQPage JSON-LD ＋ MedicalWebPage。

## 視覺素材（design-v1.1.0 起）

| 素材 | 位置 | 用途 |
|---|---|---|
| 治療圖示 ×4 | `public/visual-kit/treatments/` | 首頁治療卡、治療頁標題、主題頁「可能相關的治療」 |
| 主題圖示 ×8 | `public/visual-kit/topics/` | 首頁「從問題開始找資訊」、主題頁標題（`tendon` 主題對應 `muscle-tendon.svg`） |
| 分類插畫 ×3 | `public/visual-kit/categories/` | 首頁專欄區分類磁磚、分類列表頁標題右側 |
| 裝飾背景 ×6 | `public/visual-kit/decor/` | Hero 桌機／手機背景、醫師照片光環、區塊分隔曲線、門診區背景、頁尾背景（皆為 CSS 背景，純裝飾） |
| UI 圖示 ×12 | `public/visual-kit/ui/` | 目前未使用（網站沿用 `Icon.astro` 的 inline SVG 以支援 currentColor／hover），保留供未來替換 |
| 醫學解說圖 ×6 | `public/medical/` | 嵌入 5 篇文章的 `<figure>`（見 `docs/07-medical-figures.md`） |

對應表集中於 `src/data/visualKit.ts`；生成圖（GPT Image）放入 `src/assets/generated/` 後由 `src/lib/generated.ts` 自動優先採用，上述 SVG 退為備援。

## 圖片策略

- 原始素材保留於上層資料夾；`scripts/import-assets.mjs` 複製並縮至最長邊 1600px（JPEG q84）至 `src/assets/`。
- 頁面以 `astro:assets` `<Image>` 輸出 WebP（OG 為 JPEG），指定 `widths`/`sizes` 產生 srcset；Hero 使用 `priority`（eager + fetchpriority=high），其餘 lazy。
- 首頁 Hero 圖 440px 版本約 22KB。
