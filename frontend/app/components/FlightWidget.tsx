"use client";

import { motion } from "framer-motion";
import { Plane, Clock, AlertTriangle } from "lucide-react";

export default function FlightWidget() {
    return (
        <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-zinc-900/50 backdrop-blur border border-zinc-800 rounded-xl p-6 shadow-2xl relative overflow-hidden group"
        >
            <div className="absolute top-0 right-0 p-3 opacity-20 group-hover:opacity-40 transition-opacity">
                <Plane className="w-24 h-24 text-zinc-700" />
            </div>

            <div className="flex justify-between items-start mb-6">
                <div>
                    <h3 className="text-zinc-400 text-xs font-mono uppercase tracking-widest">Flight Status</h3>
                    <div className="text-3xl font-bold text-white mt-1">UA 400</div>
                </div>
                <div className="bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-full text-xs font-mono border border-emerald-500/20 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                    ON TIME
                </div>
            </div>

            <div className="flex justify-between items-center relative">
                {/* Origin */}
                <div className="text-center z-10">
                    <div className="text-4xl font-extrabold text-white">SFO</div>
                    <div className="text-zinc-500 text-xs mt-1">San Francisco</div>
                    <div className="text-emerald-400 font-mono text-sm mt-2">10:30 AM</div>
                </div>

                {/* Path Visual */}
                <div className="flex-1 px-4 flex flex-col items-center z-10">
                    <div className="w-full h-[2px] bg-zinc-800 relative">
                        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-zinc-950 border border-zinc-700 p-1 rounded-full">
                            <Plane className="w-4 h-4 text-zinc-400 rotate-90" />
                        </div>
                    </div>
                    <div className="text-zinc-600 text-[10px] mt-2 font-mono">2h 30m</div>
                </div>

                {/* Dest */}
                <div className="text-center z-10">
                    <div className="text-4xl font-extrabold text-white">DEN</div>
                    <div className="text-zinc-500 text-xs mt-1">Denver</div>
                    <div className="text-zinc-400 font-mono text-sm mt-2">02:00 PM</div>
                </div>
            </div>

            <div className="mt-6 pt-4 border-t border-zinc-800 grid grid-cols-2 gap-4">
                <div>
                    <div className="text-zinc-500 text-[10px] uppercase">Terminal</div>
                    <div className="text-white font-mono">3</div>
                </div>
                <div>
                    <div className="text-zinc-500 text-[10px] uppercase">Gate</div>
                    <div className="text-white font-mono">F12</div>
                </div>
            </div>
        </motion.div>
    );
}
