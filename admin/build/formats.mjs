// The bridge from build.py to the API's formats.js: the same file a reader's browser runs makes this site's markdown
// scripts and semantic graphs, so the two cannot drift. stdin: [{ key, storyboard, cast, props, url, castHref }];
// stdout: { key: { errors, md, graph, stats } }.   node admin/build/formats.mjs PATH/TO/formats.js
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const F = require(process.argv[2]);
let input = '';
process.stdin.setEncoding('utf8');
for await (const chunk of process.stdin) input += chunk;
const out = {};
for (const job of JSON.parse(input)) {
  const opts = { url: job.url, castHref: job.castHref, props: job.props };
  out[job.key] = { errors: F.validate(job.storyboard, job.cast, opts), md: F.toMarkdown(job.storyboard, job.cast, opts),
    graph: F.toGraph(job.storyboard, job.cast, Object.assign({ seriesTitle: job.seriesTitle }, opts)), stats: F.stats(job.storyboard),
    texts: job.storyboard.scenes.map((sc) => F.toText(sc, job.cast)), version: F.VERSION };
}
process.stdout.write(JSON.stringify(out));
