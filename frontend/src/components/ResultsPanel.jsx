import React from 'react';
import { CheckCircle, AlertTriangle, XCircle, Shield, AlertOctagon, Terminal, FileText, Fingerprint } from 'lucide-react';

const ResultsPanel = ({ result }) => {
    if (!result) return null;

    const { status, confidence, explanation, details } = result;

    let themeColor = 'text-green-400';
    let bgColor = 'bg-green-500/10';
    let borderColor = 'border-green-500/30';
    let meterColor = 'bg-green-500';
    let glowColor = 'shadow-[0_0_30px_rgba(34,197,94,0.3)]';
    let Icon = CheckCircle;

    if (status.toLowerCase().includes('suspicious')) {
        themeColor = 'text-yellow-400';
        bgColor = 'bg-yellow-500/10';
        borderColor = 'border-yellow-500/30';
        meterColor = 'bg-yellow-500';
        glowColor = 'shadow-[0_0_40px_rgba(234,179,8,0.4)]';
        Icon = AlertTriangle;
    } else if (status.toLowerCase().includes('malicious') || status.toLowerCase().includes('phishing') || status.toLowerCase().includes('smishing')) {
        themeColor = 'text-red-500';
        bgColor = 'bg-red-500/10';
        borderColor = 'border-red-500/40';
        meterColor = 'bg-red-500';
        glowColor = 'shadow-[0_0_50px_rgba(239,68,68,0.6)]';
        Icon = AlertOctagon;
    }

    const confidenceFormatted = confidence.toFixed(1);

    return (
        <div className={`bg-white/[0.02] backdrop-blur-3xl rounded-[40px] p-8 lg:p-10 border border-white/5 h-full flex flex-col relative overflow-hidden transition-all duration-700 ${glowColor} ring-1 ring-white/5`}>
            
            <div className={`absolute top-0 right-0 w-64 h-64 ${meterColor} opacity-10 blur-[100px] rounded-full -mr-20 -mt-20`} />

            {/* Header / Verdict */}
            <div className="flex items-center justify-between border-b border-white/10 pb-8 mb-8 relative z-10">
                <div className="flex items-center gap-6">
                    <div className={`p-4 rounded-2xl ${bgColor} border ${borderColor} backdrop-blur-md`}>
                        <Icon className={`w-12 h-12 ${themeColor} drop-shadow-md`} />
                    </div>
                    <div>
                        <p className="text-xs text-white/40 font-mono tracking-[0.3em] uppercase mb-1">AI Fusion Verdict</p>
                        <h2 className={`text-4xl lg:text-5xl font-black uppercase tracking-wider ${themeColor} drop-shadow-lg`}>
                            {status}
                        </h2>
                    </div>
                </div>
            </div>

            {/* Risk Meter */}
            <div className="mb-10 bg-black/40 p-8 rounded-3xl border border-white/5 relative overflow-hidden shadow-inner group">
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:translate-x-full duration-1000 transition-transform" />
                
                <div className="flex justify-between items-end mb-4 relative z-10">
                    <span className="text-white/60 font-semibold tracking-wide flex items-center gap-3 text-lg">
                        <Fingerprint className="w-6 h-6 text-cyber-blue" /> Computed Probability
                    </span>
                    <span className={`text-4xl font-black ${themeColor} tracking-tighter`}>{confidenceFormatted}<span className="text-2xl opacity-70">%</span></span>
                </div>
                {/* Progress Bar Container */}
                <div className="h-4 w-full bg-white/5 rounded-full overflow-hidden relative z-10 shadow-inner">
                    <div 
                        className={`h-full ${meterColor} transition-all duration-1000 ease-out`} 
                        style={{ width: `${confidence}%` }}
                    >
                         <div className="w-full h-full bg-gradient-to-r from-transparent to-white/30" />
                    </div>
                </div>
            </div>

            {/* Explainability Panel */}
            <div className="mb-8 flex-1 relative z-10">
                <h3 className="text-sm font-bold text-white/40 mb-3 flex items-center gap-3 tracking-[0.2em] uppercase">
                    <FileText className="w-5 h-5 text-cyber-purple" /> Agent Reasoning
                </h3>
                <div className="bg-cyber-purple/5 p-6 rounded-3xl border border-cyber-purple/20 text-white/80 leading-relaxed min-h-[120px] font-medium shadow-inner text-lg">
                    <p className="font-mono">{explanation}</p>
                </div>
            </div>

            {/* Extracted Features (Raw Details) */}
            <div className="mt-auto relative z-10">
                <h3 className="text-xs font-bold text-white/30 mb-3 uppercase tracking-[0.2em] flex items-center gap-2">
                    <Terminal className="w-4 h-4 text-cyber-blue" /> Extracted Telemetry
                </h3>
                <div className="bg-[#050510] p-6 rounded-3xl border border-white/5 overflow-x-auto shadow-inner">
                    <pre className="text-sm text-cyber-blue/80 font-mono tracking-wider">
                        {JSON.stringify(details, null, 2)}
                    </pre>
                </div>
            </div>
            
        </div>
    );
};

export default ResultsPanel;
