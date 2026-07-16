// Loads every study document under src/content/studies at build time.
const modules = import.meta.glob('../content/studies/**/*.json', { eager: true });

export function bookSlug(book) {
  return String(book).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

export function getAllStudies() {
  return Object.values(modules)
    .map((m) => m.default ?? m)
    .sort((a, b) => {
      if (a.book === b.book) {
        return (a.section?.order ?? 0) - (b.section?.order ?? 0);
      }
      return String(a.book).localeCompare(String(b.book));
    });
}

// Returns [{ book, slug, studies: [...] }, ...] grouped for navigation.
export function getBooks() {
  const map = new Map();
  for (const study of getAllStudies()) {
    if (!map.has(study.book)) {
      map.set(study.book, { book: study.book, slug: bookSlug(study.book), studies: [] });
    }
    map.get(study.book).studies.push(study);
  }
  return Array.from(map.values());
}
