<script setup lang="ts">
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
    <!-- Navbar -->
    <header class="h-14 flex items-center px-6 border-b bg-white dark:bg-gray-900 dark:border-gray-800 shrink-0">
      <h1 class="text-lg font-bold tracking-tight">CIXG Web</h1>
    </header>

    <div class="flex flex-1 overflow-hidden">
      <!-- Sidebar -->
      <aside class="w-72 border-r bg-white dark:bg-gray-900 dark:border-gray-800 flex flex-col shrink-0">
        <div class="p-4 border-b dark:border-gray-800">
          <h2 class="text-sm font-semibold uppercase tracking-wider text-gray-500">Archives</h2>
        </div>
        <div class="flex-1 overflow-y-auto p-2">
          <!-- File list placeholder -->
          <div class="text-sm text-gray-500 p-4 italic">No directory scanned.</div>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 flex flex-col min-w-0 bg-gray-50 dark:bg-gray-950">
        <div class="flex-1 overflow-y-auto p-6">
          <div class="max-w-4xl mx-auto">
            <!-- Editor placeholder -->
            <div class="bg-white dark:bg-gray-900 rounded-lg border dark:border-gray-800 p-8 text-center shadow-sm">
              <p class="text-gray-500">Select a comic from the sidebar to edit metadata.</p>
            </div>
          </div>
        </div>

        <!-- Log Console -->
        <section class="h-64 border-t bg-white dark:bg-gray-900 dark:border-gray-800 flex flex-col log-console shrink-0">
          <div class="px-4 py-2 border-b dark:border-gray-800 flex justify-between items-center">
            <h3 class="text-xs font-bold uppercase tracking-widest text-gray-500">Technical Log</h3>
            <button class="text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">Clear</button>
          </div>
          <div class="flex-1 overflow-y-auto p-4 font-mono text-xs bg-gray-50 dark:bg-black text-green-600 dark:text-green-400">
            <div>> System ready.</div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<style scoped>
</style>
