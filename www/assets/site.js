/* storyboards.sgit.ai: the page's own behaviour. The theme switch (kept in this browser only), the copy buttons, and the
 * exports on a storyboard's page, which hand the page's own data to the kit's export.js (api.storyboards.sgit.ai) so a
 * downloaded panel is the panel on the screen. */
(function () {
  'use strict';
  const KEY = 'storyboards.sgit.ai.theme';
  const root = document.documentElement;
  const dark = () => matchMedia('(prefers-color-scheme: dark)').matches;
  const apply = (t) => { root.dataset.theme = t || (dark() ? 'night' : 'light'); };
  let saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) { /* the default holds */ }
  apply(saved);

  document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('.theme');
    if (btn) {
      const label = () => { btn.textContent = root.dataset.theme === 'night' ? 'light' : 'dark'; };
      label();
      btn.addEventListener('click', () => {
        const t = root.dataset.theme === 'night' ? 'light' : 'night';
        apply(t); label();
        try { localStorage.setItem(KEY, t); } catch (e) { /* this visit only */ }
      });
    }
    document.querySelectorAll('[data-copy]').forEach((b) => b.addEventListener('click', async () => {
      const text = document.querySelector(b.dataset.copy).textContent;
      try { await navigator.clipboard.writeText(text); b.textContent = 'Copied'; } catch (e) { b.textContent = 'Select and copy'; }
      setTimeout(() => { b.textContent = 'Copy'; }, 1600);
    }));
    const ex = document.querySelector('.exports');
    if (ex) exports(ex);
  });

  function exports(box) {
    const data = JSON.parse(document.querySelector('script.sb-data').textContent);
    const sb = data.storyboard, cast = data.cast, slug = sb.slug;
    const current = () => Math.max(0, Math.min(sb.scenes.length - 1, parseInt((location.hash.match(/scene-(\d+)/) || [])[1] || '1', 10) - 1));
    const nn = (i) => String(i + 1).padStart(2, '0');
    const busy = async (b, fn) => {
      const was = b.querySelector('b').textContent;
      b.disabled = true; b.querySelector('b').textContent = 'Drawing…';
      try { await fn(); } catch (e) { alert('The export failed: ' + e.message); } finally { b.disabled = false; b.querySelector('b').textContent = was; }
    };
    const X = () => window.StoryboardExport;
    const jobs = {
      svg: async () => { const i = current(); X().download(await X().svg(sb, cast, i), `${slug}__${nn(i)}.svg`, 'image/svg+xml'); },
      animated: async () => { const i = current(); X().download(await X().svg(sb, cast, i, { animated: true }), `${slug}__${nn(i)}.animated.svg`, 'image/svg+xml'); },
      png: async () => { const i = current(); X().download(await X().image(sb, cast, i), `${slug}__${nn(i)}.png`); },
      jpg: async () => { const i = current(); X().download(await X().image(sb, cast, i, { type: 'image/jpeg' }), `${slug}__${nn(i)}.jpg`); },
      sheet: async () => { X().download(await X().sheet(sb, cast, { cols: 4 }), `${slug}__every-panel.svg`, 'image/svg+xml'); },
    };
    box.querySelectorAll('button[data-export]').forEach((b) => b.addEventListener('click', () => busy(b, jobs[b.dataset.export])));
    const which = box.querySelector('.which');
    if (which) { const show = () => { which.textContent = `panel ${current() + 1} of ${sb.scenes.length}`; }; show(); addEventListener('hashchange', show); setInterval(show, 800); }
  }
})();
