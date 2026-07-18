// makor-scripture.mjs
// Offline BSB scripture toolkit for the Makor study pipeline.
// Zero dependencies. Requires Node >= 22.5 (uses built-in node:sqlite).
//
// Data source: helloao "Free Use Bible API" build (BSB, public domain).
// Cross references: open-cross-ref dataset (OpenBible.info), adapted to the API format.
//
// As a module:
//   import { getPassage, getFootnotes, getCrossRefs, listBooks } from "./makor-scripture.mjs";
//
// As a CLI:
//   node makor-scripture.mjs books
//   node makor-scripture.mjs passage "GEN 1:1-2:3"
//   node makor-scripture.mjs footnotes GEN 1
//   node makor-scripture.mjs xrefs "GEN 1:1" --min-score 40 --limit 12
//   node makor-scripture.mjs xrefs "GEN 1:1-2:3" --per-verse 5
//
// Add --pretty to any command for indented JSON.

import { DatabaseSync } from "node:sqlite";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const __dir = dirname(fileURLToPath(import.meta.url));
const DB_PATH = process.env.MAKOR_DB || join(__dir, "makor-scripture.db");

let _db = null;
function db() {
  if (!_db) _db = new DatabaseSync(DB_PATH, { readOnly: true });
  return _db;
}

// ---- book helpers -------------------------------------------------------

let _bookCache = null;
function books() {
  if (!_bookCache) {
    const rows = db()
      .prepare('SELECT id, "order", commonName, name, numberOfChapters FROM book ORDER BY "order"')
      .all();
    _bookCache = { byId: new Map(), list: rows };
    for (const b of rows) _bookCache.byId.set(b.id.toUpperCase(), b);
  }
  return _bookCache;
}

export function listBooks() {
  return books().list.map((b) => ({
    id: b.id,
    order: b.order,
    commonName: b.commonName,
    chapters: b.numberOfChapters,
  }));
}

function commonName(bookId) {
  const b = books().byId.get(String(bookId).toUpperCase());
  return b ? b.commonName : bookId;
}

// Format a reference for display, e.g. "John 1:1" or "Colossians 1:15-16".
function fmtRef(bookId, chapter, verse, endVerse) {
  const base = `${commonName(bookId)} ${chapter}:${verse}`;
  return endVerse && endVerse !== verse ? `${base}-${endVerse}` : base;
}

// ---- reference parsing --------------------------------------------------

// Accepts: "GEN 1:1", "GEN 1:1-3", "GEN 1:1-2:3", "GEN 1", "GEN 1-2".
// Returns { bookId, cStart, vStart, cEnd, vEnd } with nulls meaning whole chapter(s).
export function parseRef(ref) {
  const m = String(ref).trim().match(/^([1-3]?\s?[A-Za-z]+)\s+(\d+)(?::(\d+))?(?:\s*-\s*(?:(\d+):)?(\d+))?$/);
  if (!m) throw new Error(`Cannot parse reference: "${ref}". Use forms like "GEN 1:1", "GEN 1:1-2:3", "GEN 1".`);
  const rawBook = m[1].replace(/\s+/g, "").toUpperCase();
  const b = books().byId.get(rawBook);
  if (!b) throw new Error(`Unknown book code "${rawBook}". Run "books" to list valid codes.`);
  const cStart = Number(m[2]);
  const vStart = m[3] != null ? Number(m[3]) : null;
  let cEnd, vEnd;
  if (m[4] != null && m[5] != null) { cEnd = Number(m[4]); vEnd = Number(m[5]); }      // 1:1-2:3
  else if (m[5] != null) { cEnd = cStart; vEnd = Number(m[5]); }                        // 1:1-3
  else if (m[3] == null && m[5] == null && ref.includes("-")) {                        // 1-2 (chapters)
    const cm = ref.match(/-\s*(\d+)\s*$/); cEnd = cm ? Number(cm[1]) : cStart; vEnd = null;
  } else { cEnd = cStart; vEnd = vStart; }
  return { bookId: b.id, cStart, vStart, cEnd, vEnd };
}

function inRange(chapter, verse, r) {
  // whole-chapter mode (no verses specified)
  if (r.vStart == null) return chapter >= r.cStart && chapter <= r.cEnd;
  const startOk = chapter > r.cStart || (chapter === r.cStart && verse >= r.vStart);
  const endOk = chapter < r.cEnd || (chapter === r.cEnd && verse <= r.vEnd);
  return startOk && endOk;
}

// ---- core queries -------------------------------------------------------

