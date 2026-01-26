import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    {
      type: 'doc',
      id: 'index',
      label: 'Introduction',
    },
    
    // QUICK START
    {
      type: 'category',
      label: 'Quick Start',
      collapsed: false,
      items: [
        'getting-started/index',
        'getting-started/clients',
        'getting-started/configuration',
      ],
    },

    // TUTORIALS
    {
      type: 'category',
      label: 'Tutorials',
      collapsed: false,
      items: [
        'tutorials/social-network',
        'tutorials/knowledge-graph-rag',
      ],
    },

    // DEPLOYMENT OPTIONS
    {
      type: 'category',
      label: 'Deployment',
      collapsed: true,
      items: [
        'operations/index',
        'operations/security',
        'operations/performance',
        'operations/docker',
        'operations/falkordblite',
        'operations/railway',
        'operations/lightning-ai',
        {
          type: 'category',
          label: 'FalkorDB Cloud',
          link: {
            type: 'doc',
            id: 'cloud/index',
          },
          items: [
            'cloud/features',
            'cloud/free-tier',
            'cloud/pro-tier',
            'cloud/startup-tier',
            'cloud/enterprise-tier',
          ],
        },
        {
          type: 'category',
          label: 'Enterprise Deployment',
          items: [
            'operations/k8s-support',
            'operations/kubeblocks',
            'operations/cluster',
            'operations/replication',
            'operations/persistence',
          ],
        },
      ],
    },

    // CYPHER QUERY LANGUAGE
    {
      type: 'category',
      label: 'Cypher Query Language',
      collapsed: true,
      link: {
        type: 'doc',
        id: 'cypher/index',
      },
      items: [
        'cypher/cypher-support',
        {
          type: 'category',
          label: 'Reading Data',
          items: [
            'cypher/match',
            'cypher/optional-match',
            'cypher/where',
            'cypher/return',
            'cypher/order-by',
            'cypher/skip',
            'cypher/limit',
          ],
        },
        {
          type: 'category',
          label: 'Writing Data',
          items: [
            'cypher/create',
            'cypher/merge',
            'cypher/set',
            'cypher/delete',
            'cypher/remove',
          ],
        },
        {
          type: 'category',
          label: 'Advanced Queries',
          items: [
            'cypher/with',
            'cypher/union',
            'cypher/unwind',
            'cypher/call',
            'cypher/foreach',
            'cypher/load-csv',
          ],
        },
        'cypher/functions',
        'cypher/procedures',
        {
          type: 'category',
          label: 'Indexing',
          link: {
            type: 'doc',
            id: 'cypher/indexing/index',
          },
          items: [
            'cypher/indexing/range-index',
            'cypher/indexing/fulltext-index',
            'cypher/indexing/vector-index',
          ],
        },
        'cypher/known-limitations',
      ],
    },

    // GRAPHRAG & AI
    {
      type: 'category',
      label: 'GraphRAG & AI',
      collapsed: true,
      items: [
        'genai-tools/index',
        'genai-tools/graphrag-sdk',
        'genai-tools/graphrag-toolkit',
        {
          type: 'category',
          label: 'AI Framework Integration',
          items: [
            'genai-tools/langchain',
            'genai-tools/langgraph',
            'genai-tools/llamaindex',
            'genai-tools/ag2',
          ],
        },
        {
          type: 'category',
          label: 'Agentic Memory',
          link: {
            type: 'doc',
            id: 'agentic-memory/index',
          },
          items: [
            'agentic-memory/cognee',
            'agentic-memory/graphiti',
            'agentic-memory/graphiti-mcp-server',
          ],
        },
      ],
    },

    // GRAPH ALGORITHMS
    {
      type: 'category',
      label: 'Graph Algorithms',
      link: {
        type: 'doc',
        id: 'algorithms/index',
      },
      items: [
        'algorithms/bfs',
        'algorithms/pagerank',
        'algorithms/betweenness-centrality',
        'algorithms/wcc',
        'algorithms/sspath',
        'algorithms/sppath',
        'algorithms/msf',
        'algorithms/cdlp',
      ],
    },

    // DATABASE COMMANDS
    {
      type: 'category',
      label: 'Database Commands',
      link: {
        type: 'doc',
        id: 'commands/index',
      },
      items: [
        {
          type: 'category',
          label: 'Query Commands',
          items: [
            'commands/graph.query',
            'commands/graph.ro-query',
            'commands/graph.explain',
            'commands/graph.profile',
          ],
        },
        {
          type: 'category',
          label: 'Graph Management',
          items: [
            'commands/graph.list',
            'commands/graph.info',
            'commands/graph.delete',
            'commands/graph.copy',
            'commands/graph.memory',
          ],
        },
        {
          type: 'category',
          label: 'Configuration & Constraints',
          items: [
            'commands/graph.config-get',
            'commands/graph.config-set',
            'commands/graph.constraint-create',
            'commands/graph.constraint-drop',
          ],
        },
        'commands/graph.slowlog',
        'commands/acl',
      ],
    },

    // INTEGRATIONS
    {
      type: 'category',
      label: 'Integrations',
      link: {
        type: 'doc',
        id: 'integration/index',
      },
      items: [
        'integration/bolt-support',
        'integration/rest',
        'integration/kafka-connect',
        'integration/spring-data-falkordb',
        'integration/jena',
      ],
    },

    // BROWSER UI
    {
      type: 'doc',
      id: 'browser/readme-browser',
      label: 'Browser UI',
    },

    // TROUBLESHOOTING
    {
      type: 'doc',
      id: 'troubleshooting/index',
      label: 'Troubleshooting & FAQ',
    },

    // MIGRATION
    {
      type: 'category',
      label: 'Migration Guides',
      link: {
        type: 'doc',
        id: 'operations/migration/index',
      },
      items: [
        'operations/migration/redisgraph-to-falkordb',
        'operations/migration/neo4j-to-falkordb',
        'operations/migration/kuzu-to-falkordb',
        'operations/migration/rdf-to-falkordb',
      ],
    },

    // ADVANCED TOPICS
    {
      type: 'category',
      label: 'Advanced',
      items: [
        {
          type: 'category',
          label: 'User Defined Functions',
          link: {
            type: 'doc',
            id: 'udfs/index',
          },
          items: [
            {
              type: 'category',
              label: 'Flex UDFs',
              link: {
                type: 'doc',
                id: 'udfs/flex/index',
              },
              items: [
                {
                  type: 'category',
                  label: 'Bitwise',
                  link: {
                    type: 'doc',
                    id: 'udfs/flex/bitwise/index',
                  },
                  items: [
                    'udfs/flex/bitwise/and',
                    'udfs/flex/bitwise/or',
                    'udfs/flex/bitwise/xor',
                    'udfs/flex/bitwise/not',
                    'udfs/flex/bitwise/shiftLeft',
                    'udfs/flex/bitwise/shiftRight',
                  ],
                },
                {
                  type: 'category',
                  label: 'Collections',
                  link: {
                    type: 'doc',
                    id: 'udfs/flex/collections/index',
                  },
                  items: [
                    'udfs/flex/collections/frequencies',
                    'udfs/flex/collections/intersection',
                    'udfs/flex/collections/shuffle',
                    'udfs/flex/collections/union',
                    'udfs/flex/collections/zip',
                  ],
                },
                {
                  type: 'category',
                  label: 'Date',
                  link: {
                    type: 'doc',
                    id: 'udfs/flex/date/index',
                  },
                  items: [
                    'udfs/flex/date/format',
                    'udfs/flex/date/parse',
                    'udfs/flex/date/toTimeZone',
                    'udfs/flex/date/truncate',
                  ],
                },
                {
                  type: 'category',
                  label: 'JSON',
                  link: {
                    type: 'doc',
                    id: 'udfs/flex/json/index',
                  },
                  items: [
                    'udfs/flex/json/fromJsonList',
                    'udfs/flex/json/fromJsonMap',
                    'udfs/flex/json/toJson',
                  ],
                },
                {
                  type: 'category',
                  label: 'Map',
                  link: {
                    type: 'doc',
                    id: 'udfs/flex/map/index',
                  },
                  items: [
                    'udfs/flex/map/fromPairs',
                    'udfs/flex/map/merge',
                    'udfs/flex/map/removeKey',
                    'udfs/flex/map/removeKeys',
                    'udfs/flex/map/submap',
                  ],
                },
                {
                  type: 'category',
                  label: 'Similarity',
                  link: {
                    type: 'doc',
                    id: 'udfs/flex/similarity/index',
                  },
                  items: [
                    'udfs/flex/similarity/jaccard',
                  ],
                },
                {
                  type: 'category',
                  label: 'Text',
                  link: {
                    type: 'doc',
                    id: 'udfs/flex/text/index',
                  },
                  items: [
                    'udfs/flex/text/camelCase',
                    'udfs/flex/text/capitalize',
                    'udfs/flex/text/decapitalize',
                    'udfs/flex/text/format',
                    'udfs/flex/text/indexOf',
                    'udfs/flex/text/indexesOf',
                    'udfs/flex/text/jaroWinkler',
                    'udfs/flex/text/join',
                    'udfs/flex/text/levenshtein',
                    'udfs/flex/text/lpad',
                    'udfs/flex/text/regexGroups',
                    'udfs/flex/text/repeat',
                    'udfs/flex/text/replace',
                    'udfs/flex/text/rpad',
                    'udfs/flex/text/snakeCase',
                    'udfs/flex/text/swapCase',
                    'udfs/flex/text/upperCamelCase',
                  ],
                },
              ],
            },
          ],
        },
        'operations/building-docker',
        'operations/opentelemetry',
        {
          type: 'category',
          label: 'Design & Specifications',
          link: {
            type: 'doc',
            id: 'design/index',
          },
          items: [
            'design/result-structure',
            'design/client-spec',
            'design/bulk-spec',
            'design/third-party',
          ],
        },
      ],
    },

    // REFERENCE
    {
      type: 'category',
      label: 'Reference',
      items: [
        'datatypes',
        'References',
        'license',
      ],
    },
  ],
};

export default sidebars;
