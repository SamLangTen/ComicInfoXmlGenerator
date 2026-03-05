import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from './App.vue'

describe('App', () => {
  it('renders correctly with tailwind classes', () => {
    const wrapper = mount(App)
    // Expect a root element with a common tailwind class we plan to use
    expect(wrapper.classes()).toContain('min-h-screen')
  })
})
