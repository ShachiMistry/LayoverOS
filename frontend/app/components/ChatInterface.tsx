"use client";

import React, { useState, useRef, useEffect } from "react";
import { Send, MapPin, Plane, Loader2, Info } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import clsx from "clsx";

interface Message {
  role: "user" | "agent";
  content: string;
  timestamp: string;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "agent",
      content: "Welcome to LayoverOS. I am connected to the airport grid. How can I help you today?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg: Message = {
      role: "user",
      content: input,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      // Connect to Real Backend
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMsg.content,
          user_location: "Terminal 2", // Hardcoded for demo
          airport_code: "SFO"
        }),
      });

      const data = await res.json();

      const agentMsg: Message = {
        role: "agent",
        content: data.response || "System Error: No response received.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, agentMsg]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        {
          role: "agent",
          content: "⚠️ Connection Lost. Check backend server.",
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-zinc-900/50 backdrop-blur-md border border-zinc-800 rounded-xl overflow-hidden shadow-2xl">
      {/* Header */}
      <div className="p-4 border-b border-zinc-800 bg-zinc-950/80 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <h2 className="text-zinc-200 font-medium tracking-wide text-sm">LIVE OPERATOR</h2>
        </div>
        <div className="text-xs text-zinc-500 font-mono">SFO • ONLINE</div>
      </div>

      {/* Messages Area */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-4 space-y-4 font-mono text-sm scrollbar-thin scrollbar-thumb-zinc-700 hover:scrollbar-thumb-zinc-600"
      >
        <AnimatePresence initial={false}>
          {messages.map((m, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={clsx(
                "flex w-full",
                m.role === "user" ? "justify-end" : "justify-start"
              )}
            >
              <div
                className={clsx(
                  "max-w-[80%] p-3 rounded-lg text-sm border",
                  m.role === "user"
                    ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-100"
                    : "bg-zinc-800/80 border-zinc-700 text-zinc-300"
                )}
              >
                <div className="whitespace-pre-wrap leading-relaxed">
                  {/* Simple Markdown Parsing for Bold/Newlines */}
                  {m.content.split('\n').map((line, idx) => (
                    <p key={idx} className="mb-1 min-h-[1rem]">
                      {line.split('**').map((part, j) =>
                        j % 2 === 1 ? <strong key={j} className="text-white font-bold">{part}</strong> : part
                      )}
                    </p>
                  ))}
                </div>
                <div className="mt-1 text-[10px] opacity-50 text-right">{m.timestamp}</div>
              </div>
            </motion.div>
          ))}
          {isLoading && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
              <div className="bg-zinc-800/80 border border-zinc-700 p-3 rounded-lg flex items-center gap-2">
                <Loader2 className="w-4 h-4 text-emerald-500 animate-spin" />
                <span className="text-zinc-400 text-xs">Processing Request...</span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Input Area */}
      <div className="p-4 bg-zinc-950/80 border-t border-zinc-800">

        {/* Quick Actions (Visual Hint) */}
        {messages.length === 1 && (
          <div className="flex gap-2 mb-3 overflow-x-auto pb-1 scrollbar-hide">
            <button onClick={() => setInput("Where is the nearest coffee?")} className="whitespace-nowrap px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 rounded-full text-xs text-zinc-300 transition-colors flex items-center gap-2">☕ Find Coffee</button>
            <button onClick={() => setInput("Where are the restrooms?")} className="whitespace-nowrap px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 rounded-full text-xs text-zinc-300 transition-colors flex items-center gap-2">🚽 Restrooms</button>
            <button onClick={() => setInput("Status of UA400")} className="whitespace-nowrap px-3 py-1.5 bg-emerald-900/30 hover:bg-emerald-900/50 border border-emerald-800/50 rounded-full text-xs text-emerald-300 transition-colors flex items-center gap-2">✈️ Track UA400</button>
          </div>
        )}
        <div className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Type your request... (e.g. 'Plan SFO to JFK' or 'Find coffee')"
            className="flex-1 bg-zinc-900 border border-zinc-700 text-zinc-200 text-sm rounded-md px-4 py-3 focus:outline-none focus:ring-1 focus:ring-emerald-500 placeholder-zinc-600 font-mono"
            autoFocus
          />
          <button
            onClick={handleSend}
            disabled={isLoading}
            className="bg-emerald-600 hover:bg-emerald-500 text-white rounded-md px-4 py-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
