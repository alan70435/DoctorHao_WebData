import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

const articles = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: './src/content/articles' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      description: z.string().max(200),
      category: z.enum(['sports-injury', 'weight-management', 'training']),
      tags: z.array(z.string()).default([]),
      /** 原始社群發布日期（若整理自多篇，取最早或最主要一篇） */
      pubDate: z.coerce.date(),
      /** 網站最後更新日期 */
      updatedDate: z.coerce.date(),
      /** 原始來源清單 */
      sources: z
        .array(
          z.object({
            platform: z.enum(['Facebook', 'Threads', 'Blog', 'Instagram']),
            date: z.union([z.string(), z.date().transform((d) => d.toISOString().slice(0, 10))]),
            url: z.string().url().optional(),
            note: z.string().optional(),
          }),
        )
        .default([]),
      cover: image().optional(),
      coverAlt: z.string().optional(),
      /** 首頁精選 */
      featured: z.boolean().default(false),
      /** 主要給醫療同業閱讀 */
      forProfessionals: z.boolean().default(false),
      draft: z.boolean().default(false),
    }),
});

export const collections = { articles };
