import api from './api'

const dashboardService = {
  async getDashboard() {
    const res = await api.get('/dashboard')
    return res.data.data
  },
}

export default dashboardService
