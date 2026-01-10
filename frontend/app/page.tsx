import Image from "next/image";
import ChatInterface from "./components/ChatInterface";
import FlightWidget from "./components/FlightWidget";
import { Zap, WifiOff } from "lucide-react";

export default function Home() {
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
          </div>
        </header>

        {/* Dashboard Grid */}
        <div className="flex-1 grid grid-cols-1lg:grid-cols-12 gap-6 min-h-0">

          {/* Left Panel: Context & Flight Info */}
          <div className="lg:col-span-4 flex flex-col gap-6">
            <FlightWidget />

            {/* Map Placeholder or Weather */}
            <div className="flex-1 bg-zinc-900/50 backdrop-blur border border-zinc-800 rounded-xl p-6 relative overflow-hidden">
              <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5" />
              <h3 className="text-zinc-400 text-xs font-mono uppercase tracking-widest mb-4">Live Terminal Map</h3>
              <div className="w-full h-full flex items-center justify-center border-2 border-dashed border-zinc-800 rounded-lg">
                <span className="text-zinc-600 font-mono text-sm">Interactive Map Module Loading...</span>
              </div>
            </div>
          </div>

          {/* Right Panel: The Agent */}
          <div className="lg:col-span-8 flex flex-col min-h-0">
            <ChatInterface />
          </div>

        </div>
      </div>
    </main>
  );
}
