import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Clock, ShieldAlert, ShieldCheck, Search, Loader2 } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const HistoryPanel = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const res = await axios.get(`${API_BASE_URL}/history?limit=30`);
            setHistory(res.data);
        } catch (err) {
            console.error(err);
            setError('Failed to fetch scan history from the backend database.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="bg-white/[0.01] border border-white/5 rounded-[40px] p-12 h-full flex flex-col items-center justify-center text-center flex-1 backdrop-blur-3xl shadow-2xl overflow-hidden ring-1 ring-white/5">
                <Loader2 className="w-16 h-16 animate-spin mb-6 text-cyber-purple drop-shadow-[0_0_20px_rgba(179,0,255,0.5)]" />
                <p className="text-white/50 tracking-[0.2em] uppercase font-bold text-sm">Synchronizing Logs...</p>
            </div>
        );
    }

    if (error) {
        return <div className="p-8 bg-red-500/10 text-red-400 border border-red-500/30 rounded-[30px] shadow-xl backdrop-blur-md m-6 font-mono">{error}</div>;
    }

    return (
        <div className="bg-white/[0.02] rounded-[40px] border border-white/10 shadow-[0_8px_32px_0_rgba(0,0,0,0.36)] backdrop-blur-3xl overflow-hidden flex flex-col h-full ring-1 ring-white/5 relative">
            <div className="absolute top-0 right-1/2 w-96 h-96 bg-cyber-purple/10 rounded-full blur-[120px] pointer-events-none" />

            {/* Header */}
            <div className="p-8 border-b border-white/10 bg-white/[0.01] flex justify-between items-center relative z-10">
                <h2 className="text-2xl font-black flex items-center gap-4 text-white uppercase tracking-widest">
                    <Clock className="w-6 h-6 text-cyber-purple" /> Security Ledger
                </h2>
                <div className="flex items-center gap-3 bg-black/40 rounded-2xl px-5 py-3 border border-white/10 shadow-inner group transition-all focus-within:border-cyber-blue/50">
                    <Search className="w-5 h-5 text-white/30 group-focus-within:text-cyber-blue transition-colors" />
                    <input type="text" placeholder="Query historical vectors..." className="bg-transparent border-none outline-none font-mono text-sm text-cyber-blue w-48 placeholder-white/20 focus:w-64 transition-all" />
                </div>
            </div>

            {/* Log List */}
            <div className="flex-1 overflow-y-auto p-4 md:p-6 no-scrollbar relative z-10">
                {history.length === 0 ? (
                    <div className="p-20 text-center flex flex-col items-center">
                        <ShieldCheck className="w-20 h-20 text-white/10 mb-6" />
                        <span className="text-white/30 tracking-[0.2em] uppercase font-bold text-sm">Ledger is empty. No threats recorded.</span>
                    </div>
                ) : (
                    <div className="space-y-4">
                        {history.map((item, idx) => {
                            const isMalicious = item.status.toLowerCase().includes('malicious') || item.status.toLowerCase().includes('phishing');
                            const isSuspicious = item.status.toLowerCase().includes('suspicious');
                            
                            let StatusIcon = ShieldCheck;
                            let statusColor = 'text-green-400';
                            let glowTag = 'shadow-[0_0_15px_rgba(34,197,94,0.2)] bg-green-500/10 text-green-300 border-green-500/20';
                            
                            if (isMalicious) {
                                StatusIcon = ShieldAlert;
                                statusColor = 'text-red-500';
                                glowTag = 'shadow-[0_0_20px_rgba(239,68,68,0.2)] bg-red-500/10 text-red-300 border-red-500/30';
                            } else if (isSuspicious) {
                                StatusIcon = ShieldAlert;
                                statusColor = 'text-yellow-400';
                                glowTag = 'shadow-[0_0_15px_rgba(234,179,8,0.2)] bg-yellow-500/10 text-yellow-300 border-yellow-500/30';
                            }

                            return (
                                <div key={item._id || idx} className="bg-black/20 p-6 rounded-[24px] border border-white/5 hover:border-white/20 hover:bg-white/5 transition-all group flex flex-col gap-4">
                                    <div className="flex justify-between items-start gap-4">
                                        <div className="flex items-center gap-5">
                                            <div className="bg-black/50 p-4 rounded-2xl group-hover:scale-110 transition-transform shadow-inner">
                                                <StatusIcon className={`w-6 h-6 ${statusColor}`} />
                                            </div>
                                            <div>
                                                <div className="flex items-center gap-3 mb-2">
                                                    <span className={`text-xs font-black px-3 py-1 rounded-lg border uppercase tracking-widest ${glowTag}`}>
                                                        {item.scan_type}
                                                    </span>
                                                    <span className="text-xs text-white/30 font-mono">
                                                        {new Date(item.timestamp).toLocaleString()}
                                                    </span>
                                                </div>
                                                <p className="text-white/80 font-medium truncate max-w-sm lg:max-w-[30rem] xl:max-w-[40rem] text-lg leading-relaxed" title={item.input_content}>
                                                    {item.input_content}
                                                </p>
                                            </div>
                                        </div>
                                        <div className="text-right flex flex-col items-end">
                                            <div className={`font-black uppercase tracking-widest text-xl mb-1 ${statusColor} drop-shadow-md`}>{item.status}</div>
                                            <div className="bg-black/50 px-3 py-1 rounded-lg font-mono text-xs text-white/50 border border-white/5 inline-block">Score: {item.confidence.toFixed(1)}%</div>
                                        </div>
                                    </div>
                                    {/* Explanation snippet */}
                                    <div className="bg-[#050510] p-4 rounded-xl text-sm text-cyber-blue opacity-80 font-mono border border-white/5 border-l-4 border-l-cyber-purple/50">
                                        {item.explanations || "// NO REASON PROVIDED"}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                )}
            </div>
        </div>
    );
};

export default HistoryPanel;
