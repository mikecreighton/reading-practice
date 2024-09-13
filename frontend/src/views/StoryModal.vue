<style scoped>
.ball {
  animation: moveUpDown 1.5s ease-in-out infinite;
}

@keyframes moveUpDown {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-60px);
  }
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-active {
  transition-delay: 0.5s;
}
</style>

<template>
  <div class="absolute top-0 left-0 right-0 translate-y-full bg-background h-[100vh] w-full">
    <transition name="fade">
      <div
        v-if="isLoading"
        class="loader-wrapper flex justify-center absolute items-center h-full w-full top-0"
      >
        <div class="loader flex justify-center items-center h-full gap-[20px]">
          <div
            class="ball w-[20px] h-[20px] bg-primary rounded-full relative"
            v-for="n in 3"
            :key="n"
            :style="{ animationDelay: `${(n - 1) * 0.2}s` }"
          ></div>
        </div>
      </div>
    </transition>
    <transition name="fade">
      <div
        v-if="!isLoading"
        class="story-wrapper pb-[104px] overflow-y-scroll absolute w-full h-full top-0"
      >
        <div class="p-10 md:p-[60px_40px_100px_40px]">
          <img
            class="w-full mb-6 border border-input-border rounded-lg"
            v-if="isOpenAIAvailable && illustration"
            :src="illustration"
            alt="Illustration"
          />
          <p class="text-xl md:text-3xl md:leading-relaxed lg:text-4xl lg:leading-relaxed leading-relaxed text-text">{{ story }}</p>
        </div>
      </div>
    </transition>
    <!-- Bottom action buttons -->
    <div
      class="action-buttons-container fixed bottom-0 left-0 right-0 px-10 py-5 bg-white drop-shadow-bar"
    >
      <div class="flex justify-between items-center max-w-[700px] mx-auto my-0">
        <FastButton type="secondary" @click="emit('closeRequest')">Close</FastButton>
        <FastButton
          :disabled="isLoading"
          :isDisabled="isLoading"
          customClass=""
          @click="$emit('regenerate')"
        >
          Tell me another story
        </FastButton>
      </div>
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
  isLoading: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits(["regenerate", "closeRequest"])
</script>
