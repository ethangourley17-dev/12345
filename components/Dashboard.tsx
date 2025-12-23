
import React from 'react';
import { AppTab } from '../types';

interface DashboardProps {
  onNavigate: (tab: AppTab) => void;
}

const Dashboard: React.FC<DashboardProps> = ({ onNavigate }) => {
  const stats = [
    { label: 'SEO Efficiency', value: '98%', color: 'text-green-400' },
    { label: 'Branding Quality', value: 'Elite', color: 'text-indigo-400' },
    { label: 'Signup Conversion', value: '+54%', color: 'text-blue-400' },
  ];

  const cards = [
    {
      tab: AppTab.LANDING_PAGE,
      title: 'Landing Page Builder',
      desc: 'Generate high-converting, branded Stake landing pages instantly.',
      icon: '🚀',
      bg: 'from-orange-600 to-red-600'
    },
    {
      tab: AppTab.CONTENT_WRITER,
      title: 'SEO Content Engine',
      desc: 'Grounding with Google Search & Maps for strategy articles.',
      icon: '🌍',
      bg: 'from-blue-600 to-indigo-600'
    },
    {
      tab: AppTab.MEDIA_LAB,
      title: 'Branded Image Studio',
      desc: 'Luxurious 4K images with specific aspect ratios.',
      icon: '💎',
      bg: 'from-indigo-600 to-purple-600'
    },
    {
      tab: AppTab.VIDEO_GEN,
      title: 'Cinematic Veo Video',
      desc: '720p/1080p cinematic video generation for social ads.',
      icon: '🎬',
      bg: 'from-purple-600 to-pink-600'
    },
    {
      tab: AppTab.AUDIO_LAB,
      title: 'Speaker Lab (TTS)',
      desc: 'Joe & Jane conversational multi-speaker audio production.',
      icon: '🗣️',
      bg: 'from-yellow-600 to-orange-600'
    },
    {
      tab: AppTab.LIVE_CONSULT,
      title: 'Live Affiliate Mentor',
      desc: 'Real-time voice consultation for tactical optimization.',
      icon: '🎙️',
      bg: 'from-green-600 to-teal-600'
    }
  ];

  return (
    <div className="animate-in fade-in duration-700">
      <div className="mb-12">
        <h1 className="text-5xl font-black text-white heading-font mb-4 tracking-tight">Stake Master Engine</h1>
        <p className="text-slate-400 text-xl max-w-3xl font-medium leading-relaxed">
          The all-in-one AI suite for elite Stake Casino affiliates. Dominate search rankings, captivate social audiences, and skyrocket signup rates.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {stats.map((stat, i) => (
          <div key={i} className="bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-xl hover:border-slate-700 transition-colors">
            <p className="text-slate-500 font-bold uppercase text-xs tracking-[0.2em] mb-2">{stat.label}</p>
            <p className={`text-4xl font-black ${stat.color}`}>{stat.value}</p>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {cards.map((card, i) => (
          <button
            key={i}
            onClick={() => onNavigate(card.tab)}
            className={`group text-left p-8 rounded-[2rem] bg-gradient-to-br ${card.bg} hover:scale-[1.02] active:scale-[0.98] transition-all duration-300 shadow-2xl relative overflow-hidden`}
          >
            <div className="absolute top-0 right-0 p-6 text-5xl opacity-20 group-hover:scale-125 transition-transform duration-500">
              {card.icon}
            </div>
            <div className="relative z-10">
              <h3 className="text-2xl font-bold text-white mb-3 heading-font">{card.title}</h3>
              <p className="text-white/80 font-medium leading-relaxed mb-8 text-sm">{card.desc}</p>
              <div className="flex items-center gap-2 text-white font-bold group-hover:translate-x-2 transition-transform text-sm uppercase tracking-widest">
                Launch Tool
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </div>
            </div>
          </button>
        ))}
      </div>

      <div className="mt-16 bg-slate-900 border border-slate-800 rounded-[2.5rem] p-12 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-500/10 blur-[120px] -mr-48 -mt-48" />
        <div className="relative z-10 flex flex-col lg:flex-row items-center gap-12">
          <div className="flex-1">
            <h2 className="text-4xl font-bold text-white heading-font mb-6">Traffic Conversion Pipeline</h2>
            <p className="text-slate-400 text-lg mb-8 max-w-xl">
              Our models are fine-tuned for <span className="text-indigo-400 font-bold italic underline">Casino Psychology</span>. 
              Generating content that doesn't just rank, but converts window-shoppers into high-value Stake players.
            </p>
            <div className="space-y-4">
              <div className="w-full h-4 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-indigo-500 to-green-500 w-[78%] shadow-[0_0_15px_rgba(34,197,94,0.3)]" />
              </div>
              <div className="flex justify-between items-center text-xs font-black uppercase tracking-widest">
                <span className="text-slate-500">Affiliate Tier: Platinum</span>
                <span className="text-green-500">78% to Diamond Goal</span>
              </div>
            </div>
          </div>
          <div className="bg-slate-950 p-8 rounded-3xl border border-slate-800 shadow-2xl min-w-[320px]">
             <div className="flex flex-col gap-5">
               <div className="flex items-center justify-between">
                 <div className="flex items-center gap-3 text-slate-300 text-sm font-bold uppercase tracking-wider">
                   <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse" />
                   Stake Offers
                 </div>
                 <span className="text-slate-500 text-xs font-bold">12 ACTIVE</span>
               </div>
               <div className="flex items-center justify-between">
                 <div className="flex items-center gap-3 text-slate-300 text-sm font-bold uppercase tracking-wider">
                   <div className="w-3 h-3 rounded-full bg-indigo-500" />
                   SEO Health
                 </div>
                 <span className="text-indigo-400 text-xs font-bold">OPTIMAL</span>
               </div>
               <div className="flex items-center justify-between">
                 <div className="flex items-center gap-3 text-slate-300 text-sm font-bold uppercase tracking-wider">
                   <div className="w-3 h-3 rounded-full bg-purple-500" />
                   Veo Rendering
                 </div>
                 <span className="text-purple-400 text-xs font-bold">STABLE</span>
               </div>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
