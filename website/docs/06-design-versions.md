# 06｜網站外觀版本控制（Design Versions）

網站「外觀」以獨立的版本號追蹤，與內容更新（新增文章、門診異動）分開。

## 規則

- 版本號格式 `MAJOR.MINOR.PATCH`（語意化版本）：
  - **MAJOR**：版面結構、風格或色彩系統的重大改版（使用者一眼就知道換了樣子）。
  - **MINOR**：新增或替換視覺素材、區塊調整、元件樣式變更（如加入插畫、背景、封面圖）。
  - **PATCH**：間距、對比、字級等微調與視覺 bug 修正。
- 三個地方必須同步：
  1. `src/data/site.js` 的 `DESIGN_VERSION`（會輸出到每頁 `<meta name="design-version">`）。
  2. `website/CHANGELOG.md` 新增一節。
  3. git tag `design-vX.Y.Z`（annotated tag），並 `git push --tags`。
- 內容性修改（文章、門診時間、醫師資料）**不**變更外觀版本。

## 建立新版本的步驟

```bash
# 1. 完成視覺修改並確認 build 通過
cd website && npm run build

# 2. 更新 src/data/site.js DESIGN_VERSION 與 CHANGELOG.md，然後 commit
git add -A && git commit -m "design: vX.Y.Z 摘要"

# 3. 建立 tag 並推送
git tag -a design-vX.Y.Z -m "Design vX.Y.Z：摘要"
git push origin main --tags
```

## 回到舊版外觀（比對或還原）

```bash
git checkout design-v1.0.0 -- website/src   # 只取回舊版前端原始碼到工作區（內容檔可再手動保留）
# 或直接檢視：
git diff design-v1.0.0 design-v1.1.0 --stat -- website/src
```

## 版本紀錄

完整說明見 `CHANGELOG.md`。

| 版本 | Tag | 日期 | 摘要 |
|---|---|---|---|
| 1.0.0 | `design-v1.0.0` | 2026-09-09 | 第一版本：Astro 7 首版上線外觀（Design System、首頁、治療頁、專欄、門診頁） |
| 1.1.0 | `design-v1.1.0` | 2026-09-10 | 整合 SVG 視覺素材包（治療／主題圖示、分類插畫、首頁與門診／頁尾裝飾背景）、6 張醫學解說圖嵌入文章、建立生成圖片放置區 |
