const redis = require('redis')

let client

const connectRedis = async () => {
  client = redis.createClient({
    socket: {
      host: process.env.REDIS_HOST,
      port: parseInt(process.env.REDIS_PORT),
    },
    password: process.env.REDIS_PASSWORD,
  })

  client.on('connect', () => console.log('✅ Redis connected'))
  client.on('error', (err) => console.error('❌ Redis error:', err.message))

  await client.connect()
  return client
}

const getClient = () => {
  if (!client) throw new Error('Redis belum terkoneksi')
  return client
}

module.exports = { connectRedis, getClient }