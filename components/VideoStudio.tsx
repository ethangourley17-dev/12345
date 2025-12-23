
import React, { useState, useRef } from 'react';
import { generateVeoVideo } from '../geminiService';

const VideoStudio: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [imageBase64, setImageBase64] = useState<string | null>(null);
  const [aspectRatio, setAspectRatio] = useState<'16:9' | '9:16'>('16:9');
  const [status, setStatus] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleGenerate = async () => {
    if (!prompt && !imageBase64) return;
    setIsGenerating(true);
    setStatus('Initializing Veo Engine...');
    try {
      // Simulate multiple phases for better UX since Veo is slow
      const phases = [
        "Analyzing reference frame...",
        "Simulating fluid physics...",
        "Rendering cinematic lighting...",
        "Applying final casino grade color grade..."
      ];
      
      let phaseIdx = 0;
      const interval = setInterval(() => {
        if (phaseIdx < phases.length) {
          setStatus(phases[phaseIdx]);
          phaseIdx++;
        }
      }, 8000);

      const url = await generateVeoVideo(prompt, imageBase64 || undefined, aspectRatio);
      setVideoUrl(url);
      clearInterval(interval);
    } catch (e) {
      console.error(e);
      alert("Video generation failed.");
    } finally {
      setIsGenerating(false);
      setStatus('');
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (re) => setImageBase64(re.target?.result as string);
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="space-y-8 animate-in zoom-in duration-500">
      <div className="bg-slate-900 border border-slate-800 p-10 rounded-3xl shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500" />
        <h2 className="text-3xl font-bold text-white mb-8 heading-font">Veo Cinematic Studio</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-bold text-slate-400 mb-3 uppercase tracking-widest">Target Aspect Ratio</label>
              <div className="flex gap-4">
                <button
                  onClick={() => setAspectRatio('16:9')}
                  className={`flex-1 p-4 rounded-xl border font-bold transition-all ${
                    aspectRatio === '16:9' ? 'bg-indigo-600 border-indigo-500 text-white' : 'bg-slate-950 border-slate-800 text-slate-500'
                  }`}
                >
                  Landscape (16:9)
                </button>
                <button
                  onClick={() => setAspectRatio('9:16')}
                  className={`flex-1 p-4 rounded-xl border font-bold transition-all ${
                    aspectRatio === '9:16' ? 'bg-indigo-600 border-indigo-500 text-white' : 'bg-slate-950 border-slate-800 text-slate-500'
                  }`}
                >
                  Portrait (9:16)
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-bold text-slate-400 mb-3 uppercase tracking-widest">Visual Prompt</label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="A high-stakes casino vault opening with glowing purple lights and gold bars flying out..."
                className="w-full bg-slate-950 border border-slate-800 text-white p-5 rounded-2xl h-40 outline-none focus:ring-2 focus:ring-purple-600 transition-all resize-none"
              />
            </div>

            <div className="flex items-center gap-6">
              <input type="file" ref={fileInputRef} onChange={handleFileUpload} className="hidden" accept="image/*" />
              <button
                onClick={() => fileInputRef.current?.click()}
                className="flex items-center gap-3 px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-bold transition-all border border-slate-700"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h14a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {imageBase64 ? 'Change Frame' : 'Reference Frame'}
              </button>
              {imageBase64 && (
                <div className="w-16 h-16 rounded-lg overflow-hidden border border-slate-700">
                  <img src={imageBase64} className="w-full h-full object-cover" alt="Thumb" />
                </div>
              )}
            </div>
          </div>

          <div className="flex flex-col justify-center">
            {videoUrl ? (
              <div className="rounded-2xl overflow-hidden border border-slate-800 shadow-2xl bg-black aspect-video flex items-center justify-center">
                <video src={videoUrl} controls className="w-full h-full" autoPlay loop />
              </div>
            ) : (
              <div className={`rounded-2xl border-2 border-dashed border-slate-800 aspect-video flex flex-col items-center justify-center p-8 bg-slate-950/50 ${isGenerating ? 'opacity-100' : 'opacity-50'}`}>
                {isGenerating ? (
                  <div className="flex flex-col items-center gap-8">
                    <div className="relative">
                      <div className="w-24 h-24 border-8 border-slate-800 rounded-full" />
                      <div className="w-24 h-24 border-8 border-purple-600 border-t-transparent rounded-full animate-spin absolute top-0 left-0" />
                    </div>
                    <div className="text-center space-y-2">
                      <p className="text-xl font-black heading-font text-white">{status}</p>
                      <p className="text-slate-500 font-bold uppercase tracking-widest text-xs animate-pulse">Rendering 3.1 Fast Preview...</p>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="w-16 h-16 bg-slate-900 rounded-full flex items-center justify-center mb-4 text-slate-700">
                      <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <p className="text-slate-500 font-bold">Your cinematic trailer will appear here.</p>
                  </>
                )}
              </div>
            )}
            
            <button
              onClick={handleGenerate}
              disabled={isGenerating || (!prompt && !imageBase64)}
              className={`mt-10 py-5 rounded-2xl font-black text-xl heading-font uppercase tracking-widest transition-all ${
                isGenerating ? 'bg-slate-800 text-slate-600' : 'bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white shadow-2xl shadow-indigo-500/30'
              }`}
            >
              {isGenerating ? 'RENDERING...' : 'START GENERATION'}
            </button>
          </div>
        </div>
      </div>
      
      <div className="bg-slate-900 border border-slate-800 p-8 rounded-3xl flex items-center gap-6">
        <div className="w-12 h-12 bg-green-500/10 rounded-xl flex items-center justify-center text-green-500">
           <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <h4 className="text-white font-bold">Pro Tip: Image-to-Video</h4>
          <p className="text-slate-400 text-sm">Upload a high-quality branded image in the Media Lab first, then use it as a reference frame here for maximum consistency.</p>
        </div>
      </div>
    </div>
  );
};

export default VideoStudio;
