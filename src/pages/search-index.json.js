// Build-time search index: every movement of all 66 books, with full BSB text
// for the studies that exist. Served as a static JSON file, fetched lazily by
// the header search. Lexical tokens {{key|word}} are reduced to the plain word.
import { getAllStudies, bookSlug } from '../lib/studies.js';
import { books, plans } from '../data/plan.js';

function stripTokens(s) {
  return String(s || '').replace(/\{\{[^|}]+\|([^}]*)\}\}/g, '$1');
}

export function GET() {
  const studies = getAllStudies();
  const textByKey = {};
  const availByBook = {};
  for (const s of studies) {
    (availByBook[s.book] ||= new Set()).add(s.section.slug);
    let t = '';
    for (const u of s.text?.units || []) {
      for (const v of u.verses || []) t += ' ' + stripTokens(v.text);
    }
    textByKey[s.book + '||' + s.section.slug] = t.replace(/\s+/g, ' ').trim();
  }

  const entries = [];
  let i = 0;
  for (const b of books) {
    const bslug = bookSlug(b.name);
    for (const m of plans[b.name] || []) {
      const available = (availByBook[b.name] || new Set()).has(m.slug);
      entries.push({
        i: i++,
        book: b.name,
        bookSlug: bslug,
        title: m.title,
        ref: m.ref,
        slug: m.slug,
        order: m.order,
        url: `/${bslug}/${m.slug}/`,
        available,
        text: available ? textByKey[b.name + '||' + m.slug] || '' : '',
      });
    }
  }

  return new Response(JSON.stringify(entries), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}
