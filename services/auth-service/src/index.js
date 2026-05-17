require('dotenv').config()
const express = require('express')
const helmet = require('helmet')
const cors = require('cors')
const morgan = require('morgan')
const { connectRedis } = require('./config/redis')
const authRoutes = require('./routes/auth')

const app = express()
const PORT = process.env.AUTH_PORT || 3001

app.use(helmet())
app.use(cors())
app.use(morgan('combined'))
app.use(express.json())

app.use('/auth', authRoutes)

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'auth-service', timestamp: new Date().toISOString() })
})

app.use((req, res) => {
  res.status(404).json({ error: 'Route tidak ditemukan' })
})

app.use((err, req, res, next) => {
  console.error('Unhandled error:', err.message)
  res.status(500).json({ error: 'Internal server error' })
})

const start = async () => {
  try {
    await connectRedis()
    app.listen(PORT, () => {
      console.log(`🚀 Auth service berjalan di port ${PORT}`)
    })
  } catch (err) {
    console.error('Failed to start:', err.message)
    process.exit(1)
  }
}

start()