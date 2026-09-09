# 02｜Sitemap、頁面架構與 Design Direction

## Sitemap

```
/                         首頁
/about/                   關於程皓醫師
/prolotherapy/            葡萄糖增生修復治療
/prp/                     PRP 再生修復治療
/bma/                     BMA 骨髓再生修復治療
/weight-management/       醫療體重管理（瘦瘦針相關）
/articles/                程皓醫師專欄（總覽）
/articles/sports-injury/  運動傷害及疼痛
/articles/weight-management/  體重控制及減重
/articles/training/       運動訓練
/articles/[slug]/         單篇文章
/topics/[topic]/          從問題開始找（肩膀、膝蓋、腰背、足踝、肌腱、運動傷害、體重、訓練）
/clinic/                  門診時間及預約
/404
/sitemap-index.xml, /robots.txt
```

## 主選單（桌機）
程皓醫師 LOGO｜關於程醫師｜葡萄糖增生｜PRP｜BMA｜體重管理｜程皓醫師專欄 ▾｜**門診時間及預約**（primary CTA）｜Facebook（icon，次要）

## 手機選單（hamburger）
關於程皓醫師 → 主要治療（4）→ 程皓醫師專欄（3）→ 門診時間及預約 → Facebook 粉絲專頁；底部固定「查看門診」列。

## 頁面模板
- `BaseLayout`：`<head>` SEO（title/description/canonical/OG/JSON-LD）、Header、Footer、skip link、mobile CTA bar。
- `TreatmentLayout`：11 段固定結構（是什麼→原理→可能應用→誰需要評估→流程→治療前→治療後→風險限制→FAQ→相關文章→門診資訊）。
- `ArticleLayout`：H1、前言、目錄/重點整理、內文、FAQ（選用）、來源、作者卡、相關文章。

## Design Direction

**關鍵字**：可信賴、親切、懂運動、乾淨、留白、非制式。

### 色彩
| Token | 值 | 用途 |
|---|---|---|
| `--c-brand-900` | `#0B3F4C` | 深色標題/Footer |
| `--c-brand-700` | `#0F5C6E` | 主品牌色（CTA、連結、重點） |
| `--c-brand-500` | `#1F8A96` | hover、圖示 |
| `--c-brand-100` | `#DCEEF1` | 淺底、chip |
| `--c-brand-50`  | `#F1F8F9` | 區塊底色 |
| `--c-warm-600`  | `#C9651F` | 溫暖輔助色（文字級） |
| `--c-warm-500`  | `#E0862E` | 輔助強調（少量） |
| `--c-warm-100`  | `#FBEFE3` | 輔助淺底 |
| `--c-ink`       | `#1B2430` | 主要文字 |
| `--c-text`      | `#2B3440` | 內文 |
| `--c-muted`     | `#5B6672` | 次要文字（對比 ≥ 4.5:1） |
| `--c-line`      | `#E3E8EC` | 分隔線 |
| `--c-surface`   | `#F7F9FA` | 淺灰面 |

分類色：運動傷害及疼痛＝brand teal；體重控制及減重＝warm amber；運動訓練＝green `#2F7D5B`。

### 字體
Noto Sans TC（自架，variable）＋ 系統字（PingFang TC、Microsoft JhengHei）。
- 內文 17px / 行高 1.85 / 文章欄寬 ≤ 44em（約 720px）
- 標題：600–700 weight、字距 -0.01em
- 數字與英文使用同字族，避免混排落差

### 間距／形狀
4px 基準；容器 1200px；卡片圓角 14px；按鈕圓角 10px；chip 為 pill。陰影僅一層、低飽和。動畫僅 hover/focus 過渡 150ms。

### 元件
Button（primary/secondary/ghost）、Card（治療卡、文章卡、院所卡）、Chip、Section header（eyebrow + title + lede）、Callout（提醒/注意）、FAQ（`<details>`）、Breadcrumb、Author card、Clinic table。

### 圖片
只用醫師本人真實照片；文章無合適照片時使用「分類視覺封面」（純 CSS/SVG 圖形＋標題），不使用第三方球員照或 stock photo。
