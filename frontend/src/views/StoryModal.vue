<template>
  <div class="fixed inset-0 bg-white overflow-y-scroll transform translate-y-full">
    <div class="p-10 md:p-[60px_40px_100px_40px] w-full">
      <img
        class="w-full mb-4"
        v-if="isOpenAIAvailable && illustration"
        :src="illustration"
        alt="Illustration"
      />
      <p class="text-xl md:text-3xl lg:text-4xl leading-relaxed">{{ story }}</p>
      <FastButton
        customClass="absolute top-5 right-5 w-15 h-15 text-3xl text-white bg-gray-900 hover:bg-gray-700 rounded-xl"
        @click="emit('closeRequest')"
      >
        &#x2715;
      </FastButton>
      <FastButton
        customClass="mt-4 bg-blue-500 text-white py-2 px-4 rounded-lg"
        @click="$emit('regenerate')"
      >
        Regenerate
      </FastButton>
    </div>
  </div>
</template>

<script setup>
import { inject } from "vue"
import FastButton from "@/components/FastButton.vue"

const isOpenAIAvailable = inject("isOpenAIAvailable")

const props = defineProps({
  story: {
    type: String,
    required: true,
  },
  illustration: {
    type: String,
    required: false,
  },
})

const emit = defineEmits(["regenerate", "closeRequest"])
</script>

<style scoped>
/* Remove all styles here, as they're now handled by Tailwind classes */
</style>
