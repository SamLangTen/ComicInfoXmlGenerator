import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from './App.vue'

describe('App', () => {
  it('renders correctly with tailwind classes', () => {
    const wrapper = mount(App)
    expect(wrapper.classes()).toContain('min-h-screen')
  })

  it('contains a sidebar, main content area, and log console', () => {
    const wrapper = mount(App)
    expect(wrapper.find('aside').exists()).toBe(true)
    expect(wrapper.find('main').exists()).toBe(true)
    // The console section exists
    expect(wrapper.find('section h3').text().toUpperCase()).toContain('TECHNICAL CONSOLE')
  })
})
