# lottie-clawd

A page that shows Clawd as Lottie animations. Each Clawd is personalized and animated.

**Page:** https://bmeunier1974.github.io/lottie-clawd/

## Add a Clawd

1. Put the Lottie file in `animations/`. Example: `animations/clawd-pirate.json`.
2. Add one entry to `animations/manifest.json`:

   ```json
   {
     "file": "clawd-pirate.json",
     "name": "Pirate Clawd",
     "description": "Clawd with a hat and a patch."
   }
   ```

3. Commit and push to `main`. GitHub Pages publishes the page again.

## See the page on your machine

```sh
python3 -m http.server 8000
```

Then open http://localhost:8000/. The page does not work from a `file://` address, because the browser blocks `fetch` there.

## How it works

- `index.html` reads `animations/manifest.json` and makes one card for each entry.
- [lottie-web](https://github.com/airbnb/lottie-web) 5.12.2 plays the files. It loads from cdnjs.
- There is no build step. GitHub Pages serves `main` from the root folder.

Clawd is the mascot of Claude Code, by Anthropic. This is a fan project.
