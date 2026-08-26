import api from './api'

const profileService = {
  async getProfile() {
    const res = await api.get('/profile')
    return res.data.data
  },
  async updateProfile(fields) {
    const res = await api.put('/profile', fields)
    return res.data.data
  },
}

export default profileService
