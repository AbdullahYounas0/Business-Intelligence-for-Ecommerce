import { useQuery } from '@tanstack/react-query'
import { AlertTriangle } from 'lucide-react'
import type { WsMessage } from '../hooks/useWebSocket'

interface Alert {
  alert_id: string; type: string; severity: string; product_title: string
  sku: string; units_available: number | null; pending_orders: number | null
  gpt_recommendation: string; created_at: string
}
interface Props { wsMessages: WsMessage[] }

export default function AlertsFeed({ wsMessages }: Props) {
  const { data, isLoading } = useQuery<{ alerts: Alert[] }>({
    queryKey: ['alerts'],
    queryFn: () => fetch('/inventory/alerts').then((r) => r.json()),
    refetchInterval: 30_000,
  })

  const allAlerts = (data?.alerts ?? []).slice(0, 20)

  return (
    <div className="glass rounded-2xl p-5 glow-red h-full">
      <div className="flex items-center gap-2.5 mb-5">
        <AlertTriangle size={15} className="text-red-400" />
        <span className="text-white font-semibold text-sm">Inventory Alerts</span>
        <span className="ml-auto text-xs px-2.5 py-1 rounded-full"
          style={{ background: 'rgba(239,68,68,0.1)', color: '#fca5a5' }}>
          {allAlerts.length} active
        </span>
      </div>
      {isLoading && <p className="text-gray-500 text-sm">Loading...</p>}
      {!isLoading && allAlerts.length === 0 && (
        <p className="text-center py-8 text-sm text-gray-500">No active alerts</p>
      )}
      <div className="space-y-2">
        {allAlerts.map((alert) => (
          <div key={alert.alert_id} className="rounded-xl p-3 text-sm"
            style={{ background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.25)' }}>
            <p className="font-semibold text-red-300">{alert.product_title}</p>
            <p className="text-xs text-gray-400 mt-1">{alert.gpt_recommendation}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
