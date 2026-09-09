# 圖片放置對應表（給負責生圖的 AI／人員）

生成完成後，**依下表檔名放入指定資料夾即可**，不需修改任何程式或文章 frontmatter；
重新 `npm run build` 後網站會自動偵測並使用（`src/lib/generated.ts`），現有 SVG／幾何封面自動退為備援。
機器可讀版本：`placement.json`。

## 1. 文章封面（52 張）

- 目錄：`website/src/assets/generated/articles/`
- 檔名：`{slug}.webp`（slug＝`articles-01.json` / `articles-02.json` 第一欄，即 `src/content/articles/{slug}.md`）
- 尺寸：1600×900（16:9），主體置中 55%（列表卡片 16:9、相關文章卡方形裁切、OG 1200×630 皆會用到）
- 顯示位置：專欄列表卡片、文章頁封面、相關文章小卡、社群分享 OG 圖
- 例外：`knee-pain-diagnosis-first`、`sideline-doctor-abcde`、`gymnastics-injuries` 已有真實照片封面（frontmatter `cover`），生成圖放入後**不會**覆蓋，除非移除 frontmatter 的 `cover`。

## 2. 治療頁主圖（4 張）

| brief id | 檔名 | 顯示位置 | 備援 |
|---|---|---|---|
| `treatment-prolotherapy` | `treatments/prolotherapy.webp` | `/prolotherapy/` 標題區右側（4:3） | 治療圖示 SVG |
| `treatment-prp` | `treatments/prp.webp` | `/prp/` | 同上 |
| `treatment-bma` | `treatments/bma.webp` | `/bma/`（**服務確認前請勿放入**） | 同上 |
| `treatment-weight-management` | `treatments/weight-management.webp` | `/weight-management/` | 同上 |

目錄：`website/src/assets/generated/treatments/`，1200×900。

## 3. 專欄分類橫幅（3 張）

| brief id | 檔名 | 顯示位置 | 備援 |
|---|---|---|---|
| `category-sports-injury` | `categories/sports-injury.webp` | `/articles/sports-injury/` 標題右側、首頁專欄區磁磚 | `visual-kit/categories/sports-injury.svg` |
| `category-weight-management` | `categories/weight-management.webp` | `/articles/weight-management/`、首頁 | 同上 |
| `category-training` | `categories/training.webp` | `/articles/training/`、首頁 | 同上 |

目錄：`website/src/assets/generated/categories/`，1800×600（顯示時裁為 3:2 或 112×76 小圖，請將主體置中）。

## 4. 首頁／全站裝飾背景（6 張）

| brief id | 檔名 | 顯示位置 | 備援 SVG |
|---|---|---|---|
| `home-hero-desktop` | `decor/home-hero-desktop.webp` | 首頁 Hero 背景（≥900px），左 60% 需近乎素色供文字 | `decor/hero-flow.svg` |
| `home-hero-mobile` | `decor/home-hero-mobile.webp` | 首頁 Hero 背景（<900px），上 60% 留白 | `decor/hero-flow-mobile.svg` |
| `home-portrait-surround` | `decor/home-portrait-surround.webp` | 首頁醫師照片後方 | `decor/portrait-halo.svg` |
| `home-section-divider` | `decor/home-section-divider.webp` | 首頁專欄區與門診區之間 | `decor/section-wave.svg` |
| `home-clinic-backdrop` | `decor/home-clinic-backdrop.webp` | 門診資訊區塊背景（首頁、關於頁、治療頁尾） | `decor/clinic-panel.svg` |
| `home-footer-backdrop` | `decor/home-footer-backdrop.webp` | 全站頁尾背景 | `decor/footer-flow.svg` |

目錄：`website/src/assets/generated/decor/`，尺寸依 `supplemental.json`。

## 檢查

```bash
cd website && npm run build      # 建置時會列出偵測到的生成圖（見 build log 或 generatedInventory）
```

## 注意

- 檔名需與上表**完全一致**（小寫、連字號），副檔名可為 `.webp`（建議）／`.png`／`.jpg`／`.avif`。
- 不生成程皓醫師本人、患者、假醫療影像、療效對照、藥品品牌；詳見 `spec.json` 的 `commonPrompt` 與各 brief 的 `avoid`。
- 醫療相關圖像上線前需經醫師審閱（`docs/05-todo-for-owner.md`）。