// Every BSB verse of a passage, in order.
export function getPassage(ref) {
  const r = parseRef(ref);
  const rows = db()
    .prepare("SELECT chapter, verse, text FROM verse WHERE bookId=? AND chapter BETWEEN ? AND ? ORDER BY chapter, verse")
    .all(r.bookId, r.cStart, r.cEnd)
    .filter((v) => inRange(v.chapter, v.verse, r));
  return {
    passageRef: `${commonName(r.bookId)} ${r.cStart}${r.vStart != null ? ":" + r.vStart : ""}` +
      (r.cEnd !== r.cStart || (r.vEnd != null && r.vEnd !== r.vStart)
        ? `-${r.cEnd !== r.cStart ? r.cEnd + ":" : ""}${r.vEnd != null ? r.vEnd : ""}` : ""),
    bookId: r.bookId,
    spine: "BSB",
    verses: rows.map((v) => ({ chapter: v.chapter, verse: v.verse, text: v.text })),
  };
}

// BSB footnotes for a chapter (literal renderings, alternates, NT citations).
// Feeds Makor translationNotes and lexicon hints.
export function getFootnotes(bookId, chapter) {
  const b = books().byId.get(String(bookId).toUpperCase());
  if (!b) throw new Error(`Unknown book code "${bookId}".`);
  const rows = db()
    .prepare("SELECT verse, text FROM footnote WHERE bookId=? AND chapter=? ORDER BY verse")
    .all(b.id, Number(chapter));
  return rows.map((f) => ({
    ref: `${commonName(b.id)} ${chapter}:${f.verse}`,
    verse: f.verse,
    note: f.text,
  }));
}

// Scored cross references for a verse or range. Seeds Makor study step 7.
// opts: { minScore=0, limit=null, perVerse=null }
export function getCrossRefs(ref, opts = {}) {
  const r = parseRef(ref);
  const minScore = opts.minScore ?? 0;
  const rows = db()
    .prepare("SELECT chapter, verse, refBookId, refChapter, refVerse, refEndVerse, score FROM xref WHERE bookId=? AND chapter BETWEEN ? AND ? AND score>=? ORDER BY chapter, verse, score DESC")
    .all(r.bookId, r.cStart, r.cEnd, minScore)
    .filter((x) => inRange(x.chapter, x.verse, r));

  const shape = (x) => ({
    from: fmtRef(r.bookId, x.chapter, x.verse),
    ref: fmtRef(x.refBookId, x.refChapter, x.refVerse, x.refEndVerse),
    refBookId: x.refBookId,
    refChapter: x.refChapter,
    refVerse: x.refVerse,
    score: x.score,
  });

  if (opts.perVerse) {
    const byVerse = new Map();
    for (const x of rows) {
      const k = `${x.chapter}:${x.verse}`;
      if (!byVerse.has(k)) byVerse.set(k, []);
      const arr = byVerse.get(k);
      if (arr.length < opts.perVerse) arr.push(shape(x));
    }
    return [...byVerse.values()].flat();
  }
  const out = rows.map(shape);
  return opts.limit ? out.slice(0, opts.limit) : out;
}

// ---- CLI ----------------------------------------------------------------

function flagVal(args, name) {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
}

function main() {
  const [cmd, ...rest] = process.argv.slice(2);
  const pretty = rest.includes("--pretty");
  const emit = (o) => process.stdout.write(JSON.stringify(o, null, pretty ? 2 : 0) + "\n");
  try {
    switch (cmd) {
      case "books": emit(listBooks()); break;
      case "passage": emit(getPassage(rest[0])); break;
      case "footnotes": emit(getFootnotes(rest[0], rest[1])); break;
      case "xrefs": emit(getCrossRefs(rest[0], {
        minScore: flagVal(rest, "--min-score") ? Number(flagVal(rest, "--min-score")) : 0,
        limit: flagVal(rest, "--limit") ? Number(flagVal(rest, "--limit")) : null,
        perVerse: flagVal(rest, "--per-verse") ? Number(flagVal(rest, "--per-verse")) : null,
      })); break;
      default:
        process.stderr.write(
          'Usage:\n' +
          '  node makor-scripture.mjs books\n' +
          '  node makor-scripture.mjs passage "GEN 1:1-2:3" [--pretty]\n' +
          '  node makor-scripture.mjs footnotes GEN 1 [--pretty]\n' +
          '  node makor-scripture.mjs xrefs "GEN 1:1" [--min-score N] [--limit N] [--per-verse N] [--pretty]\n');
        process.exit(cmd ? 1 : 0);
    }
  } catch (e) {
    process.stderr.write("Error: " + e.message + "\n");
    process.exit(1);
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) main();
