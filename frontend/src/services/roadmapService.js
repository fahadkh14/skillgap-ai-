import api from './api'

const roadmapService = {
  async getRoadmap(jobRoleId) {
    const params = jobRoleId ? { job_role_id: jobRoleId } : {}
    const res = await api.get('/roadmap', { params })
    return res.data.data
  },
  async updateItem(roadmapId, { skill, status, progress }) {
    const res = await api.put(`/roadmap/${roadmapId}`, { skill, status, progress })
    return res.data.data
  },
}

export default roadmapService
