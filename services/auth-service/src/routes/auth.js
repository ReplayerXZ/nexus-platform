const express = require('express')
const { body } = require('express-validator')
const { register, login, logout, me } = require('../controllers/authController')
const { authenticate } = require('../middleware/auth')
const { validate } = require('../middleware/validate')

const router = express.Router()

router.post('/register',
  [
    body('nama').trim().notEmpty().withMessage('Nama wajib diisi'),
    body('email').isEmail().withMessage('Format email tidak valid'),
    body('password').isLength({ min: 6 }).withMessage('Password minimal 6 karakter'),
  ],
  validate,
  register
)

router.post('/login',
  [
    body('email').isEmail().withMessage('Format email tidak valid'),
    body('password').notEmpty().withMessage('Password wajib diisi'),
  ],
  validate,
  login
)

router.post('/logout', authenticate, logout)
router.get('/me', authenticate, me)

module.exports = router