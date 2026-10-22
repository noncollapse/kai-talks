import { spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const require = createRequire(import.meta.url)
const cli = join(dirname(require.resolve('@slidev/cli/package.json')), 'bin/slidev.mjs')
const [command = 'list', ...args] = process.argv.slice(2)

function discoverTalks() {
  return readdirSync(join(root, 'talks'), { withFileTypes: true })
    .filter(entry => entry.isDirectory() && existsSync(join(root, 'talks', entry.name, 'slides.md')))
    .map(({ name: slug }) => {
      if (!/^[a-z0-9][a-z0-9_-]*$/.test(slug))
        throw new Error(`Use lowercase letters, numbers, underscores or hyphens for talk directories: ${slug}`)
      const directory = join(root, 'talks', slug)
      const metadataPath = join(directory, 'talk.json')
      const metadata = existsSync(metadataPath) ? JSON.parse(readFileSync(metadataPath, 'utf8')) : {}
      const { title = slug, description = '', draft = false, label = 'Talk', kind = 'Research talk', topics = [], paper = '', order = 100 } = metadata
      if (typeof title !== 'string' || typeof description !== 'string' || typeof draft !== 'boolean')
        throw new Error(`Invalid title, description or draft in ${metadataPath}`)
      if (typeof label !== 'string' || typeof kind !== 'string' || !Array.isArray(topics) || topics.some(topic => typeof topic !== 'string') || typeof paper !== 'string' || !Number.isFinite(order))
        throw new Error(`Invalid archive metadata in ${metadataPath}`)
      if (paper && !/^https:\/\//.test(paper))
        throw new Error(`Use an HTTPS paper URL in ${metadataPath}`)
      return { slug, directory, title, description, draft, label, kind, topics, paper, order }
    })
    .sort((a, b) => a.order - b.order || a.slug.localeCompare(b.slug))
}

function runSlidev(talk, options) {
  const result = spawnSync(process.execPath, [cli, ...options], {
    cwd: talk.directory,
    stdio: 'inherit',
  })
  if (result.error) throw result.error
  if (result.status !== 0) process.exit(result.status ?? 1)
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  })[char])
}

function writeIndex(talks, output) {
  const template = readFileSync(join(root, 'scripts', 'index.html'), 'utf8')
  const entries = talks.map((talk, index) => `
      <li class="talk-card" data-talk="${talk.slug}">
        <article aria-labelledby="title-${talk.slug}">
          <div class="card-meta"><span class="talk-label">${escapeHtml(talk.label)}</span><span>${escapeHtml(talk.kind)}</span><span class="card-number" aria-hidden="true">${String(index + 1).padStart(2, '0')}</span></div>
          <h3 id="title-${talk.slug}"><a href="./${talk.slug}/">${escapeHtml(talk.title)}</a></h3>
          <p class="talk-description">${escapeHtml(talk.description)}</p>
          <ul class="topics" aria-label="Topics">${talk.topics.map(topic => `<li>${escapeHtml(topic)}</li>`).join('')}</ul>
          <div class="card-links">
            <a class="open-talk" href="./${talk.slug}/" aria-label="Open talk slides: ${escapeHtml(talk.title)}">Open talk slides <span aria-hidden="true">↗</span></a>
            <div class="references"><a href="https://github.com/noncollapse/kai-talks/tree/main/talks/${talk.slug}" aria-label="Abstract and contents: ${escapeHtml(talk.label)}">Abstract <span aria-hidden="true">↗</span></a>${talk.paper ? `<a href="${escapeHtml(talk.paper)}" aria-label="Paper: ${escapeHtml(talk.label)}">Paper <span aria-hidden="true">↗</span></a>` : ''}</div>
          </div>
        </article>
      </li>`).join('')
  // Preserve links into the original deck, including named Slidev routes.
  const legacyRedirect = talks.some(talk => talk.slug === 'llm_short_course')
    ? `<script>
    if (location.hash.startsWith('#/')) {
      location.replace('./llm_short_course/' + location.search + location.hash)
    }
  </script>`
    : ''
  writeFileSync(join(output, 'index.html'), template.replace('<!-- talks -->', entries).replace('<!-- legacy-redirect -->', legacyRedirect).replaceAll('<!-- talk-count -->', String(talks.length).padStart(2, '0')))
  writeFileSync(join(output, '.nojekyll'), '')
}

try {
  if (!['list', 'index', 'dev', 'build', 'export'].includes(command))
    throw new Error(`Unknown command: ${command}. Use list, index, dev, build or export.`)

  const talks = discoverTalks()
  if (!talks.length) throw new Error('No slides.md files found under talks/.')
  if (command === 'list') {
    for (const talk of talks)
      console.log(`${talk.slug}${talk.draft ? ' [draft]' : ''}\n  ${talk.title}`)
  }
  else if (command === 'index') {
    if (args.length) throw new Error('Usage: npm run build:index')
    const output = join(root, 'dist')
    mkdirSync(output, { recursive: true })
    writeIndex(talks.filter(talk => !talk.draft), output)
    console.log(`Built talk index in ${output}`)
  }
  else {
    const slug = args[0] && !args[0].startsWith('-') ? args.shift() : undefined
    const selected = slug ? talks.find(talk => talk.slug === slug) : undefined
    if (slug && !selected)
      throw new Error(`Unknown talk: ${slug}. Available: ${talks.map(talk => talk.slug).join(', ')}`)

    if (command === 'build') {
      const includeDrafts = args.includes('--include-drafts')
      if (args.some(arg => arg !== '--include-drafts'))
        throw new Error('Usage: npm run build -- [talk] [--include-drafts]. Set BASE_PATH to change the URL prefix.')
      const targets = (selected ? [selected] : talks).filter(talk => includeDrafts || !talk.draft)
      if (!targets.length) throw new Error('No published talks selected. Use --include-drafts for a local draft build.')
      const base = `/${(process.env.BASE_PATH || '').replace(/^\/+|\/+$/g, '')}/`.replace(/^\/\/$/, '/')
      const output = join(root, 'dist')
      // Rebuild from scratch so a previous draft build cannot leak into a public build.
      rmSync(output, { recursive: true, force: true })
      mkdirSync(output, { recursive: true })
      for (const talk of targets) {
        console.log(`Building ${talk.slug}`)
        runSlidev(talk, ['build', 'slides.md', '--base', `${base}${talk.slug}/`, '--out', join(output, talk.slug), '--download', 'false'])
      }
      writeIndex(targets, output)
      console.log(`Built ${targets.length} talk(s) and index in ${output}`)
    }
    else {
      const talk = selected ?? talks.find(talk => talk.slug === 'llm_short_course') ?? talks[0]
      runSlidev(talk, command === 'dev' ? ['slides.md', ...args] : ['export', 'slides.md', ...args])
    }
  }
}
catch (error) {
  console.error(error.message)
  process.exitCode = 1
}
