import { useState, useRef } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Database, Users, Package, MessageSquare, FileText,
  Upload, CheckCircle2, XCircle, Loader2, ChevronDown, Sparkles,
} from 'lucide-react'

interface ActionResult { ok: boolean; message: string }

function useAction(url: string, method = 'POST', invalidates: string[] = []) {
  const qc = useQueryClient()
  const [result, setResult] = useState<ActionResult | null>(null)

  const mutation = useMutation({
    mutationFn: () => fetch(url, { method }).then(async (r) => {
      const data = await r.json()
      if (!r.ok) throw new Error(data.detail ?? 'Request failed')
      return data
    }),
    onSuccess: (data) => {
      setResult({ ok: true, message: JSON.stringify(data).replace(/[{}"]/g, '').replace(/,/g, ' · ') })
      invalidates.forEach((k) => qc.invalidateQueries({ queryKey: [k] }))
      setTimeout(() => setResult(null), 4000)
    },
    onError: (e: Error) => {
      setResult({ ok: false, message: e.message })
      setTimeout(() => setResult(null), 5000)
    },
  })

  return { run: mutation.mutate, isPending: mutation.isPending, result }
}

interface ActionBtnProps {
  icon: React.ElementType
  label: string
  description: string
  accentColor: string
  accentBg: string
  accentBorder: string
  onClick: () => void
  isPending: boolean
  result: ActionResult | null
}

function ActionBtn({ icon: Icon, label, description, accentColor, accentBg, accentBorder, onClick, isPending, result }: ActionBtnProps) {
  return (
    <motion.button
      onClick={onClick}
      disabled={isPending}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className="relative w-full text-left rounded-xl p-4 transition-all disabled:opacity-60 disabled:cursor-not-allowed overflow-hidden"
      style={{ background: accentBg, border: `1px solid ${accentBorder}` }}
    >
      {/* Icon + text */}
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 mt-0.5"
          style={{ background: `color-mix(in srgb, ${accentColor} 15%, transparent)`, border: `1px solid ${accentBorder}` }}>
          {isPending
            ? <Loader2 size={14} style={{ color: accentColor }} className="animate-spin" />
            : <Icon size={14} style={{ color: accentColor }} />}
        </div>
        <div className="min-w-0">
          <p className="text-sm font-semibold leading-tight" style={{ color: '#e2e8f0' }}>{label}</p>
          <p className="text-xs mt-0.5" style={{ color: 'rgba(148,163,184,0.6)' }}>{description}</p>
        </div>
      </div>

      {/* Result toast */}
      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
            className="mt-3 flex items-start gap-2 text-xs rounded-lg px-3 py-2"
            style={{ background: result.ok ? 'rgba(74,222,128,0.08)' : 'rgba(239,68,68,0.08)',
                     border: `1px solid ${result.ok ? 'rgba(74,222,128,0.2)' : 'rgba(239,68,68,0.2)'}` }}
          >
            {result.ok
              ? <CheckCircle2 size={12} className="text-green-400 mt-0.5 shrink-0" />
              : <XCircle     size={12} className="text-red-400 mt-0.5 shrink-0" />}
            <span style={{ color: result.ok ? '#86efac' : '#fca5a5' }} className="break-all">{result.message}</span>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.button>
  )
}

function CsvUpload() {
  const [table, setTable] = useState('orders')
  const [file, setFile]   = useState<File | null>(null)
  const [result, setResult] = useState<ActionResult | null>(null)
  const [isPending, setIsPending] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)
  const qc = useQueryClient()

  const upload = async () => {
    if (!file) return
    setIsPending(true)
    const fd = new FormData()
    fd.append('file', file)
    try {
      const r = await fetch(`/ingest/upload?table=${table}`, { method: 'POST', body: fd })
      const data = await r.json()
      if (!r.ok) throw new Error(data.detail ?? 'Upload failed')
      setResult({ ok: true, message: `Uploaded ${data.uploaded} rows to ${table}` })
      setFile(null)
      qc.invalidateQueries({ queryKey: ['at-risk'] })
      qc.invalidateQueries({ queryKey: ['alerts'] })
    } catch (e: any) {
      setResult({ ok: false, message: e.message })
    } finally {
      setIsPending(false)
      setTimeout(() => setResult(null), 4000)
    }
  }

  return (
    <div className="rounded-xl p-4" style={{ background: 'rgba(99,102,241,0.06)', border: '1px solid rgba(99,102,241,0.15)' }}>
      <div className="flex items-center gap-2 mb-3">
        <Upload size={13} className="text-indigo-400" />
        <span className="text-sm font-semibold" style={{ color: '#e2e8f0' }}>CSV Upload → BigQuery</span>
      </div>

      {/* Table selector */}
      <div className="relative mb-2">
        <select value={table} onChange={(e) => setTable(e.target.value)}
          className="w-full appearance-none text-xs rounded-lg px-3 py-2 pr-7 outline-none"
          style={{ background: 'rgba(15,18,40,0.8)', border: '1px solid rgba(255,255,255,0.08)', color: '#e2e8f0' }}>
          <option value="orders">orders</option>
          <option value="products">products</option>
          <option value="reviews">reviews</option>
        </select>
        <ChevronDown size={11} className="absolute right-2.5 top-2.5 pointer-events-none" style={{ color: 'rgba(148,163,184,0.5)' }} />
      </div>

      {/* File picker */}
      <div
        onClick={() => inputRef.current?.click()}
        className="cursor-pointer rounded-lg px-3 py-3 text-center text-xs mb-2 transition-all"
        style={{ border: '1px dashed rgba(99,102,241,0.3)', color: 'rgba(148,163,184,0.6)',
                 background: file ? 'rgba(99,102,241,0.06)' : 'transparent' }}
      >
        {file ? <span style={{ color: '#a5b4fc' }}>{file.name}</span> : 'Click to select CSV file'}
        <input ref={inputRef} type="file" accept=".csv" className="hidden"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
      </div>

      {/* Upload button */}
      <motion.button
        onClick={upload}
        disabled={!file || isPending}
        whileTap={{ scale: 0.97 }}
        className="w-full text-xs font-semibold py-2 rounded-lg transition-all disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        style={{ background: 'rgba(99,102,241,0.2)', color: '#a5b4fc', border: '1px solid rgba(99,102,241,0.3)' }}
      >
        {isPending ? <><Loader2 size={11} className="animate-spin" /> Uploading...</> : <><Upload size={11} /> Upload</>}
      </motion.button>

      <AnimatePresence>
        {result && (
          <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
            className="mt-2 flex items-center gap-2 text-xs rounded-lg px-3 py-2"
            style={{ background: result.ok ? 'rgba(74,222,128,0.08)' : 'rgba(239,68,68,0.08)',
                     border: `1px solid ${result.ok ? 'rgba(74,222,128,0.2)' : 'rgba(239,68,68,0.2)'}` }}>
            {result.ok
              ? <CheckCircle2 size={11} className="text-green-400 shrink-0" />
              : <XCircle size={11} className="text-red-400 shrink-0" />}
            <span style={{ color: result.ok ? '#86efac' : '#fca5a5' }}>{result.message}</span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default function ControlPanel() {
  const seed      = useAction('/demo',                    'POST', ['at-risk', 'alerts', 'sentiment-summary', 'costs'])
  const churn     = useAction('/churn/trigger',           'POST', ['at-risk'])
  const inventory = useAction('/inventory/trigger',       'POST', ['alerts'])
  const sentiment = useAction('/sentiment/trigger',       'POST', ['sentiment-summary'])
  const report    = useAction('/sentiment/report/generate','POST', ['sentiment-summary'])

  const actions = [
    { ...seed,      icon: Database,      label: 'Seed Demo Data',       description: 'Insert mock data into BigQuery',   accentColor: '#818cf8', accentBg: 'rgba(99,102,241,0.06)',  accentBorder: 'rgba(99,102,241,0.18)' },
    { ...churn,     icon: Users,         label: 'Run Churn Analysis',   description: 'Compute RFM scores, flag at-risk', accentColor: '#c084fc', accentBg: 'rgba(192,132,252,0.06)', accentBorder: 'rgba(192,132,252,0.18)' },
    { ...inventory, icon: Package,       label: 'Scan Inventory',       description: 'Detect low stock & stalled orders',accentColor: '#f87171', accentBg: 'rgba(239,68,68,0.06)',  accentBorder: 'rgba(239,68,68,0.18)'  },
    { ...sentiment, icon: MessageSquare, label: 'Classify Reviews',     description: 'Run GPT-4o sentiment analysis',    accentColor: '#34d399', accentBg: 'rgba(52,211,153,0.06)',  accentBorder: 'rgba(52,211,153,0.18)' },
    { ...report,    icon: FileText,      label: 'Generate Report',      description: 'Create weekly GPT narrative',      accentColor: '#fbbf24', accentBg: 'rgba(251,191,36,0.06)',  accentBorder: 'rgba(251,191,36,0.18)' },
  ]

  return (
    <motion.div
      initial={{ opacity: 0, y: -16 }} animate={{ opacity: 1, y: 0 }}
      className="glass rounded-2xl p-5 mb-5"
    >
      <div className="flex items-center gap-2.5 mb-5">
        <div className="w-8 h-8 rounded-lg flex items-center justify-center"
          style={{ background: 'linear-gradient(135deg,rgba(99,102,241,0.3),rgba(139,92,246,0.3))', border: '1px solid rgba(99,102,241,0.3)' }}>
          <Sparkles size={14} className="text-indigo-300" />
        </div>
        <div>
          <p className="text-white font-semibold text-sm leading-none">Control Panel</p>
          <p className="text-xs mt-0.5" style={{ color: 'rgba(148,163,184,0.5)' }}>Trigger jobs · Upload data · Manage everything</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-3">
        {/* Action buttons — first 5 columns */}
        {actions.map((a) => (
          <ActionBtn key={a.label} {...a} onClick={a.run} />
        ))}

        {/* CSV Upload — last column */}
        <CsvUpload />
      </div>
    </motion.div>
  )
}
