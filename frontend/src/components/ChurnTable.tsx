import { useQuery } from '@tanstack/react-query'
import { Users, ChevronRight } from 'lucide-react'

interface Customer {
  customer_id: string; name: string; email: string; rfm_score: number
  recency_days: number; frequency: number; monetary: number
  lifetime_value: number; last_order_date: string
}

const rfmStyle = (s: number) =>
  s < 20 ? { color: '#f87171', bg: 'rgba(239,68,68,0.12)', border: 'rgba(239,68,68,0.3)' }
         : s < 30 ? { color: '#fbbf24', bg: 'rgba(245,158,11,0.12)', border: 'rgba(245,158,11,0.3)' }
                  : { color: '#4ade80', bg: 'rgba(74,222,128,0.12)', border: 'rgba(74,222,128,0.3)' }

export default function ChurnTable() {
  const { data, isLoading } = useQuery<{ total: number; customers: Customer[] }>({
    queryKey: ['at-risk'],
    queryFn: () => fetch('/churn/at-risk').then((r) => r.json()),
    refetchInterval: 60_000,
  })

  return (
    <div className="glass rounded-2xl p-5 glow-indigo h-full flex flex-col">
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ background: 'rgba(99,102,241,0.15)', border: '1px solid rgba(99,102,241,0.3)' }}>
            <Users size={15} className="text-indigo-400" />
          </div>
          <span className="text-white font-semibold text-sm">At-Risk Customers</span>
        </div>
        <span className="text-xs px-2.5 py-1 rounded-full font-medium"
          style={{ background: 'rgba(99,102,241,0.1)', color: '#a5b4fc', border: '1px solid rgba(99,102,241,0.2)' }}>
          {data?.total ?? '—'} at risk
        </span>
      </div>

      {isLoading && (
        <div className="space-y-2 flex-1">
          {[1,2,3].map(i => <div key={i} className="h-10 rounded-lg animate-pulse" style={{ background: 'rgba(255,255,255,0.04)' }} />)}
        </div>
      )}

      {!isLoading && (
        <div className="overflow-x-auto flex-1">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-xs border-b" style={{ color: 'rgba(148,163,184,0.6)', borderColor: 'rgba(255,255,255,0.06)' }}>
                <th className="text-left pb-3 font-medium">Customer</th>
                <th className="text-left pb-3 font-medium">RFM</th>
                <th className="text-left pb-3 font-medium hidden sm:table-cell">Last Order</th>
                <th className="text-right pb-3 font-medium">LTV</th>
                <th className="w-5" />
              </tr>
            </thead>
            <tbody>
              {(data?.customers ?? []).map((c) => {
                const rfm = rfmStyle(c.rfm_score)
                return (
                  <tr key={c.customer_id} className="border-b cursor-pointer"
                    style={{ borderColor: 'rgba(255,255,255,0.04)' }}>
                    <td className="py-3 pr-3">
                      <div className="font-medium" style={{ color: '#e2e8f0' }}>{c.name}</div>
                      <div className="text-xs" style={{ color: 'rgba(148,163,184,0.5)' }}>{c.email}</div>
                    </td>
                    <td className="py-3 pr-3">
                      <span className="text-xs font-bold px-2 py-0.5 rounded-md"
                        style={{ color: rfm.color, background: rfm.bg, border: `1px solid ${rfm.border}` }}>
                        {c.rfm_score}
                      </span>
                    </td>
                    <td className="py-3 pr-3 hidden sm:table-cell text-xs" style={{ color: 'rgba(148,163,184,0.6)' }}>
                      {c.last_order_date}
                    </td>
                    <td className="py-3 text-right text-sm font-medium" style={{ color: '#e2e8f0' }}>
                      ${c.lifetime_value.toFixed(2)}
                    </td>
                    <td className="py-3 pl-1">
                      <ChevronRight size={13} style={{ color: 'rgba(148,163,184,0.3)' }} />
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
