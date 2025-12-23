
import React, { useState } from 'react';
import { generateLandingPageData } from '../geminiService';

const LandingPageBuilder: React.FC = () => {
  const [offer, setOffer] = useState('$50 No Deposit Bonus + 10% Rakeback (Code: GEMINI)');
  const [audience, setAudience] = useState('High stakes crypto whales and professional slot hunters');
  const [style, setStyle] = useState('CanadaStake');
  const [isGenerating, setIsGenerating] = useState(false);
  const [data, setData] = useState<any>(null);

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const result = await generateLandingPageData(offer, audience, style);
      setData(result);
    } catch (e) {
      console.error(e);
      alert("Failed to build the full landing page.");
    } finally {
      setIsGenerating(false);
    }
  };

  const copyToClipboard = () => {
    const jsonStr = JSON.stringify(data, null, 2);
    navigator.clipboard.writeText(jsonStr);
    alert("Full page structure JSON copied to clipboard!");
  };

  const styles = [
    { name: 'CanadaStake', icon: '🇨🇦', desc: 'Localized for Canadian markets' },
    { name: 'Stake Global', icon: '🌎', desc: 'Standard high-converting international style' },
    { name: 'Crypto Luxury', icon: '💎', desc: 'Focus on high-net-worth crypto whales' },
    { name: 'Neon Arcade', icon: '🕹️', desc: 'Vibrant, high-energy gaming aesthetic' }
  ];

  return (
    <div className="space-y-12 animate-in slide-in-from-bottom-8 duration-700 pb-24">
      <div className="bg-slate-900 border border-slate-800 p-10 rounded-[2.5rem] shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-orange-600/5 blur-[100px] pointer-events-none" />
        <h2 className="text-4xl font-black text-white mb-4 heading-font tracking-tight">Full Page Gen Studio</h2>
        <p className="text-slate-400 mb-10 max-w-2xl text-lg font-medium">
          Generate high-converting, multi-section landing pages instantly. Optimized for SEO, trust, and instant Stake signups.
        </p>

        <div className="space-y-8">
          <div>
            <label className="block text-xs font-black text-slate-500 uppercase tracking-[0.25em] mb-4">Select Page Context / Style</label>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {styles.map(s => (
                <button
                  key={s.name}
                  onClick={() => setStyle(s.name)}
                  className={`p-4 rounded-2xl border text-left transition-all ${
                    style === s.name ? 'bg-orange-600 border-orange-500 text-white shadow-lg' : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'
                  }`}
                >
                  <div className="text-2xl mb-1">{s.icon}</div>
                  <div className="font-black text-sm">{s.name}</div>
                  <div className={`text-[10px] uppercase font-bold tracking-tighter mt-1 ${style === s.name ? 'text-orange-100' : 'text-slate-600'}`}>
                    {s.desc}
                  </div>
                </button>
              ))}
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-4">
              <label className="block text-xs font-black text-slate-500 uppercase tracking-[0.25em]">Primary Affiliate Offer</label>
              <input
                type="text"
                value={offer}
                onChange={(e) => setOffer(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 text-white p-5 rounded-2xl focus:ring-2 focus:ring-orange-600 outline-none transition-all placeholder:text-slate-700"
                placeholder="e.g., Exclusive $2000 Matching Bonus"
              />
            </div>
            <div className="space-y-4">
              <label className="block text-xs font-black text-slate-500 uppercase tracking-[0.25em]">Target Traffic Persona</label>
              <input
                type="text"
                value={audience}
                onChange={(e) => setAudience(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 text-white p-5 rounded-2xl focus:ring-2 focus:ring-orange-600 outline-none transition-all placeholder:text-slate-700"
                placeholder="e.g., Crypto casuals on YouTube"
              />
            </div>
          </div>
        </div>
        
        <button
          onClick={handleGenerate}
          disabled={isGenerating}
          className={`w-full mt-10 py-5 rounded-2xl font-black text-xl heading-font uppercase tracking-[0.1em] transition-all flex items-center justify-center gap-4 ${
            isGenerating ? 'bg-slate-800 text-slate-600' : 'bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-500 hover:to-red-500 text-white shadow-2xl shadow-orange-500/30'
          }`}
        >
          {isGenerating ? (
            <>
              <div className="w-6 h-6 border-4 border-slate-700 border-t-white rounded-full animate-spin" />
              Structuring {style} Layout...
            </>
          ) : (
            <>
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clipRule="evenodd" /></svg>
              AI INSTANT GEN: FULL PAGE
            </>
          )}
        </button>
      </div>

      {data && (
        <div className="space-y-8">
          <div className="flex justify-between items-center bg-slate-900 border border-slate-800 p-4 rounded-2xl">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center text-green-500">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/></svg>
              </div>
              <span className="text-white font-black text-xs uppercase tracking-widest">
                {style} Page Built Successfully
              </span>
            </div>
            <button onClick={copyToClipboard} className="bg-slate-800 hover:bg-slate-700 text-white px-6 py-2 rounded-xl text-sm font-bold border border-slate-700 transition-all flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
              Copy CMS Ready JSON
            </button>
          </div>

          <div className="bg-slate-950 rounded-[3rem] overflow-hidden shadow-2xl border border-slate-800/50 animate-in fade-in zoom-in-95 duration-1000 ring-1 ring-slate-800">
            {/* Landing Page Preview - Inner Container */}
            <div className="bg-white text-slate-950 font-sans selection:bg-indigo-100 min-h-screen">
              
              {/* Header */}
              <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-slate-100 px-8 py-4 flex justify-between items-center shadow-sm">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center text-white font-black shadow-lg shadow-indigo-600/20 italic text-xl">S</div>
                  <span className="font-black text-xl tracking-tighter uppercase italic">
                    {style.includes('Canada') ? 'STAKECANADA' : 'STAKEPRO'}
                  </span>
                </div>
                <nav className="hidden md:flex items-center gap-8 text-xs font-black text-slate-400 uppercase tracking-widest">
                  <span className="hover:text-indigo-600 cursor-pointer transition-colors">Games</span>
                  <span className="hover:text-indigo-600 cursor-pointer transition-colors">VIP Club</span>
                  <span className="hover:text-indigo-600 cursor-pointer transition-colors">Provably Fair</span>
                </nav>
                <button className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-2xl font-black text-xs transition-all shadow-xl shadow-indigo-600/20 uppercase tracking-widest">
                  {data.hero.cta}
                </button>
              </header>

              {/* Hero Section */}
              <section className="relative px-8 py-24 md:py-36 text-center max-w-5xl mx-auto space-y-10">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[80%] h-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-indigo-50/70 via-transparent to-transparent -z-10" />
                <div className="inline-block px-5 py-2.5 bg-indigo-50 border border-indigo-100 rounded-full text-indigo-600 text-[10px] font-black uppercase tracking-[0.3em] mb-2 animate-bounce">
                  {style.includes('Canada') ? '🇨🇦 No.1 Ranked in Canada 🇨🇦' : 'Global Partnership Exclusive'}
                </div>
                <h1 className="text-6xl md:text-8xl font-black leading-[0.95] tracking-tighter text-slate-950 uppercase italic">
                  {data.hero.title}
                </h1>
                <p className="text-xl md:text-2xl text-slate-500 font-bold max-w-2xl mx-auto leading-relaxed">
                  {data.hero.subtitle}
                </p>
                <div className="pt-8">
                  <button className="bg-indigo-600 hover:bg-indigo-700 text-white px-14 py-7 rounded-[2rem] text-3xl font-black shadow-2xl shadow-indigo-600/30 transition-all hover:scale-105 active:scale-95 uppercase tracking-tighter italic">
                    {data.hero.cta} NOW
                  </button>
                  <p className="mt-5 text-slate-400 font-bold text-xs uppercase tracking-widest">Limited Time Offer • Instant Rakeback • Fast Crypto Cashouts</p>
                </div>
              </section>

              {/* Stats Bar */}
              <section className="bg-slate-950 grid grid-cols-2 md:grid-cols-4 border-y border-slate-900 shadow-2xl">
                {data.stats.map((stat: any, i: number) => (
                  <div key={i} className="py-14 px-8 text-center border-r border-slate-900 last:border-0 hover:bg-slate-900 transition-colors cursor-default">
                    <p className="text-5xl font-black text-white mb-2 tracking-tighter italic">{stat.value}</p>
                    <p className="text-[10px] font-black text-indigo-500 uppercase tracking-[0.25em]">{stat.label}</p>
                  </div>
                ))}
              </section>

              {/* Features Grid */}
              <section className="px-8 py-32 max-w-7xl mx-auto">
                <div className="text-center mb-24">
                   <h2 className="text-5xl font-black text-slate-950 mb-6 tracking-tighter uppercase italic">Why the pros choose Stake</h2>
                   <div className="w-20 h-1.5 bg-indigo-600 mx-auto rounded-full mb-6"></div>
                   <p className="text-slate-500 font-bold max-w-xl mx-auto text-lg leading-relaxed">The only platform built by players, for players. Industry-leading rewards and unmatched game variety.</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
                  {data.features.map((feature: any, i: number) => (
                    <div key={i} className="p-12 rounded-[3rem] bg-slate-50 border border-slate-100 shadow-sm hover:shadow-2xl hover:-translate-y-3 transition-all group relative overflow-hidden">
                      <div className="absolute top-0 right-0 p-8 text-6xl opacity-5 group-hover:opacity-20 transition-opacity translate-x-4 -translate-y-4">
                        {feature.icon}
                      </div>
                      <div className="text-6xl mb-8 group-hover:scale-110 transition-transform origin-left">{feature.icon}</div>
                      <h3 className="text-2xl font-black text-slate-950 mb-4 uppercase tracking-tighter">{feature.title}</h3>
                      <p className="text-slate-500 leading-relaxed font-bold text-sm">{feature.description}</p>
                    </div>
                  ))}
                </div>
              </section>

              {/* Testimonials */}
              <section className="bg-slate-950 py-32 px-8 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-500/10 blur-[150px]" />
                <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-20 items-center relative z-10">
                   <div>
                     <h2 className="text-5xl md:text-7xl font-black text-white mb-8 leading-[1] tracking-tighter uppercase italic">
                       Trusted by the <br/>
                       <span className="text-indigo-600 underline decoration-indigo-600/20 underline-offset-12">Winners</span>
                     </h2>
                     <p className="text-slate-400 text-xl font-bold leading-relaxed mb-10">Join the elite community of high-rollers and casual winners alike.</p>
                     <div className="flex gap-4">
                        <div className="p-4 bg-slate-900 rounded-2xl border border-slate-800">
                           <p className="text-white font-black text-2xl mb-1">$500M+</p>
                           <p className="text-slate-500 text-[9px] font-black uppercase tracking-widest">Paid out daily</p>
                        </div>
                        <div className="p-4 bg-slate-900 rounded-2xl border border-slate-800">
                           <p className="text-white font-black text-2xl mb-1">2s</p>
                           <p className="text-slate-500 text-[9px] font-black uppercase tracking-widest">Avg. Withdrawal</p>
                        </div>
                     </div>
                   </div>
                   <div className="space-y-6">
                     {data.testimonials.map((t: any, i: number) => (
                       <div key={i} className="bg-slate-900/50 backdrop-blur-md border border-slate-800 p-10 rounded-[2.5rem] hover:bg-slate-900 transition-colors group">
                          <div className="flex gap-1.5 mb-6">
                            {[...Array(t.rating)].map((_, i) => (
                              <svg key={i} className="w-5 h-5 text-indigo-500 fill-current" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                            ))}
                          </div>
                          <p className="text-2xl text-white font-black mb-6 italic leading-snug group-hover:scale-[1.01] transition-transform">"{t.quote}"</p>
                          <div className="flex items-center gap-4">
                             <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center text-indigo-500 font-black">
                                {t.name[0]}
                             </div>
                             <p className="text-slate-500 font-black uppercase text-xs tracking-[0.2em]">{t.name}</p>
                          </div>
                       </div>
                     ))}
                   </div>
                </div>
              </section>

              {/* FAQ Section */}
              <section className="px-8 py-32 max-w-4xl mx-auto">
                <div className="text-center mb-20">
                   <h2 className="text-5xl font-black text-slate-950 mb-4 tracking-tighter uppercase italic">The Inside Scoop</h2>
                   <p className="text-slate-400 font-bold uppercase text-xs tracking-widest">Frequently Asked Questions</p>
                </div>
                <div className="space-y-6">
                  {data.faq.map((item: any, i: number) => (
                    <details key={i} className="group p-8 bg-slate-50 rounded-[2rem] border border-slate-100 cursor-pointer select-none">
                      <summary className="flex justify-between items-center text-xl font-black text-slate-950 uppercase tracking-tighter italic list-none">
                        {item.q}
                        <svg className="w-6 h-6 text-indigo-600 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M19 9l-7 7-7-7"/></svg>
                      </summary>
                      <div className="mt-6 pt-6 border-t border-slate-200 text-slate-500 font-bold leading-relaxed">
                        {item.a}
                      </div>
                    </details>
                  ))}
                </div>
              </section>

              {/* Final CTA */}
              <section className="px-8 py-32 text-center bg-indigo-600 relative overflow-hidden">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(255,255,255,0.1)_0%,transparent_100%)]" />
                <div className="relative z-10 space-y-10">
                   <h2 className="text-6xl md:text-8xl font-black text-white tracking-tighter uppercase italic leading-[0.9]">Claim your <br/>destiny</h2>
                   <p className="text-indigo-100 text-2xl font-bold max-w-2xl mx-auto">{offer} is waiting for you.</p>
                   <button className="bg-white text-indigo-600 px-16 py-8 rounded-[3rem] text-4xl font-black shadow-[0_35px_60px_-15px_rgba(0,0,0,0.3)] transition-all hover:scale-110 active:scale-95 uppercase tracking-tighter italic">
                      LFG!
                   </button>
                </div>
              </section>

              {/* Footer */}
              <footer className="bg-slate-950 py-24 px-8 border-t border-slate-900 text-center">
                <div className="flex items-center justify-center gap-3 mb-10">
                  <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center text-white font-black shadow-lg shadow-indigo-600/20 italic">S</div>
                  <span className="font-black text-xl text-white tracking-tighter uppercase italic">STAKE<span className="text-indigo-600">PRO</span></span>
                </div>
                <p className="text-slate-500 max-w-2xl mx-auto text-[10px] font-black uppercase tracking-[0.2em] leading-relaxed">
                  {data.footerText}
                  <br/><br/>
                  BeGambleAware.org • 18+ • Gamble Responsibly.
                  <br/>
                  Stake is the world's leading crypto casino and sports betting platform.
                  <br/><br/>
                  © 2024 Affiliate Master Engine. Powered by Gemini Flash 3.
                </p>
              </footer>

            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LandingPageBuilder;
