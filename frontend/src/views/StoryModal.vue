<style scoped lang="postcss">
.story-modal {
  @apply fixed inset-0 w-full bg-story h-[100dvh];
  height: -webkit-fill-available;
}

.story-content {
  @apply h-full overflow-y-auto pb-[104px];
  -webkit-overflow-scrolling: touch;
}

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

.generating-text-enter-active,
.generating-text-leave-active {
  transition: all 0.5s ease;
}

.generating-text-enter-from,
.generating-text-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>

<template>
  <div class="story-modal">
    <transition name="fade">
      <div
        v-if="isLoading"
        class="loader-wrapper flex flex-col justify-center items-center h-full w-full overflow-y-hidden"
      >
        <div class="loader flex flex-col items-center">
          <div class="flex justify-center items-center gap-[20px] mb-[80px]">
            <div
              class="ball w-[20px] h-[20px] bg-text rounded-full relative"
              v-for="n in 3"
              :key="n"
              :style="{ animationDelay: `${(n - 1) * 0.2}s` }"
            ></div>
          </div>
          <div class="h-[40px] relative w-full flex justify-center">
            <!-- Reserve space for text -->
            <transition name="generating-text" mode="out-in">
              <div v-if="showGeneratingText" :key="currentTextIndex" class="text-text text-2xl">
                {{ generatingTexts[currentTextIndex] }}
              </div>
            </transition>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="!isLoading" class="story-content">
        <div class="p-10 md:p-[60px_40px_100px_40px] max-w-[700px] mx-auto">
          <img
            class="w-full mb-6 md:mb-10 border border-story-illustration-border rounded-lg"
            v-if="isOpenAIAvailable && illustration"
            :src="illustration"
            alt="Illustration"
          />
          <p
            class="text-xl leading-relaxed sm:text-2xl sm:leading-relaxed md:leading-relaxed text-text"
          >
            {{ story }}
          </p>
        </div>
      </div>
    </transition>

    <!-- Bottom action buttons -->
    <div
      class="action-buttons-container fixed bottom-0 left-0 right-0 bg-bottom-bar drop-shadow-bar"
    >
      <div class="flex justify-between items-center max-w-[700px] px-10 py-5 mx-auto my-0">
        <FastButton name="Close" type="secondary" @click="emit('closeRequest')">Close</FastButton>
        <FastButton
          :disabled="isLoading"
          :isDisabled="isLoading"
          customClass=""
          @click="$emit('regenerate')"
          name="Regenerate"
        >
          Tell me another story
        </FastButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject, ref, onMounted, onUnmounted, watch } from "vue"
import FastButton from "@/components/FastButton.vue"

const isOpenAIAvailable = inject("isOpenAIAvailable")

const generatingTexts = [
  "Brainstorming plot twists...",
  "Crafting unique characters...",
  "Weaving magical elements...",
  "Designing the story world...",
  "Sprinkling in humor...",
  "Adding suspenseful moments...",
  "Polishing dialogue...",
  "Perfecting the ending...",
  "Enhancing descriptions...",
  "Fine-tuning the narrative...",
  "Conjuring vivid imagery...",
  "Infusing story with emotions...",
  "Developing character arcs...",
  "Adding whimsical details...",
  "Creating memorable scenes...",
  "Sprinkling in vocabulary words...",
  "Polishing the story's rhythm...",
]

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

const currentTextIndex = ref(0)
const showGeneratingText = ref(false)
const randomizedGeneratingTexts = ref([])
let textInterval

const clearTextInterval = () => {
  if (textInterval) {
    clearInterval(textInterval)
    textInterval = null
  }
}

onMounted(() => {
  if (props.isLoading) {
    randomizedGeneratingTexts.value = generatingTexts.sort(() => 0.5 - Math.random())
    waitToStartGeneratingText()
    setTimeout(startGeneratingText, 4500)
  }
})

const waitToStartGeneratingText = () => {
  setTimeout(() => {
    showGeneratingText.value = true
  }, 1500)
}

const startGeneratingText = () => {
  showGeneratingText.value = true
  textInterval = setInterval(() => {
    currentTextIndex.value = (currentTextIndex.value + 1) % randomizedGeneratingTexts.value.length
  }, 3000)
}

onUnmounted(() => {
  clearTextInterval()
})

watch(
  () => props.isLoading,
  (newValue) => {
    if (!newValue) {
      clearTextInterval()
      showGeneratingText.value = false
    } else {
      randomizedGeneratingTexts.value = generatingTexts.sort(() => 0.5 - Math.random())
      waitToStartGeneratingText()
      setTimeout(startGeneratingText, 4500)
    }
  },
)
</script>
