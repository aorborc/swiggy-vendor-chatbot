import React, { useState, useRef, useEffect } from 'react';
import ChatMessage from './components/ChatMessage';

function App() {
  const [messages, setMessages] = useState([
    { text: "Hello! I'm your Swiggy Vendor Assistant. How can I help you today? You can ask about **invoices**, **payments**, or your **statement of account**.", isBot: true }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    setMessages(prev => [...prev, { text: userMessage, isBot: false }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setMessages(prev => [...prev, { text: data.response, isBot: true }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { text: "Sorry, I'm having trouble connecting to the server. Please try again later.", isBot: true }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Background Decoration */}
      <div className="absolute top-0 left-0 w-full h-64 bg-gradient-to-b from-orange-50 to-transparent -z-10"></div>
      <div className="absolute -top-20 -right-20 w-96 h-96 bg-orange-100 rounded-full blur-3xl opacity-50 -z-10"></div>
      <div className="absolute top-40 -left-20 w-72 h-72 bg-blue-50 rounded-full blur-3xl opacity-50 -z-10"></div>

      {/* Header */}
      <header className="glass sticky top-0 z-20 border-b border-white/20">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-10 h-10 flex items-center justify-center transform transition-transform hover:scale-105">
              <img src="/logo.svg" alt="Swiggy Logo" className="w-full h-full object-contain" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-800 tracking-tight">Swiggy Vendor Chat</h1>
              <div className="flex items-center space-x-2">
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                <p className="text-xs text-gray-500 font-medium">Online • Powered by Gemini</p>
              </div>
            </div>
          </div>
          <button className="text-sm text-gray-500 hover:text-primary transition-colors font-medium">
            Help & Support
          </button>
        </div>
      </header>

      {/* Chat Area */}
      <main className="flex-1 max-w-4xl w-full mx-auto p-6 flex flex-col">
        <div className="flex-1 space-y-6 pb-4">
          {messages.map((msg, index) => (
            <ChatMessage key={index} message={msg.text} isBot={msg.isBot} />
          ))}
          
          {isLoading && (
            <div className="flex justify-start mb-6 animate-fade-in">
               <div className="w-8 h-8 rounded-full bg-white border border-gray-100 flex items-center justify-center shadow-sm mr-3 mt-1 shrink-0 overflow-hidden p-1">
                <img src="/logo.svg" alt="Bot" className="w-full h-full object-contain" />
              </div>
              <div className="bg-white rounded-2xl rounded-tl-none px-5 py-4 shadow-sm border border-gray-100 flex items-center space-x-1.5">
                <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot"></div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Area */}
      <footer className="sticky bottom-0 z-20">
        <div className="w-full">
          <div className="glass rounded-none p-2 shadow-soft border-t border-white/50">
            <form onSubmit={sendMessage} className="flex items-center space-x-2 px-6">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about invoices, payments, or statements..."
                className="flex-1 bg-transparent border-none px-6 py-4 focus:outline-none text-gray-700 placeholder-gray-400 text-base w-full"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="bg-gradient-to-r from-primary to-primary-dark hover:shadow-glow text-white rounded-xl px-8 py-4 font-semibold transition-all transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-none"
              >
                Send
              </button>
            </form>
          </div>
          <div className="text-center py-2">
             <p className="text-[10px] text-gray-400">AI can make mistakes. Please verify important information.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;

