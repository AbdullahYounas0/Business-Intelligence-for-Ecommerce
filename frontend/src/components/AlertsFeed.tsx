import { useEffect, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import { Package, Clock, TrendingUp, Bell, AlertTriangle } from 'lucide-react'
import type { WsMessage } from '../hooks/useWebSocket'

interface Alert {
  alert_id: string; type: string; severity: string; product_title: string
  sku: string; units_available: number | null; pending_orders: number | null
  gpt_recommendation: string; created_at: string
}
interface Props { wsMessages: WsMessage[] }

const severityStyle = {
  high:   { bg: 'rgba(239,68,68,0.08)',   border: 'rgba(239,68,68,0.25)',   text: '#fca5a5', dot: '#ef4444' },
  medium: { bg: 'rgba(245,158,11,0.08)',  border: 'rgba(245,158,11,0.25)',  text: '#fcd34d', dot: '#f59e0b' },
  low:    { bg: 'rgba(99,102,241,0.08)',  border: 'rgba(99,102,241,0.25)', text: '#a5b4fc', dot: '#6366f1' },
}
const TypeIcon = ({ type }: { type: string }) => {
  const cls = 'shrink-0'
  if (type === 'low_stock')    return <Package size={14} className={cls} />
  if (type === 'stalled_order') return <Clock size={14} className={cls} />
  if (type === 'demand_spike') return <TrendingUp size={14} className={cls} />
  return <Bell size={14} className={cls} />
}

export default function AlertsFeed({ wsMessages }: Props) {
  const { data, isLoading } = useQuery<{ alerts: Alert[] }>({
    queryKey: ['alerts'],
    queryFn: () => fetch('/inventory/alerts').then((r) => r.json()),
    refetchInterval: 30_000,
  })
  const [liveAlerts, setLiveAlerts] = useState<Alert[]>([])
  useEffect(() => {
    const inv = wsMessages.filter((m) => m.type === 'inventory_alert').map((m) => m.alert as Alert)
    setLiveAlerts(inv)
  }, [wsMessages])

  const allAlerts = [...liveAlerts, ...(data?.alerts ?? [])]
    .filter((a, i, arr) => arr.findIndex((x) => x.alert_id === a.alert_id) === i)
    .slice(0, 20)

  return (
    <div className="glass rounded-2xl p-5 glow-red h-full">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ background: 'rgba(239,68,68,0.15)', border: '1px solid rgba(239,68,68,0.25)' }}>
            <AlertTriangle size={15} className="text-red-400" />
          </div>
          <span className="text-white font-semibold text-sm">Inventory Alerts</span>
        </div>
        <span className="text-xs px-2.5 py-1 rounded-full font-medium"
          style={{ background: 'rgba(239,68,68,0.1)', color: '#fca5a5', border: '1px solid rgba(239,68,68,0.2)' }}>
          {allAlerts.length} active
        </span>
      </div>

      {isLoading && (
        <div className="space-y-2">
          {[1,2,3].map(i => <div key={i} className="h-16 rounded-lg animate-pulse" style={{ background: 'rgba(255,255,255,0.04)' }} />)}
        </div>
      )}

      <div className="space-y-2.5 max-h-80 overflow-y-auto pr-1">
        {allAlerts.length === 0 && !isLoading && (
          <p className="text-center py-8 text-sm" style={{ color: 'rgba(148,163,184,0.5)' }}>No active alerts</p>
        )}
        <AnimatePresence>
          {allAlerts.map((alert, i) => {
            const s = severityStyle[alert.severity as keyof typeof severityStyle] ?? severityStyle.low
            return (
              <motion.div key={alert.alert_id}
                initial={{ opacity: 0, x: -16 }} animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05, duration: 0.3 }}
                className="rounded-xl p-3 text-sm"
                style={{ background: s.bg, border: `1px solid ${s.border}` }}
              >
                <div className="flex items-center gap-2 mb-1" style={{ color: s.text }}>
                  <TypeIcon type={alert.type} />
                  <span className="font-semibold truncate">{alert.product_title}</span>
                  <span className="ml-auto text-xs opacity-60 capitalize shrink-0">{alert.severity}</span>
                </div>
                {alert.units_available !== null && (
                  <p className="text-xs mb-1 opacity-70" style={{ color: s.text }}>
                    {alert.units_available} units · {alert.pending_orders} pending
                  </p>
                )}
                {alert.gpt_recommendation && (
                  <p className="text-xs leading-relaxed" style={{ color: 'rgba(203,213,225,0.8)' }}>
                    {alert.gpt_recommendation}
                  </p>
                )}
              </motion.div>
            )
          })}
        </AnimatePresence>
      </div>
    </div>
  )
}
