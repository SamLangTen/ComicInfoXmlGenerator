<script setup lang="ts">
import { ref, watch } from 'vue'
import { apiService } from './services/api'
import ArchiveList from './components/ArchiveList.vue'
import MetadataEditor from './components/MetadataEditor.vue'

const directory = ref('')
const archives = ref<string[]>([])
const selectedPaths = ref<string[]>([])
const currentComic = ref<any>(null)
const logs = ref<string[]>([])

const addLog = (msg: string) => {
  logs.value.push(`> ${msg}`)
}

const handleScan = async () => {
  if (!directory.value) return
  try {
    addLog(`Scanning directory: ${directory.value}`)
    const response = await apiService.scanDirectory(directory.value)
    archives.value = response.files
    addLog(`Found ${archives.value.length} archives.`)
  } catch (err: any) {
    addLog(`Error scanning directory: ${err.message}`)
  }
}

const handleSelectionChanged = async (paths: string[]) => {
  selectedPaths.value = paths
  if (paths.length === 1) {
    addLog(`Loading metadata: ${paths[0].split(/[\\/]/).pop()}`)
    try {
      currentComic.value = await apiService.getMetadata(paths[0])
    } catch (err: any) {
      addLog(`Error loading metadata: ${err.message}`)
    }
  } else {
    currentComic.value = null
    if (paths.length > 1) addLog(`Selected ${paths.length} items.`)
  }
}

// Auto-save metadata when it changes
watch(currentComic, async (newVal) => {
  if (newVal && selectedPaths.value.length === 1) {
    try {
      await apiService.updateMetadata(newVal)
    } catch (err: any) {
      console.error('Failed to auto-save metadata', err)
    }
  }
}, { deep: true })

