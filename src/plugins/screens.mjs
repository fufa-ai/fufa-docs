// Screenshots in src/assets/screens are captured at 2x (scripts/capture).
// Show each one at the size it has on screen in the app, so a dialog reads as a
// dialog rather than being stretched to the column width.
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const pngWidth = (file) => readFileSync(file).subarray(0, 24).readUInt32BE(16);

/** A hast plugin for Astro's markdown processor (satteri). */
const screensPlugin = {
	name: 'fufa-screens',
	element: {
		filter: ['img'],
		visit(node, ctx) {
			const src = String(node.properties?.src ?? '');
			if (!ctx.fileURL || !src.includes('assets/screens/') || !src.endsWith('.png')) return;
			try {
				const width = Math.round(pngWidth(resolve(dirname(fileURLToPath(ctx.fileURL)), decodeURI(src))) / 2);
				ctx.setProperty(node, 'style', `width: min(100%, ${width}px)`);
				ctx.setProperty(node, 'className', ['fd-screen']);
			} catch {
				// Missing file: let Astro report it.
			}
		},
	},
};

/** Adds the plugin to the configured processor, the way Starlight adds its own. */
export default function screens() {
	return {
		name: 'fufa-screens',
		hooks: {
			'astro:config:setup': ({ config, logger }) => {
				const plugins = config.markdown?.processor?.options?.hastPlugins;
				if (Array.isArray(plugins)) plugins.push(screensPlugin);
				else logger.warn('Markdown processor has no hastPlugins; screenshots keep their full size.');
			},
		},
	};
}
