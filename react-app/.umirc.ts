import { defineConfig } from 'umi';

export default defineConfig({
  // layout: {},
  nodeModulesTransform: {
    type: 'none',
  },
  routes: [
    { path: '/', component: '@/pages/index' },
    { path: '/analysis', component: '@/pages/analysis' },
    { path: '/recommendation', component: '@/pages/recommendation' }
  ],
  fastRefresh: {},
  proxy: {
    '/api': {
      'target': 'http://localhost:5000',
      'changeOrigin': true,
      'pathRewrite': {'^/api': ''},
    },
  },
});
