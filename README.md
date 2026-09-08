# 程皓醫師 網路資料彙整（Dr. Cheng Hao Web Data）

為「程皓醫師。好動人生」官方網站開發所收集的公開網路資料彙整。

- **對象**：程皓醫師 — 復健科／家庭醫學科／運動醫學科，聯新國際醫院運動醫學科專任醫師、樂天桃猿隨隊醫療團隊
- **收集日期**：2026-09-08
- **用途**：網站建置參考素材（內容著作權屬程皓醫師及各原平台所有）

## 目錄結構

```
DoctorHao_WebData/
├── website_blog/          # 官方 Blogger 部落格「程皓醫師。好動人生」
│   ├── posts/             #   7 篇文章全文（.md，含標題/日期/原文URL）
│   ├── html/              #   每篇原始 HTML
│   └── images/            #   21 張文章圖片
├── facebook/              # FB 粉專「程皓醫師好動人生-運動與家庭醫學」(ID: 100090796624852)
│   ├── posts/             #   152 則貼文全文（2023-03-15 創立 ～ 2026-08-01 完整歷史）
│   └── images/            #   211 張照片（預設相簿全量 2022-09 起 + 大頭貼 + 封面照）
├── threads/               # Threads @drchenghao（已認證帳號）
│   ├── posts/             #   1071 則貼文（含回覆/續文/引用轉發）
│   └── images/            #   413 張圖片
├── instagram/             # IG @drchenghao
│   ├── posts/             #   個人檔摘要 + 12 則貼文的圖片資訊
│   └── images/            #   12 張貼文圖(全解析度) + 12 張格線縮圖 + 大頭貼
├── hospital_profiles/     # 醫院/診所醫師介紹頁（聯新國際醫院、板新醫院、ME美醫誌、Doctoreasyfind）
├── youtube/               # YouTube 相關影片 metadata（videos.json）
└── metadata/              # 收集記錄（來源、時間、方法成敗）
```

## 收集統計

| 平台 | 數量 | 範圍 | 狀態 |
|------|------|------|------|
| Blogger 部落格 | 7 篇全文 + 21 圖 | 2023-03 ~ 2023-05 | ✅ 完整（feed 總數即 7 篇） |
| Threads | 1071 則 + 413 圖 | 2025-03-26 ~ 2026-09-08 | ✅ 完整歷史（分頁至 has_next=false） |
| Facebook 粉專 | **152 則全文** + 211 圖 | 2022-09（相簿最早）~ 2026-08-01 | ✅ 貼文全史（GraphQL 匿名重放至 cursor 耗盡）＋相簿全量 |
| Instagram | 12/25 張貼文圖 | — | ⚠️ 貼文文字需登入，僅取得圖片層 |
| 醫院介紹頁 | 4 頁 + 1 張醫師照 | — | ✅ |
| YouTube | 2 支相關影片 metadata | — | ✅（另 1 支為同姓他人、1 支已下架） |

## 收集方法摘要（詳見 metadata/）

- **Blogger**：Atom feed JSON（`/feeds/posts/default?alt=json`）取全文，圖片以 s1600 參數取原尺寸
- **Threads**：Googlebot UA 取個人頁內嵌 JSON；GraphQL 分頁 API（doc_id 自官方 JS bundle 解出：首頁 `28581921448092834`、翻頁 `28150103917987977`），53 頁跑完整時間軸
- **Facebook**：Googlebot UA 直抓個人頁（最新 20 則全文）；**歷史全史突破**——GitHub 社群分享的匿名 GraphQL doc_id 重放法（`/api/graphql/` + doc_id `28591463417151325` + `__user=0`，免登入免 cookie），cursor 翻頁至耗盡取回 2023-03-16 首篇起的全部 150 篇（+2 則系統文 = 152 則），完整方法與 payload 記錄於 metadata/community_github.json；圖片經 `lookaside.fbsbx.com/lookaside/crawler/media/` 端點，相簿以 `photo.php?fbid=` prev/next 鏈 BFS 走完（211 張，最早 2022-09，owner 欄位過濾非本粉專照片）
- **Instagram**：格線縮圖 `ig_cache_key` 解碼換算 shortcode，`/p/<code>/embed/captioned/` 帶 Referer 取全解析度圖片

## 限制記錄

1. **Facebook 貼文歷史已完整取得**（2026-09-09 更新）：透過社群分享的匿名 GraphQL doc_id 重放法取回全部 150 篇 + 2 則創立系統文。小限制：重放回應不含附件照片對應（照片已由相簿 BFS 全量取得，但圖↔文對應僅最新 27 張有記錄）；社群同步調查結論：免登入 post_id 枚舉原為公開無解（Reddit/HN/SO 交叉證實），本次為透過 GitHub 開源專案 `mohdtalal3/facebook_post_comment_scraper` 分享的手法突破
2. **Instagram 貼文文字**：caption 全數在登入牆後（`web_profile_info` API 回 401 require_login）；Threads 內容多同步自 IG，可作為近似替代
3. **影片檔未下載**：Threads 17 部影片、YouTube 影片僅記錄 URL 與 metadata
4. **動態內容**：聯新/板新頁面的逐週看診時段表為 JS 動態載入，靜態 HTML 不含時段

## metadata 索引

| 檔案 | 內容 |
|------|------|
| `metadata/website_sources.json` | 部落格/醫院頁/YouTube 40 個項目逐項記錄 |
| `metadata/threads_full.json` | Threads 1071 則逐篇摘要 + 方法細節 |
| `metadata/fb_ig_sources.json` | FB/IG 每個繞道方法的 HTTP 狀態與成敗 |
| `metadata/fb_history_text.json` | FB 歷史貼文挖掘：各 URL 變體/方法成敗、新聞內嵌連結管線、未竟線索 |
| `metadata/fb_history_images.json` | FB 相簿鏈式枚舉記錄：photo_id→檔名、owner 過濾、驗證統計 |
| `metadata/community_github.json` | GitHub/PyPI 開源工具調研（14 個候選）+ GraphQL 重放完整 payload |
| `metadata/community_forums.json` | Reddit/HN/Stack Overflow 社群方法調研（6 管道交叉查證） |
| `metadata/graphql_replay_posts_20260908.json` | GraphQL 重放收穫的 150 篇貼文原始資料（post_id/時間/全文） |
| `metadata/social_sources.json` | 首輪收集記錄（保留供回溯） |
| `metadata/ig_shortcodes_from_threads.txt` | 從 Threads 文字中挖出的 IG 貼文連結 |
