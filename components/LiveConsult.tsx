
import React, { useState, useRef, useEffect } from 'react';
import { GoogleGenAI, Modality, LiveServerMessage } from '@google/genai';
import { decode, encode, decodeAudioData } from '../geminiService';

const LiveConsult: React.FC = () => {
  const [isActive, setIsActive] = useState(false);
  const [status, setStatus] = useState('Standby');
  const [transcriptions, setTranscriptions] = useState<{ role: string; text: string }[]>([]);
  
  const audioContextRef = useRef<AudioContext | null>(null);
  const outputAudioContextRef = useRef<AudioContext | null>(null);
  const nextStartTimeRef = useRef(0);
  const sourcesRef = useRef<Set<AudioBufferSourceNode>>(new Set());
  const sessionRef = useRef<any>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const startSession = async () => {
    try {
      setStatus('Connecting to Live Mentor...');
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
      
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 16000 });
      outputAudioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 });
      
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      const sessionPromise = ai.live.connect({
        model: 'gemini-2.5-flash-native-audio-preview-09-2025',
        config: {
          responseModalities: [Modality.AUDIO],
          speechConfig: {
            voiceConfig: { prebuiltVoiceConfig: { voiceName: 'Zephyr' } },
          },
          systemInstruction: 'You are an elite live affiliate strategy mentor. You speak in a professional, encouraging, and highly tactical tone. You help marketers optimize their Stake Casino signup flows. Keep your responses concise and punchy for voice interaction.',
          inputAudioTranscription: {},
          outputAudioTranscription: {},
        },
        callbacks: {
          onopen: () => {
            setIsActive(true);
            setStatus('Live');
            const source = audioContextRef.current!.createMediaStreamSource(stream);
            const scriptProcessor = audioContextRef.current!.createScriptProcessor(4096, 1, 1);
            
            scriptProcessor.onaudioprocess = (e) => {
              const inputData = e.inputBuffer.getChannelData(0);
              const int16 = new Int16Array(inputData.length);
              for (let i = 0; i < inputData.length; i++) {
                int16[i] = inputData[i] * 32768;
              }
              const pcmBlob = {
                data: encode(new Uint8Array(int16.buffer)),
                mimeType: 'audio/pcm;rate=16000',
              };
              sessionPromise.then(session => session.sendRealtimeInput({ media: pcmBlob }));
            };
            
            source.connect(scriptProcessor);
            scriptProcessor.connect(audioContextRef.current!.destination);
          },
          onmessage: async (message: LiveServerMessage) => {
            if (message.serverContent?.outputTranscription) {
               const text = message.serverContent.outputTranscription.text;
               setTranscriptions(prev => {
                 const last = prev[prev.length - 1];
                 if (last && last.role === 'Mentor') {
                   return [...prev.slice(0, -1), { role: 'Mentor', text: last.text + text }];
                 }
                 return [...prev, { role: 'Mentor', text }];
               });
            } else if (message.serverContent?.inputTranscription) {
               const text = message.serverContent.inputTranscription.text;
               setTranscriptions(prev => {
                 const last = prev[prev.length - 1];
                 if (last && last.role === 'You') {
                   return [...prev.slice(0, -1), { role: 'You', text: last.text + text }];
                 }
                 return [...prev, { role: 'You', text }];
               });
            }

            const base64Audio = message.serverContent?.modelTurn?.parts[0]?.inlineData?.data;
            if (base64Audio) {
              const ctx = outputAudioContextRef.current!;
              nextStartTimeRef.current = Math.max(nextStartTimeRef.current, ctx.currentTime);
              const buffer = await decodeAudioData(decode(base64Audio), ctx, 24000, 1);
              const source = ctx.createBufferSource();
              source.buffer = buffer;
              source.connect(ctx.destination);
              source.start(nextStartTimeRef.current);
              nextStartTimeRef.current += buffer.duration;
              sourcesRef.current.add(source);
              source.onended = () => sourcesRef.current.delete(source);
            }

            if (message.serverContent?.interrupted) {
              sourcesRef.current.forEach(s => s.stop());
              sourcesRef.current.clear();
              nextStartTimeRef.current = 0;
            }
          },
          onclose: () => stopSession(),
          onerror: (e) => {
            console.error(e);
            stopSession();
          }
        }
      });
      sessionRef.current = await sessionPromise;
    } catch (e) {
      console.error(e);
      setStatus('Failed to start.');
    }
  };

  const stopSession = () => {
    setIsActive(false);
    setStatus('Standby');
    if (streamRef.current) streamRef.current.getTracks().forEach(t => t.stop());
    if (audioContextRef.current) audioContextRef.current.close();
    if (outputAudioContextRef.current) outputAudioContextRef.current.close();
    sessionRef.current = null;
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] animate-in fade-in duration-700">
      <div className="bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-2xl mb-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-green-500/5 blur-[100px]" />
        
        <div className="flex flex-col md:flex-row items-center gap-10">
          <div className="flex-1 space-y-4">
            <div className="flex items-center gap-3">
              <div className={`w-3 h-3 rounded-full ${isActive ? 'bg-green-500 animate-pulse' : 'bg-slate-700'}`} />
              <span className="font-bold uppercase tracking-widest text-xs text-slate-500">{status}</span>
            </div>
            <h2 className="text-3xl font-black heading-font text-white">Live Affiliate Mentor</h2>
            <p className="text-slate-400 max-w-lg leading-relaxed">
              Experience real-time voice consultation. Ask about campaign pacing, bonus optimization, or high-intent traffic sources.
            </p>
            
            <button
              onClick={isActive ? stopSession : startSession}
              className={`px-8 py-4 rounded-2xl font-black text-lg transition-all shadow-xl flex items-center gap-3 ${
                isActive 
                  ? 'bg-red-600 hover:bg-red-500 text-white shadow-red-500/20' 
                  : 'bg-green-600 hover:bg-green-500 text-white shadow-green-500/20'
              }`}
            >
              {isActive ? (
                <>
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clipRule="evenodd" /></svg>
                  Terminate Session
                </>
              ) : (
                <>
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" /></svg>
                  Connect to Mentor
                </>
              )}
            </button>
          </div>

          <div className="w-64 h-64 flex items-center justify-center relative">
            <div className={`absolute inset-0 border-4 border-indigo-600/20 rounded-full ${isActive ? 'animate-ping' : ''}`} />
            <div className={`absolute inset-4 border-2 border-indigo-500/40 rounded-full ${isActive ? 'animate-pulse' : ''}`} />
            <div className="w-32 h-32 bg-indigo-600 rounded-full flex items-center justify-center shadow-2xl shadow-indigo-500/40 relative z-10">
              <svg className={`w-12 h-12 text-white ${isActive ? 'animate-bounce' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 bg-slate-900 border border-slate-800 rounded-3xl p-8 overflow-y-auto space-y-6">
        {transcriptions.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-slate-600 text-center">
            <svg className="w-12 h-12 mb-4 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            <p className="font-bold uppercase tracking-widest text-xs">Awaiting Voice Input</p>
          </div>
        ) : (
          transcriptions.map((t, i) => (
            <div key={i} className={`flex ${t.role === 'You' ? 'justify-end' : 'justify-start'}`}>
               <div className={`max-w-[70%] p-4 rounded-2xl ${t.role === 'You' ? 'bg-indigo-600/20 text-indigo-100 border border-indigo-500/30' : 'bg-slate-800 text-slate-300 border border-slate-700'}`}>
                 <p className="text-xs font-black uppercase tracking-widest mb-1 opacity-50">{t.role}</p>
                 <p className="leading-relaxed">{t.text}</p>
               </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default LiveConsult;
