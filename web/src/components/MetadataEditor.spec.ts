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

  it('shows visual validation cues for invalid numbers', async () => {
    const comic = { Volume: 1 }
    const wrapper = mount(MetadataEditor, {
      props: { modelValue: comic }
    })
    const volumeInput = wrapper.find('input[name="Volume"]')
    
    // Set an invalid numeric value
    await volumeInput.setValue('abc')
    expect(volumeInput.classes()).toContain('border-red-500')
    
    // Set a valid value
    await volumeInput.setValue('5')
    expect(volumeInput.classes()).not.toContain('border-red-500')
  })
})
