import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ArchiveList from './ArchiveList.vue'

describe('ArchiveList', () => {
  it('renders a list of files', () => {
    const files = ['comic1.cbz', 'comic2.cbz']
    const wrapper = mount(ArchiveList, {
      props: { files }
    })
    expect(wrapper.findAll('.file-item')).toHaveLength(2)
    expect(wrapper.text()).toContain('comic1.cbz')
  })

  it('emits selection-changed when a file is clicked', async () => {
    const files = ['comic1.cbz']
    const wrapper = mount(ArchiveList, {
      props: { files }
    })
    await wrapper.find('.file-item').trigger('click')
    expect(wrapper.emitted('selection-changed')).toBeTruthy()
    expect(wrapper.emitted('selection-changed')![0]).toEqual([['comic1.cbz']])
  })
})
