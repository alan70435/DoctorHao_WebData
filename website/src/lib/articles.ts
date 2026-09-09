import { getCollection, type CollectionEntry } from 'astro:content';
import type { CategoryId } from '@/data/categories';

export type Article = CollectionEntry<'articles'>;

export async function getPublishedArticles(): Promise<Article[]> {
  const all = await getCollection('articles', ({ data }) => !data.draft);
  return all.sort((a, b) => b.data.pubDate.getTime() - a.data.pubDate.getTime());
}

export async function getArticlesByCategory(category: CategoryId) {
  return (await getPublishedArticles()).filter((a) => a.data.category === category);
}

export async function getArticlesByTags(tags: string[], limit?: number) {
  const list = (await getPublishedArticles()).filter((a) => a.data.tags.some((t) => tags.includes(t)));
  return limit ? list.slice(0, limit) : list;
}

export async function getFeaturedArticles(limit = 6) {
  const all = await getPublishedArticles();
  const featured = all.filter((a) => a.data.featured);
  // 若精選不足，補上最新文章，並確保三個分類都有出現
  const picked: Article[] = [...featured];
  for (const a of all) {
    if (picked.length >= limit) break;
    if (!picked.includes(a)) picked.push(a);
  }
  return picked.slice(0, limit);
}

/** 相關文章：先依指定 slug，再依共同 tag 補齊 */
export async function getRelatedArticles(opts: { slugs?: string[]; tags?: string[]; exclude?: string; limit?: number }) {
  const { slugs = [], tags = [], exclude, limit = 4 } = opts;
  const all = await getPublishedArticles();
  const bySlug = slugs.map((s) => all.find((a) => a.id === s)).filter((a): a is Article => !!a && a.id !== exclude);
  const result: Article[] = [...bySlug];
  if (tags.length) {
    const scored = all
      .filter((a) => a.id !== exclude && !result.includes(a))
      .map((a) => ({ a, score: a.data.tags.filter((t) => tags.includes(t)).length }))
      .filter((x) => x.score > 0)
      .sort((x, y) => y.score - x.score || y.a.data.pubDate.getTime() - x.a.data.pubDate.getTime());
    for (const { a } of scored) {
      if (result.length >= limit) break;
      result.push(a);
    }
  }
  return result.slice(0, limit);
}

export function formatDate(d: Date) {
  return d.toLocaleDateString('zh-TW', { year: 'numeric', month: '2-digit', day: '2-digit' }).replace(/\//g, '.');
}

export function isoDate(d: Date) {
  return d.toISOString().slice(0, 10);
}

/** 粗估閱讀時間（中文以每分鐘 400 字計） */
export function readingMinutes(body?: string) {
  if (!body) return 1;
  const chars = body.replace(/\s+/g, '').length;
  return Math.max(1, Math.round(chars / 400));
}
