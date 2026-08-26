import api from './api'

const authService = {
  async register({ fullName, email, password, confirmPassword }) {
    const res = await api.post('/auth/register', {
      full_name: fullName,
      email,
      password,
      confirm_password: confirmPassword,
    })
    return res.data.data
  },

  async login({ email, password }) {
    const res = await api.post('/auth/login', { email, password })
    return res.data.data
  },

  async logout() {
    try {
      await api.post('/auth/logout')
    } finally {
      localStorage.removeItem('skillgap_token')
      localStorage.removeItem('skillgap_user')
    }
  },

  async getCurrentUser() {
    const res = await api.get('/auth/me')
    return res.data.data
  },
}

export default authService
