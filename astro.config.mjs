// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://majsterkovic.github.io',
  base: '/tokensavemaxxing',
  integrations: [
    starlight({
      title: 'tokensavemaxxing',
      description: 'The Agentic Coding & Context Engineering Vault',
      defaultLocale: 'root',
      locales: {
        root: {
          label: 'Polski',
          lang: 'pl',
        },
      },
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/majsterkovic/tokensavemaxxing',
        },
      ],
      sidebar: [
        {
          label: '🚀 Wprowadzenie',
          items: [
            { label: 'Strona Główna', slug: 'index' },
          ],
        },
        {
          label: '📚 Artykuły & Badania',
          items: [{ autogenerate: { directory: 'articles' } }],
        },
        {
          label: '🛠️ Katalog Narzędzi',
          items: [{ autogenerate: { directory: 'tools' } }],
        },
        {
          label: '📋 Playbooki Operacyjne',
          items: [{ autogenerate: { directory: 'playbooks' } }],
        },
        {
          label: '🏛️ Architektura Kontekstu',
          items: [{ autogenerate: { directory: 'architecture' } }],
        },
      ],
    }),
  ],
});
