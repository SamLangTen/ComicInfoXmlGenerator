<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  modelValue: any
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: any): void
}>()

const activeTab = ref('General')
const localComic = ref({ ...props.modelValue })

watch(() => props.modelValue, (newVal) => {
  localComic.value = { ...newVal }
}, { deep: true })

const updateField = (field: string, value: any) => {
  localComic.value[field] = value
  emit('update:modelValue', { ...localComic.value })
}

const tabs = ['General', 'Credits', 'Tags', 'Publishing']

const fieldGroups = {
  General: [
    { label: 'Title', key: 'Title', type: 'text' },
    { label: 'Series', key: 'Series', type: 'text' },
    { label: 'Number', key: 'Number', type: 'text' },
    { label: 'Volume', key: 'Volume', type: 'number' },
    { label: 'Year', key: 'Year', type: 'number' },
    { label: 'Month', key: 'Month', type: 'number' },
    { label: 'Day', key: 'Day', type: 'number' },
    { label: 'Summary', key: 'Summary', type: 'textarea' }
  ],
  Credits: [
    { label: 'Writer', key: 'Writer', type: 'text' },
    { label: 'Penciller', key: 'Penciller', type: 'text' },
    { label: 'Inker', key: 'Inker', type: 'text' },
    { label: 'Colorist', key: 'Colorist', type: 'text' },
    { label: 'Letterer', key: 'Letterer', type: 'text' },
    { label: 'Cover Artist', key: 'CoverArtist', type: 'text' },
    { label: 'Editor', key: 'Editor', type: 'text' }
  ],
  Tags: [
    { label: 'Genre', key: 'Genre', type: 'text' },
    { label: 'Characters', key: 'Characters', type: 'text' },
    { label: 'Teams', key: 'Teams', type: 'text' },
    { label: 'Locations', key: 'Locations', type: 'text' },
    { label: 'Story Arc', key: 'StoryArc', type: 'text' },
    { label: 'Series Group', key: 'SeriesGroup', type: 'text' }
  ],
  Publishing: [
    { label: 'Publisher', key: 'Publisher', type: 'text' },
    { label: 'Imprint', key: 'Imprint', type: 'text' },
    { label: 'Age Rating', key: 'AgeRating', type: 'text' },
    { label: 'Web URL', key: 'Web', type: 'text' },
    { label: 'Black & White', key: 'BlackAndWhite', type: 'enum' },
    { label: 'Manga', key: 'Manga', type: 'enum' }
  ]
}
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- Tab Headers -->
    <div class="flex border-b dark:border-gray-800 mb-6">
      <button
        v-for="tab in tabs"
        :key="tab"
        class="px-6 py-3 text-sm font-medium transition-colors duration-150 border-b-2 -mb-px"
        :class="[
          activeTab === tab
            ? 'border-blue-600 text-blue-600'
            : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
        ]"
        @click="activeTab = tab"
      >
        {{ tab }}
      </button>
    </div>

    <!-- Tab Content -->
    <div class="flex-1 overflow-y-auto pr-2">
      <div v-if="activeTab === 'General' || activeTab === 'Credits' || activeTab === 'Tags' || activeTab === 'Publishing'">
        <div class="grid grid-cols-1 gap-y-4">
          <div v-for="field in (fieldGroups as any)[activeTab]" :key="field.key" class="flex flex-col space-y-1">
            <label :for="field.key" class="text-xs font-semibold text-gray-500 uppercase tracking-wider">
              {{ field.label }}
            </label>
            
            <textarea
              v-if="field.type === 'textarea'"
              :id="field.key"
              :name="field.key"
              rows="4"
              class="block w-full px-3 py-2 text-sm border rounded-md dark:bg-gray-800 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              :value="localComic[field.key]"
              @input="updateField(field.key, ($event.target as HTMLTextAreaElement).value)"
            ></textarea>

            <select
              v-else-if="field.type === 'enum'"
              :id="field.key"
              :name="field.key"
              class="block w-full px-3 py-2 text-sm border rounded-md dark:bg-gray-800 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              :value="localComic[field.key]"
              @change="updateField(field.key, ($event.target as HTMLSelectElement).value)"
            >
              <option value="Yes">Yes</option>
              <option value="No">No</option>
              <option value="Unknown">Unknown</option>
            </select>

            <input
              v-else
              :id="field.key"
              :name="field.key"
              :type="field.type"
              class="block w-full px-3 py-2 text-sm border rounded-md dark:bg-gray-800 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              :value="localComic[field.key] === -1 ? '' : localComic[field.key]"
              @input="updateField(field.key, field.type === 'number' ? parseInt(($event.target as HTMLInputElement).value) || -1 : ($event.target as HTMLInputElement).value)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
