/**
 * 從原始素材資料夾複製並最佳化網站用照片。
 * - 原始檔案不會被修改。
 * - 輸出至 src/assets/photos（醫師照片）與 src/assets/articles（文章圖）。
 * - 最長邊縮至 MAX_EDGE，JPEG 品質 84；Astro 建置時再依需求產生 AVIF/WebP 與多尺寸。
 *
 * 執行：npm run import-assets
 */
import { mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

const SOURCE_ROOT = path.resolve(process.cwd(), '..');
const MAX_EDGE = 1600;

/** [來源相對路徑, 目的檔名, 說明] */
const PHOTOS = [
  ['facebook/images/profile.jpg', 'doctor-portrait-studio.jpg', '白袍攝影棚人像（Hero）'],
  ['hospital_profiles/panshin_chenghao_photo.jpg', 'doctor-portrait-formal.jpg', '院方正式肖像（About）'],
  ['facebook/images/161022503600970.jpg', 'event-2023-nig-tennis.jpg', '2023 全大運 網球場邊'],
  ['facebook/images/161022470267640.jpg', 'event-2023-nig-booth.jpg', '2023 全大運 聯新運醫醫護站'],
  ['facebook/images/932585863111293-1_932585636444649.jpg', 'event-2026-nig-gymnastics.jpg', '2026 全大運 競技體操'],
  ['facebook/images/683411734695375.jpg', 'lecture-coaches-stage.jpg', '百位教練前演講'],
  ['facebook/images/683411788028703.jpg', 'lecture-coaches-screen.jpg', '演講投影：運動醫學與科學'],
  ['facebook/images/364005309969354.jpg', 'lecture-xinyi-sports-center.jpg', '信義運動中心演講'],
  ['facebook/images/883995274637019.jpg', 'teaching-nthu-selfie.jpg', '清華大學授課'],
  ['facebook/images/641204692249413.jpg', 'rakuten-stadium-selfie.jpg', '樂天桃園棒球場出診'],
  ['facebook/images/394016256968259.jpg', 'rakuten-monkeys-sign.jpg', 'Rakuten Monkeys'],
  ['website_blog/images/2023-04-20-01.jpg', 'wbc-2023-medical-station.jpg', '2023 WBC 醫護站'],
  ['website_blog/images/2023-04-20-02.jpg', 'wbc-2023-stadium.jpg', '2023 WBC 球場'],
  ['threads/images/DYPELE-k3sJ-1.jpg', 'teaching-resident-clinic.jpg', '住院醫師跟診'],
  ['facebook/images/630257516677464.jpg', 'conference-pain-2025.jpg', '2025 疼痛醫學會年會'],
  ['facebook/images/921131584256721-4_921131527590060.jpg', 'conference-pain-2026.jpg', '2026 疼痛醫學會年會'],
];

const ARTICLE_IMAGES = [
  ['facebook/images/460528130317071.jpg', 'clinic-sketch-knee.jpg', '運動醫學診間手繪圖：膝關節'],
  ['facebook/images/461995630170321.jpg', 'clinic-sketch-hip.jpg', '運動醫學診間手繪圖：髖與腰'],
  ['website_blog/images/2023-05-18-01.jpg', 'nig-2023-gymnastics-venue-1.jpg', '2023 全大運 體操館'],
  ['website_blog/images/2023-05-18-02.jpg', 'nig-2023-gymnastics-venue-2.jpg', '2023 全大運 體操館 2'],
  ['website_blog/images/2023-05-10-01.jpg', 'gymnastics-injury-card.jpg', '體操相關運動傷害圖卡'],
  ['website_blog/images/2023-04-20-04.jpg', 'atls-abcde-card.jpg', '高級外傷救命術 ABCDE'],
  ['website_blog/images/2023-04-20-02.jpg', 'wbc-2023-stadium.jpg', '2023 WBC 球場'],
  ['facebook/images/804547845915096.jpg', 'diet-education-1.jpg', '減重飲食衛教圖卡 1'],
  ['facebook/images/804547955915085.jpg', 'diet-education-2.jpg', '減重飲食衛教圖卡 2'],
  ['facebook/images/804548079248406.jpg', 'diet-education-3.jpg', '減重飲食衛教圖卡 3'],
  ['facebook/images/804548112581736.jpg', 'diet-education-4.jpg', '減重飲食衛教圖卡 4'],
  ['facebook/images/641204692249413.jpg', 'rakuten-stadium-selfie.jpg', '樂天桃園棒球場出診'],
  ['facebook/images/161022503600970.jpg', 'event-2023-nig-tennis.jpg', '2023 全大運 網球場邊'],
  ['facebook/images/683411734695375.jpg', 'lecture-coaches-stage.jpg', '百位教練前演講'],
  ['threads/images/DYPELE-k3sJ-1.jpg', 'teaching-resident-clinic.jpg', '住院醫師跟診'],
];

async function importList(list, outDir) {
  await mkdir(outDir, { recursive: true });
  for (const [rel, name, desc] of list) {
    const src = path.join(SOURCE_ROOT, rel);
    const dest = path.join(outDir, name);
    if (!existsSync(src)) {
      console.warn(`  ✗ 找不到來源：${rel}`);
      continue;
    }
    const img = sharp(src, { failOn: 'none' }).rotate();
    const meta = await img.metadata();
    const longest = Math.max(meta.width ?? 0, meta.height ?? 0);
    const pipeline = longest > MAX_EDGE ? img.resize({ width: MAX_EDGE, height: MAX_EDGE, fit: 'inside', withoutEnlargement: true }) : img;
    await pipeline.jpeg({ quality: 84, mozjpeg: true, progressive: true }).toFile(dest);
    const out = await sharp(dest).metadata();
    console.log(`  ✓ ${name}  ${out.width}x${out.height}  ← ${rel}  （${desc}）`);
  }
}

console.log('→ 醫師照片');
await importList(PHOTOS, path.resolve('src/assets/photos'));
console.log('→ 文章圖片');
await importList(ARTICLE_IMAGES, path.resolve('src/assets/articles'));
console.log('完成。原始素材未變動。');
