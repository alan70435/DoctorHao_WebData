import { categoryList } from './categories';
import { doctor } from './doctor';

export interface NavItem {
  label: string;
  href: string;
  children?: NavItem[];
  /** 桌機顯示用的短標籤 */
  short?: string;
}

/** 桌機主選單（治療項目直接放第一層） */
export const primaryNav: NavItem[] = [
  { label: '關於程皓醫師', short: '關於程醫師', href: '/about/' },
  { label: '葡萄糖增生修復治療', short: '葡萄糖增生', href: '/prolotherapy/' },
  { label: 'PRP 再生修復治療', short: 'PRP', href: '/prp/' },
  { label: 'BMA 骨髓再生修復治療', short: 'BMA', href: '/bma/' },
  { label: '醫療體重管理', short: '體重管理', href: '/weight-management/' },
  {
    label: '程皓醫師專欄',
    short: '程皓醫師專欄',
    href: '/articles/',
    children: categoryList.map((c) => ({ label: c.name, href: c.path })),
  },
];

export const clinicCta: NavItem = { label: '門診時間及預約', href: '/clinic/' };

export const facebookLink = {
  label: 'Facebook 粉絲專頁',
  href: doctor.social.facebook.url,
};

/** 手機選單分組 */
export const mobileNavGroups = [
  { heading: null, items: [{ label: '關於程皓醫師', href: '/about/' }] },
  {
    heading: '主要治療',
    items: [
      { label: '葡萄糖增生修復治療', href: '/prolotherapy/' },
      { label: 'PRP 再生修復治療', href: '/prp/' },
      { label: 'BMA 骨髓再生修復治療', href: '/bma/' },
      { label: '醫療體重管理', href: '/weight-management/' },
    ],
  },
  {
    heading: '程皓醫師專欄',
    items: [{ label: '專欄總覽', href: '/articles/' }, ...categoryList.map((c) => ({ label: c.name, href: c.path }))],
  },
];

export const footerNav = {
  treatments: [
    { label: '葡萄糖增生修復治療', href: '/prolotherapy/' },
    { label: 'PRP 再生修復治療', href: '/prp/' },
    { label: 'BMA 骨髓再生修復治療', href: '/bma/' },
    { label: '醫療體重管理', href: '/weight-management/' },
  ],
  articles: [{ label: '專欄總覽', href: '/articles/' }, ...categoryList.map((c) => ({ label: c.name, href: c.path }))],
  about: [
    { label: '關於程皓醫師', href: '/about/' },
    { label: '門診時間及預約', href: '/clinic/' },
  ],
};
