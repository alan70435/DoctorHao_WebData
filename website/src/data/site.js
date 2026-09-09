// 網站層級設定（JS 檔以便 astro.config.mjs 直接 import）
// TODO：正式網域尚未確認。上線前請將 SITE_URL 改為實際網址（影響 canonical / sitemap / Open Graph）。
export const SITE_URL = process.env.SITE_URL || 'https://www.drchenghao.tw';
export const SITE_NAME = '程皓醫師｜運動醫學・疼痛治療・體重管理';
export const SITE_SHORT_NAME = '程皓醫師';
export const DEFAULT_DESCRIPTION =
  '程皓醫師，聯新國際醫院運動醫學科醫師、樂天桃猿棒球隊醫療團隊醫師。專注運動傷害、疼痛治療、增生注射（葡萄糖、PRP）、醫療體重管理與運動訓練。門診資訊、治療說明與衛教專欄。';
export const LOCALE = 'zh_TW';

/**
 * 網站「外觀版本」（Design version）。規則見 docs/06-design-versions.md。
 * MAJOR：版面／風格重大改版；MINOR：視覺素材或區塊調整；PATCH：微調。
 * 每次變更外觀請同步更新此值、CHANGELOG.md，並建立 git tag `design-vX.Y.Z`。
 */
export const DESIGN_VERSION = '1.1.0';
