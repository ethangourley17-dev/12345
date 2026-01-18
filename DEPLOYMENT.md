# Deployment Guide

This application is now ready to be deployed to the web! You have multiple deployment options configured.

## Quick Deploy Options

### 🚀 Fastest: One-Click Deploy

Choose your preferred platform and click the button:

**Netlify (Recommended):**
- Click: [![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start)
- Set `API_KEY` environment variable in Netlify dashboard

**Vercel:**
- Click: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)
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

4. Your app will be live at: `https://YOUR_USERNAME.github.io/YOUR_REPOSITORY/`

**Note:** If deploying to a repository (not username.github.io), uncomment and update the `base` line in `vite.config.ts`:
```typescript
base: '/your-repository-name/',
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

## Security Considerations

⚠️ **Important:** This is a client-side application where the API key is embedded in the built JavaScript files and will be visible in the browser. This means:

- The API key can be extracted by anyone viewing the deployed site
- It's recommended to use API key restrictions in the Google Cloud Console
- For production applications, consider implementing a backend API proxy to keep keys secure
- Monitor your API usage regularly to detect any abuse

To restrict your Gemini API key:
1. Go to https://aistudio.google.com/app/apikey
2. Click on your API key
3. Set up restrictions (e.g., HTTP referrer restrictions for your domain)

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
