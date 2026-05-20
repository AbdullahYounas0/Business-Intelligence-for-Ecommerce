import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import { BarChart3, ThumbsUp, Minus, ThumbsDown, Sparkles } from 'lucide-react'

interface TopicRow { topic: string; positive: number; neutral: number; negative: number }
interface SummaryData {
  total_reviews: number
  breakdown: { positive: number; neutral: number; negative: number }
  by_topic: TopicRow[]
  narrative: string
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-xl p-3 text-xs" style={{ background: 'rgba(15,18,40,0.95)', border: '1px solid rgba(255,255,255,0.08)', backdropFilter: 'blur(16px)' }}>
      <p className="font-semibold mb-2" style={{ color: '#e2e8f0' }}>{label}</p>
      {payload.map((p: any) => (
        <div key={p.dataKey} className="flex items-center gap-2 mb-1">
          <div className="w-2 h-2 rounded-full" style={{ background: p.fill }} />
          <span style={{ color: 'rgba(148,163,184,0.8)' }}>{p.dataKey}: </span>
          <span style={{ color: '#e2e8f0' }}>{p.value}</span>
        </div>
      ))}
    </div>
  )
}

export default function SentimentChart() {
  const { data, isLoading } = useQuery<SummaryData>({
    queryKey: ['sentiment-summary'],
    queryFn: () => fetch('/sentiment/summary').then((r) => r.json()),
    refetchInterval: 120_000,
  })

  const breakdown = data?.breakdown
  const pills = breakdown ? [
    { icon: ThumbsUp,   label: 'Positive', value: breakdown.positive ?? 0, color: '#4ade80', bg: 'rgba(74,222,128,0.1)',   border: 'rgba(74,222,128,0.25)'  },
    { icon: Minus,      label: 'Neutral',  value: breakdown.neutral  ?? 0, color: '#94a3b8', bg: 'rgba(148,163,184,0.08)', border: 'rgba(148,163,184,0.2)'  },
    { icon: ThumbsDown, label: 'Negative', value: breakdown.negative ?? 0, color: '#f87171', bg: 'rgba(239,68,68,0.1)',    border: 'rgba(239,68,68,0.25)'   },
  ] : []

  return (
    <div className="glass rounded-2xl p-5 glow-green h-full">
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ background: 'rgba(74,222,128,0.12)', border: '1px solid rgba(74,222,128,0.25)' }}>
            <BarChart3 size={15} className="text-green-400" />
          </div>
          <span className="text-white font-semibold text-sm">Review Sentiment</span>
        </div>
        {data && (
          <span className="text-xs px-2.5 py-1 rounded-full"
            style={{ background: 'rgba(74,222,128,0.08)', color: '#86efac', border: '1px solid rgba(74,222,128,0.2)' }}>
            {data.total_reviews ?? 0} reviews · 7d
          </span>
        )}
      </div>

      {isLoading && (
        <div className="space-y-3">
          <div className="h-8 rounded-lg animate-pulse" style={{ background: 'rgba(255,255,255,0.04)' }} />
          <div className="h-48 rounded-lg animate-pulse" style={{ background: 'rgba(255,255,255,0.04)' }} />
        </div>
      )}

      {data && (
        <>
          {/* Pills */}
          <div className="flex gap-2 mb-5">
            {pills.map(({ icon: Icon, label, value, color, bg, border }, i) => (
              <motion.div key={label} initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.08 }}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium"
                style={{ background: bg, border: `1px solid ${border}`, color }}>
                <Icon size={11} />
                <span>{value} {label}</span>
              </motion.div>
            ))}
          </div>

          {/* Chart */}
          <ResponsiveContainer width="100%" height={190}>
            <BarChart data={data.by_topic ?? []} margin={{ top: 0, right: 0, left: -22, bottom: 0 }} barCategoryGap="30%">
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" vertical={false} />
              <XAxis dataKey="topic" tick={{ fill: 'rgba(148,163,184,0.6)', fontSize: 10 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: 'rgba(148,163,184,0.6)', fontSize: 10 }} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
              <Bar dataKey="positive" fill="#4ade80" radius={[4,4,0,0]} />
              <Bar dataKey="neutral"  fill="rgba(148,163,184,0.4)" radius={[4,4,0,0]} />
              <Bar dataKey="negative" fill="#f87171" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>

          {/* Narrative */}
          {data.narrative && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}
              className="mt-4 rounded-xl p-3"
              style={{ background: 'rgba(74,222,128,0.05)', border: '1px solid rgba(74,222,128,0.12)' }}>
              <div className="flex items-center gap-1.5 mb-2">
                <Sparkles size={11} className="text-green-400" />
                <span className="text-xs font-medium text-green-400">GPT Weekly Summary</span>
              </div>
              <p className="text-xs leading-relaxed" style={{ color: 'rgba(203,213,225,0.8)' }}>{data.narrative}</p>
            </motion.div>
          )}
        </>
      )}
    </div>
  )
}
