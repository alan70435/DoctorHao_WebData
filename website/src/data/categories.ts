export type CategoryId = 'sports-injury' | 'weight-management' | 'training';

export interface Category {
  id: CategoryId;
  name: string;
  shortName: string;
  description: string;
  path: string;
  /** design token 名稱，對應 CSS 變數 --cat-* */
  tone: 'teal' | 'amber' | 'green';
}

export const categories: Record<CategoryId, Category> = {
  'sports-injury': {
    id: 'sports-injury',
    name: '運動傷害及疼痛',
    shortName: '運動傷害及疼痛',
    description: '肩、膝、腰背、足踝與肌腱問題，運動傷害的成因、評估與治療觀念。',
    path: '/articles/sports-injury/',
    tone: 'teal',
  },
  'weight-management': {
    id: 'weight-management',
    name: '體重控制及減重',
    shortName: '體重控制及減重',
    description: '醫療體重管理、瘦瘦針（腸泌素類藥物）常見問題、飲食與生活型態。',
    path: '/articles/weight-management/',
    tone: 'amber',
  },
  training: {
    id: 'training',
    name: '運動訓練',
    shortName: '運動訓練',
    description: '肌力訓練、動作要領、運動營養與補劑，讓訓練成為保養與治療的一部分。',
    path: '/articles/training/',
    tone: 'green',
  },
};

export const categoryList: Category[] = Object.values(categories);
