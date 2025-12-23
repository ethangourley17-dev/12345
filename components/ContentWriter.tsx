
import React, { useState } from 'react';
import { generateSEOContent, generateLocalizedStrategy } from '../geminiService';

const ContentWriter: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [keywords, setKeywords] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [useLocal, setUseLocal] = useState(false);

  const handleGenerate = async () => {
    if (!topic) return;
    setIsGenerating(true);
    try {
      if (useLocal) {
        // Attempt to get location if available
        let lat, lng;
        try {
          const pos = await new Promise<GeolocationPosition>((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject);
          });
          lat = pos.coords.latitude;
          lng = pos.coords.longitude;
        } catch (e) {
          console.warn("Location not granted, using topic only.");
        }
        const data = await generateLocalizedStrategy(topic, lat, lng);
        setResult({
          title: `Localized Strategy: ${topic}`,
          body: data.body,
          metaDescription: "Localized competitive analysis for affiliate marketing.",
          suggestedSeoKeywords: ["local betting", "casino comparison", "localized marketing"],
          sources: data.sources
        });
      } else {
        const data = await generateSEOContent(topic, keywords.split(',').map(k => k.trim()));
        setResult(data);
      }
    } catch (error) {
      console.error(error);
      alert("Failed to generate content.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="space-y-8 animate-in slide-in-from-bottom-4 duration-500">
      <div className="bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-xl">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-white heading-font">SEO Content Engine</h2>
          <div className="flex items-center gap-3 bg-slate-950 p-2 rounded-xl border border-slate-800">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Localized Mode</span>
            <button
              onClick={() => setUseLocal(!useLocal)}
              className={`w-12 h-6 rounded-full transition-all relative ${useLocal ? 'bg-indigo-600' : 'bg-slate-800'}`}
            >
              <div className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${useLocal ? 'left-7' : 'left-1'}`} />
            </button>
          </div>
        </div>
        
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-bold text-slate-400 mb-2 uppercase tracking-wider">
              {useLocal ? 'Target Region / Theme' : 'Content Topic'}
            </label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder={useLocal ? "e.g., Casinos in Las Vegas vs Stake" : "e.g., Best Stake Casino Slot Strategies 2024"}
              className="w-full bg-slate-950 border border-slate-800 text-white p-4 rounded-xl focus:ring-2 focus:ring-indigo-600 outline-none transition-all"
            />
          </div>
          {!useLocal && (
            <div>
              <label className="block text-sm font-bold text-slate-400 mb-2 uppercase tracking-wider">Keywords (Comma separated)</label>
              <input
                type="text"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                placeholder="stake bonus, casino strategy, high rtp slots"
                className="w-full bg-slate-950 border border-slate-800 text-white p-4 rounded-xl focus:ring-2 focus:ring-indigo-600 outline-none transition-all"
              />
            </div>
          )}
          <button
            onClick={handleGenerate}
            disabled={isGenerating}
            className={`w-full py-4 rounded-xl font-bold text-white flex items-center justify-center gap-3 transition-all ${
              isGenerating ? 'bg-slate-800 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-500/20'
            }`}
          >
            {isGenerating ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                {useLocal ? 'Mining Local Maps Data...' : 'Mining Search Grounding...'}
              </>
            ) : (
              <>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                {useLocal ? 'Generate Localized Comparison' : 'Generate SEO Article'}
              </>
            )}
          </button>
        </div>
      </div>

      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 pb-12">
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-xl prose prose-invert max-w-none">
              <h1 className="text-3xl font-black heading-font text-white mb-6">{result.title}</h1>
              <div className="whitespace-pre-wrap text-slate-300 leading-relaxed text-lg" dangerouslySetInnerHTML={{ __html: result.body.replace(/\n/g, '<br/>') }} />
            </div>
          </div>
          <div className="space-y-6">
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-3xl shadow-xl">
              <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                Metadata & Context
              </h3>
              <p className="text-sm text-slate-400 mb-4">{result.metaDescription}</p>
              <div className="flex flex-wrap gap-2">
                {result.suggestedSeoKeywords.map((k: string, i: number) => (
                  <span key={i} className="px-3 py-1 bg-slate-800 border border-slate-700 text-slate-300 text-xs rounded-full font-medium">
                    {k}
                  </span>
                ))}
              </div>
            </div>
            <div className="bg-slate-900 border border-slate-800 p-6 rounded-3xl shadow-xl">
              <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Grounding Sources
              </h3>
              <ul className="space-y-3">
                {result.sources.map((source: any, i: number) => (
                  <li key={i}>
                    <a
                      href={source.uri}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-indigo-400 hover:underline flex items-center gap-2 truncate"
                    >
                      <svg className="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                      {source.title}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ContentWriter;
