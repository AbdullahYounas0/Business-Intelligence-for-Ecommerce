import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { Cpu, Coins, Hash } from 'lucide-react'

interface CostRow {
  module: string; date: string
  prompt_tokens: number; completion_tokens: number; cost_usd: number
}

const moduleStyle: Record<string, { color: string; bg: string; border: string }> = {
  churn:     { color: '#c084fc', bg: 'rgba(192,132,252,0.1)',  border: 'rgba(192,132,252,0.25)' },
  inventory: { color: '#60a5fa', bg: 'rgba(96,165,250,0.1)',   border: 'rgba(96,165,250,0.25)'  },
  sentiment: { color: '#34d399', bg: 'rgba(52,211,153,0.1)',   border: 'rgba(52,211,153,0.25)'  },
}

export default function CostAudit() {
  const { data, isLoading } = useQuery<CostRow[]>({
    queryKey: ['costs'],
    queryFn: () => fetch('/analytics/costs').then((r) => r.json()),
    refetchInterval: 300_000,
  })

  const rows = data ?? []
  const totalCost   = rows.reduce((s, r) => s + r.cost_usd, 0)
  const totalTokens = rows.reduce((s, r) => s + r.prompt_tokens + r.completion_tokens, 0)

  return (
    <div className="glass rounded-2xl p-5 glow-indigo h-full">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ background: 'rgba(99,102,241,0.15)', border: '1px solid rgba(99,102,241,0.3)' }}>
            <Cpu size={15} className="text-indigo-400" />
          </div>
          <span className="text-white font-semibold text-sm">GPT Cost Audit</span>
        </div>
        {!isLoading && rows.length > 0 && (
          <span className="text-xs px-2.5 py-1 rounded-full font-medium"
            style={{ background: 'rgba(99,102,241,0.1)', color: '#a5b4fc', border: '1px solid rgba(99,102,241,0.2)' }}>
            90-day window
          </span>
        )}
      </div>

      {isLoading && (
        <div className="space-y-2">
          {[1,2].map(i => <div key={i} className="h-16 rounded-xl animate-pulse" style={{ background: 'rgba(255,255,255,0.04)' }} />)}
        </div>
      )}

      {rows.length > 0 && (
        <>
          {/* Stat cards */}
          <div className="grid grid-cols-2 gap-3 mb-5">
            {[
              { icon: Coins, label: 'Total Cost',   value: `$${totalCost.toFixed(4)}` },
              { icon: Hash,  label: 'Total Tokens', value: totalTokens.toLocaleString() },
            ].map(({ icon: Icon, label, value }, i) => (
              <motion.div key={label} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="rounded-xl p-3"
                style={{ background: 'rgba(99,102,241,0.06)', border: '1px solid rgba(99,102,241,0.12)' }}>
                <div className="flex items-center gap-1.5 mb-1.5">
                  <Icon size={11} style={{ color: 'rgba(165,180,252,0.6)' }} />
                  <p className="text-xs" style={{ color: 'rgba(148,163,184,0.6)' }}>{label}</p>
                </div>
                <p className="font-bold text-base shimmer-text">{value}</p>
              </motion.div>
            ))}
          </div>

          {/* Table */}
          <div className="overflow-y-auto max-h-48">
            <table className="w-full text-xs">
              <thead className="sticky top-0" style={{ background: 'rgba(4,5,15,0.8)' }}>
                <tr className="border-b" style={{ color: 'rgba(148,163,184,0.5)', borderColor: 'rgba(255,255,255,0.06)' }}>
                  <th className="text-left pb-2 font-medium">Module</th>
                  <th className="text-left pb-2 font-medium">Date</th>
                  <th className="text-right pb-2 font-medium">Tokens</th>
                  <th className="text-right pb-2 font-medium">Cost</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row, i) => {
                  const s = moduleStyle[row.module] ?? { color: '#94a3b8', bg: 'transparent', border: 'transparent' }
                  return (
                    <motion.tr key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                      transition={{ delay: i * 0.04 }}
                      className="border-b" style={{ borderColor: 'rgba(255,255,255,0.04)' }}>
                      <td className="py-2 pr-3">
                        <span className="px-2 py-0.5 rounded text-xs font-semibold"
                          style={{ color: s.color, background: s.bg, border: `1px solid ${s.border}` }}>
                          {row.module}
                        </span>
                      </td>
                      <td className="py-2 pr-3" style={{ color: 'rgba(148,163,184,0.6)' }}>{row.date}</td>
                      <td className="py-2 pr-3 text-right" style={{ color: '#e2e8f0' }}>
                        {(row.prompt_tokens + row.completion_tokens).toLocaleString()}
                      </td>
                      <td className="py-2 text-right font-medium" style={{ color: '#e2e8f0' }}>
                        ${row.cost_usd.toFixed(4)}
                      </td>
                    </motion.tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  )
}
