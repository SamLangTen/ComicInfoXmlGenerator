<script setup lang="ts">
import { ref } from 'vue'
import SeriesView from './SeriesView.vue'
import ArchiveList from './ArchiveList.vue'

const props = defineProps<{
  seriesList: any[],
  activeTasks: Record<string, any>,
  libraryStatus: any
}>()

const emit = defineEmits<{
  (e: 'select-archive', path: string): void,
  (e: 'select-archives', paths: string[]): void
}>()

const selectedSeries = ref<any>(null)
const viewMode = ref<'grid' | 'list'>('grid')

const handleSelectSeries = (series: any) => {
  selectedSeries.value = series
}

const handleArchiveSelection = (paths: string[]) => {
  if (paths.length === 1 && paths[0]) {
    emit('select-archive', paths[0])
  } else if (paths.length > 1) {
    emit('select-archives', paths)
  }
}

const getSeriesName = (series: any) => series.name || 'Unknown Series'
const getCoverUrl = (path: string) => {
  if (!path) return ''
  return `/api/cover?path=${encodeURIComponent(path)}`
}
</script>

<template>
  <div class="h-full flex flex-col">
    <!-- Breadcrumbs / Header -->
    <header class="mb-8 shrink-0">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button 
            v-if="selectedSeries" 
            @click="selectedSeries = null"
            class="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-xl transition-colors text-gray-500"
          >
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div>
            <h2 class="text-4xl font-black tracking-tighter">
              {{ selectedSeries ? getSeriesName(selectedSeries) : 'Your Library' }}
            </h2>
            <p class="text-gray-500 font-medium mt-1">
              <span v-if="selectedSeries">{{ selectedSeries.count }} Volumes</span>
              <span v-else>{{ seriesList.length }} Series found in {{ libraryStatus.manga_root }}</span>
            </p>
          </div>
        </div>

        <!-- View Controls (only for series list) -->
        <div v-if="!selectedSeries" class="flex items-center bg-gray-100 dark:bg-gray-800 p-1 rounded-xl">
          <button 
            @click="viewMode = 'grid'"
            class="p-2 rounded-lg transition-all"
            :class="viewMode === 'grid' ? 'bg-white dark:bg-gray-700 shadow-sm text-blue-600' : 'text-gray-400 hover:text-gray-600'"
          >
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
          </button>
          <button 
            @click="viewMode = 'list'"
            class="p-2 rounded-lg transition-all"
            :class="viewMode === 'list' ? 'bg-white dark:bg-gray-700 shadow-sm text-blue-600' : 'text-gray-400 hover:text-gray-600'"
          >
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="flex-1 overflow-hidden">
      <!-- Series Master View -->
      <div v-if="!selectedSeries" class="h-full overflow-y-auto pr-4 custom-scrollbar">
        <!-- Grid Mode -->
        <SeriesView 
          v-if="viewMode === 'grid'" 
          :seriesList="seriesList" 
          :activeTasks="activeTasks" 
          @select-series="handleSelectSeries" 
        />
        
        <!-- List Mode -->
        <div v-else class="space-y-2">
          <div 
            v-for="series in seriesList" 
            :key="series.name"
            @click="handleSelectSeries(series)"
            class="group flex items-center p-4 bg-white dark:bg-gray-900 rounded-2xl border dark:border-gray-800 shadow-sm hover:shadow-md hover:border-blue-500/50 transition-all cursor-pointer"
          >
            <div class="w-12 h-16 bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden mr-4 shrink-0">
              <img 
                v-if="series.cover_path" 
                :src="getCoverUrl(series.cover_path)" 
                class="w-full h-full object-cover" 
                loading="lazy"
              />
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="font-bold truncate group-hover:text-blue-600 transition-colors">{{ getSeriesName(series) }}</h3>
              <p class="text-xs text-gray-500">{{ series.count }} Volumes</p>
            </div>
            <div class="ml-4">
              <svg class="w-5 h-5 text-gray-300 group-hover:text-blue-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="seriesList.length === 0 && !libraryStatus.is_scanning" class="h-full flex flex-col items-center justify-center text-center opacity-30">
          <svg class="w-20 h-20 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          <p class="text-xl font-bold">No series found yet.</p>
          <p class="text-sm">Try rescanning your library.</p>
        </div>
      </div>

      <!-- Series Detail View -->
      <div v-else class="h-full flex overflow-hidden animate-in slide-in-from-right-4 duration-300">
        <!-- Series Sidebar (Optional, but user said "keep library display") -->
        <!-- We can keep a mini list of series on the left -->
        <aside class="w-72 border-r dark:border-gray-800 flex flex-col overflow-hidden mr-8 shrink-0">
          <div class="flex-1 overflow-y-auto custom-scrollbar pr-2 space-y-1">
            <div 
              v-for="series in seriesList" 
              :key="series.name"
              @click="handleSelectSeries(series)"
              class="px-4 py-3 rounded-xl cursor-pointer transition-all text-sm font-bold truncate"
              :class="selectedSeries.name === series.name ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20' : 'text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800'"
            >
              {{ getSeriesName(series) }}
            </div>
          </div>
        </aside>

        <!-- Archive List for selected series -->
        <div class="flex-1 overflow-y-auto custom-scrollbar">
          <div class="bg-white dark:bg-gray-900 rounded-3xl border dark:border-gray-800 shadow-sm p-6">
            <ArchiveList 
              :files="selectedSeries.paths" 
              :activeTasks="activeTasks" 
              @selection-changed="handleArchiveSelection" 
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(156, 163, 175, 0.2); border-radius: 10px; }
</style>
