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

const isInvalidNumber = (key: string) => {
  const val = localComic.value[key]
  if (val === undefined || val === null || val === '') return false
  if (val === -1) return false
  const strVal = String(val)
  return !/^-?\d+$/.test(strVal)
}

const tabs = ['General', 'Credits', 'Tags', 'Publishing']

const fieldGroups = {
  General: [
    { label: 'Title', key: 'Title', type: 'text', span: 2 },
    { label: 'Series', key: 'Series', type: 'text', span: 2 },
    { label: 'Number', key: 'Number', type: 'text', span: 1 },
    { label: 'Volume', key: 'Volume', type: 'number', span: 1 },
    { label: 'Year', key: 'Year', type: 'number', span: 1 },
    { label: 'Month', key: 'Month', type: 'number', span: 1 },
    { label: 'Day', key: 'Day', type: 'number', span: 1 },
    { label: 'Summary', key: 'Summary', type: 'textarea', span: 2 }
  ],
  Credits: [
    { label: 'Writer', key: 'Writer', type: 'text', span: 1 },
    { label: 'Penciller', key: 'Penciller', type: 'text', span: 1 },
    { label: 'Inker', key: 'Inker', type: 'text', span: 1 },
    { label: 'Colorist', key: 'Colorist', type: 'text', span: 1 },
    { label: 'Letterer', key: 'Letterer', type: 'text', span: 1 },
    { label: 'Cover Artist', key: 'CoverArtist', type: 'text', span: 1 },
    { label: 'Editor', key: 'Editor', type: 'text', span: 1 }
  ],
  Tags: [
    { label: 'Genre', key: 'Genre', type: 'text', span: 1 },
    { label: 'Characters', key: 'Characters', type: 'text', span: 1 },
    { label: 'Teams', key: 'Teams', type: 'text', span: 1 },
    { label: 'Locations', key: 'Locations', type: 'text', span: 1 },
    { label: 'Story Arc', key: 'StoryArc', type: 'text', span: 1 },
    { label: 'Series Group', key: 'SeriesGroup', type: 'text', span: 1 }
  ],
  Publishing: [
    { label: 'Publisher', key: 'Publisher', type: 'text', span: 1 },
    { label: 'Imprint', key: 'Imprint', type: 'text', span: 1 },
    { label: 'Age Rating', key: 'AgeRating', type: 'text', span: 1 },
    { label: 'Web URL', key: 'Web', type: 'text', span: 1 },
    { label: 'Black & White', key: 'BlackAndWhite', type: 'enum', span: 1 },
    { label: 'Manga', key: 'Manga', type: 'enum', span: 1 }
  ]
}
</script>

<template>
  <div class="flex flex-col h-full overflow-hidden">
    <!-- Tab Headers -->
    <div class="flex space-x-1 p-1 bg-gray-100 dark:bg-gray-800 rounded-lg mb-6 shrink-0">
      <button
        v-for="tab in tabs"
        :key="tab"
        class="flex-1 py-2 text-xs font-bold uppercase tracking-wider transition-all duration-200 rounded-md"
        :class="[
          activeTab === tab
            ? 'bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 shadow-sm'
            : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
        ]"
        @click="activeTab = tab"
      >
        {{ tab }}
      </button>
    </div>

    <!-- Tab Content -->
    <div class="flex-1 overflow-y-auto pr-4 custom-scrollbar">
      <div v-if="fieldGroups[activeTab as keyof typeof fieldGroups]">
        <div class="grid grid-cols-2 gap-x-6 gap-y-5 pb-4">
          <div 
            v-for="field in (fieldGroups as any)[activeTab]" 
            :key="field.key" 
            class="flex flex-col space-y-1.5"
            :class="[field.span === 2 ? 'col-span-2' : 'col-span-2 md:col-span-1']"
          >
            <div class="flex justify-between items-center">
              <label :for="field.key" class="text-[10px] font-black text-gray-400 uppercase tracking-widest">
                {{ field.label }}
              </label>
              <span v-if="field.type === 'number' && isInvalidNumber(field.key)" class="text-[9px] font-bold text-red-500 uppercase">Invalid Number</span>
            </div>
            
            <textarea
              v-if="field.type === 'textarea'"
              :id="field.key"
              :name="field.key"
              rows="6"
              class="block w-full px-4 py-3 text-sm border rounded-xl dark:bg-gray-800/50 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all resize-none leading-relaxed"
              placeholder="Enter summary..."
              :value="localComic[field.key]"
              @input="updateField(field.key, ($event.target as HTMLTextAreaElement).value)"
            ></textarea>

            <div v-else-if="field.type === 'enum'" class="relative">
              <select
                :id="field.key"
                :name="field.key"
                class="appearance-none block w-full px-4 py-2.5 text-sm border rounded-xl dark:bg-gray-800/50 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all pr-10"
                :value="localComic[field.key]"
                @change="updateField(field.key, ($event.target as HTMLSelectElement).value)"
              >
                <option value="Yes">Yes</option>
                <option value="No">No</option>
                <option value="Unknown">Unknown</option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center px-3 pointer-events-none text-gray-400">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M19 9l-7 7-7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              </div>
            </div>

            <input
              v-else
              :id="field.key"
              :name="field.key"
              :type="field.type === 'number' ? 'text' : field.type"
              class="block w-full px-4 py-2.5 text-sm border rounded-xl dark:bg-gray-800/50 dark:border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
              :class="{ 'border-red-500 ring-2 ring-red-500/20 bg-red-50 dark:bg-red-900/10': field.type === 'number' && isInvalidNumber(field.key) }"
              :placeholder="'Enter ' + field.label.toLowerCase() + '...'"
              :value="localComic[field.key] === -1 ? '' : localComic[field.key]"
              @input="updateField(field.key, ($event.target as HTMLInputElement).value)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
