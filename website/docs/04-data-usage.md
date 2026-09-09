# 04｜本機資料如何被整理／使用

原始資料夾（`facebook/`、`threads/`、`website_blog/`、`instagram/`、`hospital_profiles/`、`youtube/`、`metadata/`）**未被修改**。網站所有內容皆為讀取後重新整理。

## 醫師資料 → `src/data/doctor.ts`

| 網站欄位 | 來源 |
|---|---|
| 現職、簡介、主治項目、語言 | `hospital_profiles/landseed_chenghao.md`（聯新官網） |
| 學歷、經歷（榮總、北醫訓練醫師、機場醫療中心） | 聯新、板新醫院頁 |
| 三總訓練醫師、樂天桃猿隊醫、板新運醫主治 | `hospital_profiles/memedia_finddoc755.md` |
| 家庭醫學科專科資格 | ME 美醫誌；`doctoreasyfind_chenghao.md`（衛福部登錄） |
| 針灸／針刀、運動醫學醫學會會員、小鐵人場邊醫師 | `website_blog/posts/2023-03-blog-post.md` |
| 2023-08 加入運醫科、平鎮高中服務、高壓氧訓練、Aspetar、清大授課、2026 全大運 | Facebook 貼文（日期於 doctor.ts 註記） |
| 醫療理念引言（4 句） | Threads 2025-05-15、2025-08-15、2026-01-08、2026-04-28 原文 |
| 社群連結 | FB page id 100090796624852；Threads/IG @drchenghao；Blogger |
| 相關影片 | `youtube/videos.json`（僅兩支與本人直接相關者） |

**未使用**：部落格圖片中的個人 email（未經確認不上站）、IG 追蹤數等社群數據、家庭與旅遊照片。

## 門診資訊 → `src/data/clinics.ts`

- 時段：FB 2026-02-01「最新熱騰騰門診時刻表」＋ Threads 2026-01-03 回覆（兩者一致）。
- 地址、電話、掛號連結：FB 2023-03-16、2023-08-06、2024-08-07 貼文，以及聯新／板新官網頁。
- 2024 年曾出現的桃新醫院、埔新永美診所因 2026 公告未列而排除。
- 就診須知：Threads 2025-12-18（減重門診流程）、FB 2024-10-13（初診 30 分鐘）。

## 治療頁 → `src/data/treatments.ts`

- 「程皓醫師曾這樣說」區塊：逐字引用 FB/Threads 原文（附日期）。
- 其餘段落（是什麼、原理、應用、流程、注意事項、風險、FAQ）為一般醫療衛教資訊整理，頁面頂端與各段皆標示「需經醫師評估」，不含價格、療效保證、次數承諾。
- 醫療體重管理頁的適應症（BMI 27／24–27）、禁忌、副作用與流程，皆取自程皓醫師 Threads 系列文（2025-06 ~ 2026-02）。

## 專欄文章 → `src/content/articles/*.md`（52 篇）

| 分類 | 篇數 | 主要來源 |
|---|---|---|
| 運動傷害及疼痛 | 27 | 部落格 6 篇、FB 約 20 則、Threads 約 15 則 |
| 體重控制及減重 | 13 | Threads「打瘦瘦針前你必須知道的事」ep1–25 及相關系列、FB 5 則 |
| 運動訓練 | 12 | Threads「健身必備小知識」ep1–12、補劑篇、陷阱卡 1–3、FB 6 則 |

整理原則：
1. 保留原文的醫療觀點、數據與引用文獻；不新增醫師未表達的主張。
2. 重新加上 H2/H3、重點整理、系列串連；口語與 emoji 精簡。
3. 每篇文末列出「原始來源」（平台＋日期＋原文開頭），並有免責說明。
4. 需要補充非原文資訊時，以 `<div class="supplement">` 標示「補充說明（非原始文章內容）」（目前僅 1 處：神經解套注射的一般定義）。
5. 原文提到的研究以 `<div class="note">` 列出參考資料。
6. 個案分享（糖尿病阿姨、50 歲膝痛患者）為醫師本人公開分享，文中加註「個案經驗，不代表可預期結果」。

**未收錄**：純賽事動態、活動宣傳、生活分享、追蹤數里程碑、NBA 賽況評論（僅取其中的醫學說明部分）、與醫療無關的時事評論。

## 照片 → `src/assets/`（`scripts/import-assets.mjs`）

| 網站檔名 | 原始檔 | 用途 |
|---|---|---|
| doctor-portrait-studio.jpg | facebook/images/profile.jpg | 首頁 Hero、預設 OG |
| doctor-portrait-formal.jpg | hospital_profiles/panshin_chenghao_photo.jpg | 關於頁主圖、作者卡 |
| event-2023-nig-tennis.jpg | facebook/images/161022503600970.jpg | 首頁關於區、關於頁相簿 |
| event-2026-nig-gymnastics.jpg | facebook/images/932585863111293-1_… | 關於頁相簿 |
| lecture-coaches-stage.jpg | facebook/images/683411734695375.jpg | 關於頁相簿 |
| lecture-xinyi-sports-center.jpg | facebook/images/364005309969354.jpg | 關於頁相簿 |
| teaching-nthu-selfie.jpg | facebook/images/883995274637019.jpg | 關於頁相簿 |
| rakuten-stadium-selfie.jpg | facebook/images/641204692249413.jpg | 關於頁相簿 |
| wbc-2023-medical-station.jpg | website_blog/images/2023-04-20-01.jpg | 關於頁相簿 |
| wbc-2023-stadium.jpg | website_blog/images/2023-04-20-02.jpg | 文章封面（場邊醫師） |
| teaching-resident-clinic.jpg | threads/images/DYPELE-k3sJ-1.jpg | 關於頁相簿 |
| clinic-sketch-knee.jpg | facebook/images/460528130317071.jpg | 文章封面（膝痛診斷） |
| nig-2023-gymnastics-venue-1.jpg | website_blog/images/2023-05-18-01.jpg | 文章封面（體操傷害） |

已匯入但目前未用（保留供日後文章）：clinic-sketch-hip、atls-abcde-card、gymnastics-injury-card、diet-education-1~4、rakuten-monkeys-sign、event-2023-nig-booth、lecture-coaches-screen、conference-pain-2025/2026。

**刻意不用**：NBA 球員照片與新聞截圖（第三方版權）、Threads 手機截圖、IG 低解析縮圖、家庭／旅遊照片。無合適照片的文章以 `CategoryCover` 幾何封面呈現（未來可由 `src/assets/generated/articles/` 的生成圖取代）。

## 外部 AI 製作的素材（design-v1.1.0 納入）

| 素材 | 來源 | 放置位置 | 說明 |
|---|---|---|---|
| 33 張 SVG（圖示、插畫、裝飾） | 分支 `assets/visual-kit-gpt25-briefs`（已合併） | `website/public/visual-kit/` | 程式繪製、無外部資源；`manifest.json` 含 sha256 |
| 65 份 GPT Image 提示詞 | 同上 | `website/design/image-production/` | 尚未生成任何圖片；放置對應表 `PLACEMENT.md`／`placement.json` |
| 6 張醫學解說圖 SVG | `main` 上另一 AI 的 commit（原放於 `website_blog/medical_3d_assets/`） | `website/public/medical/`（已 git mv） | 依部落格文章製作；已嵌入對應文章 |

原始爬蟲資料夾（`website_blog/` 等）已恢復為僅含爬蟲資料。
