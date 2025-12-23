
import React, { useState, useRef } from 'react';
import { generateCasinoImage, editImageWithNano, analyzeImage } from '../geminiService';

const MediaLab: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [aspectRatio, setAspectRatio] = useState('16:9');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImageUrl, setGeneratedImageUrl] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [editPrompt, setEditPrompt] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const ratios = ["1:1", "3:4", "4:3", "9:16", "16:9", "21:9"];

  const handleGenerate = async () => {
    if (!prompt) return;
    setIsGenerating(true);
    setAnalysis(null);
    try {
      const url = await generateCasinoImage(prompt, aspectRatio);
      setGeneratedImageUrl(url);
    } catch (e) {
      console.error(e);
      alert("Generation failed.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleEdit = async () => {
    if (!generatedImageUrl || !editPrompt) return;
    setIsGenerating(true);
    try {
      const editedUrl = await editImageWithNano(generatedImageUrl, editPrompt);
      setGeneratedImageUrl(editedUrl);
      setEditPrompt('');
    } catch (e) {
      console.error(e);
      alert("Editing failed.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleAnalyze = async () => {
    if (!generatedImageUrl) return;
    setIsAnalyzing(true);
    try {
      const res = await analyzeImage(generatedImageUrl);
      setAnalysis(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (re) => {
        setGeneratedImageUrl(re.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="space-y-8 animate-in slide-in-from-left-4 duration-500">
      <div className="bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-xl">
        <h2 className="text-2xl font-bold text-white mb-6 heading-font">Visual Branding Lab</h2>
        <div className="flex flex-col gap-6">
          <div className="flex flex-wrap gap-4">
            {ratios.map(r => (
              <button
                key={r}
                onClick={() => setAspectRatio(r)}
                className={`px-4 py-2 rounded-lg font-bold border transition-all ${
                  aspectRatio === r ? 'bg-indigo-600 border-indigo-500 text-white' : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-600'
                }`}
              >
                {r}
              </button>
            ))}
          </div>
          <div className="flex gap-4">
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Luxurious high-stakes poker table with golden cards..."
              className="flex-1 bg-slate-950 border border-slate-800 text-white p-4 rounded-xl outline-none focus:ring-2 focus:ring-indigo-600"
            />
            <button
              onClick={handleGenerate}
              disabled={isGenerating}
              className="bg-indigo-600 hover:bg-indigo-500 text-white px-8 rounded-xl font-bold shadow-lg shadow-indigo-500/20 disabled:bg-slate-800"
            >
              {isGenerating ? 'Creating...' : 'Generate'}
            </button>
          </div>
          <div className="flex items-center gap-4">
            <input type="file" ref={fileInputRef} onChange={handleFileUpload} className="hidden" accept="image/*" />
            <button
              onClick={() => fileInputRef.current?.click()}
              className="text-slate-400 hover:text-white flex items-center gap-2 text-sm font-bold uppercase tracking-widest"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              Upload Asset
            </button>
          </div>
        </div>
      </div>

      {generatedImageUrl && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-4">
            <div className="bg-slate-900 border border-slate-800 p-4 rounded-3xl overflow-hidden shadow-2xl group relative">
              <img src={generatedImageUrl} alt="Generated" className="w-full h-auto rounded-2xl object-contain" />
              {isGenerating && (
                <div className="absolute inset-0 bg-slate-950/60 backdrop-blur-sm flex items-center justify-center">
                  <div className="flex flex-col items-center gap-4">
                    <div className="w-12 h-12 border-4 border-indigo-600 border-t-white rounded-full animate-spin" />
                    <span className="text-white font-black tracking-widest text-sm italic">PROCESSING...</span>
                  </div>
                </div>
              )}
            </div>
            <div className="flex gap-4">
              <button
                onClick={() => setEditMode(!editMode)}
                className="flex-1 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-bold transition-all border border-slate-700"
              >
                {editMode ? 'Cancel Edit' : 'Edit with Nano'}
              </button>
              <button
                onClick={handleAnalyze}
                disabled={isAnalyzing}
                className="flex-1 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-bold transition-all border border-blue-500 shadow-lg shadow-blue-500/20"
              >
                {isAnalyzing ? 'Analyzing...' : 'Analyze Market Appeal'}
              </button>
            </div>
            
            {editMode && (
              <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl animate-in zoom-in-95 duration-200">
                <p className="text-xs font-bold text-slate-500 mb-3 uppercase">AI Quick Edit Prompt</p>
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={editPrompt}
                    onChange={(e) => setEditPrompt(e.target.value)}
                    placeholder="e.g., Make it look like a vintage polaroid or add golden sparks"
                    className="flex-1 bg-slate-950 border border-slate-800 text-white p-3 rounded-xl text-sm focus:ring-1 focus:ring-indigo-600 outline-none"
                  />
                  <button
                    onClick={handleEdit}
                    className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 rounded-xl font-bold"
                  >
                    Apply
                  </button>
                </div>
              </div>
            )}
          </div>

          <div className="space-y-6">
            {analysis && (
              <div className="bg-slate-900 border border-slate-800 p-8 rounded-3xl shadow-xl h-full">
                <h3 className="text-xl font-bold text-white mb-4 heading-font flex items-center gap-2">
                   <svg className="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  Image Intelligence
                </h3>
                <div className="prose prose-invert prose-indigo max-w-none">
                  <p className="text-slate-300 whitespace-pre-wrap leading-relaxed">
                    {analysis}
                  </p>
                </div>
              </div>
            )}
            {!analysis && !isAnalyzing && (
              <div className="h-full flex flex-col items-center justify-center border-2 border-dashed border-slate-800 rounded-3xl p-8 text-center bg-slate-900/30">
                <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mb-4 text-slate-600">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h4 className="text-white font-bold mb-2">Awaiting Intelligence</h4>
                <p className="text-slate-500 text-sm">Click Analyze to generate marketing insights and SEO tags for this asset.</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default MediaLab;
