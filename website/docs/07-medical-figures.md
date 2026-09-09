# 07｜醫學解說圖（public/medical/）

6 張由另一個 AI 依部落格文章內容製作的 SVG 醫學衛教示意圖，原先放在原始資料夾 `website_blog/medical_3d_assets/`，
已於 design-v1.1.0 移入網站專案 `website/public/medical/`（git mv，歷史可追溯），原始資料夾恢復為純爬蟲資料。

> 定位：醫學教育與衛教示意，不取代診斷影像、臨床評估或個別醫療建議。圖為深色資訊圖表風格，內含中文說明文字；在文章中以 `<figure>` 呈現並附圖說。

## 素材與文章對應（已嵌入）

| 檔案 | 文章（slug） | 插入位置 |
|---|---|---|
| `knee-acl-hyperextension-3d.svg` | `acl-tear-return-to-play` | 「膝關節過度伸直／膝外翻外轉」段落之後 |
| `landing-mechanics-3d.svg` | `acl-tear-return-to-play` | 「直膝單腳落地為什麼危險」段落之後 |
| `sideline-abcde-3d.svg` | `sideline-doctor-abcde` | ABCDE 清單之後 |
| `msk-ultrasound-guidance-3d.svg` | `msk-ultrasound-self-study` | 前言引言之後 |
| `gymnast-wrist-growth-plate-3d.svg` | `gymnastics-injuries` | 「上肢的特殊負荷」段落之後 |
| `sport-concussion-pathway-3d.svg` | `sport-related-concussion` | 「11 個 R」段落之後 |

所有 alt 文字描述圖中內容（含 ABCDE／R 流程），定義集中於 `src/data/visualKit.ts` 的 `medicalFigures`（文章中直接使用相同文字）。

## 使用方式（Markdown）

```html
<figure class="figure">
  <img src="/medical/knee-acl-hyperextension-3d.svg" alt="…描述圖中內容…" width="1600" height="1000" loading="lazy" />
  <figcaption>圖說（概念示意圖，非診斷影像）。</figcaption>
</figure>
```

## 設計原則（原作者）

- 1600×1000，適合文章主視覺與社群裁切。
- 深色醫療視覺、立體漸層、重點色標示；中文主標＋必要英文醫學名詞。
- 圖內避免宣稱單一機轉必然導致特定傷害；侵入性操作與腦震盪素材加入安全提示。

## 待醫師審閱

- 圖中的解剖位置與文字主張（尤其超音波導引、腦震盪回場原則）需由程皓醫師確認。
- 風格較網站主體為深色；若希望一致，可請原作者輸出淺色版本或改以 GPT 生成圖取代（放置區見 `src/assets/generated/README.md`）。
