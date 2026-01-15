import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'FalkorDB Docs',
  tagline: 'The fastest way to your knowledge',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://falkordb.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'FalkorDB', // Usually your GitHub org/user name.
  projectName: 'docs', // Usually your repo name.

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/', // Serve docs at the root
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/FalkorDB/docs/edit/main/',
          showLastUpdateTime: false,
          showLastUpdateAuthor: false,
          // Enable previous/next navigation at the bottom of each doc page
          editCurrentVersion: true,
        },
        blog: false, // Disable blog
        theme: {
          customCss: './src/css/custom.css',
        },
        gtag: {
          trackingID: 'GTM-MBWB627H',
          anonymizeIP: true,
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-client-redirects',
      {
        redirects: [
          {
            from: '/design/result_structure.html',
            to: '/design/result-structure',
          },
          {
            from: '/design/bulk_spec.html',
            to: '/design/bulk-spec',
          },
          {
            from: '/design/client_spec.html',
            to: '/design/client-spec',
          },
          {
            from: '/third-party.html',
            to: '/design/third-party',
          },
          {
            from: '/graphrag_sdk.html',
            to: '/genai-tools/graphrag-sdk',
          },
          {
            from: '/llm_integrations.html',
            to: '/genai-tools',
          },
          {
            from: '/bolt-support.html',
            to: '/integration/bolt-support',
          },
          {
            from: '/algorithms/betweenness_centrality.html',
            to: '/algorithms/betweenness-centrality',
          },
          {
            from: '/cypher/algorithms.html',
            to: '/algorithms',
          },
          {
            from: '/cypher/load_csv.html',
            to: '/cypher/load-csv',
          },
          {
            from: '/cypher/cypher_support.html',
            to: '/cypher/cypher-support',
          },
          {
            from: '/cypher/known_limitations.html',
            to: '/cypher/known-limitations',
          },
          {
            from: '/cypher/order_by.html',
            to: '/cypher/order-by',
          },
          {
            from: '/cypher/optional_match.html',
            to: '/cypher/optional-match',
          },
          {
            from: '/operation/replication',
            to: '/operations/replication',
          },
          {
            from: '/operations/k8s_support.html',
            to: '/operations/k8s-support',
          },
          {
            from: '/building-docker.html',
            to: '/operations/building-docker',
          },
          {
            from: '/operation',
            to: '/operations',
          },
          {
            from: '/opentelemetry.html',
            to: '/operations/opentelemetry',
          },
          {
            from: '/clients.html',
            to: '/getting-started/clients',
          },
          {
            from: '/getting_started.html',
            to: '/getting-started',
          },
          {
            from: '/configuration.html',
            to: '/getting-started/configuration',
          },
          {
            from: '/commands/graph.ro_query.html',
            to: '/commands/graph.ro-query',
          },
          {
            from: '/migration.html',
            to: '/operations/migration',
          },
          {
            from: '/redisgraph-to-falkordb.html',
            to: '/operations/migration/redisgraph-to-falkordb',
          },
          {
            from: '/cypher/indexing.html',
            to: '/cypher/indexing',
          },
        ],
      },
    ],
    [
      require.resolve("@easyops-cn/docusaurus-search-local"),
      {
        hashed: true,
        indexDocs: true,
        indexBlog: false,
        docsRouteBasePath: "/",
      },
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: 'FalkorDB',
      logo: {
        alt: 'FalkorDB Logo',
        src: 'img/falkor-logo.png',
        href: '/',
        target: '_self',
      },
      items: [
        {
          href: 'https://www.falkordb.com',
          label: 'Website',
          position: 'left',
        },
        {
          href: 'https://app.falkordb.cloud',
          label: 'Try Cloud',
          position: 'left',
        },
        {
          href: 'https://github.com/falkordb/falkordb',
          label: 'GitHub',
          position: 'right',
        },
        {
          href: 'https://discord.gg/ErBEqN9E',
          label: 'Discord',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'light',
      copyright: `© ${new Date().getFullYear()} FalkorDB`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['cypher', 'java', 'python', 'javascript', 'bash', 'cpp', 'rust'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
