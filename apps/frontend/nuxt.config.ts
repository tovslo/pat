// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui'
  ],

  devtools: {
    enabled: true
  },

  css: ['~/assets/css/main.css'],

  routeRules: {
    '/': { prerender: true }
  },

  compatibilityDate: '2025-01-15',

  // Proxy /api/* and /ws/* to FastAPI in dev
  nitro: {
    devProxy: {
      '/api': { target: 'http://localhost:8000/api', changeOrigin: true, ws: true },
      '/ws': { target: 'http://localhost:8000/ws', changeOrigin: true, ws: true }
    }
  },

  vite: {
    optimizeDeps: {
      include: ['vee-validate', '@vee-validate/zod', 'zod', 'pinia', '@vue/devtools-api']
    }
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }
})
