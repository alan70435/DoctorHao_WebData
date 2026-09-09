# 06｜文章醫學圖解與 3D 素材

本次範圍是網站 `src/content/articles/` 的 **52 篇文章**，不是把原始社群庫的每一則回覆、活動紀錄都當成醫學文章。原始 Markdown、既有照片與社群資料保持不變。

## 交付內容

- 每篇 6 個靜態檔：1600×900 封面 WebP、800×450 與 480×270 響應式版本、1600×1120 SVG 解說圖卡與 WebP 版本、1200×630 JPG 分享圖，共 **312 個逐篇圖片檔**。
- **47 組 GLB 3D 模型**及各自的 WebP 預覽。部分文章共用相同結構模型，但解說、注意事項、來源與分享圖逐篇對應。
- 1 支膝屈曲 MP4，附繁體中文 VTT；GLB 也有同一剛性鉸鏈動畫。
- 全部素材集中於 `public/medical-visuals/`。`manifest.json` 記錄文章、來源、檔案位置、模型部件與 SHA-256；`src/data/medical-visuals.json` 供 Astro 使用。
- `/medical-visuals/` 提供可搜尋的逐篇素材索引與膝屈曲示範。

`models/` 包含膝 ACL／MCL／半月板／髕腱／鵝掌部位／退化概念、肩袖與關節囊、阿基里斯腱、足底筋膜、腿後肌、小腿肌、肘部尺神經、上肢肌腱、腕部負荷、肌纖維、腦震盪概念、靜脈瓣與血栓，以及運動、營養、體重管理等概念模型。模型名稱不是診斷結果。

## 重要：仍是待審示意素材

**所有素材均標為 `clinician-review-pending`，不是醫師已審定的教科書圖譜。**

圖像與模型採原創參數化幾何；未使用參考影片像素、病人掃描、原始照片或第三方解剖模型。骨骼、肌腱、神經、關節囊等均有簡化、放大或局部省略，不能用來量測、辨識個人病灶、設計手術／注射路徑或提供復健角度處方。橙色表示閱讀焦點，不表示撕裂分級、急性發炎程度或治療效果。

膝屈曲為 **0–72° 單一剛性鉸鏈**，不是生物力學模擬。模型省略韌帶與髕骨動態，不宣稱呈現真實滾滑、髕骨軌跡或正常活動度。動畫角度由程式設定，不是量測資料。

臨床重點由 `catalog.py` 逐篇編寫，並保留 AAOS、CDC、WHO、NIH／NIDDK／NHLBI／ODS、FDA 和 Amsterdam concussion consensus 等參考資料。這些機構是概念核對來源，**不是圖像作者，也不表示它們認證了素材**。完整 URL 及核對日期在 manifest 中。醫師審稿項目見 `07-medical-visual-review.md`。

## 網站整合

`ArticleCard.astro` 和 `ArticleLayout.astro` 只在文章原本沒有 `data.cover` 時，採用新增的 3D 封面；既有照片不被替換。分享圖也遵循相同原則。新文章若沒有素材對應，會保留既有 `CategoryCover`，不自動猜測疾病圖像。

`MedicalVisual.astro` 提供可閱讀的 HTML 三點解說、注意事項、靜態圖、3D 模型和下載連結。手機不需要放大整張文字圖片才能閱讀。3D 模組透過 `@google/model-viewer` 在按下按鈕後才動態載入；模型由本站提供，沒有執行時外部 CDN、追蹤服務或 AI API 需求。

互動支援拖曳、按鈕旋轉、縮放及重設；動畫不自動播放。滑出畫面、頁籤隱藏、減少動態效果設定改變時會暫停。載入失敗或關閉 JavaScript 都保留靜態圖。GLB 亦可在支援 glTF 2.0 的軟體中開啟與再編輯。

## 重建與品質檢查

需要 Python 3.11、ffmpeg、Noto CJK 字型，以及專案要求的 Node.js 版本。**字型僅在建置時用於點陣化，不隨素材分享或提交。**

```sh
cd website
python -m pip install -r scripts/medical-visuals/requirements.txt
python scripts/medical-visuals/build.py
python scripts/medical-visuals/validate.py
npm ci
npm run check
npm run build
```

Linux 的字型與 ffmpeg 可由 `sudo apt-get install fonts-noto-cjk ffmpeg` 安裝。`--quick` 僅供本機試作，會略過影片；正式驗證要求影片存在。`build.py` 不連網、不呼叫付費服務。

`.github/workflows/medical-visuals.yml` 執行完整重建、SHA／尺寸／SVG／GLB 結構檢查、Khronos glTF Validator、Astro check/build，以及 Chromium／軟體 WebGL 的手機與桌面檢查。通過後才由 bot 提交指定的素材與整合檔，不修改原始文章、來源照片，也不強制推送。建置報告不等於醫療審閱。

來源碼在 `scripts/medical-visuals/`，可修改 `catalog.py` 的逐篇 brief 與 `geometry.py` 的幾何。新增或移除文章會使覆蓋率檢查失敗，必須先補上對應素材規劃，避免悄悄漏圖。

## 授權與來源界線

本次沒有匯入第三方照片、掃描或模型，也沒有重新散布參考影片。新增的程式與圖解為本專案製作；本提交不替整個專案另行指定新授權，原有文章與照片的權利資訊維持原樣。檢視器是 Apache-2.0 的 `@google/model-viewer` 相依套件，其授權依套件原檔。參考機構名稱和文章連結僅用於來源說明，不暗示合作或背書。
