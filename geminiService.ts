
import { GoogleGenAI, Type, Modality } from "@google/genai";

// Creating a new instance per call ensures we always have the latest API key from the user dialog.
const getAI = () => new GoogleGenAI({ apiKey: process.env.API_KEY });

export const generateSEOContent = async (topic: string, keywords: string[]): Promise<any> => {
  const ai = getAI();
  const prompt = `Write a high-converting, SEO-optimized casino strategy blog post about "${topic}". 
  Include these keywords: ${keywords.join(', ')}. 
  The goal is to encourage readers to sign up for Stake Casino using a free signup bonus offer. 
  Structure the output as JSON with title, body (markdown), and metaDescription.`;

  const response = await ai.models.generateContent({
    model: 'gemini-3-flash-preview',
    contents: prompt,
    config: {
      tools: [{ googleSearch: {} }],
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          title: { type: Type.STRING },
          body: { type: Type.STRING },
          metaDescription: { type: Type.STRING },
          suggestedSeoKeywords: { type: Type.ARRAY, items: { type: Type.STRING } }
        },
        required: ["title", "body", "metaDescription", "suggestedSeoKeywords"]
      }
    }
  });

  const data = JSON.parse(response.text);
  const sources = response.candidates?.[0]?.groundingMetadata?.groundingChunks?.map((chunk: any) => ({
    title: chunk.web?.title || 'Source',
    uri: chunk.web?.uri || '#'
  })) || [];

  return { ...data, sources };
};

export const generateLandingPageData = async (offer: string, audience: string, style: string = 'Stake Global'): Promise<any> => {
  const ai = getAI();
  const prompt = `Generate a COMPREHENSIVE high-converting full landing page for a Stake Casino affiliate offer.
  Brand Style/Context: ${style} (if CanadaStake, focus on Canadian players, CAD, and local trust).
  Offer: ${offer}
  Target Audience: ${audience}
  Goal: Maximal high-intent signups for Stake.
  Return JSON matching the schema.`;

  const response = await ai.models.generateContent({
    model: 'gemini-3-flash-preview',
    contents: prompt,
    config: {
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          hero: {
            type: Type.OBJECT,
            properties: {
              title: { type: Type.STRING },
              subtitle: { type: Type.STRING },
              cta: { type: Type.STRING }
            },
            required: ["title", "subtitle", "cta"]
          },
          features: {
            type: Type.ARRAY,
            items: {
              type: Type.OBJECT,
              properties: {
                title: { type: Type.STRING },
                description: { type: Type.STRING },
                icon: { type: Type.STRING }
              },
              required: ["title", "description", "icon"]
            }
          },
          stats: {
            type: Type.ARRAY,
            items: {
              type: Type.OBJECT,
              properties: {
                label: { type: Type.STRING },
                value: { type: Type.STRING }
              },
              required: ["label", "value"]
            }
          },
          testimonials: {
            type: Type.ARRAY,
            items: {
              type: Type.OBJECT,
              properties: {
                name: { type: Type.STRING },
                quote: { type: Type.STRING },
                rating: { type: Type.NUMBER }
              },
              required: ["name", "quote", "rating"]
            }
          },
          faq: {
            type: Type.ARRAY,
            items: {
              type: Type.OBJECT,
              properties: {
                q: { type: Type.STRING },
                a: { type: Type.STRING }
              },
              required: ["q", "a"]
            }
          },
          footerText: { type: Type.STRING }
        },
        required: ["hero", "features", "stats", "testimonials", "faq", "footerText"]
      }
    }
  });
  return JSON.parse(response.text);
};

export const generateMultiSpeakerAudio = async (joeText: string, janeText: string): Promise<string> => {
  const ai = getAI();
  const prompt = `TTS the following conversation between Joe and Jane about Stake Casino strategy:
      Joe: ${joeText}
      Jane: ${janeText}`;

  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash-preview-tts",
    contents: [{ parts: [{ text: prompt }] }],
    config: {
      responseModalities: [Modality.AUDIO],
      speechConfig: {
        multiSpeakerVoiceConfig: {
          speakerVoiceConfigs: [
            {
              speaker: 'Joe',
              voiceConfig: { prebuiltVoiceConfig: { voiceName: 'Kore' } }
            },
            {
              speaker: 'Jane',
              voiceConfig: { prebuiltVoiceConfig: { voiceName: 'Puck' } }
            }
          ]
        }
      }
    }
  });

  const base64Audio = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
  if (!base64Audio) throw new Error("Audio generation failed");
  return base64Audio;
};

