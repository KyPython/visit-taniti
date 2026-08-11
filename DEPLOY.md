# Visit Taniti — deploy

Live: https://visit-taniti-seven.vercel.app/

## GitHub repo

Code for Vercel/GitHub: **https://github.com/KyPython/visit-taniti**

### Update the live site

```bash
cd ~/visit-taniti
# edit files, or sync from monorepo then:
git add -A && git commit -m "Update site" && git push
```

If Vercel is connected to that repo (Project Settings → Git), push = deploy.

### One-time: connect Vercel ↔ GitHub

1. https://vercel.com (personal Hobby account)
2. Open project `visit-taniti` / `visit-taniti-seven`
3. Settings → Git → Connect → `KyPython/visit-taniti`
4. Framework: Other, no build command, output `.`

### Local

```bash
cd apps/demos/portfolio-labs/taniti-tourism
./start-dev.sh
```
