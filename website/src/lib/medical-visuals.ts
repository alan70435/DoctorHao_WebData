import raw from '@/data/medical-visuals.json';
export interface MedicalVisual {
  slug: string; scene: string; title: string; articleTitle: string; category: string;
  alt: string; cover: string; coverSmall: string; coverMedium: string;
  figure: string; figureRaster: string; og: string; model: string; poster: string;
  modelNotes: string; caution: string; camera: number[]; reviewStatus: string;
  points: { heading: string; text: string }[]; structures: string[][]; sourceIds: string[];
}
interface Model { src: string; poster: string; notes: string; camera: number[]; bytes: number; }
interface Registry {
  articles: Record<string, MedicalVisual>; models: Record<string, Model>;
  sources: Record<string, {label: string; url: string; checkedOn: string}>;
}
export const medicalVisuals = raw as unknown as Registry;
/** New/unmapped articles keep the existing CategoryCover; never guess a medical illustration. */
export const getMedicalVisual = (slug: string): MedicalVisual | undefined => medicalVisuals.articles[slug];
