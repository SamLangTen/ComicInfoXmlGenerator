<script setup lang="ts">
import { ref } from 'vue'
import { apiService } from './services/api'
import ArchiveList from './components/ArchiveList.vue'

const directory = ref('')
const archives = ref<string[]>([])
const selectedPaths = ref<string[]>([])
const logs = ref<string[]>([])

const addLog = (msg: string) => {
  logs.value.push(`> ${msg}`)
  // Autoscroll logic can be added later
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

const handleSelectionChanged = (paths: string[]) => {
  selectedPaths.value = paths
  if (paths.length === 1) {
    addLog(`Selected: ${paths[0].split(/[\\/]/).pop()}`)
  } else if (paths.length > 1) {
    addLog(`Selected ${paths.length} items.`)
  }
}
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
    <!-- Navbar -->
    <header class="h-14 flex items-center justify-between px-6 border-b bg-white dark:bg-gray-900 dark:border-gray-800 shrink-0">
      <h1 class="text-lg font-bold tracking-tight">CIXG Web</h1>
      <div class="flex items-center space-x-2">
        <input 
          v-model="directory"
          type="text" 
          placeholder="Enter directory path..." 
          class="text-sm px-3 py-1.5 border rounded dark:bg-gray-800 dark:border-gray-700 w-96 focus:outline-none focus:ring-2 focus:ring-blue-500"
          @keyup.enter="handleScan"
        />
        <button 
          @click="handleScan"
          class="text-sm bg-blue-600 hover:bg-blue-700 text-white px-4 py-1.5 rounded font-medium transition-colors"
        >
          Scan
        </button>
      </div>
    </header>

    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
      <aside class="w-72 border-r bg-white dark:bg-gray-900 dark:border-gray-800 flex flex-col shrink-0">
        <div class="p-4 border-b dark:border-gray-800">
          <h2 class="text-sm font-semibold uppercase tracking-wider text-gray-500">Archives ({{ archives.length }})</h2>
        </div>
        <div class="flex-1 overflow-y-auto p-2">
          <ArchiveList 
            v-if="archives.length > 0"
            :files="archives" 
            @selection-changed="handleSelectionChanged"
          />
          <div v-else class="text-sm text-gray-500 p-4 italic text-center">
            No directory scanned.
          </div>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 flex flex-col min-w-0 bg-gray-50 dark:bg-gray-950">
        <div class="flex-1 overflow-y-auto p-6">
          <div class="max-w-4xl mx-auto">
            <!-- Editor placeholder -->
            <div v-if="selectedPaths.length === 0" class="bg-white dark:bg-gray-900 rounded-lg border dark:border-gray-800 p-8 text-center shadow-sm">
              <p class="text-gray-500">Select a comic from the sidebar to edit metadata.</p>
            </div>
            <div v-else class="bg-white dark:bg-gray-900 rounded-lg border dark:border-gray-800 p-8 shadow-sm">
               <h2 class="text-xl font-bold mb-4">Metadata Editor</h2>
               <p class="text-sm text-gray-500 mb-6">Editing: {{ selectedPaths.length }} item(s)</p>
               <!-- Editor form will go here -->
               <div class="p-12 border-2 border-dashed border-gray-200 dark:border-gray-800 rounded-lg text-center">
                 <p class="text-gray-400">Editor Form Implementation Coming Soon</p>
               </div>
            </div>
          </div>
        </div>

        <!-- Log Console -->
        <section class="h-64 border-t bg-white dark:bg-gray-900 dark:border-gray-800 flex flex-col log-console shrink-0">
          <div class="px-4 py-2 border-b dark:border-gray-800 flex justify-between items-center">
            <h3 class="text-xs font-bold uppercase tracking-widest text-gray-500">Technical Log</h3>
            <button @click="logs = []" class="text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">Clear</button>
          </div>
          <div class="flex-1 overflow-y-auto p-4 font-mono text-xs bg-gray-50 dark:bg-black text-green-600 dark:text-green-400">
            <div v-for="(log, i) in logs" :key="i">{{ log }}</div>
            <div v-if="logs.length === 0" class="text-gray-600 dark:text-gray-800 italic">No logs yet.</div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<style scoped>
</style>
