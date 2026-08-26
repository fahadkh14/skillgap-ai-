import api from './api'

const skillService = {
  async listSkills({ search = '', proficiency = '' } = {}) {
    const params = {}
    if (search) params.search = search
    if (proficiency) params.proficiency = proficiency
    const res = await api.get('/skills', { params })
    return res.data.data
  },
  async addSkill(skill) {
    const res = await api.post('/skills', skill)
    return res.data.data
  },
  async updateSkill(id, fields) {
    const res = await api.put(`/skills/${id}`, fields)
    return res.data.data
  },
  async deleteSkill(id) {
    const res = await api.delete(`/skills/${id}`)
    return res.data
  },
}

export default skillService
