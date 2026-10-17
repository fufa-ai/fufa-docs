// @ts-check
import { readdirSync } from 'node:fs';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import starlightLlmsTxt from 'starlight-llms-txt';

const SITE = 'https://docs.fufa.ai';

// The sidebar follows a new customer through the product, one folder per group.
// Each group lists whatever pages its folder holds, so a page appears because its file exists.
// A group with no pages yet stays out of the sidebar.
const GROUPS = [
	['start', 'Start'],
	['channels', 'Channels'],
	['inbox', 'Inbox'],
	['contacts', 'Contacts'],
	['campaigns', 'Campaigns'],
	['agents', 'Agents'],
	['workflows', 'Workflows'],
	['commerce', 'Commerce'],
	['workspace', 'Workspace'],
];
const hasPages = (dir) => {
	try {
		return readdirSync(new URL(`./src/content/docs/${dir}`, import.meta.url)).some((f) => /\.mdx?$/.test(f));
	} catch {
		return false;
	}
};
const sidebar = GROUPS.filter(([dir]) => dir === 'start' || hasPages(dir)).map(([dir, label]) => ({
	label,
	items:
		dir === 'start'
			? [{ label: 'What is Fufa', slug: 'index' }, { autogenerate: { directory: dir } }]
			: [{ autogenerate: { directory: dir } }],
}));

// https://astro.build/config
export default defineConfig({
	site: SITE,
	integrations: [
		starlight({
			title: 'Fufa Docs',
			description:
				'How to set up and run Fufa: connect WhatsApp, live chat, Instagram, email, Telegram and phone, answer customers from one inbox, and deploy AI agents that sell for your store.',
			logo: { src: './src/assets/logo.png', replacesTitle: false },
			favicon: '/favicon.png',
			customCss: ['./src/styles/custom.css', './src/styles/design.css'],
			lastUpdated: true,
			pagination: true,
			routeMiddleware: './src/route-data.ts',
			components: {
				Hero: './src/components/Hero.astro',
				PageTitle: './src/components/PageTitle.astro',
				Footer: './src/components/Footer.astro',
				SiteTitle: './src/components/SiteTitle.astro',
				SocialIcons: './src/components/SocialIcons.astro',
			},
			head: [
				{ tag: 'meta', attrs: { property: 'og:site_name', content: 'Fufa Docs' } },
				{ tag: 'meta', attrs: { name: 'twitter:card', content: 'summary' } },
				{ tag: 'link', attrs: { rel: 'alternate', type: 'text/plain', title: 'llms.txt', href: '/llms.txt' } },
			],
			plugins: [
				starlightLlmsTxt({
					projectName: 'Fufa',
					description:
						'Fufa is an AI customer platform for online stores. Conversations from WhatsApp, website live chat, Instagram, email, Telegram and phone land in one inbox, and AI agents answer, sell and hand over to the team.',
					details: [
						'Each page covers one task. The page title is the task and the first paragraph is the result.',
						'Every page is also available as plain markdown: add `.md` to its URL, for example `/channels/whatsapp.md`.',
						'UI labels are written exactly as they appear in the Fufa app, in bold.',
					].join('\n'),
					promote: ['index*', 'start/**'],
					customSets: [
						{ label: 'Getting live', description: 'The shortest path from sign-up to a live store: workspace, channels, inbox, team, agent and Shopify.', paths: ['index*', 'start/**', 'channels/**', 'inbox/**', 'workspace/**', 'agents/create-an-agent*', 'commerce/shopify*'] },
						{ label: 'AI agents', description: 'Creating, teaching, testing and deploying Fufa AI agents.', paths: ['agents/**'] },
					],
				}),
			],
			sidebar,
		}),
		sitemap(),
	],
});
