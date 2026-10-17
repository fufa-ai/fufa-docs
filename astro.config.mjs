// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import starlightLlmsTxt from 'starlight-llms-txt';

// https://astro.build/config
export default defineConfig({
	site: 'https://docs.fufa.ai',
	integrations: [
		starlight({
			title: 'Fufa',
			description: 'Documentation for Fufa, the omnichannel CRM.',
			plugins: [starlightLlmsTxt()],
			sidebar: [
				{
					label: 'Start',
					items: [{ label: 'Introduction', slug: 'index' }],
				},
			],
		}),
		sitemap(),
	],
});
