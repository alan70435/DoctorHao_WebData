/**
 * 門診資訊（單一來源）。
 * 依據：FB 貼文 2026-02-01「最新熱騰騰門診時刻表」＋ Threads 2026-01-03 回覆。
 * 每次更新請同步修改 lastConfirmed。
 */

export type Session = 'morning' | 'afternoon' | 'evening';

export const sessionTimes: Record<Session, { label: string; time: string }> = {
  morning: { label: '早診', time: '09:00–12:00' },
  afternoon: { label: '午診', time: '13:30–16:45' },
  evening: { label: '晚診', time: '18:30–21:00' },
};

export const weekdays = ['週一', '週二', '週三', '週四', '週五', '週六', '週日'] as const;
export type Weekday = (typeof weekdays)[number];

export interface Clinic {
  id: string;
  name: string;
  shortName: string;
  department: string;
  address: string;
  city: string;
  phone?: string;
  phoneNote?: string;
  registrationUrl?: string;
  registrationLabel?: string;
  lineUrl?: string;
  mapQuery: string;
  schedule: Partial<Record<Weekday, Session[]>>;
  notes?: string[];
  todo?: string[];
  primary?: boolean;
}

export const clinics: Clinic[] = [
  {
    id: 'landseed',
    name: '聯新國際醫院',
    shortName: '聯新國際醫院',
    department: '運動醫學科',
    address: '桃園市平鎮區廣泰路77號',
    city: '桃園',
    phone: '03-4941234',
    registrationUrl: 'https://www.landseedhospital.com.tw/lishin/reg/news.php',
    registrationLabel: '前往院方網路掛號',
    mapQuery: '聯新國際醫院 桃園市平鎮區廣泰路77號',
    schedule: {
      週一: ['morning'],
      週四: ['morning', 'afternoon'],
      週五: ['morning', 'afternoon'],
      週六: ['morning'],
    },
    notes: [
      '減重相關諮詢建議優先前往此院區：藥物選項較完整，並可安排營養與運動諮詢、InBody 身體組成檢測（程皓醫師 2026-01-03 說明）。',
      '初診評估時間較長（常超過 30 分鐘），如需抽血請預留時間並可空腹前來。',
    ],
    primary: true,
  },
  {
    id: 'panshin',
    name: '板新醫院',
    shortName: '板新醫院',
    department: '運動醫學科',
    address: '新北市板橋區中正路189號',
    city: '新北',
    phone: '02-2960-9955',
    phoneNote: '院方代表號',
    registrationUrl: 'http://reg.panshin.com.tw/',
    registrationLabel: '前往院方網路掛號',
    mapQuery: '板新醫院 新北市板橋區中正路189號',
    schedule: {
      週一: ['evening'],
    },
    todo: ['TODO：確認板新醫院掛號電話（院方頁面為 02-2960-9955；程醫師 2023 年貼文曾列 02-2960-4545）。'],
  },
  {
    id: 'landseed-taipei',
    name: '台北聯新國際診所',
    shortName: '台北聯新國際診所',
    department: '運動醫學',
    address: '台北市大安區仁愛路四段77號3樓',
    city: '台北',
    phone: '02-2721-6698',
    phoneNote: '2023 年貼文所列電話',
    lineUrl: 'https://lin.ee/kD8WWO5',
    registrationLabel: 'LINE 官方帳號預約',
    mapQuery: '台北聯新國際診所 台北市大安區仁愛路四段77號3樓',
    schedule: {
      週二: ['morning'],
    },
    notes: ['週二早診自 08:30 開始。'],
    todo: ['TODO：確認台北聯新國際診所目前的預約方式（電話／LINE）是否仍有效。'],
  },
];

/** 門診表最後一次依公開資料確認的日期 */
export const lastConfirmed = '2026-02-01';

export const scheduleTodo = [
  'TODO：確認程皓醫師目前（2026 年 9 月）門診時間是否與 2026-02-01 公告相同。',
  'TODO：確認是否有臨時停診、代診或加診資訊需要公告。',
];

/** 就診須知（依本人貼文整理） */
export const visitTips = [
  '初診會完整問診、理學檢查，視需要安排 X 光或超音波檢查，評估時間較長，請預留時間。',
  '減重門診初診：當天看診諮詢、抽血、檢視報告、安排 InBody 與運動營養衛教、藥局取藥與教學；若時間不足可下次再看報告。',
  '複診請於報到時告知，流程較快；用藥期間會針對效果與副作用調整。',
  '門診可能因學會、賽事支援或天候（停班停課）異動，出發前建議先以院方公告或粉絲專頁確認。',
];
