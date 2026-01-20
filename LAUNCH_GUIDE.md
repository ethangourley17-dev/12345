# StakeAffiliate AI Engine - Launch Guide

## 🚀 Application Successfully Launched!

This guide provides step-by-step instructions for launching the StakeAffiliate AI Engine application.

## Prerequisites

- **Node.js** (v16 or higher recommended)
- **npm** (comes with Node.js)
- **Gemini API Key** from [Google AI Studio](https://ai.google.dev/)

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

This will install all required packages including:
- React 19
- Vite 6
- TypeScript
- TailwindCSS
- Google Generative AI SDK

### 2. Configure API Key

Create a `.env.local` file in the root directory and add your Gemini API key:

```env
API_KEY=your_api_key_here
```

**Note:** The `.env.local` file is already created with placeholders. Replace `your_api_key_here` with your actual API key.

### 3. Launch the Development Server

```bash
npm run dev
```

The application will start on `http://localhost:5173/`

### 4. Access the Application

Open your browser and navigate to:
```
http://localhost:5173/
```

## Available Scripts

- **`npm run dev`** - Start the development server with hot reload
- **`npm run build`** - Build the application for production
- **`npm run preview`** - Preview the production build locally

## Application Features

The StakeAffiliate AI Engine includes 8 powerful tools:

1. **🚀 Landing Page Builder** - Generate high-converting Stake landing pages
2. **🌍 SEO Content Engine** - Create strategy articles with Google Search grounding
3. **💎 Branded Image Studio** - Generate luxurious 4K images
4. **🎬 Cinematic Veo Video** - Create 720p/1080p cinematic videos
5. **🗣️ Speaker Lab (TTS)** - Multi-speaker audio production
6. **🎙️ Live Affiliate Mentor** - Real-time voice consultation
7. **💬 Strategy Chat** - AI-powered strategy advisor
8. **📊 Dashboard** - Track your performance metrics

## Build for Production

To create an optimized production build:

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Troubleshooting

### Port Already in Use
If port 5173 is already in use, Vite will automatically try the next available port.

### API Key Issues
- Ensure your API key is valid and has billing enabled
- Check that the `.env.local` file is in the root directory
- Restart the dev server after adding the API key

### Build Warnings
The build may show warnings about chunk sizes. This is normal for development and can be optimized later with code splitting if needed.

## Project Structure

```
/
├── components/          # React components for each feature
├── App.tsx             # Main application component
├── index.tsx           # Application entry point
├── geminiService.ts    # Google AI integration
├── types.ts            # TypeScript type definitions
├── vite.config.ts      # Vite configuration
├── tsconfig.json       # TypeScript configuration
└── package.json        # Project dependencies
```

## Support

For more information, visit:
- [AI Studio](https://ai.studio/apps/drive/1PZeAd8WzVS-Z8mPg-_lf0yf_y2BY6lHi)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Gemini Billing Information](https://ai.google.dev/gemini-api/docs/billing)

---

**Status:** ✅ Application launched successfully and fully operational!
