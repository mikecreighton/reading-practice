<style scoped>

</style>

<template>
  <div class="absolute top-0 left-0 right-0 translate-y-full bg-white h-[100vh] w-full">
    <div class="settings-wrapper pb-[104px] overflow-y-scroll absolute w-full h-full top-0">
      <div class="p-10 md:p-[60px_40px_100px_40px]">
        <h2 class="text-2xl md:text-3xl font-bold mb-6">Settings</h2>
        <!-- Add your settings content here -->
        
      </div>
    </div>
    <!-- Bottom action buttons -->
    <div
      class="action-buttons-container fixed bottom-0 left-0 right-0 px-10 py-5 bg-white drop-shadow-bar"
    >
      <div class="flex justify-between items-center max-w-[700px] mx-auto my-0">
        <FastButton type="secondary" @click="$emit('cancel')">Cancel</FastButton>
        <FastButton @click="$emit('close')">Close</FastButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import FastButton from "@/components/FastButton.vue"

defineEmits(["close", "cancel"])
</script>