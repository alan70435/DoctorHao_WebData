/**
 * 醫師個人資料（單一來源）。
 * 所有欄位皆有可查證來源；未能確認者以 TODO 註記，不自行推測。
 * 來源縮寫：LS=聯新國際醫院官網醫師頁；PS=板新醫院醫師頁；ME=ME 美醫誌；DEF=醫生查；
 *          BLOG=drchenghao.blogspot.com；FB=粉專貼文；TH=Threads 貼文。
 */

export const doctor = {
  name: '程皓',
  displayName: '程皓醫師',
  englishName: 'Dr. Cheng Hao',
  title: '運動醫學科醫師',
  hospital: '聯新國際醫院',
  department: '運動醫學科',
  jobTitle: '聯新國際醫院 運動醫學科醫師',

  /** 首頁 Hero 副標 */
  heroSubtitle: '運動傷害｜疼痛治療｜體重管理｜運動訓練',

  /** 個人定位（依本人社群陳述整理，避免浮誇） */
  tagline: '把疼痛處理好，然後回到你喜歡的運動與生活。',

  /** 簡介（依 LS 官網＋本人貼文整理） */
  intro:
    '程皓醫師現任聯新國際醫院運動醫學科醫師，並擔任樂天桃猿棒球隊醫療團隊醫師。專長為急慢性運動傷害、退化性關節疾病、增生注射與超音波導引注射治療，以及慢性病與醫療體重管理。擁有美國運動醫學會私人教練（ACSM-CPT）認證，擅長結合運動醫學與運動訓練，為患者制定個人化的治療與訓練方案。曾任 2023 世界棒球經典賽、2023 全大運、2025 世界壯年運動會場邊醫師。',

  languages: ['國語', '英語'],

  /** 專業領域（LS 官網「主治項目」） */
  specialties: [
    '急慢性運動傷害',
    '退化性關節疾病',
    '增生注射治療（葡萄糖、PRP）',
    '超音波導引注射治療',
    '體重控制及減重治療',
    '三高慢性病控制',
    '針灸及針刀治療',
    '運動前評估及檢測',
    '運動處方開立',
    '運動訓練',
  ],

  /** 現職 */
  currentPositions: [
    { title: '聯新國際醫院 運動醫學科 醫師', source: 'LS' },
    { title: '板新醫院 運動醫學科／家庭醫學科 醫師', source: 'PS, ME' },
    { title: '台北聯新國際診所 門診醫師', source: 'FB 2026-02-01' },
    { title: '樂天桃猿棒球隊 醫療團隊醫師', source: 'LS, ME' },
    { title: '清華大學 運動醫學課程 講師', source: 'LS；FB 2024-09、2025-03、2026-03' },
  ],

  education: [{ title: '國防醫學院 醫學士', source: 'LS, PS' }],

  /** 專科／證照 */
  credentials: [
    { title: '家庭醫學科 專科醫師', source: 'ME；醫生查（衛福部登錄專科：家庭醫學科）' },
    { title: '美國運動醫學會 私人教練 ACSM-CPT', source: 'LS, PS, ME' },
    { title: '針灸、針刀', source: 'BLOG 2023-03-16 自述；LS 主治項目「針灸及針刀治療」' },
  ],

  /** 經歷（時間順序不完整處保留原文） */
  experience: [
    { title: '台北榮民總醫院 訓練醫師', source: 'LS, PS' },
    { title: '三軍總醫院 訓練醫師', source: 'ME, BLOG' },
    { title: '台北醫學院 訓練醫師', source: 'PS' },
    { title: '桃園國際機場醫療中心 駐診醫師', source: 'LS, PS, ME' },
    { title: '聯新國際醫院 家庭醫學科 專任醫師', source: 'LS, PS' },
    { title: '聯新國際醫院 運動醫學科（2023 年 8 月起）', source: 'FB 2023-08-06' },
    { title: '平鎮高中 運動醫學服務（2023 年起）', source: 'FB 2024-11-27' },
    { title: '三軍總醫院 高壓氧訓練（2025 年 3–5 月）', source: 'FB 2025-02-20' },
  ],

  /** 賽事／運動醫療經歷 */
  sportsMedicine: [
    { title: '2023 世界棒球經典賽（WBC）場邊醫師', source: 'LS, PS, ME, BLOG' },
    { title: '2023 全國大專運動會 場邊醫師（競技體操、網球）', source: 'LS, BLOG 2023-05-18' },
    { title: '2025 世界壯年運動會 場邊醫師', source: 'LS' },
    { title: '2026 全國大專運動會 場邊醫師（競技體操）', source: 'FB 2026-05-03' },
    { title: '樂天桃猿棒球隊 隨隊／駐診醫師', source: 'ME, FB 2024-05、2025-05、2026-04' },
    { title: '小鐵人挑戰賽 場邊醫師', source: 'BLOG 2023-03-16' },
    { title: '卡達 Aspetar 國際運動醫學研討會（2025 年 10 月）', source: 'FB 2025-09-24、2025-10-12' },
  ],

  memberships: [
    { title: '台灣運動醫學醫學會 會員', source: 'BLOG 2023-03-16' },
    { title: '骨質疏鬆醫學會 會員', source: 'LS, PS' },
    { title: '骨骼肌肉超音波醫學會 會員', source: 'LS, PS' },
  ],

  /** 醫療理念：直接引用本人公開文字（附來源） */
  philosophy: [
    {
      quote: '我們幾乎不會對病人說：你不能再打球、跑步了，快去休息。只要你想，我們會全力協助你。',
      source: 'Threads，2025-05-15',
    },
    {
      quote: '我從不會輕易脫口說出「你是退化性關節炎啦」，而是需要再三排除所有可能後，才能告訴患者這句話。',
      source: 'Threads，2025-08-15',
    },
    {
      quote: '門診最重要的不是讓你體重減輕而已，而是希望能找到幫助健康的關鍵。',
      source: 'Threads，2026-01-08',
    },
    {
      quote: '真正的好，不是痛好了而已，是找回以前的自己，重拾愛好。',
      source: 'Threads，2026-04-28',
    },
  ],

  /** 個人：運動背景（本人自述） */
  personal: [
    '業餘籃球愛好者，從國中起幾乎每週固定打球；以深蹲、硬舉等肌力訓練預防運動傷害。',
    '長年關注各種運動賽事，常以 NBA、職棒球員傷勢為例，分享運動傷害知識。',
  ],

  social: {
    facebook: {
      label: 'Facebook 粉絲專頁',
      name: '程皓醫師｜好動人生。運動與家庭醫學',
      url: 'https://www.facebook.com/profile.php?id=100090796624852',
    },
    threads: {
      label: 'Threads',
      handle: '@drchenghao',
      url: 'https://www.threads.com/@drchenghao',
    },
    instagram: {
      label: 'Instagram',
      handle: '@drchenghao',
      url: 'https://www.instagram.com/drchenghao/',
    },
    blog: {
      label: '部落格「程皓醫師。好動人生」',
      url: 'https://drchenghao.blogspot.com/',
    },
  },

  /** 相關影片（非本人頻道，僅外連） */
  videos: [
    {
      title: '如何擺脫【肌肉關節疼痛】?!',
      channel: '聯新國際醫院 Landseed Hospital',
      url: 'https://www.youtube.com/watch?v=V2mLhFtZed0',
    },
    {
      title: '瘦瘦針詳解 ft. 程皓醫師【ME 美醫誌】',
      channel: 'ME Media 美醫誌',
      url: 'https://www.youtube.com/watch?v=VpVQ1n4Ojbg',
    },
  ],
} as const;

export type Doctor = typeof doctor;
