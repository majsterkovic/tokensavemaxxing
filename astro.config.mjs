// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://majsterkovic.github.io',
  base: '/tokensavemaxxing',
  redirects: {
    '/articles/readme': '/tokensavemaxxing/articles/',
    '/tools/readme': '/tokensavemaxxing/tools/',
    '/playbooks/readme': '/tokensavemaxxing/playbooks/',
    '/architecture/readme': '/tokensavemaxxing/architecture/',
  },
  integrations: [
    starlight({
      title: 'tokensavemaxxing',
      description: 'The Agentic Coding & Context Engineering Vault - kompendium optymalizacji tokenów, architektury agentowej i context engineeringu.',
      defaultLocale: 'root',
      locales: {
        root: {
          label: 'Polski',
          lang: 'pl',
        },
      },
      head: [
        {
          tag: 'meta',
          attrs: {
            name: 'keywords',
            content: 'tokensavemaxxing, agentic coding, context pruning, prompt caching, token optimization, cursor rules, claude code, opencode, rtk, context rot, llm finops, ai engineering, kadanedial, dynamic context pruning, local llm 12gb, multi-agent workflows, superpowers, agent skills',
          },
        },
        {
          tag: 'meta',
          attrs: {
            name: 'author',
            content: 'Mariusz (majsterkovic)',
          },
        },
        {
          tag: 'meta',
          attrs: {
            property: 'og:site_name',
            content: 'tokensavemaxxing',
          },
        },
        {
          tag: 'meta',
          attrs: {
            property: 'og:type',
            content: 'website',
          },
        },
        {
          tag: 'meta',
          attrs: {
            name: 'twitter:card',
            content: 'summary_large_image',
          },
        },
        {
          tag: 'meta',
          attrs: {
            name: 'robots',
            content: 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1',
          },
        },
      ],
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
