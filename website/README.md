# Church of the First Gift website

The website lives in [`docs/`](../docs/index.html) and is ready for GitHub Pages. It uses ordinary HTML, CSS, JavaScript, local artwork, and system fonts. No Node packages, framework, database, API keys, tracking, or paid hosting are required.

**Church of the First Gift** names the church. **The Unfolding** names its origin story. The original booklet and film remain available under their founding-edition titles.

## GitHub Pages hosting

The intended publishing source is **Deploy from a branch → main → /docs** in the repository's **Settings → Pages**. The `.nojekyll` file lets GitHub serve the built files directly. After the Pages build completes, the project address is:

<https://thescogg.github.io/the-unfolding/>

The repository slug remains `the-unfolding` to preserve existing links. A custom domain can be configured separately if desired; no domain is registered or assumed by this source.

## Edit and rebuild

1. Edit the layout and fixed website copy in [`index.template.html`](index.template.html).
2. Edit the story in [`founding-story/README.md`](../founding-story/README.md) and the FAQ in [`faq/README.md`](../faq/README.md). These two sections are generated from their canonical Markdown source.
3. Edit [`docs/styles.css`](../docs/styles.css) or [`docs/site.js`](../docs/site.js) for styles and interactions.
4. Run this from the repository root using Python 3:

```sh
python3 scripts/build_site.py
```

5. Commit the updated source and generated `docs/` files to `main`. GitHub Pages republishes the site from that directory.

To preview locally:

```sh
python3 -m http.server 8765 --directory docs
```

Open `http://localhost:8765` and stop the server with Ctrl+C when finished. Relative paths also support the `/the-unfolding/` project URL. The generated `docs/index.html` is committed so contributors do not need a build environment to host a copy.

## Interactions and accessibility

- The FAQ uses native disclosure elements and remains available without JavaScript.
- With JavaScript disabled, all three interpretations are visible. With JavaScript enabled, they become keyboard-accessible tabs supporting arrow keys, Home, and End.
- The optional attention timer supports start, pause, continue, reset, and completion without accounts or saved data.
- Mobile navigation supports keyboard operation and Escape to close.
- The page respects reduced-motion settings and includes a skip link and visible focus styles.
- The 42-second painted film has native playback controls, English WebVTT captions, a painted poster, a transcript and visual-description link, and a download fallback. Narration uses Daniel, a stock synthetic voice. The film loads from the public v0.2.0 GitHub release when the visitor chooses playback.
- The site builder copies the poster and captions from `art/film/painted/` into `docs/assets/`.

The page adds no analytics or forms. GitHub Pages and GitHub's media service have their own infrastructure logging and policies.

Text and original art follow CC BY-SA 4.0 where applicable rights are held; software scripts and styles follow MIT. See [`LICENSE.md`](../LICENSE.md).
