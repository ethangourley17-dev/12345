
import React, { useState, useRef } from 'react';
import { generateMultiSpeakerAudio, decode, decodeAudioData } from '../geminiService';

const AudioLab: React.FC = () => {
  const [joeText, setJoeText] = useState("Jane, did you see the new RTP stats on Stake? The Dragon Tower game is paying out crazy today.");
  const [janeText, setJaneText] = useState("I did Joe! Plus that 10% rakeback code we got for our followers is driving insane volume. People love free value.");
  const [isGenerating, setIsGenerating] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  
  const audioContextRef = useRef<AudioContext | null>(null);
  const sourceRef = useRef<AudioBufferSourceNode | null>(null);

  const handleGenerateAndPlay = async () => {
    setIsGenerating(true);
    try {
      if (sourceRef.current) sourceRef.current.stop();
      
      const base64 = await generateMultiSpeakerAudio(joeText, janeText);
      const data = decode(base64);
      
      if (!audioContextRef.current) {
        audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 });
      }
      
      const buffer = await decodeAudioData(data, audioContextRef.current, 24000, 1);
      const source = audioContextRef.current.createBufferSource();
      source.buffer = buffer;
      source.connect(audioContextRef.current.destination);
      
      source.onended = () => setIsPlaying(false);
      source.start();
      sourceRef.current = source;
      setIsPlaying(true);
    } catch (e) {
      console.error(e);
      alert("Audio generation failed.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleStop = () => {
    if (sourceRef.current) {
      sourceRef.current.stop();
      setIsPlaying(false);
    }
  };

  return (
    <div className="space-y-8 animate-in slide-in-from-right-6 duration-700">
      <div className="bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-2xl">
        <h2 className="text-3xl font-bold text-white mb-8 heading-font">Speaker Lab (Joe & Jane)</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <div className="flex justify-between items-center mb-2">
              <label className="text-xs font-black text-indigo-400 uppercase tracking-widest">Speaker: Joe (Kore)</label>
              <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
            </div>
            <textarea
              value={joeText}
              onChange={(e) => setJoeText(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 text-white p-5 rounded-2xl h-40 outline-none focus:ring-2 focus:ring-indigo-600 transition-all resize-none"
              placeholder="Joe's lines..."
            />
          </div>
          <div className="space-y-4">
            <div className="flex justify-between items-center mb-2">
              <label className="text-xs font-black text-pink-400 uppercase tracking-widest">Speaker: Jane (Puck)</label>
              <span className="w-2 h-2 rounded-full bg-pink-500 animate-pulse"></span>
            </div>
            <textarea
              value={janeText}
              onChange={(e) => setJaneText(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 text-white p-5 rounded-2xl h-40 outline-none focus:ring-2 focus:ring-pink-600 transition-all resize-none"
              placeholder="Jane's lines..."
            />
          </div>
        </div>

        <div className="mt-10 flex gap-4">
          <button
            onClick={isPlaying ? handleStop : handleGenerateAndPlay}
            disabled={isGenerating}
            className={`flex-1 py-5 rounded-2xl font-black text-xl heading-font uppercase tracking-widest transition-all flex items-center justify-center gap-4 ${
              isGenerating 
                ? 'bg-slate-800 text-slate-600' 
                : isPlaying 
                  ? 'bg-red-600 hover:bg-red-500 text-white shadow-red-500/20' 
                  : 'bg-gradient-to-r from-indigo-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white shadow-2xl shadow-indigo-500/20'
            }`}
          >
            {isGenerating ? (
              <>
                <div className="w-6 h-6 border-4 border-slate-700 border-t-white rounded-full animate-spin"></div>
                Producing Masters...
              </>
            ) : isPlaying ? (
              <>
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M6 6h12v12H6z"/></svg>
                Stop Production
              </>
            ) : (
              <>
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                Generate Dialogue
              </>
            )}
          </button>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 p-8 rounded-3xl flex items-center gap-8 relative overflow-hidden">
        <div className="absolute inset-y-0 right-0 w-32 bg-gradient-to-l from-orange-500/5 to-transparent pointer-events-none"></div>
        <div className="w-20 h-20 rounded-full bg-orange-600/10 flex items-center justify-center text-orange-500 shrink-0 border border-orange-500/20">
           <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
           </svg>
        </div>
        <div>
          <h4 className="text-white font-bold text-lg mb-2">Strategy Podcast Engine</h4>
          <p className="text-slate-400 leading-relaxed">
            Use this tool to create high-engagement social media clips. Conversations between two experts (Joe & Jane) build trust faster than generic ad copy. 
            Export these to your video editor to overlay onto your <strong>Veo Cinematic Studio</strong> renders.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AudioLab;
