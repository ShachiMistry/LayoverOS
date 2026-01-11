"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, CreditCard, ShieldCheck, Zap } from "lucide-react";

interface PaymentModalProps {
    isOpen: boolean;
    onClose: () => void;
    onPay: () => void;
}

export default function PaymentModal({ isOpen, onClose, onPay }: PaymentModalProps) {
    const [processing, setProcessing] = useState(false);
    const [success, setSuccess] = useState(false);

    const handlePay = () => {
        setProcessing(true);
        setTimeout(() => {
            setProcessing(false);
            setSuccess(true);
            setTimeout(() => {
                onPay();
                setSuccess(false);
                onClose();
            }, 2000);
        }, 2000);
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center">
                    {/* Backdrop */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
                    />

                    {/* Modal Container */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9, y: 20 }}
                        className="relative w-full max-w-md bg-zinc-900/90 border border-zinc-700/50 rounded-2xl shadow-2xl overflow-hidden"
                    >
                        {/* Glossy Gradient Overlay */}
                        <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 to-transparent pointer-events-none" />

                        {/* Header */}
                        <div className="flex justify-between items-center p-6 border-b border-zinc-800">
                            <div className="flex items-center gap-2">
                                <div className="p-2 bg-emerald-500/10 rounded-lg">
                                    <Zap className="w-5 h-5 text-emerald-400" />
                                </div>
                                <div>
                                    <h3 className="text-lg font-bold text-white tracking-tight">Premium Access</h3>
                                    <p className="text-xs text-zinc-400">United Club • SFO Terminal 3</p>
                                </div>
                            </div>
                            <button onClick={onClose} className="p-2 hover:bg-zinc-800 rounded-full text-zinc-400 transition-colors">
                                <X size={18} />
                            </button>
                        </div>

                        {/* Body */}
                        <div className="p-6 flex flex-col gap-6">

                            {/* Digital Card Preview */}
                            <div className="relative aspect-[1.58/1] rounded-xl overflow-hidden shadow-lg group">
                                <div className="absolute inset-0 bg-gradient-to-br from-zinc-800 to-black" />
                                <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-20" />
                                <div className="absolute inset-0 bg-gradient-to-tr from-emerald-500/20 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700" />

                                <div className="relative h-full p-6 flex flex-col justify-between z-10">
                                    <div className="flex justify-between items-start">
                                        <ShieldCheck className="text-emerald-500" />
                                        <span className="text-xs font-mono text-zinc-500">**** 4242</span>
                                    </div>
                                    <div>
                                        <div className="text-xs text-zinc-400 uppercase tracking-widest mb-1">Total Amount</div>
                                        <div className="text-2xl font-bold text-white">$50.00 <span className="text-sm font-normal text-zinc-500">USDC</span></div>
                                    </div>
                                </div>
                            </div>

                            {/* Action Button */}
                            <button
                                onClick={handlePay}
                                disabled={processing || success}
                                className="relative w-full py-4 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold tracking-wide shadow-lg shadow-emerald-900/20 overflow-hidden group disabled:opacity-80 disabled:cursor-not-allowed"
                            >
                                <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 pointer-events-none" />

                                {processing ? (
                                    <div className="flex items-center justify-center gap-2">
                                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                        <span>Processing...</span>
                                    </div>
                                ) : success ? (
                                    <div className="flex items-center justify-center gap-2 text-white">
                                        <ShieldCheck className="w-5 h-5" />
                                        <span>Payment Successful</span>
                                    </div>
                                ) : (
                                    <div className="flex items-center justify-center gap-2">
                                        <CreditCard className="w-4 h-4" />
                                        <span>Confirm Payment</span>
                                    </div>
                                )}
                            </button>

                            <div className="flex justify-center items-center gap-2 text-[10px] text-zinc-500 sans-serif">
                                <ShieldCheck size={10} />
                                <span>Secure enclaved transaction via MongoDB</span>
                            </div>

                        </div>
                    </motion.div>
                </div>
            )}
        </AnimatePresence>
    );
}
