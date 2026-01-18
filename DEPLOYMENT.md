# Deployment Guide

This application is now ready to be deployed to the web! You have multiple deployment options configured.

## Quick Deploy Options

### 🚀 Fastest: One-Click Deploy

Choose your preferred platform and click the button:

**Netlify (Recommended):**
- Click: [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/ethangourley17-dev/12345)
- Set `API_KEY` environment variable in Netlify dashboard

**Vercel:**
- Click: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/ethangourley17-dev/12345)
- Set `API_KEY` environment variable in Vercel dashboard

### 📦 GitHub Pages (Automated)

GitHub Pages deployment is configured with GitHub Actions:

1. Enable GitHub Pages:
   - Go to repository **Settings → Pages**
   - Set **Source** to "GitHub Actions"

2. Add API Key Secret:
   - Go to **Settings → Secrets and variables → Actions**
   - Click **New repository secret**
   - Name: `API_KEY`
   - Value: Your Gemini API key from https://aistudio.google.com/app/apikey

3. Trigger Deployment:
   - Push to `main` branch, OR
   - Go to **Actions** tab → **Deploy to GitHub Pages** → **Run workflow**

4. Your app will be live at: `https://ethangourley17-dev.github.io/12345/`

**Note:** If deploying to a repository (not username.github.io), uncomment the `base` line in `vite.config.ts`:
```typescript
base: '/12345/',
```

## Platform-Specific Instructions

### Netlify

**Via CLI:**
```bash
npm install -g netlify-cli
npm run build
netlify deploy --prod --dir=dist
```

**Configuration:** `netlify.toml` is configured with:
- Build command: `npm run build`
- Publish directory: `dist`
- SPA routing redirects

### Vercel

**Via CLI:**
```bash
npm install -g vercel
vercel
```

**Configuration:** `vercel.json` is configured with:
- Build command: `npm run build`
- Output directory: `dist`
- SPA routing rewrites

### Cloudflare Pages

**Via CLI:**
```bash
npm install -g wrangler
wrangler login
npm run build
wrangler pages deploy dist
```

**Configuration:** `wrangler.json` is configured with:
- Name: `stake-affiliate-ai`
- Output directory: `dist`

## Environment Variables

All platforms require the `API_KEY` environment variable:
- **Value:** Your Gemini API key
- **Get key from:** https://aistudio.google.com/app/apikey

### Setting Environment Variables:

**Netlify:**
- Dashboard → Site settings → Environment variables → Add variable

**Vercel:**
- Dashboard → Settings → Environment Variables → Add

**Cloudflare:**
- Dashboard → Pages → Settings → Environment variables → Add variable

**GitHub Pages:**
- Repository Settings → Secrets and variables → Actions → New repository secret

## Verification

After deployment:
1. Visit your deployed URL
2. The app should load with the StakeAffiliate AI Engine interface
3. If you see an API key prompt, ensure the `API_KEY` environment variable is set correctly
4. Check your platform's deployment logs if issues occur

## Files Created for Deployment

- `.github/workflows/deploy.yml` - GitHub Actions workflow for GitHub Pages
- `netlify.toml` - Netlify configuration
- `vercel.json` - Vercel configuration
- `wrangler.json` - Cloudflare Pages configuration (already existed)
- `_redirects` - SPA routing for Netlify
- `.env.example` - Template for local environment variables

## Support

For deployment issues:
- **Netlify:** https://docs.netlify.com
- **Vercel:** https://vercel.com/docs
- **Cloudflare Pages:** https://developers.cloudflare.com/pages
- **GitHub Pages:** https://docs.github.com/pages
