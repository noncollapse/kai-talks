import { cp, mkdir, readdir, rm, writeFile } from 'node:fs/promises'

const root = new URL('../', import.meta.url)
const output = new URL('.cloudflare-assets/', root)
// This directory contains generated deployment assets only.
await rm(output, { recursive: true, force: true })
await mkdir(output, { recursive: true })
await cp(new URL('dist/', root), new URL('kai-talks/', output), { recursive: true })
const decks = (await readdir(new URL('dist/', root), { withFileTypes: true }))
  .filter(entry => entry.isDirectory()).map(entry => entry.name)
const paths = ['/kai-talks/', ...decks.map(slug => `/kai-talks/${slug}/`)]
await writeFile(new URL('_headers', output), paths.map(path =>
  `${path}\n  Link: <https://kaiye.noncollapse.com${path}>; rel="canonical"\n`
).join('\n'))
await writeFile(new URL('_redirects', output), '/kai-talks /kai-talks/ 301\n')
await writeFile(new URL('kai-talks/sitemap.xml', output),
  `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${paths.map(path => `  <url><loc>https://kaiye.noncollapse.com${path}</loc></url>`).join('\n')}\n</urlset>\n`)
console.log('Prepared Cloudflare assets at /kai-talks/ without changing the decks.')
