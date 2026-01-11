"use client";

"use client";

import Image from "next/image";
import ChatInterface from "./components/ChatInterface";
import FlightWidget from "./components/FlightWidget";
import TerminalMap from "./components/TerminalMap";
import PaymentModal from "./components/PaymentModal";
import { Zap, WifiOff, CreditCard } from "lucide-react";
import React, { useState } from "react";

export default function Home() {
  const [isPaymentOpen, setIsPaymentOpen] = useState(false);
  return (
    <main className="min-h-screen bg-zinc-950 text-white relative overflow-hidden font-sans selection:bg-emerald-500/30">

      {/* Background Ambience */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none z-0">
        <div className="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] bg-emerald-900/20 rounded-full blur-[128px]" />
        <div className="absolute bottom-[0%] right-[0%] w-[40%] h-[40%] bg-indigo-900/10 rounded-full blur-[128px]" />
      </div>

      <div className="relative z-10 h-screen flex flex-col p-6 gap-6 max-w-7xl mx-auto">

        {/* Header Bar */}
        <header className="flex items-center justify-between py-2">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-700 rounded-lg flex items-center justify-center shadow-lg shadow-emerald-900/20">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">LayoverOS</h1>
              <div className="flex items-center gap-2">
                <span className="text-[10px] text-zinc-400 font-mono uppercase tracking-widest">
                  System v1.0 • Connected
                </span>
                <div className="flex items-center gap-1 bg-zinc-900/50 px-2 py-0.5 rounded-full border border-zinc-800">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                  <span className="text-[9px] text-zinc-400 font-mono">MONGO_DB</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex items-center gap-2 text-zinc-500 text-xs font-mono bg-zinc-900 border border-zinc-800 px-3 py-1.5 rounded-md">
              <WifiOff className="w-3 h-3" />
              <span>OFFLINE MODE READY</span>
            </div>
            <button
              onClick={() => setIsPaymentOpen(true)}
              className="flex items-center gap-2 bg-gradient-to-r from-amber-500/10 to-orange-500/10 hover:from-amber-500/20 hover:to-orange-500/20 border border-amber-500/20 text-amber-500 text-xs font-mono px-3 py-1.5 rounded-md transition-all cursor-pointer"
            >
              <CreditCard className="w-3 h-3" />
              <span>UNITED CLUB ACCESS</span>
            </button>
          </div>
        </header>

        {/* Dashboard Grid */}
        <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-0">

          {/* Left Panel: Context & Flight Info */}
          {/* Left Panel: Flight Mode & Navigation */}
          <div className="lg:col-span-4 flex flex-col gap-6">

            {/* 1. Flight Tracker Section */}
            <div className="relative group">
              <div className="absolute -inset-0.5 bg-gradient-to-r from-emerald-500 to-teal-600 rounded-2xl opacity-20 group-hover:opacity-40 transition duration-500 blur"></div>
              <div className="relative bg-zinc-900 rounded-xl border border-zinc-800 overflow-hidden">
                <div className="px-4 py-2 bg-zinc-950/50 border-b border-zinc-800 flex justify-between items-center">
                  <span className="text-[10px] font-mono uppercase tracking-widest text-emerald-500">Flight Mode</span>
                  <span className="text-[10px] text-zinc-500">Optional</span>
                </div>
                <div className="p-2">
                  <FlightWidget />
                </div>
              </div>
            </div>

            {/* 2. Interactive Terminal Map */}
            <div className="flex-1 bg-zinc-900/50 backdrop-blur border border-zinc-800 rounded-xl p-6 relative overflow-hidden min-h-[300px]">
              <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5" />
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-zinc-400 text-xs font-mono uppercase tracking-widest">Live Terminal Map</h3>
                <span className="text-[10px] bg-zinc-800 px-2 py-0.5 rounded text-zinc-400">Interactive</span>
              </div>
              <div className="w-full h-[300px] rounded-lg overflow-hidden border border-zinc-800 bg-zinc-950/50">
                <TerminalMap />
              </div>
            </div>
          </div>

          {/* Right Panel: The Agent */}
          <div className="lg:col-span-8 flex flex-col min-h-0">
            <ChatInterface onTriggerPayment={() => setIsPaymentOpen(true)} />
          </div>

        </div>
      </div>

      <PaymentModal
        isOpen={isPaymentOpen}
        onClose={() => setIsPaymentOpen(false)}
        onPay={() => {
          // Future: Call Bursar Node
          console.log("Payment Confirmed");
        }}
      />
    </main >
  );
}
