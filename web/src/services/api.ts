import axios from 'axios'

const API_BASE_URL = '/api'

export const apiService = {
  async getHealth() {
    const response = await axios.get(`${API_BASE_URL}/health`)
    return response.data
  },

  async getConfig() {
    const response = await axios.get(`${API_BASE_URL}/config`)
    return response.data
  },

  async updateConfig(config: any) {
    const response = await axios.post(`${API_BASE_URL}/config`, config)
    return response.data
  },

  async scanDirectory(directory: string) {
    const response = await axios.post(`${API_BASE_URL}/scan`, { directory })
    return response.data
  },

  async getMetadata(path: string) {
    const response = await axios.get(`${API_BASE_URL}/metadata`, { params: { path } })
    return response.data
  },

  async updateMetadata(data: any) {
    const response = await axios.post(`${API_BASE_URL}/metadata`, data)
    return response.data
  },

  async triggerScrape(paths: string[], strategy: string) {
    const response = await axios.post(`${API_BASE_URL}/scrape`, { paths, strategy })
    return response.data
  },

  async triggerInject(paths: string[]) {
    const response = await axios.post(`${API_BASE_URL}/inject`, { paths })
    return response.data
  },

  async getLibrarySeries() {
    const response = await axios.get(`${API_BASE_URL}/library/series`)
    return response.data
  },

  async triggerLibraryScan() {
    const response = await axios.post(`${API_BASE_URL}/library/scan`)
    return response.data
  },

  async getLibraryStatus() {
    const response = await axios.get(`${API_BASE_URL}/library/status`)
    return response.data
  }
}
