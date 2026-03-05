import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'
import { apiService } from './api'

vi.mock('axios')
const mockedAxios = axios as vi.Mocked<typeof axios>

describe('apiService', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })

  it('fetches health status', async () => {
    const mockData = { status: 'ok' }
    mockedAxios.get.mockResolvedValueOnce({ data: mockData })

    const result = await apiService.getHealth()
    expect(result).toEqual(mockData)
    expect(mockedAxios.get).toHaveBeenCalledWith('/api/health')
  })

  it('fetches configuration', async () => {
    const mockConfig = { llm_model: 'gpt-test' }
    mockedAxios.get.mockResolvedValueOnce({ data: mockConfig })

    const result = await apiService.getConfig()
    expect(result).toEqual(mockConfig)
    expect(mockedAxios.get).toHaveBeenCalledWith('/api/config')
  })
})
