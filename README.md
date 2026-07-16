# Makor

A Christ centred Scripture study site. Each study is a JSON file under
`src/content/studies/<book>/NN-slug.json`, matching the study pipeline schema.
The site renders every study to a static page, including tappable lexicon words
and all nine study sections.

## Run locally
```
npm install
npm run dev
```
Then open the address it prints (usually http://localhost:4321).

## Build
```
npm run build
```
Output goes to `dist/`.

## Publish a study
Drop the JSON into `src/content/studies/`, then:
```
git add .
git commit -m "Add <study> study"
git push
```
Cloudflare Pages rebuilds and republishes automatically.

See "Makor-setup-and-publish-guide.md" for the full step by step, including
first time setup and connecting the domain.
