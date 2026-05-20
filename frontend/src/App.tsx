import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { useWebSocket } from './hooks/useWebSocket'
import Header from './components/Header'
import ControlPanel from './components/ControlPanel'
import AlertsFeed from './components/AlertsFeed'
import ChurnTable from './components/ChurnTable'
import SentimentChart from './components/SentimentChart'
import CostAudit from './components/CostAudit'

const queryClient = new QueryClient()
const WS_URL = `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}/ws`

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.1 } },
}
const cardVariant = {
  hidden: { opacity: 0, y: 24 },
  show:   { opacity: 1, y: 0 },
}

function Dashboard() {
  const { messages, connected } = useWebSocket(WS_URL)

  return (
    <div className="min-h-screen" style={{ background: 'radial-gradient(ellipse 80% 50% at 50% -10%, rgba(99,102,241,0.12) 0%, transparent 70%), #04050f' }}>
      {/* Subtle grid overlay */}
      <div className="fixed inset-0 pointer-events-none" style={{
        backgroundImage: 'linear-gradient(rgba(99,102,241,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(99,102,241,0.03) 1px, transparent 1px)',
        backgroundSize: '48px 48px',
      }} />

      <Header connected={connected} />

      <div className="relative z-10 p-4 md:p-6 max-w-7xl mx-auto">
        <ControlPanel />
        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 md:grid-cols-2 gap-5"
        >
          <motion.div variants={cardVariant}><AlertsFeed wsMessages={messages} /></motion.div>
          <motion.div variants={cardVariant}><ChurnTable /></motion.div>
          <motion.div variants={cardVariant}><SentimentChart /></motion.div>
          <motion.div variants={cardVariant}><CostAudit /></motion.div>
        </motion.div>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Dashboard />
    </QueryClientProvider>
  )
}
