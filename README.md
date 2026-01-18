<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/drive/1PZeAd8WzVS-Z8mPg-_lf0yf_y2BY6lHi

## Run Locally

**Prerequisites:**  Node.js (v18 or higher)

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env.local
   ```
   Then edit `.env.local` and set your Gemini API key:
   ```
   API_KEY=your_gemini_api_key_here
   ```
   Get your API key from: https://aistudio.google.com/app/apikey

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open http://localhost:5173 in your browser

## Deploy to Web

This app can be deployed to various platforms. Choose the one that fits your needs:

### Option 1: Deploy to Netlify (Recommended)

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start)

**Manual Deployment:**
1. Install Netlify CLI: `npm install -g netlify-cli`
2. Build the app: `npm run build`
3. Deploy: `netlify deploy --prod --dir=dist`
4. Set environment variable `API_KEY` in Netlify dashboard

**Configuration:** The `netlify.toml` file is already configured.

### Option 2: Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

**Manual Deployment:**
1. Install Vercel CLI: `npm install -g vercel`
2. Run: `vercel`
3. Set environment variable `API_KEY` in Vercel dashboard

**Configuration:** The `vercel.json` file is already configured.

### Option 3: Deploy to Cloudflare Pages

1. Install Wrangler: `npm install -g wrangler`
2. Login: `wrangler login`
3. Build: `npm run build`
4. Deploy: `wrangler pages deploy dist`
5. Set environment variable `API_KEY` in Cloudflare dashboard

**Configuration:** The `wrangler.json` file is already configured.

### Option 4: Deploy to GitHub Pages

1. Go to your repository Settings > Pages
2. Set Source to "GitHub Actions"
3. Add `API_KEY` secret in Settings > Secrets and variables > Actions
4. Push to `main` branch or manually trigger the workflow

The deployment workflow is configured in `.github/workflows/deploy.yml`

### Environment Variables

All deployment platforms require setting the `API_KEY` environment variable:
- Get your API key from: https://aistudio.google.com/app/apikey
- Set it in your hosting platform's dashboard or CLI

## Build for Production

```bash
npm run build
```

The optimized production build will be in the `dist` directory.
