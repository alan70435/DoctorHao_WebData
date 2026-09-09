/**
 * 「從問題開始找資訊」入口：每個主題對應文章 tag。
 * 文章 frontmatter 的 tags 使用相同 id。
 */
export interface Topic {
  id: string;
  name: string;
  description: string;
  /** 對應文章 tags（任一符合即列出） */
  tags: string[];
  /** 建議延伸閱讀的治療頁 */
  treatments?: string[];
}

export const topics: Topic[] = [
  {
    id: 'shoulder',
    name: '肩膀疼痛',
    description: '五十肩、旋轉肌袖、肩關節夾擠',
    tags: ['shoulder'],
    treatments: ['prolotherapy', 'prp'],
  },
  {
    id: 'knee',
    name: '膝蓋疼痛',
    description: '退化性關節炎、半月板、韌帶、跑者膝',
    tags: ['knee'],
    treatments: ['prolotherapy', 'prp', 'bma'],
  },
  {
    id: 'back',
    name: '腰背疼痛',
    description: '下背痛、核心穩定、姿勢與訓練',
    tags: ['back'],
    treatments: ['prolotherapy'],
  },
  {
    id: 'ankle-foot',
    name: '足踝問題',
    description: '足底筋膜炎、踝關節扭傷與不穩定',
    tags: ['ankle-foot'],
    treatments: ['prolotherapy', 'prp'],
  },
  {
    id: 'tendon',
    name: '肌腱疼痛',
    description: '肌腱炎、肌肉拉傷與撕裂傷、阿基里斯腱',
    tags: ['tendon', 'muscle'],
    treatments: ['prolotherapy', 'prp'],
  },
  {
    id: 'sports-injury',
    name: '運動傷害',
    description: '籃球、羽球、跑步、匹克球等運動常見傷害',
    tags: ['sports-injury'],
  },
  {
    id: 'weight',
    name: '體重控制',
    description: '醫療體重管理、瘦瘦針、飲食與生活型態',
    tags: ['weight'],
    treatments: ['weight-management'],
  },
  {
    id: 'training',
    name: '運動訓練',
    description: '肌力訓練、動作要領、運動營養',
    tags: ['training'],
  },
];

export const topicById = Object.fromEntries(topics.map((t) => [t.id, t])) as Record<string, Topic>;
