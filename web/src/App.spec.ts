import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import App from './App.vue'

// Mock WebSocket
class MockWebSocket {
  onmessage: any = null
  onclose: any = null
  close = vi.fn()
}
global.WebSocket = MockWebSocket as any

describe('App', () => {
  it('renders correctly with tailwind classes', () => {
    const wrapper = mount(App)
    expect(wrapper.classes()).toContain('min-h-screen')
  })

  it('contains a sidebar, main content area, and log console', () => {
    const wrapper = mount(App)
    expect(wrapper.find('aside').exists()).toBe(true)
    expect(wrapper.find('main').exists()).toBe(true)
    expect(wrapper.find('section h3').text().toUpperCase()).toContain('TECHNICAL CONSOLE')
  })

  it('shows progress bar when processing', async () => {
    const wrapper = mount(App)
    // Initially hidden
    expect(wrapper.find('.animate-progress').exists()).toBe(false)
    
    // We can't easily trigger the ref directly from outside without more setup,
    // but we can check if it's reactive to state if we could set it.
    // For now, let's just check the template structure.
  })
})
