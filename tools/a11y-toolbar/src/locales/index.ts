import type { PartialTranslations, ToolbarLanguage, ToolbarTranslations } from '../types';
import { en } from './en';
import { he } from './he';

export { en, he };

const LOCALES: Readonly<Record<ToolbarLanguage, ToolbarTranslations>> = { he, en };

/** Merges partial overrides onto a complete locale. Empty or non-string overrides are ignored. */
export function createTranslations(
  language: ToolbarLanguage = 'he',
  overrides: PartialTranslations = {},
): ToolbarTranslations {
  const base = LOCALES[language];
  const merged: Record<keyof ToolbarTranslations, string> = { ...base };
  for (const key of Object.keys(base) as (keyof ToolbarTranslations)[]) {
    const value = overrides[key];
    if (typeof value === 'string' && value.trim() !== '') merged[key] = value;
  }
  return merged;
}

export function formatMessage(template: string, values: Readonly<Record<string, string>>): string {
  return template.replace(/\{(\w+)\}/g, (match, name: string) => values[name] ?? match);
}

export function isToolbarLanguage(value: unknown): value is ToolbarLanguage {
  return value === 'he' || value === 'en';
}
