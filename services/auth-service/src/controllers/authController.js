const bcrypt = require('bcryptjs')
const jwt = require('jsonwebtoken')
const pool = require('../config/db')
const { getClient } = require('../config/redis')  // ← ganti ini

const generateToken = (payload) => {
  return jwt.sign(payload, process.env.JWT_SECRET, {
    expiresIn: process.env.JWT_EXPIRES_IN || '7d'
  })
}

const register = async (req, res) => {
  const { nama, email, password } = req.body
  try {
    const existing = await pool.query('SELECT id FROM users WHERE email = $1', [email])
    if (existing.rows.length > 0) {
      return res.status(409).json({ error: 'Email sudah terdaftar' })
    }
    const hashedPassword = await bcrypt.hash(password, 12)
    const result = await pool.query(
      `INSERT INTO users (nama, email, password)
       VALUES ($1, $2, $3)
       RETURNING id, nama, email, role, created_at`,
      [nama, email, hashedPassword]
    )
    const user = result.rows[0]
    const token = generateToken({ id: user.id, email: user.email, role: user.role })
    res.status(201).json({
      message: 'Registrasi berhasil',
      token,
      user: { id: user.id, nama: user.nama, email: user.email, role: user.role }
    })
  } catch (err) {
    console.error('Register error:', err.message)
    res.status(500).json({ error: 'Internal server error' })
  }
}

const login = async (req, res) => {
  const { email, password } = req.body
  try {
    const result = await pool.query('SELECT * FROM users WHERE email = $1', [email])
    if (result.rows.length === 0) {
      return res.status(401).json({ error: 'Email atau password salah' })
    }
    const user = result.rows[0]
    const isValid = await bcrypt.compare(password, user.password)
    if (!isValid) {
      return res.status(401).json({ error: 'Email atau password salah' })
    }
    const token = generateToken({ id: user.id, email: user.email, role: user.role })

    // Simpan session di Redis
    const redisClient = getClient()  // ← gunakan getClient()
    await redisClient.setEx(
      `session:${user.id}`,
      7 * 24 * 60 * 60,
      JSON.stringify({ id: user.id, email: user.email, role: user.role })
    )
    res.json({
      message: 'Login berhasil',
      token,
      user: { id: user.id, nama: user.nama, email: user.email, role: user.role }
    })
  } catch (err) {
    console.error('Login error:', err.message)
    res.status(500).json({ error: 'Internal server error' })
  }
}

const logout = async (req, res) => {
  try {
    const redisClient = getClient()  // ← gunakan getClient()
    await redisClient.del(`session:${req.user.id}`)
    res.json({ message: 'Logout berhasil' })
  } catch (err) {
    console.error('Logout error:', err.message)
    res.status(500).json({ error: 'Internal server error' })
  }
}

const me = async (req, res) => {
  try {
    const result = await pool.query(
      'SELECT id, nama, email, role, created_at FROM users WHERE id = $1',
      [req.user.id]
    )
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'User tidak ditemukan' })
    }
    res.json({ user: result.rows[0] })
  } catch (err) {
    console.error('Me error:', err.message)
    res.status(500).json({ error: 'Internal server error' })
  }
}

module.exports = { register, login, logout, me }