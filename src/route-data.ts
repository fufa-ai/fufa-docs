import { defineRouteMiddleware } from '@astrojs/starlight/route-data';

// Structured data for answer engines, written once here for every page:
// - TechArticle for the page itself, with its group as a breadcrumb.
// - FAQPage built from the page's "## Common questions" section (### question, then the answer).
// - A link to the page's plain-markdown copy at `<path>.md`.

const SITE = 'https://docs.fufa.ai';
const GROUP_LABELS: Record<string, string> = {
	start: 'Start',
	channels: 'Channels',
	inbox: 'Inbox',
	contacts: 'Contacts',
	campaigns: 'Campaigns',
	agents: 'Agents',
	workflows: 'Workflows',
	commerce: 'Commerce',
	workspace: 'Workspace',
};

/** Questions and answers from the "## Common questions" section, as plain text. */
export function faqFromMarkdown(body: string): { q: string; a: string }[] {
	const section = body.split(/^## Common questions\s*$/m)[1];
	if (!section) return [];
	const until = section.split(/^## /m)[0];
	return until
		.split(/^### /m)
		.slice(1)
		.map((block) => {
			const [q, ...rest] = block.split('\n');
			const a = plain(rest.join('\n'));
			return { q: q.trim(), a };
		})
		.filter((x) => x.q && x.a);
}

/** Markdown to readable plain text for JSON-LD. */
export function plain(md: string): string {
	return md
		.replace(/```[\s\S]*?```/g, '')
		.replace(/:::\w+(\[[^\]]*\])?|:::/g, '')
		.replace(/!\[[^\]]*\]\([^)]*\)/g, '')
		.replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
		.replace(/[*_`>#]/g, '')
		.replace(/\s+/g, ' ')
		.trim();
}

export const onRequest = defineRouteMiddleware((context) => {
	const route = context.locals.starlightRoute;
	const { entry } = route;
	const id = entry.id === 'index' ? '' : entry.id;
	const url = `${SITE}/${id ? `${id}/` : ''}`;
	const title = entry.data.title;
	const description = entry.data.description ?? '';
	const group = id.split('/')[0];

	const graph: Record<string, unknown>[] = [
		{
			'@type': 'TechArticle',
			'@id': `${url}#article`,
			headline: title,
			description,
			url,
			inLanguage: 'en',
			...(route.lastUpdated ? { dateModified: route.lastUpdated.toISOString() } : {}),
			isPartOf: { '@type': 'WebSite', name: 'Fufa Docs', url: `${SITE}/` },
			about: { '@type': 'SoftwareApplication', name: 'Fufa', applicationCategory: 'BusinessApplication', url: 'https://www.fufa.ai' },
			publisher: { '@type': 'Organization', name: 'Fufa', url: 'https://www.fufa.ai', logo: `${SITE}/favicon.png` },
		},
	];
	if (id && GROUP_LABELS[group]) {
		graph.push({
			'@type': 'BreadcrumbList',
			itemListElement: [
				{ '@type': 'ListItem', position: 1, name: 'Fufa Docs', item: `${SITE}/` },
				{ '@type': 'ListItem', position: 2, name: GROUP_LABELS[group] },
				{ '@type': 'ListItem', position: 3, name: title, item: url },
			],
		});
	}
	const faq = faqFromMarkdown(entry.body ?? '');
	if (faq.length) {
		graph.push({
			'@type': 'FAQPage',
			mainEntity: faq.map(({ q, a }) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })),
		});
	}

	route.head.push(
		{ tag: 'script', attrs: { type: 'application/ld+json' }, content: JSON.stringify({ '@context': 'https://schema.org', '@graph': graph }) },
		{ tag: 'link', attrs: { rel: 'alternate', type: 'text/markdown', href: `/${id || 'index'}.md` } },
	);
});
