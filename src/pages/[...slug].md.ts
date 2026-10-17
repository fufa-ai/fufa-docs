import type { APIRoute, GetStaticPaths } from 'astro';
import { getCollection } from 'astro:content';

// Every page as plain markdown at `<path>.md`, so an agent can fetch exactly one task.
export const getStaticPaths = (async () => {
	const docs = await getCollection('docs');
	return docs.map((entry) => ({ params: { slug: entry.id }, props: { entry } }));
}) satisfies GetStaticPaths;

export const GET: APIRoute = ({ props }) => {
	const { entry } = props as { entry: Awaited<ReturnType<typeof getCollection<'docs'>>>[number] };
	const url = `https://docs.fufa.ai/${entry.id === 'index' ? '' : `${entry.id}/`}`;
	const body = `# ${entry.data.title}\n\n> ${entry.data.description ?? ''}\n\nSource: ${url}\n\n${(entry.body ?? '').trim()}\n`;
	return new Response(body, { headers: { 'Content-Type': 'text/markdown; charset=utf-8' } });
};
