# 超音波六部位：立體解剖＋探頭位置

AI 輔助製作的概念性教學素材，尚待程皓醫師審閱；不是患者影像、標準化完整檢查流程或操作認證。

本系列提供 6 張 1800×1200 圖卡（SVG / PNG / WebP）、12 個 GLB 模型變體（6 部位 × 長短軸）及 12 張延遲載入海報。GLB 是可旋轉的真實三維網格；SVG 的文字可編輯，三維場景以內嵌 PNG 保存。

**範圍界線：**六部位都有素材，但每部位只建模一個代表性視窗。另列 24 項區域閱讀路線，並未建模全部診斷視窗或完整人體。

[開啟靜態圖庫](index.html) · 網站建置後的互動路徑：`/ultrasound-atlas/` · [索引與雜湊](manifest.json)

| 部位 | 核心視窗 | 圖卡 | GLB |
|---|---|---|---|
| 肩關節 | 肱二頭肌長頭肌腱・結節間溝 | [PNG](shoulder-anatomy-probe.png) / [SVG](shoulder-anatomy-probe.svg) / [WebP](shoulder-anatomy-probe.webp) | [長軸](shoulder-long.glb) / [短軸](shoulder-short.glb) |
| 肘關節 | 外上髁・共同伸肌腱 | [PNG](elbow-anatomy-probe.png) / [SVG](elbow-anatomy-probe.svg) / [WebP](elbow-anatomy-probe.webp) | [長軸](elbow-long.glb) / [短軸](elbow-short.glb) |
| 腕關節 | 近端腕隧道・正中神經 | [PNG](wrist-anatomy-probe.png) / [SVG](wrist-anatomy-probe.svg) / [WebP](wrist-anatomy-probe.webp) | [長軸](wrist-long.glb) / [短軸](wrist-short.glb) |
| 髖關節 | 前方關節隱窩・股骨頭頸 | [PNG](hip-anatomy-probe.png) / [SVG](hip-anatomy-probe.svg) / [WebP](hip-anatomy-probe.webp) | [長軸](hip-long.glb) / [短軸](hip-short.glb) |
| 膝關節 | 髕骨下極・髕腱・脛骨粗隆 | [PNG](knee-anatomy-probe.png) / [SVG](knee-anatomy-probe.svg) / [WebP](knee-anatomy-probe.webp) | [長軸](knee-long.glb) / [短軸](knee-short.glb) |
| 踝關節 | 阿基里斯腱・跟骨附著處 | [PNG](ankle-anatomy-probe.png) / [SVG](ankle-anatomy-probe.svg) / [WebP](ankle-anatomy-probe.webp) | [長軸](ankle-long.glb) / [短軸](ankle-short.glb) |

## 醫學與技術界線

幾何形狀、組織厚度與比例均經簡化；局部皮膚接觸片僅用於解釋探頭接觸與切面。青色平面不是積液、不是診斷圖像，也不模擬聲束衰減、折射或回音。暖色不是疾病分級。模型不含針具、穿刺路徑或治療劑量。

腕隧道模型包含 4 條 FDS、4 條 FDP、1 條 FPL 與正中神經；支持帶透明化是為了可讀性。沒有把尺神經、尺動脈或橈側屈腕肌腱放入腕隧道。髖模型是成人前方視窗。膝模型未移開髕骨，不以此評估完整十字韌帶或半月板。

方向標記是本系列的約定，不宣稱所有設備或科室均相同。GLB 採 Y-up；單位為任意設計單位，不可量測。模型的機器檢查通過不代表臨床內容通過審查。

## 來源與權利

圖像由專案中的原創參數化幾何生成，不複製學會 PDF 圖片、醫療影像、影片截圖或第三方模型，也不包含個資。引用參考文件不表示學會或程皓醫師背書。沒有另外替既有專案或第三方資料變更授權。

- [AIUM 2023 Practice Parameter](https://doi.org/10.1002/jum.16228)：一般掃描與多切面原則。
- [ESSR 肩關節](https://essr.org/content-essr/uploads/2016/10/shoulder.pdf)：PDF pp. 2–8；主視窗 p. 2。
- [ESSR 肘關節](https://essr.org/content-essr/uploads/2016/10/elbow.pdf)：PDF pp. 2–7；主視窗 p. 4。
- [ESSR 腕關節](https://essr.org/content-essr/uploads/2016/10/wrist.pdf)：PDF pp. 2–7；主視窗 pp. 6–7。
- [ESSR 髖關節](https://essr.org/content-essr/uploads/2016/10/hip.pdf)：PDF pp. 2–7；主視窗 pp. 2–3。
- [ESSR 膝關節](https://essr.org/content-essr/uploads/2016/10/knee.pdf)：PDF pp. 2–8；主視窗 pp. 2, 4。
- [ESSR 踝關節](https://essr.org/content-essr/uploads/2016/10/ankle.pdf)：PDF pp. 2–9；主視窗 p. 8。

## 重建

從版本庫根目錄執行：

```sh
python -m pip install -r website/scripts/ultrasound-atlas/requirements.txt
python website/scripts/ultrasound-atlas/build.py
python website/scripts/ultrasound-atlas/validate.py
cd website && npm ci && npm run build
```

可用 `--only shoulder --no-integrate` 重建單一部位，供繪圖測試；發布時必須不帶 `--only` 重建全系列及索引。CI 只提交本系列的白名單路徑，保留其他醫學素材、文章與原始 HTML。推送 GitHub 不等於已發布至外部 Blogger 網站。

生成工具：Python、NumPy、VTK、trimesh、CairoSVG、Pillow。不同字型與圖形驅動環境的光柵輸出可能不同；manifest 中的 SHA-256 對應該次實際生成檔。沒有打包字型檔。
