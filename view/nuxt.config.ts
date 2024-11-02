// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: false },
  modules: ["@nuxt/ui"],

  app: {
    head: {
      title: 'Theft Prediction',
      meta: [
        {
          name: 'description', content: 'AI-powered prediction system.'
        }
      ],
      link: [
        {
          rel: 'shortcut icon', type: 'image/png', href: '/icon.png'
        }
      ]
    }
  },

  colorMode: {
    preference: "light"
  },

  css: [
    "~/assets/css/main.css"
  ],

  ui: {
    icons: ["lucide"]
  },

  tailwindcss: {
    config: {
      theme: {
        extend: {
          colors: {
            custom: {
              50: '#f6f7f9',
              100: '#eceef2',
              200: '#d5dae2',
              300: '#b0b9c9',
              400: '#8694aa',
              500: '#667691',
              600: '#526077',
              700: '#434d61',
              800: '#373f4e',
              900: '#343a46',
              950: '#22262f',
            }
          }
        },
      },
    }
  },

  compatibilityDate: '2024-10-08'
})