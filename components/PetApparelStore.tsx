import React, { useState, useRef } from 'react';

interface Product {
  id: string;
  name: string;
  price: string;
  image: string; // Placeholder image URL
  type: 'shirt' | 'hoodie' | 'accessory';
}

interface Message {
  id: string;
  role: 'user' | 'ai';
  content: string;
  image?: string;
}

const PetApparelStore: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'ai',
      content: 'Hello! I am your Pet Apparel Assistant. Upload a photo of your pet, and I will help you customize our products!'
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const products: Product[] = [
    {
      id: 'p1',
      name: 'Classic Cotton Tee',
      price: '$29.99',
      image: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3',
      type: 'shirt'
    },
    {
      id: 'p2',
      name: 'Cozy Hoodie',
      price: '$49.99',
      image: 'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3',
      type: 'hoodie'
    },
    {
      id: 'p3',
      name: 'Pet Bandana',
      price: '$14.99',
      image: 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3',
      type: 'accessory'
    },
    {
      id: 'p4',
      name: 'Canvas Tote',
      price: '$19.99',
      image: 'https://images.unsplash.com/photo-1597484662317-9bd7bdda2907?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3',
      type: 'accessory'
    }
  ];

  const handleSendMessage = () => {
    if (!inputText.trim()) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputText
    };

    setMessages(prev => [...prev, newMessage]);
    setInputText('');

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: 'ai',
        content: uploadedImage
          ? "That's a great photo! I've applied it to the products on the right. How does it look?"
          : "I can help with that. Please upload a photo of your pet first so we can see how it looks on the gear!"
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const result = reader.result as string;
        setUploadedImage(result);

        // Add message about upload
        const uploadMsg: Message = {
          id: Date.now().toString(),
          role: 'user',
          content: 'Uploaded a photo.',
          image: result
        };
        setMessages(prev => [...prev, uploadMsg]);

        // Simulate AI processing
        setTimeout(() => {
            const aiResponse: Message = {
              id: (Date.now() + 1).toString(),
              role: 'ai',
              content: "Awesome! I've extracted your pet's image and applied it to our collection. Check out the preview!"
            };
            setMessages(prev => [...prev, aiResponse]);
        }, 1500);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="flex h-full gap-6">
      {/* Left Pane: Chat Interface */}
      <div className="w-1/3 flex flex-col bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">
        <div className="p-4 border-b border-slate-800 bg-slate-800/50">
          <h2 className="font-bold text-white flex items-center gap-2">
            <span className="text-xl">🤖</span> AI Stylist
          </h2>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] rounded-2xl p-3 ${
                  msg.role === 'user'
                    ? 'bg-indigo-600 text-white rounded-br-none'
                    : 'bg-slate-800 text-slate-200 rounded-bl-none'
                }`}
              >
                {msg.image && (
                  <img src={msg.image} alt="User upload" className="mb-2 rounded-lg max-h-40 w-full object-cover" />
                )}
                <p className="text-sm">{msg.content}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="p-4 border-t border-slate-800 bg-slate-900">
          <div className="flex gap-2">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              className="hidden"
              accept="image/*"
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              className="p-2 bg-slate-800 text-slate-400 hover:text-white rounded-xl hover:bg-slate-700 transition-colors"
              title="Upload Photo"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h14a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </button>
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type a message..."
              className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-indigo-500 transition-colors"
            />
            <button
              onClick={handleSendMessage}
              className="p-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-500 transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Right Pane: Store Display */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-white mb-2">Custom Pet Apparel Store</h1>
          <p className="text-slate-400">Preview your pet on our premium collection.</p>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-3 gap-6 overflow-y-auto pb-6 pr-2 custom-scrollbar">
          {products.map((product) => (
            <div key={product.id} className="group bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden hover:border-indigo-500/50 transition-all hover:shadow-xl hover:shadow-indigo-500/10">
              <div className="relative aspect-square overflow-hidden bg-slate-800">
                {/* Base Product Image */}
                <img
                  src={product.image}
                  alt={product.name}
                  className="w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-500"
                />

                {/* Overlay Uploaded Image (Mock Integration) */}
                {uploadedImage && (
                  <div className="absolute inset-0 flex items-center justify-center pointer-events-none mix-blend-multiply opacity-90">
                    <img
                        src={uploadedImage}
                        alt="Pet Overlay"
                        className="w-1/3 h-1/3 object-contain drop-shadow-xl filter contrast-125"
                        style={{
                            transform: product.type === 'shirt' ? 'translateY(-10%)' : 'none'
                        }}
                    />
                  </div>
                )}

                {/* Badge */}
                <div className="absolute top-3 left-3 bg-black/60 backdrop-blur-md px-3 py-1 rounded-full border border-white/10">
                  <span className="text-xs font-bold text-white uppercase tracking-wider">{product.type}</span>
                </div>
              </div>

              <div className="p-5">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-bold text-white text-lg">{product.name}</h3>
                  <span className="text-indigo-400 font-bold">{product.price}</span>
                </div>
                <p className="text-sm text-slate-400 mb-4">High-quality material tailored for your pet's comfort.</p>
                <button className="w-full py-3 bg-slate-800 hover:bg-indigo-600 text-white rounded-xl font-medium transition-colors flex items-center justify-center gap-2 group-hover:bg-indigo-600">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                  </svg>
                  Add to Cart
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PetApparelStore;
