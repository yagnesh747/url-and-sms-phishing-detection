import React, { useState } from 'react';
import axios from 'axios';
import { Shield, Activity, Loader2, Link as LinkIcon, MessageSquare, Hexagon, Zap, History, AlertTriangle } from 'lucide-react';
import ResultsPanel from './components/ResultsPanel.jsx';
import HistoryPanel from './components/HistoryPanel.jsx';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

function App() {
    const [url, setUrl] = useState('');
    const [sms, setSms] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');
    const [view, setView] = useState('scan'); 

    const handleScan = async (type) => {
        setLoading(true);
        setResult(null);
        setError('');

        try {
            let endpoint = '';
            let payload = {};

            if (type === 'url') {
                endpoint = '/analyze-url';
                payload = { url };
            } else if (type === 'sms') {
                endpoint = '/analyze-sms';
                payload = { sms };
            } else if (type === 'full') {
                endpoint = '/full-scan';
                payload = { url, sms };
            }

            const res = await axios.post(`${API_BASE_URL}${endpoint}`, payload);
            setResult(res.data);
        } catch (err) {
            console.error(err);
            if (err.response && err.response.status === 404) {
                 // Ignore if hitting default path
            } else {
                 setError('Failed to securely connect to the detection engine. Ensure backend is running.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-cyber-900 text-slate-100 font-sans p-4 sm:p-6 md:p-10 selection:bg-cyber-blue/30 relative overflow-hidden">
            
            {/* Animated Background Orbs */}
            <div className="absolute top-0 right-0 w-96 h-96 bg-cyber-blue/20 rounded-full mix-blend-screen filter blur-[120px] animate-blob -z-10" />
            <div className="absolute top-0 left-0 w-96 h-96 bg-cyber-purple/20 rounded-full mix-blend-screen filter blur-[120px] animate-blob animation-delay-2000 -z-10" />
            <div className="absolute -bottom-32 left-1/2 w-96 h-96 bg-cyber-pink/20 rounded-full mix-blend-screen filter blur-[120px] animate-blob animation-delay-4000 -z-10" />
            
            <div className="max-w-[1400px] mx-auto z-10 relative">
                
                {/* Header */}
                <header className="flex flex-col md:flex-row items-center justify-between mb-16 px-4">
                    <div className="flex items-center gap-4 mb-6 md:mb-0">
                        <div className="relative group">
                            <div className="absolute inset-0 bg-gradient-to-r from-cyber-blue to-cyber-purple rounded-xl blur-lg opacity-70 group-hover:opacity-100 transition-opacity duration-500" />
                            <div className="relative bg-cyber-900 border border-white/10 p-4 rounded-xl">
                                <Hexagon className="w-8 h-8 text-white absolute -top-1 -right-1 opacity-20" />
                                <Shield className="w-10 h-10 text-white fill-cyber-blue/20" />
                            </div>
                        </div>
                        <div>
                            <h1 className="text-4xl lg:text-5xl font-black tracking-tight text-white mb-1">
                                Cyber<span className="text-transparent bg-clip-text bg-gradient-to-r from-cyber-blue to-cyber-purple">Shield</span> AI
                            </h1>
                            <p className="text-slate-400 font-medium tracking-wide flex items-center gap-2">
                                <span className="w-2 h-2 rounded-full bg-cyber-blue animate-pulse" /> Live Multi-Agent Protection
                            </p>
                        </div>
                    </div>

                    {/* Navigation Pills */}
                    <div className="flex bg-white/5 backdrop-blur-3xl p-1.5 rounded-2xl border border-white/10 shadow-2xl">
                        <button 
                            onClick={() => setView('scan')}
                            className={`px-8 py-3 rounded-xl font-bold text-sm tracking-wide transition-all duration-300 flex items-center gap-2 ${view === 'scan' ? 'bg-gradient-to-r from-cyber-blue to-cyber-purple text-white shadow-lg' : 'text-slate-400 hover:text-white hover:bg-white/5'}`}
                        >
                           <Activity className="w-4 h-4" /> ENGINE
                        </button>
                        <button 
                            onClick={() => setView('history')}
                            className={`px-8 py-3 rounded-xl font-bold text-sm tracking-wide transition-all duration-300 flex items-center gap-2 ${view === 'history' ? 'bg-gradient-to-r from-cyber-blue to-cyber-purple text-white shadow-lg' : 'text-slate-400 hover:text-white hover:bg-white/5'}`}
                        >
                           <History className="w-4 h-4" /> LOGS
                        </button>
                    </div>
                </header>

                {view === 'history' ? (
                    <div className="h-[750px] animate-in fade-in zoom-in-95 duration-700 w-full drop-shadow-2xl">
                        <HistoryPanel />
                    </div>
                ) : (
                    <div className="grid grid-cols-1 xl:grid-cols-12 gap-8 lg:gap-12 w-full animate-in fade-in slide-in-from-bottom-8 duration-700">
                        
                        {/* LEFT COLUMN: SCANNERS */}
                        <div className="xl:col-span-5 flex flex-col gap-8">
                            
                            {/* URL Card */}
                            <div className="bg-white/[0.02] backdrop-blur-2xl rounded-3xl p-8 border border-white/10 shadow-[0_8px_32px_0_rgba(0,0,0,0.36)] relative group overflow-hidden">
                                <div className="absolute top-0 right-0 w-32 h-32 bg-cyber-blue/10 rounded-full blur-3xl transition-all duration-700 group-hover:bg-cyber-blue/30 group-hover:w-48 group-hover:h-48 group-hover:-top-10 group-hover:-right-10" />
                                
                                <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                                    <div className="w-12 h-12 rounded-2xl bg-cyber-blue/20 flex items-center justify-center border border-cyber-blue/30 backdrop-blur-md">
                                        <LinkIcon className="w-6 h-6 text-cyber-blue" />
                                    </div>
                                    URL Inspection
                                </h2>
                                
                                <div className="space-y-4 relative z-10">
                                    <input
                                        type="url"
                                        placeholder="Enter suspicious domain or link..."
                                        className="w-full bg-black/40 border border-white/10 rounded-2xl px-6 py-4 focus:outline-none focus:ring-1 focus:ring-cyber-blue focus:border-cyber-blue transition-all font-mono text-sm text-cyber-blue placeholder-slate-600 outline-none shadow-inner"
                                        value={url}
                                        onChange={(e) => setUrl(e.target.value)}
                                        spellCheck="false"
                                    />
                                    <button
                                        onClick={() => handleScan('url')}
                                        disabled={!url || loading}
                                        className="w-full bg-white/5 hover:bg-cyber-blue/10 border border-white/10 hover:border-cyber-blue/50 disabled:opacity-30 disabled:hover:border-white/10 text-white font-bold tracking-widest uppercase py-4 rounded-2xl transition-all duration-300 flex items-center justify-center gap-3"
                                    >
                                        Execute Phishing Scan
                                    </button>
                                </div>
                            </div>

                            {/* SMS Card */}
                            <div className="bg-white/[0.02] backdrop-blur-2xl rounded-3xl p-8 border border-white/10 shadow-[0_8px_32px_0_rgba(0,0,0,0.36)] relative group overflow-hidden">
                                <div className="absolute top-0 right-0 w-32 h-32 bg-cyber-purple/10 rounded-full blur-3xl transition-all duration-700 group-hover:bg-cyber-purple/30 group-hover:w-48 group-hover:h-48 group-hover:-top-10 group-hover:-right-10" />
                                
                                <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                                    <div className="w-12 h-12 rounded-2xl bg-cyber-purple/20 flex items-center justify-center border border-cyber-purple/30 backdrop-blur-md">
                                        <MessageSquare className="w-6 h-6 text-cyber-purple" />
                                    </div>
                                    SMS Introspection
                                </h2>
                                
                                <div className="space-y-4 relative z-10">
                                    <textarea
                                        placeholder="Paste full SMS or email body content..."
                                        className="w-full bg-black/40 border border-white/10 rounded-2xl px-6 py-4 h-32 focus:outline-none focus:ring-1 focus:ring-cyber-purple focus:border-cyber-purple transition-all resize-none text-sm text-cyber-purple placeholder-slate-600 font-mono leading-relaxed shadow-inner no-scrollbar"
                                        value={sms}
                                        onChange={(e) => setSms(e.target.value)}
                                        spellCheck="false"
                                    />
                                    <button
                                        onClick={() => handleScan('sms')}
                                        disabled={!sms || loading}
                                        className="w-full bg-white/5 hover:bg-cyber-purple/10 border border-white/10 hover:border-cyber-purple/50 disabled:opacity-30 disabled:hover:border-white/10 text-white font-bold tracking-widest uppercase py-4 rounded-2xl transition-all duration-300 flex items-center justify-center gap-3"
                                    >
                                        Execute Smishing Scan
                                    </button>
                                </div>
                            </div>

                            {/* Deep Scan Fusion */}
                            <button
                                onClick={() => handleScan('full')}
                                disabled={(!url && !sms) || loading}
                                className="w-full h-20 bg-gradient-to-r from-cyber-blue to-cyber-purple hover:scale-[1.02] disabled:hover:scale-100 disabled:opacity-20 text-white font-black text-lg uppercase tracking-[0.2em] rounded-3xl shadow-[0_0_40px_rgba(0,240,255,0.3)] transition-all duration-300 flex justify-center items-center gap-4 relative overflow-hidden group"
                            >
                                <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-500 ease-in-out" />
                                <Zap className="w-6 h-6 animate-pulse relative z-10" /> 
                                <span className="relative z-10">Force Deep Fusion Scan</span>
                            </button>

                        </div>

                        {/* RIGHT COLUMN: RESULTS */}
                        <div className="xl:col-span-7 flex flex-col h-full min-h-[600px] mt-8 xl:mt-0">
                            {error && (
                                <div className="backdrop-blur-xl bg-red-500/10 border border-red-500/50 p-6 rounded-3xl flex items-center gap-5 mb-8 shadow-[0_0_30px_rgba(239,68,68,0.2)]">
                                    <div className="bg-red-500/20 p-3 rounded-full">
                                        <AlertTriangle className="w-8 h-8 text-red-500" />
                                    </div>
                                    <div>
                                        <h4 className="font-bold text-red-100 text-lg">System Override Failed</h4>
                                        <p className="text-sm mt-1 text-red-300 font-medium">{error}</p>
                                    </div>
                                </div>
                            )}

                            {loading ? (
                                <div className="bg-white/[0.01] border border-white/5 rounded-[40px] p-12 h-full flex flex-col items-center justify-center text-center flex-1 backdrop-blur-3xl shadow-2xl relative overflow-hidden ring-1 ring-white/10">
                                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-cyber-blue/10 via-transparent to-transparent animate-pulse-slow" />
                                    <div className="relative z-10 flex flex-col items-center">
                                        <div className="w-32 h-32 border-2 border-cyber-blue/20 border-t-cyber-blue rounded-full animate-spin mb-8 flex items-center justify-center shadow-[0_0_50px_rgba(0,240,255,0.2)]">
                                            <div className="w-24 h-24 border-2 border-cyber-purple/20 border-b-cyber-purple rounded-full animate-spin-reverse" />
                                        </div>
                                        <h3 className="text-3xl font-black mb-3 text-transparent bg-clip-text bg-gradient-to-r from-cyber-blue to-white tracking-[0.2em] uppercase">Interrogating AI Agents</h3>
                                        <p className="max-w-md text-cyber-blue/60 font-mono text-sm leading-relaxed pulse">Transmitting payload to global threat heuristics grid and executing NLP transformer pipelines...</p>
                                    </div>
                                </div>
                            ) : result ? (
                                <div className="flex-1 h-full animate-in zoom-in-[0.98] fade-in duration-700">
                                    <ResultsPanel result={result} />
                                </div>
                            ) : (
                                <div className="bg-white/[0.01] border border-white/5 rounded-[40px] p-12 h-full flex flex-col items-center justify-center text-center flex-1 backdrop-blur-3xl shadow-2xl ring-1 ring-white/5">
                                    <div className="relative mb-8 group">
                                        <div className="absolute inset-0 bg-cyber-blue blur-3xl opacity-0 group-hover:opacity-20 transition-duration-1000" />
                                        <div className="w-24 h-24 rounded-full border border-white/10 bg-white/5 flex items-center justify-center relative animate-float">
                                            <Shield className="w-10 h-10 text-white/30" />
                                        </div>
                                    </div>
                                    <h3 className="text-3xl font-bold mb-4 tracking-[0.2em] uppercase text-white/40">Awaiting Payload</h3>
                                    <p className="max-w-md text-white/30 font-medium leading-relaxed">System initialized. Awaiting URL or SMS input vector to begin Multi-Agent threat analysis.</p>
                                </div>
                            )}
                        </div>

                    </div>
                )}
            </div>
        </div>
    );
}

export default App;
