import api from './api'

const resumeService = {
  async uploadResume(file) {
    const formData = new FormData()
    formData.append('file', file)
    const res = await api.post('/resume/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return res.data.data
  },
}

export default resumeService
