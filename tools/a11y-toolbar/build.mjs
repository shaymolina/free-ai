// Builds the toolbar: an ES module package (dist/) and the drop-in script used by the site.
import { build } from 'esbuild';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const site = resolve(here, '../../site/assets');

/** Loads `*.css?raw` imports as plain strings (the same convention Vite/Vitest use). */
const rawCss = {
  name: 'raw-css',
  setup(b) {
    b.onResolve({ filter: /\.css\?raw$/ }, (args) => ({
      path: resolve(args.resolveDir, args.path.replace(/\?raw$/, '')),
      namespace: 'raw-css',
    }));
    b.onLoad({ filter: /.*/, namespace: 'raw-css' }, async (args) => ({
      contents: (await readFile(args.path, 'utf8')).replace(/\/\*[\s\S]*?\*\//g, '').replace(/\n\s*\n/g, '\n'),
      loader: 'text',
    }));
  },
};

const common = { bundle: true, minify: true, target: ['es2020', 'safari14'], plugins: [rawCss], legalComments: 'none' };

await build({ ...common, entryPoints: [resolve(here, 'src/index.ts')], format: 'esm', outfile: resolve(here, 'dist/index.js'), sourcemap: true });
await build({ ...common, entryPoints: [resolve(here, 'src/auto.ts')], format: 'iife', outfile: resolve(site, 'js/a11y-toolbar.js') });

await mkdir(resolve(here, 'dist'), { recursive: true });
const css = (await Promise.all(['accessibility-preferences.css', 'accessibility-toolbar.css']
  .map((f) => readFile(resolve(here, 'src/styles', f), 'utf8')))).join('\n');
await writeFile(resolve(here, 'dist/styles.css'), css);
console.log('a11y-toolbar: built dist/ and site/assets/js/a11y-toolbar.js');