const handleInject = async () => {
  if (selectedPaths.value.length === 0) return
  try {
    addLog(`Injecting metadata into ${selectedPaths.value.length} file(s)...`)
    const response = await apiService.triggerInject(selectedPaths.value)
    addLog(`Injection complete. Status: ${response.status}`)
    // Show individual results
    Object.entries(response.results).forEach(([path, status]) => {
      const name = path.split(/[\\/]/).pop()
      addLog(`- ${name}: ${status}`)
    })
  } catch (err: any) {
    addLog(`Error injecting metadata: ${err.message}`)
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 font-sans">
    <!-- Navbar -->
    <header class="h-14 flex items-center justify-between px-6 border-b bg-white dark:bg-gray-900 dark:border-gray-800 shrink-0 shadow-sm z-10">
      <div class="flex items-center space-x-4">
        <h1 class="text-lg font-bold tracking-tight text-blue-600 dark:text-blue-400">CIXG Web</h1>
      </div>
      <div class="flex items-center space-x-3">
        <div class="relative">
          <input 
            v-model="directory"
            type="text" 
            placeholder="Absolute directory path..." 
            class="text-sm px-4 py-1.5 border rounded-full dark:bg-gray-800 dark:border-gray-700 w-96 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
            @keyup.enter="handleScan"
          />
        </div>
        <button 
          @click="handleScan"
          class="text-sm bg-blue-600 hover:bg-blue-700 text-white px-5 py-1.5 rounded-full font-semibold shadow-md active:transform active:scale-95 transition-all"
        >
          Scan
        </button>
      </div>
    </header>

    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
      <aside class="w-80 border-r bg-white dark:bg-gray-900 dark:border-gray-800 flex flex-col shrink-0 shadow-sm">
        <div class="p-4 border-b dark:border-gray-800 flex justify-between items-center bg-gray-50 dark:bg-gray-900/50">
          <h2 class="text-xs font-bold uppercase tracking-widest text-gray-500">Archive Library</h2>
          <span v-if="archives.length" class="bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-[10px] px-2 py-0.5 rounded-full font-bold">
            {{ archives.length }}
          </span>
        </div>
        <div class="flex-1 overflow-y-auto p-3 custom-scrollbar">
          <ArchiveList 
            v-if="archives.length > 0"
            :files="archives" 
            @selection-changed="handleSelectionChanged"
          />
          <div v-else class="flex flex-col items-center justify-center h-full text-center space-y-2 opacity-50 p-8">
            <svg class="w-12 h-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
            </svg>
            <p class="text-sm italic">No archives found. Enter a path above to scan.</p>
          </div>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 flex flex-col min-w-0">
        <div class="flex-1 overflow-hidden relative">
          <div class="absolute inset-0 overflow-y-auto p-8 custom-scrollbar">
            <div class="max-w-4xl mx-auto h-full">
              <!-- No selection state -->
              <div v-if="selectedPaths.length === 0" class="h-full flex flex-col items-center justify-center text-center space-y-4 opacity-40">
                <svg class="w-20 h-20 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <div>
                  <h3 class="text-lg font-medium">No Comic Selected</h3>
                  <p class="text-sm max-w-xs">Select an archive from the sidebar to view or edit its metadata.</p>
                </div>
              </div>

              <!-- Multi-selection overview -->
              <div v-else-if="selectedPaths.length > 1" class="bg-white dark:bg-gray-900 rounded-xl border dark:border-gray-800 p-10 shadow-xl text-center space-y-6 animate-in fade-in zoom-in duration-300">
                 <div class="w-20 h-20 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center mx-auto">
                   <svg class="w-10 h-10 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                     <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                   </svg>
                 </div>
                 <div>
                   <h2 class="text-2xl font-bold mb-2">Batch Processing</h2>
                   <p class="text-gray-500">You have selected <span class="font-bold text-blue-600 dark:text-blue-400">{{ selectedPaths.length }}</span> comic archives.</p>
                 </div>
                 <div class="flex justify-center space-x-4">
                   <button class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-2.5 rounded-lg font-bold shadow-lg shadow-blue-500/20 transition-all">
                     Apply Scraper to All
                   </button>
                   <button 
                    @click="handleInject"
                    class="bg-green-600 hover:bg-green-700 text-white px-8 py-2.5 rounded-lg font-bold shadow-lg shadow-green-500/20 transition-all"
                   >
                     Inject All ({{ selectedPaths.length }})
                   </button>
                 </div>
              </div>

              <!-- Single selection editor -->
              <div v-else-if="currentComic" class="bg-white dark:bg-gray-900 rounded-xl border dark:border-gray-800 shadow-xl flex flex-col h-full overflow-hidden animate-in slide-in-from-bottom-4 duration-300">
                 <div class="px-8 py-6 border-b dark:border-gray-800 bg-gray-50/50 dark:bg-gray-900/50 flex justify-between items-center">
                   <div>
                     <h2 class="text-xl font-extrabold truncate max-w-md">{{ currentComic.Title || 'Untitled' }}</h2>
                     <p class="text-xs text-gray-400 font-mono mt-1 truncate max-w-md">{{ selectedPaths[0] }}</p>
                   </div>
                   <div class="flex items-center space-x-2">
                     <button class="text-xs bg-gray-200 dark:bg-gray-800 hover:bg-gray-300 dark:hover:bg-gray-700 px-3 py-1.5 rounded-md font-bold transition-all">
                       Scrape
                     </button>
                     <button 
                      @click="handleInject"
                      class="text-xs bg-green-600 hover:bg-green-700 text-white px-4 py-1.5 rounded-md font-bold shadow-md shadow-green-500/20 transition-all"
                     >
                       Inject
                     </button>
                   </div>
                 </div>
                 <div class="flex-1 p-8 overflow-y-auto">
                   <MetadataEditor v-model="currentComic" />
                 </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Log Console -->
        <section class="h-64 border-t bg-white dark:bg-gray-900 dark:border-gray-800 flex flex-col shrink-0 overflow-hidden shadow-2xl relative z-10">
          <div class="px-6 py-3 border-b dark:border-gray-800 flex justify-between items-center bg-gray-50/80 dark:bg-black/40 backdrop-blur-md">
            <h3 class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">Technical Console</h3>
            <button @click="logs = []" class="text-[10px] uppercase tracking-widest text-gray-400 hover:text-red-500 font-bold transition-colors">Clear Output</button>
          </div>
          <div class="flex-1 overflow-y-auto p-6 font-mono text-[11px] leading-relaxed bg-black text-gray-300 custom-scrollbar">
            <div v-for="(log, i) in logs" :key="i" class="mb-1">
              <span class="text-blue-500/50 mr-2">{{ new Date().toLocaleTimeString() }}</span>
              <span :class="{ 'text-green-400': log.includes('Success'), 'text-red-400': log.includes('Error'), 'text-yellow-400': log.includes('Warning') }">{{ log }}</span>
            </div>
            <div v-if="logs.length === 0" class="text-gray-700 italic flex items-center h-full justify-center">Console ready for operations...</div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<style>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.2);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.4);
}
</style>
