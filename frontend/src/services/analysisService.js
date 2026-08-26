import api from './api'

const analysisService = {
  async runAnalysis(jobRoleId) {
    const res = await api.post('/analysis', { job_role_id: jobRoleId })
    return res.data.data
  },
  async listAnalyses() {
    const res = await api.get('/analysis')
    return res.data.data
  },
  async getAnalysis(id) {
    const res = await api.get(`/analysis/${id}`)
    return res.data.data
  },
}

export default analysisService