export const generateLocalizedStrategy = async (topic: string, lat?: number, lng?: number): Promise<any> => {
  const ai = getAI();
  const prompt = `Research local gambling venues and betting trends for: ${topic}. 
  Compare physical options to the benefits of joining Stake Casino. 
  Provide a list of physical locations found and then a marketing strategy.`;

  const config: any = {
    // Maps grounding is only supported in Gemini 2.5 series models.
    tools: [{ googleMaps: {} }, { googleSearch: {} }],
  };

  if (lat && lng) {
    config.toolConfig = {
      retrievalConfig: {
        latLng: { latitude: lat, longitude: lng }
      }
    };
  }

  const response = await ai.models.generateContent({
    model: 'gemini-2.5-flash-preview-09-2025',
    contents: prompt,
    config: config,
  });

  const sources = response.candidates?.[0]?.groundingMetadata?.groundingChunks?.map((chunk: any) => ({
    title: chunk.maps?.title || chunk.web?.title || 'Location Source',
    uri: chunk.maps?.uri || chunk.web?.uri || '#'
  })) || [];

  return { body: response.text, sources };
};

export const generateCasinoImage = async (prompt: string, aspectRatio: string): Promise<string> => {
  const ai = getAI();
  const response = await ai.models.generateContent({
    model: 'gemini-3-pro-image-preview',
    contents: {
      parts: [{ text: `High-end, cinematic casino branding image, luxurious gold and neon theme: ${prompt}` }]
    },
    config: {
      imageConfig: {
        aspectRatio: aspectRatio as any,
        imageSize: "1K"
      },
      tools: [{ googleSearch: {} }] // Pro image supports search for real-time accuracy
    }
  });

  for (const part of response.candidates[0].content.parts) {
    if (part.inlineData) {
      return `data:image/png;base64,${part.inlineData.data}`;
    }
  }
  throw new Error("No image generated");
};

export const editImageWithNano = async (base64Image: string, editPrompt: string): Promise<string> => {
  const ai = getAI();
  const response = await ai.models.generateContent({
    model: 'gemini-2.5-flash-image',
    contents: {
      parts: [
        { inlineData: { data: base64Image.split(',')[1], mimeType: 'image/png' } },
        { text: editPrompt }
      ]
    }
  });

  for (const part of response.candidates[0].content.parts) {
    if (part.inlineData) {
      return `data:image/png;base64,${part.inlineData.data}`;
    }
  }
  throw new Error("No image generated");
};

export const generateVeoVideo = async (prompt: string, imageBase64?: string, aspectRatio: '16:9' | '9:16' = '16:9'): Promise<string> => {
  const ai = getAI();
  const payload: any = {
    model: 'veo-3.1-fast-generate-preview',
    prompt: `Professional casino affiliate marketing cinematic trailer: ${prompt}`,
    config: {
      numberOfVideos: 1,
      resolution: '720p',
      aspectRatio
    }
  };

  if (imageBase64) {
    payload.image = {
      imageBytes: imageBase64.split(',')[1],
      mimeType: 'image/png'
    };
  }

  let operation = await ai.models.generateVideos(payload);
  
  while (!operation.done) {
    await new Promise(resolve => setTimeout(resolve, 10000));
    operation = await ai.operations.getVideosOperation({ operation: operation });
  }

  const downloadLink = operation.response?.generatedVideos?.[0]?.video?.uri;
  // Use current API key for video download
  const res = await fetch(`${downloadLink}&key=${process.env.API_KEY}`);
  const blob = await res.blob();
  return URL.createObjectURL(blob);
};

export const analyzeImage = async (imageBase64: string): Promise<string> => {
  const ai = getAI();
  const response = await ai.models.generateContent({
    model: 'gemini-3-pro-preview',
    contents: {
      parts: [
        { inlineData: { data: imageBase64.split(',')[1], mimeType: 'image/png' } },
        { text: "Analyze this casino-related image. Provide insights for marketing strategy and SEO keywords." }
      ]
    }
  });
  return response.text || "Analysis failed.";
};

// LIVE API HELPERS
export function decode(base64: string) {
  const binaryString = atob(base64);
  const len = binaryString.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes;
}

export function encode(bytes: Uint8Array) {
  let binary = '';
  const len = bytes.byteLength;
  for (let i = 0; i < len; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}

export async function decodeAudioData(
  data: Uint8Array,
  ctx: AudioContext,
  sampleRate: number,
  numChannels: number,
): Promise<AudioBuffer> {
  const dataInt16 = new Int16Array(data.buffer);
  const frameCount = dataInt16.length / numChannels;
  const buffer = ctx.createBuffer(numChannels, frameCount, sampleRate);

  for (let channel = 0; channel < numChannels; channel++) {
    const channelData = buffer.getChannelData(channel);
    for (let i = 0; i < frameCount; i++) {
      channelData[i] = dataInt16[i * numChannels + channel] / 32768.0;
    }
  }
  return buffer;
}
