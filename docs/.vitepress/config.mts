import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "Supernest",
  description: "Nested sampling accelerated",
  themeConfig: {
	nav: [
	  { text: 'Docs', link: '/api-docs' },
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
