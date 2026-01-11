"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { Plus, Minus, Maximize, MapPin, Coffee } from "lucide-react";

export default function TerminalMap() {
    const [scale, setScale] = useState(1);

    const zoomIn = () => setScale((prev) => Math.min(prev + 0.5, 4));
    const zoomOut = () => setScale((prev) => Math.max(prev - 0.5, 1));
    const resetZoom = () => setScale(1);

    return (
        <div className="relative w-full h-full min-h-[400px] bg-zinc-950/50 rounded-xl overflow-hidden border border-zinc-800">

            {/* Background Grid */}
            <div className="absolute inset-0 z-0 opacity-20 pointer-events-none"
                style={{ backgroundImage: 'radial-gradient(circle, #333 1px, transparent 1px)', backgroundSize: '20px 20px' }} />

            {/* Map Implementation */}
            <motion.div
                className="w-full h-full flex items-center justify-center cursor-grab active:cursor-grabbing"
                drag
                dragConstraints={{ left: -300, right: 300, top: -200, bottom: 200 }}
                dragElastic={0.1}
                animate={{ scale: scale }}
                transition={{ type: "spring", stiffness: 300, damping: 30 }}
            >
                <svg
                    viewBox="0 0 800 600"
                    className="w-[120%] h-[120%] drop-shadow-[0_0_15px_rgba(16,185,129,0.2)]"
                >
                    {/* --- TERMINAL ARCHITECTURE (Sci-Fi Blueprint) --- */}

                    {/* Main Concourse Body */}
                    <path
                        d="M 100 300 
               L 150 150 L 650 150 L 700 300 
               L 650 450 L 150 450 Z"
                        fill="none"
                        stroke="#10b981"
                        strokeWidth="2"
                        className="opacity-40"
                    />

                    {/* Inner Walkways */}
                    <path
                        d="M 180 300 L 620 300"
                        stroke="#10b981"
                        strokeWidth="4"
                        strokeDasharray="10 5"
                        className="opacity-60"
                    />

                    <path
                        d="M 400 150 L 400 450"
                        stroke="#10b981"
                        strokeWidth="2"
                        className="opacity-30"
                    />

                    {/* Gates (Top) */}
                    {[200, 300, 500, 600].map((x, i) => (
                        <g key={`gate-top-${i}`}>
                            <rect x={x - 20} y={130} width={40} height={20} fill="#10b981" opacity="0.2" />
                            <text x={x} y={120} fill="#10b981" fontSize="12" textAnchor="middle" className="font-mono opacity-80">G{i + 1}</text>
                        </g>
                    ))}

                    {/* Gates (Bottom) */}
                    {[200, 300, 500, 600].map((x, i) => (
                        <g key={`gate-bot-${i}`}>
                            <rect x={x - 20} y={450} width={40} height={20} fill="#10b981" opacity="0.2" />
                            <text x={x} y={490} fill="#10b981" fontSize="12" textAnchor="middle" className="font-mono opacity-80">G{i + 5}</text>
                        </g>
                    ))}

                    {/* --- AMENITIES POIs (Pulsing Dots) --- */}

                    {/* Coffee Shop */}
                    <g className="cursor-pointer hover:opacity-100 transition-opacity">
                        <circle cx="400" cy="300" r="8" fill="#f59e0b" className="animate-pulse" />
                        <circle cx="400" cy="300" r="16" fill="#f59e0b" opacity="0.2" className="animate-ping" />
                        <foreignObject x="415" y="285" width="100" height="40">
                            <div className="bg-zinc-950/80 border border-amber-500/50 px-2 py-1 rounded text-[8px] text-amber-500 font-mono flex items-center gap-1 w-fit">
                                <Coffee size={8} /> Cafe
                            </div>
                        </foreignObject>
                    </g>

                    {/* User Location */}
                    <g>
                        <circle cx="200" cy="300" r="6" fill="#10b981" />
                        <circle cx="200" cy="300" r="40" stroke="#10b981" strokeWidth="1" fill="none" opacity="0.3">
                            <animate attributeName="r" from="10" to="40" dur="2s" repeatCount="indefinite" />
                            <animate attributeName="opacity" from="0.5" to="0" dur="2s" repeatCount="indefinite" />
                        </circle>
                        <foreignObject x="170" y="320" width="80" height="40">
                            <div className="text-[10px] text-emerald-400 font-mono text-center bg-black/50 px-1 rounded">YOU</div>
                        </foreignObject>
                    </g>

                </svg>
            </motion.div>

            {/* Controls Overlay */}
            <div className="absolute top-4 right-4 flex flex-col gap-2 bg-zinc-900/80 backdrop-blur-sm p-1.5 rounded-lg border border-zinc-800 z-10 shadow-xl">
                <button onClick={zoomIn} className="p-1.5 hover:bg-zinc-800 rounded-md text-zinc-400 hover:text-white transition-colors">
                    <Plus size={16} />
                </button>
                <button onClick={zoomOut} className="p-1.5 hover:bg-zinc-800 rounded-md text-zinc-400 hover:text-white transition-colors">
                    <Minus size={16} />
                </button>
                <button onClick={resetZoom} className="p-1.5 hover:bg-zinc-800 rounded-md text-zinc-400 hover:text-white transition-colors border-t border-zinc-800 mt-1 pt-2">
                    <Maximize size={16} />
                </button>
            </div>

            {/* Legend Overlay */}
            <div className="absolute bottom-4 left-4 flex gap-3 text-[10px] font-mono pointer-events-none">
                <div className="flex items-center gap-1.5 bg-zinc-950/80 px-2 py-1 rounded-full border border-zinc-800">
                    <div className="w-2 h-2 rounded-full bg-emerald-500" />
                    <span className="text-zinc-400">Your Location</span>
                </div>
                <div className="flex items-center gap-1.5 bg-zinc-950/80 px-2 py-1 rounded-full border border-zinc-800">
                    <div className="w-2 h-2 rounded-full bg-amber-500" />
                    <span className="text-zinc-400">Amenities</span>
                </div>
            </div>

        </div>
    );
}
