# 程皓醫師網站｜視覺素材與 GPT Image 2.5 製作規格

## 本次真正完成的範圍

**33 張已建立的 SVG；65 份圖片製作規格；GPT Image 圖片產出 0 張。**

這個工作階段沒有可呼叫的 GPT Image 2.5 生圖工具，也沒有呼叫圖片 API、建立 API key 或使用其他模型冒充指定模型。SVG 是獨立的程式繪製素材，不是 GPT Image 輸出。此變更不代表使用者要求的 GPT 生圖已完成。

所有新增檔案位於兩個獨立目錄：

- `website/public/visual-kit/`：33 張 SVG、`manifest.json`、預覽頁。
- `website/design/image-production/`：配圖規格、製作清單、提示詞匯出器、驗證程式與檢查紀錄。

**沒有修改原始爬蟲資料、醫師照片、文章 Markdown、首頁、路由或既有封面，也沒有將任何新圖自動接到正式頁面。**

## SVG 清單

| 類型 | 數量 | 用途 |
|---|---:|---|
| `ui/` | 12 | 門診、時間、地點、電話、詢問、箭頭、外連、展開、書本、搜尋、選單、關閉 |
| `topics/` | 8 | 肩、膝、背、足踝、肌肉肌腱、運動傷害、體重、訓練 |
| `treatments/` | 4 | 葡萄糖增生、PRP、BMA 資訊、醫療體重管理 |
| `categories/` | 3 | 運動傷害、體重管理、運動訓練插畫 |
| `decor/` | 6 | 桌機、手機、肖像外框、分隔線、門診、頁尾背景 |

色彩沿用現有 `website/docs/03-design-system.md`。圖內不烘焙標題與按鈕文字、不使用外部資源或字型檔。

## 預覽

在專案根目錄執行：

```sh
python3 -m http.server 8765 --directory website/public
```

開啟 `http://localhost:8765/visual-kit/`。也可直接以瀏覽器開啟 `website/public/visual-kit/index.html`。預覽頁是靜態 HTML，不需要額外 JavaScript、API 或追蹤碼。

## 與現有網站接合

圖示建議使用 `<img src="/visual-kit/ui/calendar.svg" alt="" width="20" height="20">`，搭配可見的「門診時間及預約」文字。純裝飾背景使用 `alt=""` 或 CSS 背景。圖示不是可點擊區本身，互動仍由有文字名稱的 `<a>` 或 `<button>` 負責。

SVG 使用獨立 `<img>` 資源；若改成內嵌 SVG，須重寫 `title` / `desc` 的 ID，避免同頁重複。分類圖是主題插畫，不是臨床示意圖或診療紀錄。

網站 `ArticleCard.astro` 一般卡片使用 16:9，compact 使用方形。本次文章圖片規格因此採 1600 × 900 交付目標，主體置於中央裁切安全區。這是交付尺寸規劃，不是已驗證的 API 請求參數。

## GPT 配圖待辦

見 [QUEUE.md](QUEUE.md) 與 [spec.json](spec.json)。`articles-01.json` 和 `articles-02.json` 包含 52 篇文章規格；`supplemental.json` 包含另外 13 份規格。

文章規格的主題標籤不是原文標題。除 `spec.json` 明列的兩篇之外，尚未逐篇完整閱讀文章；主要依專案的文章檔名與編輯盤點整理，**生圖前必須讀完對應原文並修訂規格**。

```sh
python3 website/design/image-production/export-prompts.py --output /tmp/doctorhao-image-prompts
```

這只輸出 65 份提示詞文字檔，**不會呼叫模型，也不會產生圖片**。指定的模型家族是 GPT Image 2.5；偏好模型 ID 依 OpenAI 官方文件設定為 `gpt-image-2.5-sunburst`。實際執行時仍需確認可用工具與模型，不可把模型名稱寫入 metadata 就視為已生成。

## 上線前審查

BMA：`website/docs/01-content-inventory.md` 記錄的是參加工作坊，並註明尚無本人臨床施作陳述。圖示僅表示資訊主題，不證明程醫師提供該服務。確認實際技術、服務與可公開文案後再使用，不能用圖片消除這項不確定性。

保留現有真實醫師肖像，不生成假醫師或患者；不生成假超音波、X 光或病歷；不畫治療前後改善對照、組織再生保證、藥品品牌包裝或注射教學。解剖位置、診療意涵與文字主張需由醫師審閱。

## 驗證

```sh
python3 website/design/image-production/validate-kit.py
```

詳見 [QA.md](QA.md)。此次僅新增素材與文件；未執行完整 Astro production build，不能視為全站已測試或已部署。

## 來源

盤點基準 commit：`44ec3cca8a22ea31a3df7074602be6994c10e5bb`。

- `website/docs/01-content-inventory.md`
- `website/docs/03-design-system.md`
- `website/docs/04-data-usage.md`
- `website/src/pages/index.astro`
- `website/src/components/ArticleCard.astro`
- `website/src/content/articles/` 的 52 個檔案路徑
- OpenAI 模型文件：https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst
