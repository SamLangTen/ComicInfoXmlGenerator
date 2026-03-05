import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MetadataEditor from './MetadataEditor.vue'

describe('MetadataEditor', () => {
  it('renders tabs for different categories', () => {
    const comic = { Series: 'Spider-Man', Number: '1' }
    const wrapper = mount(MetadataEditor, {
      props: { modelValue: comic }
    })
    expect(wrapper.text()).toContain('General')
    expect(wrapper.text()).toContain('Credits')
    expect(wrapper.text()).toContain('Tags')
    expect(wrapper.text()).toContain('Publishing')
  })

  it('renders input fields for metadata', () => {
    const comic = { Series: 'Spider-Man', Number: '1' }
    const wrapper = mount(MetadataEditor, {
      props: { modelValue: comic }
    })
    const seriesInput = wrapper.find('input[name="Series"]')
    expect(seriesInput.exists()).toBe(true)
    expect((seriesInput.element as HTMLInputElement).value).toBe('Spider-Man')
  })
})
