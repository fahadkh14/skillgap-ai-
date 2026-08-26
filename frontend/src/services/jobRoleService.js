import api from './api'

const jobRoleService = {
  async listRoles() {
    const res = await api.get('/job-roles')
    return res.data.data
  },
  async getRole(id) {
    const res = await api.get(`/job-roles/${id}`)
    return res.data.data
  },
}

export default jobRoleService
