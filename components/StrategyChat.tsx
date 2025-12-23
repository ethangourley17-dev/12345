
import React, { useState, useRef, useEffect } from 'react';
import { GoogleGenAI, GenerateContentResponse } from "@google/genai";

const StrategyChat: React.FC = () => {
  const [messages, setMessages] = useState<{ role: 'user' | 'bot'; text: string }[]>([
    { role: 'bot', text: 'Welcome to the Affiliate Strategy Center. How can I help you optimize your Stake Casino conversions today?' }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isTyping) return;
    
    const userMsg = input.trim();
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setInput('');
    setIsTyping(true);

    try {
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
      const chat = ai.chats.create({
        model: 'gemini-3-pro-preview',
        config: {
          systemInstruction: 'You are an elite casino affiliate marketing consultant. You specialize in high-converting strategies for Stake Casino. You advise on SEO, branding, video marketing, and localized gambling laws. Keep answers professional, strategic, and focused on driving signup conversions.'
        }
      });

      const response: GenerateContentResponse = await chat.sendMessage({ message: userMsg });
      setMessages(prev => [...prev, { role: 'bot', text: response.text || "I apologize, I couldn't process that strategy query." }]);
    } catch (e) {
      console.error(e);
      setMessages(prev => [...prev, { role: 'bot', text: "Strategy server error. Please check your API key." }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)] animate-in fade-in duration-500">
      <div className="flex-1 bg-slate-900 border border-slate-800 rounded-t-3xl overflow-y-auto p-8 space-y-6" ref={scrollRef}>
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-5 rounded-2xl ${
              m.role === 'user' 
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/10 rounded-tr-none' 
                : 'bg-slate-800 text-slate-200 border border-slate-700 rounded-tl-none'
            }`}>
              <p className="whitespace-pre-wrap leading-relaxed">{m.text}</p>
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-slate-800 p-5 rounded-2xl rounded-tl-none border border-slate-700 flex gap-2">
              <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" />
              <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce [animation-delay:0.2s]" />
              <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce [animation-delay:0.4s]" />
            </div>
          </div>
        )}
      </div>
      <div className="p-4 bg-slate-900 border-x border-b border-slate-800 rounded-b-3xl">
        <div className="flex gap-4 p-2 bg-slate-950 border border-slate-800 rounded-2xl">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask about SEO niches, bonus structures, or content strategy..."
            className="flex-1 bg-transparent text-white p-3 outline-none"
          />
          <button
            onClick={handleSend}
            disabled={isTyping}
            className="bg-indigo-600 hover:bg-indigo-500 text-white px-6 rounded-xl font-bold transition-all disabled:bg-slate-800"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default StrategyChat;
