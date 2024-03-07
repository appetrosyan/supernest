import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Supernest",
  description: "Nested sampling accelerated",
  themeConfig: {
	// https://vitepress.dev/reference/default-theme-config
	nav: [
	  { text: 'Home', link: '/' },
	  { text: 'Examples', link: '/markdown-examples' }
	],

	sidebar: [
	  {
		text: 'Documentation',
		collapsed: false,
		items: [
		  {
			text: 'API Documentation',
			link: '/api-docs',
			collapsed: false,
			items: [
			  {
				text: 'Basic usage',
				link: 'api/basic_usage',
			  }
			],
		  },
		  {
			text: 'Integrations',
			link: 'integrations'
		  }
		]
	  }
	],

	socialLinks: [
	  { icon: 'github', link: 'https://github.com/vuejs/vitepress' }
	]
  }
})
