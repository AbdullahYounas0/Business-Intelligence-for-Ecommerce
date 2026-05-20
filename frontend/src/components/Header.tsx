import { Zap, Radio } from 'lucide-react'
import { motion } from 'framer-motion'

interface Props { connected: boolean }

export default function Header({ connected }: Props) {
  return (
    <header className="relative z-20 border-b px-6 py-4 flex items-center justify-between"
      style={{ background: 'rgba(4,5,15,0.8)', backdropFilter: 'blur(20px)', borderColor: 'rgba(255,255,255,0.06)' }}>

      {/* Logo */}
      <div className="flex items-center gap-3">
        <div className="relative w-9 h-9 rounded-xl flex items-center justify-center"
          style={{ background: 'linear-gradient(135deg,#6366f1,#8b5cf6)', boxShadow: '0 0 20px rgba(99,102,241,0.4)' }}>
          <Zap size={16} className="text-white" fill="white" />
        </div>
        <div>
          <h1 className="text-white font-semibold text-base leading-none tracking-tight">
            E-Commerce Intelligence Hub
          </h1>
          <p className="text-xs mt-0.5" style={{ color: 'rgba(148,163,184,0.7)' }}>
            BigQuery · GPT-4o · Real-time
          </p>
        </div>
      </div>

      {/* Live status */}
      <motion.div
        className="flex items-center gap-2 px-3 py-1.5 rounded-full"
        style={{ background: connected ? 'rgba(74,222,128,0.08)' : 'rgba(239,68,68,0.08)',
                 border: `1px solid ${connected ? 'rgba(74,222,128,0.2)' : 'rgba(239,68,68,0.2)'}` }}
        animate={{ opacity: [0.8, 1, 0.8] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        <div className="relative flex items-center justify-center w-2 h-2">
          <div className={`absolute w-2 h-2 rounded-full ${connected ? 'bg-green-400 live-ping' : 'bg-red-400'}`} />
          <div className={`w-2 h-2 rounded-full ${connected ? 'bg-green-400' : 'bg-red-400'}`} />
        </div>
        <Radio size={11} className={connected ? 'text-green-400' : 'text-red-400'} />
        <span className={`text-xs font-medium ${connected ? 'text-green-400' : 'text-red-400'}`}>
          {connected ? 'Live' : 'Reconnecting'}
        </span>
      </motion.div>
    </header>
  )
}
