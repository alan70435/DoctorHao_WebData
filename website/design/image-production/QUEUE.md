# GPT Image 2.5｜配圖製作清單

**狀態：65 份規格已依提示詞生成（xAI Imagine）。** 64 張已放入 `src/assets/generated/` 並自動啟用；BMA 放在 `treatments/_hold/`，服務確認前不上線。詳見 `GENERATION.md`。

目前網站 52 篇文章各有一份封面規格，另有 4 份治療圖、3 份專欄分類圖、6 份首頁裝飾圖。
文章題目欄為主題標籤，不宣稱是原文標題。多數規格取自檔名與既有編輯盤點；執行前仍須讀完逐篇原文。

共用風格、英文場景提示詞與排除條件、來源和裁切尺寸，見 [`spec.json`](spec.json)、`articles-01.json`、`articles-02.json`、`supplemental.json`。使用 `export-prompts.py` 可合成完整提示詞；它不會生成圖片。

| 類型 | 主題 | 來源／對應頁 | 狀態 |
|---|---|---|---|
| article-cover | 阿基里斯腱傷後重返運動 | `website/src/content/articles/achilles-rupture-return.md` | 已生成 |
| article-cover | 前十字韌帶與重返運動 | `website/src/content/articles/acl-tear-return-to-play.md` | 已生成 |
| article-cover | 飲酒與體重管理 | `website/src/content/articles/alcohol-and-weight-loss.md` | 已生成 |
| article-cover | 運動者與血栓議題 | `website/src/content/articles/athletes-and-blood-clots.md` | 已生成 |
| article-cover | 羽球與身體負荷 | `website/src/content/articles/badminton-is-not-leisure.md` | 已生成 |
| article-cover | 籃球傷害與訓練準備 | `website/src/content/articles/basketball-injury-prevention.md` | 已生成 |
| article-cover | 小腿肌拉傷 | `website/src/content/articles/calf-muscle-tear.md` | 已生成 |
| article-cover | 硬舉訓練入門 | `website/src/content/articles/deadlift-everyone-should-learn.md` | 已生成 |
| article-cover | 糖尿病與生活管理 | `website/src/content/articles/diabetes-aunt-three-things.md` | 已生成 |
| article-cover | 慢跑與膝部健康 | `website/src/content/articles/does-jogging-hurt-knees.md` | 已生成 |
| article-cover | 運動後的飲食安排 | `website/src/content/articles/eating-for-training.md` | 已生成 |
| article-cover | 魚油與維生素 D | `website/src/content/articles/fish-oil-and-vitamin-d.md` | 已生成 |
| article-cover | 油炸食物與情緒議題 | `website/src/content/articles/fried-food-and-mood.md` | 已生成 |
| article-cover | 肩部活動受限 | `website/src/content/articles/frozen-shoulder-self-check.md` | 已生成 |
| article-cover | 體重管理治療期間 | `website/src/content/articles/glp1-during-treatment.md` | 已生成 |
| article-cover | 用藥前的評估與注意事項 | `website/src/content/articles/glp1-precautions-and-contraindications.md` | 已生成 |
| article-cover | 體重管理藥物的認識與評估 | `website/src/content/articles/glp1-what-it-is-and-who-fits.md` | 已生成 |
| article-cover | 臀肌訓練 | `website/src/content/articles/glute-training-best-exercises.md` | 已生成 |
| article-cover | 健身房常見訓練陷阱 | `website/src/content/articles/gym-trap-cards.md` | 已生成 |
| article-cover | 體操與運動傷害 | `website/src/content/articles/gymnastics-injuries.md` | 已生成 |
| article-cover | 腿後肌拉傷 | `website/src/content/articles/hamstring-strain-curry.md` | 已生成 |
| article-cover | 登山與身體準備 | `website/src/content/articles/hiking-is-strength-training.md` | 已生成 |
| article-cover | 每週運動安排 | `website/src/content/articles/how-much-exercise-per-week.md` | 已生成 |
| article-cover | 退化性膝關節的評估選項 | `website/src/content/articles/knee-oa-treatment-options.md` | 已生成 |
| article-cover | 膝痛先找原因 | `website/src/content/articles/knee-pain-diagnosis-first.md` | 已生成 |
| article-cover | 膝內側韌帶議題 | `website/src/content/articles/mcl-sprain-grades.md` | 已生成 |
| article-cover | 進食安排與食物選擇 | `website/src/content/articles/meal-order-veg-protein-carb.md` | 已生成 |
| article-cover | 半月板與膝部問題 | `website/src/content/articles/meniscus-tear-embiid.md` | 已生成 |
| article-cover | 肌肉骨骼超音波學習 | `website/src/content/articles/msk-ultrasound-self-study.md` | 已生成 |
| article-cover | 手麻與神經相關評估 | `website/src/content/articles/numbness-nerve-hydrodissection.md` | 已生成 |
| article-cover | 疼痛與用藥評估 | `website/src/content/articles/painkillers-headache-menstrual.md` | 已生成 |
| article-cover | 膝內側下方疼痛 | `website/src/content/articles/pes-anserine-bursitis.md` | 已生成 |
| article-cover | 匹克球與傷害風險 | `website/src/content/articles/pickleball-injury-risks.md` | 已生成 |
| article-cover | 晨起足跟疼痛 | `website/src/content/articles/plantar-fasciitis-morning-heel-pain.md` | 已生成 |
| article-cover | 快速減重藥袋的風險辨識 | `website/src/content/articles/quick-weight-loss-pill-bags.md` | 已生成 |
| article-cover | 家務與肩部不適 | `website/src/content/articles/rotator-cuff-housework.md` | 已生成 |
| article-cover | 跑者膝與髕骨帶 | `website/src/content/articles/runners-knee-and-patellar-strap.md` | 已生成 |
| article-cover | 跑者的肌力訓練 | `website/src/content/articles/runners-need-strength.md` | 已生成 |
| article-cover | 場邊醫療與評估 | `website/src/content/articles/sideline-doctor-abcde.md` | 已生成 |
| article-cover | 運動性腦震盪 | `website/src/content/articles/sport-related-concussion.md` | 已生成 |
| article-cover | 深蹲訓練要領 | `website/src/content/articles/squat-essentials.md` | 已生成 |
| article-cover | 減重與運動一起規劃 | `website/src/content/articles/start-exercise-with-weight-loss.md` | 已生成 |
| article-cover | 肌力訓練與長期照護 | `website/src/content/articles/strength-is-maintenance-and-treatment.md` | 已生成 |
| article-cover | 運動補充品的選擇 | `website/src/content/articles/supplements-overview-ranking.md` | 已生成 |
| article-cover | 保健食品與藥物的角色 | `website/src/content/articles/supplements-vs-medication-cholesterol.md` | 已生成 |
| article-cover | 肌肉疼痛與激痛點評估 | `website/src/content/articles/trigger-point-injection.md` | 已生成 |
| article-cover | 靜脈曲張與重量訓練 | `website/src/content/articles/varicose-veins-and-lifting.md` | 已生成 |
| article-cover | 體重與關節不適 | `website/src/content/articles/weight-and-joint-pain.md` | 已生成 |
| article-cover | 體重不只是數字 | `website/src/content/articles/weight-is-not-the-only-number.md` | 已生成 |
| article-cover | 減重不只靠意志力 | `website/src/content/articles/why-diet-and-exercise-alone-is-hard.md` | 已生成 |
| article-cover | 棒球與訓練方式 | `website/src/content/articles/yamamoto-no-weight-training.md` | 已生成 |
| article-cover | 教練與訓練規劃 | `website/src/content/articles/you-need-a-coach.md` | 已生成 |
| treatment-illustration | 葡萄糖增生治療 | `website/src/data/treatments.ts` | 已生成 |
| treatment-illustration | PRP 治療 | `website/src/data/treatments.ts` | 已生成 |
| treatment-illustration | BMA 骨髓相關資訊 | `website/src/data/treatments.ts` | 已生成（`treatments/_hold/`，服務確認前不上線） |
| treatment-illustration | 醫療體重管理 | `website/src/data/treatments.ts` | 已生成 |
| category-banner | 運動傷害及疼痛 | `website/docs/03-design-system.md` | 已生成 |
| category-banner | 體重控制及減重 | `website/docs/03-design-system.md` | 已生成 |
| category-banner | 運動訓練 | `website/docs/03-design-system.md` | 已生成 |
| homepage-decoration | 首頁桌機主視覺背景 | `website/src/pages/index.astro` | 已生成 |
| homepage-decoration | 首頁手機主視覺背景 | `website/src/pages/index.astro` | 已生成 |
| homepage-decoration | 真實醫師照片後方裝飾 | `website/src/pages/index.astro` | 已生成 |
| homepage-decoration | 段落分隔裝飾 | `website/src/pages/index.astro` | 已生成 |
| homepage-decoration | 門診資訊區背景 | `website/src/pages/index.astro` | 已生成 |
| homepage-decoration | 網站頁尾背景 | `website/src/pages/index.astro` | 已生成 |
