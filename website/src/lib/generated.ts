/**
 * 自動偵測 src/assets/generated/ 內的生成圖片（GPT Image 產出後直接放入即生效，無需改程式）。
 *
 * 目錄與命名（見 design/image-production/PLACEMENT.md）：
 *   generated/articles/{article-slug}.webp        文章封面 1600×900
 *   generated/treatments/{treatment-slug}.webp    治療頁主圖 1200×900
 *   generated/categories/{category-id}.webp       分類橫幅 1800×600
 *   generated/decor/{decor-id}.webp               首頁裝飾背景
 *
 * 支援 .webp / .png / .jpg / .jpeg / .avif；同名多格式時取第一個匹配。
 */
import type { ImageMetadata } from 'astro';
import { getImage } from 'astro:assets';
import { decorSvg, type DecorId } from '@/data/visualKit';

type Globbed = Record<string, ImageMetadata>;

const articleFiles = import.meta.glob<ImageMetadata>('/src/assets/generated/articles/*.{webp,png,jpg,jpeg,avif}', {
  eager: true,
  import: 'default',
});
const treatmentFiles = import.meta.glob<ImageMetadata>('/src/assets/generated/treatments/*.{webp,png,jpg,jpeg,avif}', {
  eager: true,
  import: 'default',
});
const categoryFiles = import.meta.glob<ImageMetadata>('/src/assets/generated/categories/*.{webp,png,jpg,jpeg,avif}', {
  eager: true,
  import: 'default',
});
const decorFiles = import.meta.glob<ImageMetadata>('/src/assets/generated/decor/*.{webp,png,jpg,jpeg,avif}', {
  eager: true,
  import: 'default',
});

function byBasename(files: Globbed): Map<string, ImageMetadata> {
  const map = new Map<string, ImageMetadata>();
  for (const [path, img] of Object.entries(files)) {
    const base = path.split('/').pop()!.replace(/\.(webp|png|jpe?g|avif)$/i, '');
    if (!map.has(base)) map.set(base, img);
  }
  return map;
}

const articleCovers = byBasename(articleFiles);
const treatmentImages = byBasename(treatmentFiles);
const categoryBanners = byBasename(categoryFiles);
const decorImages = byBasename(decorFiles);

export function generatedArticleCover(slug: string): ImageMetadata | undefined {
  return articleCovers.get(slug);
}
export function generatedTreatmentImage(slug: string): ImageMetadata | undefined {
  return treatmentImages.get(slug);
}
export function generatedCategoryBanner(categoryId: string): ImageMetadata | undefined {
  return categoryBanners.get(categoryId);
}

/** decor brief id（spec: home-hero-desktop 等）→ 內部 DecorId */
const decorBriefToId: Record<string, DecorId> = {
  'home-hero-desktop': 'heroDesktop',
  'home-hero-mobile': 'heroMobile',
  'home-portrait-surround': 'portraitHalo',
  'home-section-divider': 'sectionWave',
  'home-clinic-backdrop': 'clinicPanel',
  'home-footer-backdrop': 'footerFlow',
};
const decorIdToBrief = Object.fromEntries(Object.entries(decorBriefToId).map(([k, v]) => [v, k])) as Record<DecorId, string>;

/**
 * 取得裝飾背景的 URL：有生成圖則回傳最佳化後的 URL，否則回傳 SVG 備援。
 */
export async function decorBackground(id: DecorId, width = 1920): Promise<string> {
  const brief = decorIdToBrief[id];
  const img = brief ? decorImages.get(brief) : undefined;
  if (img) {
    const out = await getImage({ src: img, width: Math.min(width, img.width), format: 'webp', quality: 80 });
    return out.src;
  }
  return decorSvg[id];
}

/** 提供管理文件／檢查用：目前偵測到的生成圖清單 */
export const generatedInventory = {
  articles: [...articleCovers.keys()],
  treatments: [...treatmentImages.keys()],
  categories: [...categoryBanners.keys()],
  decor: [...decorImages.keys()],
};

// 建置時輸出偵測結果，方便確認生成圖是否被讀到
console.log(
  `[generated] 文章封面 ${generatedInventory.articles.length}、治療主圖 ${generatedInventory.treatments.length}、分類橫幅 ${generatedInventory.categories.length}、裝飾背景 ${generatedInventory.decor.length}`,
);
