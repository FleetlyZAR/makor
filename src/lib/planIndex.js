// Build-time reading plan indexes for the Live in the Word page (/plan/).
// Each index is the full ordered list of COMMITTED studies only, so a
// downloaded calendar always points at pages that exist. Every deploy
// regenerates these, so new studies flow into the plan automatically.
// Item shape consumed by the plan page: { title, ref, summary, url }.
import { getAllStudies, bookSlug } from './studies.js';
import { books } from '../data/plan.js';

const SITE = 'https://makor.co.za';

// Canonical position of every book, from the canon list.
const CANON_POS = new Map(books.map((b, i) => [b.name, i]));

// Book level chronological ordering: the rough order the events happened.
// Within a book, studies keep their section order. This is an honest
// approximation at book level; parallel accounts (Kings and Chronicles,
// the four Gospels) sit adjacent rather than interleaved verse by verse.
const CHRONOLOGICAL_ORDER = [
  'Genesis', 'Job', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy',
  'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Chronicles',
  'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon',
  '1 Kings', '2 Kings', '2 Chronicles',
  'Obadiah', 'Joel', 'Jonah', 'Amos', 'Hosea', 'Isaiah', 'Micah',
  'Nahum', 'Zephaniah', 'Habakkuk', 'Jeremiah', 'Lamentations',
  'Ezekiel', 'Daniel', 'Ezra', 'Haggai', 'Zechariah', 'Esther',
  'Nehemiah', 'Malachi',
  'Matthew', 'Mark', 'Luke', 'John', 'Acts',
  'James', 'Galatians', '1 Thessalonians', '2 Thessalonians',
  '1 Corinthians', '2 Corinthians', 'Romans', 'Colossians', 'Philemon',
  'Ephesians', 'Philippians', '1 Timothy', 'Titus', '2 Timothy',
  '1 Peter', '2 Peter', 'Hebrews', 'Jude',
  '1 John', '2 John', '3 John', 'Revelation',
];
const CHRONO_POS = new Map(CHRONOLOGICAL_ORDER.map((b, i) => [b, i]));

// Multi-track: a little from several parts of the Bible each day.
// Four streams, each read canonically within itself, interleaved so that
// all four finish together. Consuming the array in order therefore cycles
// through an Old Testament story, a psalm or wisdom passage, a Gospel
// scene, and a letter.
const WISDOM = new Set(['Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon']);
const GOSPELS_ACTS = new Set(['Matthew', 'Mark', 'Luke', 'John', 'Acts']);
function trackOf(book) {
  if (WISDOM.has(book)) return 1; // wisdom and psalms
  if (GOSPELS_ACTS.has(book)) return 2; // Gospels and Acts
  const pos = CANON_POS.get(book) ?? 0;
  if (pos >= CANON_POS.get('Romans')) return 3; // letters and Revelation
  return 0; // Old Testament story and prophets
}

function toItem(s) {
  return {
    title: s.section?.title || '',
    ref: s.section?.passageRef || '',
    summary: s.section?.thesis || '',
    url: `${SITE}/${bookSlug(s.book)}/${s.section?.slug}/`,
  };
}

function byBookOrder(posMap) {
  return (a, b) => {
    const pa = posMap.get(a.book) ?? 999;
    const pb = posMap.get(b.book) ?? 999;
    if (pa !== pb) return pa - pb;
    return (a.section?.order ?? 0) - (b.section?.order ?? 0);
  };
}

export function buildPlanIndex(order) {
  const studies = getAllStudies();

  if (order === 'canonical') {
    return studies.slice().sort(byBookOrder(CANON_POS)).map(toItem);
  }

  if (order === 'chronological') {
    return studies.slice().sort(byBookOrder(CHRONO_POS)).map(toItem);
  }

  // multitrack (default)
  const tracks = [[], [], [], []];
  for (const s of studies.slice().sort(byBookOrder(CANON_POS))) {
    tracks[trackOf(s.book)].push(s);
  }
  const totals = tracks.map((t) => t.length);
  const taken = [0, 0, 0, 0];
  const out = [];
  const n = totals.reduce((a, b) => a + b, 0);
  for (let i = 0; i < n; i++) {
    // pick the track that is furthest behind its fair share
    let pick = -1, best = Infinity;
    for (let t = 0; t < 4; t++) {
      if (taken[t] >= totals[t]) continue;
      const ratio = totals[t] ? taken[t] / totals[t] : 1;
      if (ratio < best) { best = ratio; pick = t; }
    }
    if (pick < 0) break;
    out.push(toItem(tracks[pick][taken[pick]++]));
  }
  return out;
}

export function planIndexResponse(order) {
  return new Response(JSON.stringify(buildPlanIndex(order)), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}
