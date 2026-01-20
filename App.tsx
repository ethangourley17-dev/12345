
import React, { useState, useEffect } from 'react';
import { AppTab } from './types';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import ContentWriter from './components/ContentWriter';
import MediaLab from './components/MediaLab';
import VideoStudio from './components/VideoStudio';
import StrategyChat from './components/StrategyChat';
import LiveConsult from './components/LiveConsult';
import LandingPageBuilder from './components/LandingPageBuilder';
import AudioLab from './components/AudioLab';
import PetApparelStore from './components/PetApparelStore';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<AppTab>(AppTab.DASHBOARD);
  const [isKeySelected, setIsKeySelected] = useState(false);

  useEffect(() => {
    const checkKey = async () => {
      // @ts-ignore
      if (window.aistudio?.hasSelectedApiKey) {
        // @ts-ignore
        const hasKey = await window.aistudio.hasSelectedApiKey();
        setIsKeySelected(hasKey);
      } else {
        setIsKeySelected(true); // Fallback for dev environments
      }
    };
    checkKey();
  }, []);

  const handleSelectKey = async () => {
    // @ts-ignore
    if (window.aistudio?.openSelectKey) {
      // @ts-ignore
      await window.aistudio.openSelectKey();
      setIsKeySelected(true);
    }
  };

  if (!isKeySelected) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-6 text-center">
        <div className="max-w-md bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-2xl">
          <div className="w-20 h-20 bg-indigo-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg shadow-indigo-500/20">
            <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold mb-4 heading-font text-white">Unlock Pro Features</h1>
          <p className="text-slate-400 mb-8">
            StakeAffiliate AI requires a valid Google Cloud API key for high-quality video and image generation.
          </p>
          <button
            onClick={handleSelectKey}
            className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-4 rounded-xl transition-all shadow-lg hover:shadow-indigo-500/30"
          >
            Connect API Key
          </button>
          <p className="mt-4 text-xs text-slate-500">
            Ensure your project has billing enabled. <a href="https://ai.google.dev/gemini-api/docs/billing" target="_blank" className="text-indigo-400 hover:underline">Learn more</a>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-slate-950 overflow-hidden text-slate-200">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="flex-1 relative overflow-y-auto bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-slate-900 via-slate-950 to-black">
        <div className="p-8 max-w-7xl mx-auto min-h-full pb-24">
          {activeTab === AppTab.DASHBOARD && <Dashboard onNavigate={setActiveTab} />}
          {activeTab === AppTab.CONTENT_WRITER && <ContentWriter />}
          {activeTab === AppTab.MEDIA_LAB && <MediaLab />}
          {activeTab === AppTab.VIDEO_GEN && <VideoStudio />}
          {activeTab === AppTab.STRATEGY_CHAT && <StrategyChat />}
          {activeTab === AppTab.LIVE_CONSULT && <LiveConsult />}
          {activeTab === AppTab.LANDING_PAGE && <LandingPageBuilder />}
          {activeTab === AppTab.AUDIO_LAB && <AudioLab />}
          {activeTab === AppTab.PET_APPAREL_STORE && <PetApparelStore />}
        </div>
      </main>
    </div>
  );
};

export default App;
