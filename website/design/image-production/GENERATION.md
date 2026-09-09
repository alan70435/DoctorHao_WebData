# 生成紀錄（2026-09-10）

規格來源：`spec.json`、`articles-01.json`、`articles-02.json`、`supplemental.json`。
實際模型：xAI Imagine（`grok-imagine-image`），不是規格中偏好的 GPT Image 2.5。
風格：先產一張象牙桌面／青綠靜物基準圖，文章封面由此衍生以維持色盤與光線一致。

## 產出

| 類型 | 張數 | 放置 |
|---|---:|---|
| 文章封面 | 52 | `src/assets/generated/articles/{slug}.webp`（1600×900） |
| 治療主圖 | 3 | `treatments/prolotherapy.webp`、`prp.webp`、`weight-management.webp`（1200×900） |
| 分類橫幅 | 3 | `categories/{id}.webp`（1800×600） |
| 首頁裝飾 | 6 | `decor/home-*.webp`（依 supplemental 目標尺寸） |
| BMA（暫不上線） | 1 | `treatments/_hold/bma.webp` |

共 65 張。64 張會被 `src/lib/generated.ts` 自動偵測。三篇已有真實照片封面的文章（`knee-pain-diagnosis-first`、`sideline-doctor-abcde`、`gymnastics-injuries`）仍以 frontmatter `cover` 為優先，生成圖待命。

## 例外

- `hamstring-strain-curry`：含「後側大腿輪廓」的提示詞被內容審核擋下。改為籃球、毛巾、評估筆記本與阻力帶的器材靜物，不畫身體部位。
- BMA：已生成資訊性靜物（密閉容器＋抽象骨骼剪影），依規格不自動上線。
- 未生成程皓醫師本人、可辨識患者、假超音波／X 光、療效對照或藥品品牌。

## 仍需醫師審閱

這些是編輯概念圖，不是臨床圖譜。上線前請抽查解剖意涵與文案是否一致（見 `docs/05-todo-for-owner.md`）。
