# Static site verification

This prototype has no compilation step. Its test and build commands verify the static output at the repository root. Existing page content and interactions are outside this verification change.

## Requirements

- SITE-QA-1: `pnpm test` executes real checks, fails on a failed check, and requires no network or third-party Python packages.
- SITE-QA-2: Every root HTML page has an HTML doctype, a nonempty document language and title, exactly one main landmark, and no duplicate IDs.
- SITE-QA-3: Local `href` and `src` targets resolve to existing files within the site root. Named fragments in HTML or SVG targets resolve to an ID. Query strings do not hide missing paths. Remote URLs and non-file schemes are not fetched.
- SITE-QA-3a: This checker does not support `<base href>`; it fails explicitly if one is introduced so document-relative checks cannot silently pass for the wrong URL. `file:` links fail because they refer to a local machine rather than deployed static output.
- SITE-QA-4: Relative and root-relative links resolve correctly. A path must not escape the site root, including through symlinks. Declared path case must match disk entries even on a case-insensitive filesystem.
- SITE-QA-5: `pnpm build` checks the static output and the syntax of shared `js/site.js`; it does not claim to compile a bundle.
- SITE-QA-6: CI runs test and build on pull requests, pushes to main, and manual validation. The job has a finite timeout, read-only permissions and pinned official actions. It performs no deployment.
- SITE-QA-7: Independent temporary fixtures demonstrate that the checker fails for missing files, missing fragments, duplicate IDs, missing document structure, empty sites and path escapes. Fixtures do not alter the real pages.
- SITE-QA-8: Local and CI validation use the declared pnpm version.

## Verification

Run `pnpm test` and `pnpm build` using Node 22, pnpm 10.30.3 and Python 3.12. No installation is necessary: the checker uses Python's standard library and JavaScript syntax checking uses Node. `pnpm test` runs the checker's fault fixtures as well as the real pages.

The checker covers root HTML pages and their explicit `href`/`src` targets. It does not execute browser interactions, syntax-check inline scripts, scan CSS URLs or `srcset`, validate remote resources, assess visual layout, or establish WCAG conformance. Existing accessibility automation supplies separate evidence. A successful static check alone does not establish production readiness.
