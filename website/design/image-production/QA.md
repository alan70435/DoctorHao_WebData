# 檢查紀錄

## 已完成的檢查

- 33 / 33 SVG：XML 可解析、固定 viewBox 與寬高、title/desc、manifest 雜湊吻合。
- 33 / 33 SVG：無 script、foreignObject、嵌入點陣圖、外部引用或事件處理器。
- 33 / 33 SVG：使用 CairoSVG 實際渲染為 PNG；已檢視圖示與分類插畫合成預覽。
- 52 篇文章配圖規格 ID 不重複；分類為 27 篇運動傷害、13 篇體重管理、12 篇運動訓練，與既有盤點數量一致。
- 13 份其他圖片規格，加總 65 份；實際 GPT 圖片產出仍為 0。
- 提示詞匯出器成功輸出 65 個文字檔；拒絕覆寫已有內容的目錄。
- 靜態預覽 HTML 的 34 個圖片引用、所有檔案連結及頁內錨點均能解析；圖片具 alt 與尺寸；無 JavaScript、追蹤碼或外部資源。

## 未完成／不能宣稱通過的項目

- GPT Image 2.5 生成：本對話未提供可呼叫工具，沒有任何圖片生成 API 請求。
- 完整 Astro production build：未執行。容器無法解析 GitHub 主機，無法 clone 完整專案；檔案透過 GitHub 連接工具讀取及提交。
- 真實瀏覽器桌機／手機檢查：Playwright 預設瀏覽器檔案不存在；使用系統 Chromium 後，file:// 與本機 HTTP 預覽均被環境政策拒絕（ERR_BLOCKED_BY_ADMINISTRATOR），因此沒有完成瀏覽器截圖、互動、水平溢出或實際手機版測試。
- 本機完整來源檔案覆蓋比對：隔離素材包不包含原始文章，因此 validator 跳過此項；在完整 repo 執行時會檢查 52 個檔案路徑是否完全吻合。
- 逐篇完整原文審閱：僅 spec.json 明列的兩篇已讀全文；其餘配圖規格主要依據檔名與編輯盤點，生成前須完整閱讀原文。
- 醫療／解剖正確性與 BMA 服務資格確認：尚需醫師審查；SVG 是導航與主題插畫，不是臨床圖譜。
- 正式網站接圖、合併 main 與部署：不在此次新增素材變更中。

## 可重現的檢查

```sh
python3 website/design/image-production/validate-kit.py
python3 website/design/image-production/export-prompts.py --output /tmp/doctorhao-new-prompts
```

`validate-kit.py` 僅使用 Python 標準函式庫，不會發送網路請求或呼叫模型。
