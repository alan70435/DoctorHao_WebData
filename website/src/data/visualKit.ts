/**
 * 視覺素材對應表（SVG 素材包：public/visual-kit/，來源見 design/image-production/README.md）。
 * 這些 SVG 是「導航／主題插畫」與「裝飾背景」，不是臨床示意圖。
 * 當 src/assets/generated/ 中有對應的 GPT 生成圖時，lib/generated.ts 會優先使用生成圖並以此處的 SVG 為備援。
 */

const KIT = '/visual-kit';

/** 主題入口圖示（topics.ts 的 id → 檔名） */
const topicIconFile: Record<string, string> = {
  shoulder: 'shoulder',
  knee: 'knee',
  back: 'back',
  'ankle-foot': 'ankle-foot',
  tendon: 'muscle-tendon',
  'sports-injury': 'sports-injury',
  weight: 'weight',
  training: 'training',
};

export function topicIcon(topicId: string): string | undefined {
  const f = topicIconFile[topicId];
  return f ? `${KIT}/topics/${f}.svg` : undefined;
}

export function treatmentIcon(slug: string): string {
  return `${KIT}/treatments/${slug}.svg`;
}

/** 專欄分類插畫（600×400） */
export function categoryIllustration(categoryId: string): string {
  return `${KIT}/categories/${categoryId}.svg`;
}

/** 裝飾背景（皆為純裝飾，alt 為空或以 CSS 背景使用） */
export const decorSvg = {
  heroDesktop: `${KIT}/decor/hero-flow.svg`,
  heroMobile: `${KIT}/decor/hero-flow-mobile.svg`,
  portraitHalo: `${KIT}/decor/portrait-halo.svg`,
  sectionWave: `${KIT}/decor/section-wave.svg`,
  clinicPanel: `${KIT}/decor/clinic-panel.svg`,
  footerFlow: `${KIT}/decor/footer-flow.svg`,
} as const;

export type DecorId = keyof typeof decorSvg;

/** 醫學解說圖（public/medical/，深色資訊圖表，內含中文說明文字） */
export const medicalFigures = {
  'knee-acl-hyperextension': {
    src: '/medical/knee-acl-hyperextension-3d.svg',
    alt: '概念示意圖：膝關節過度伸直時前十字韌帶（ACL）承受較大負荷，並標示較佳落地策略——髖、膝微彎、肌肉主動減速，避免直膝單腳硬著地',
  },
  'landing-mechanics': {
    src: '/medical/landing-mechanics-3d.svg',
    alt: '概念示意圖：直膝落地（高風險模式）與髖膝屈曲吸震（較佳模式）的比較，說明臀肌、股四頭肌與腿後肌協助減速',
  },
  'sideline-abcde': {
    src: '/medical/sideline-abcde-3d.svg',
    alt: '示意圖：場邊急性傷害 ABCDE 初步評估——Airway 呼吸道與頸椎保護、Breathing 呼吸與換氣、Circulation 循環與出血控制、Disability 意識與神經學評估、Exposure/Extremities 露身檢查與肢體評估',
  },
  'msk-ultrasound-guidance': {
    src: '/medical/msk-ultrasound-guidance-3d.svg',
    alt: '概念示意圖：骨骼肌肉超音波導引注射，探頭下可見目標組織、需避開的神經與血管，以及全程保持可視的針尖；標示超音波導引三要點',
  },
  'gymnast-wrist-growth-plate': {
    src: '/medical/gymnast-wrist-growth-plate-3d.svg',
    alt: '概念示意圖：體操選手手腕承重與遠端橈骨生長板位置，列出常需留意的區域——生長板過度使用、TFCC／尺側疼痛、舟狀骨壓力性傷害、關節囊與肌腱問題',
  },
  'sport-concussion-pathway': {
    src: '/medical/sport-concussion-pathway-3d.svg',
    alt: '示意圖：運動性腦震盪場邊流程——Recognise 辨識、Remove 疑似腦震盪立即停止參賽、Re-evaluate 完整神經學與認知評估、Relative rest 短暫休息後漸進增加活動；當天確診者不得回場，並列出需立即升級處置的警訊',
  },
} as const;

export type MedicalFigureId = keyof typeof medicalFigures;
