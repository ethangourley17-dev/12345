
export enum AppTab {
  DASHBOARD = 'dashboard',
  CONTENT_WRITER = 'content-writer',
  MEDIA_LAB = 'media-lab',
  VIDEO_GEN = 'video-gen',
  STRATEGY_CHAT = 'strategy-chat',
  LIVE_CONSULT = 'live-consult',
  LANDING_PAGE = 'landing-page',
  AUDIO_LAB = 'audio-lab',
  PET_APPAREL_STORE = 'pet-apparel-store'
}

export interface GeneratedContent {
  title: string;
  body: string;
  seoKeywords: string[];
  sources: { title: string; uri: string }[];
}

export interface MediaAsset {
  id: string;
  type: 'image' | 'video';
  url: string;
  prompt: string;
  createdAt: number;
}
