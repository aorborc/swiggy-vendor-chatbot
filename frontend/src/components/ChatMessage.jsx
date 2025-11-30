import React from 'react';
import ReactMarkdown from 'react-markdown';

const ChatMessage = ({ message, isBot }) => {
  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-6 animate-fade-in group`}>
      {isBot && (
        <div className="w-8 h-8 rounded-full bg-white border border-gray-100 flex items-center justify-center shadow-sm mr-3 mt-1 shrink-0 overflow-hidden p-1">
          <img src="/logo.svg" alt="Bot" className="w-full h-full object-contain" />
        </div>
      )}
      
      <div
        className={`max-w-[80%] rounded-2xl px-5 py-3.5 shadow-sm transition-all duration-200 hover:shadow-md ${
          isBot
            ? 'bg-white text-gray-800 rounded-tl-none border border-gray-100'
            : 'bg-gradient-to-r from-primary to-primary-dark text-white rounded-tr-none shadow-glow'
        }`}
      >
        <div className={`text-sm prose prose-sm max-w-none ${isBot ? 'prose-headings:text-gray-800' : 'prose-headings:text-white prose-p:text-white prose-strong:text-white prose-table:text-white'}`}>
          {isBot ? (
            <ReactMarkdown
              components={{
                table: ({node, ...props}) => <div className="overflow-x-auto my-2"><table className="min-w-full divide-y divide-gray-200" {...props} /></div>,
                thead: ({node, ...props}) => <thead className="bg-gray-50" {...props} />,
                th: ({node, ...props}) => <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" {...props} />,
                td: ({node, ...props}) => <td className="px-3 py-2 whitespace-nowrap text-sm text-gray-600 border-t border-gray-100" {...props} />,
              }}
            >
              {message}
            </ReactMarkdown>
          ) : (
            <p className="leading-relaxed">{message}</p>
          )}
        </div>
        <div className={`text-[10px] mt-1.5 font-medium opacity-70 ${isBot ? 'text-gray-400' : 'text-orange-50 text-right'}`}>
          {isBot ? 'Swiggy Assistant' : 'You'}
        </div>
      </div>

      {!isBot && (
        <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 text-xs font-bold ml-3 mt-1 shrink-0">
          U
        </div>
      )}
    </div>
  );
};

export default ChatMessage;

