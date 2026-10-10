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

## Change a role Clawd

A script makes the six role Clawds: admin, accountant, marketing, CEO, coder and engineer.

```sh
python3 tools/make_role_clawds.py
```

Change the script, then run it. It writes the six files in `animations/` again.

## Change a job Clawd

A second script makes the 20 job Clawds. Each job is one an AI agent can do, from researcher to tutor.

```sh
python3 tools/make_job_clawds.py
```

It uses the parts of Clawd from `tools/make_role_clawds.py`. The list of jobs is `JOBS`, at the end of the script.

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
