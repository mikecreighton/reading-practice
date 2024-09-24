<style scoped lang="postcss">
.welcome-screen {
  touch-action: none;
}

.force-3d {
  /* Hack to force 3D context to prevent text from moving at 1px increments */
  transform: rotateX(0.001deg);
}
</style>

<template>
  <div ref="welcomeScreen" class="welcome-screen fixed top-0 left-0 w-full h-full bg-background text-text">
    <div
      ref="content"
      class="welcome-screen-content flex flex-col items-center justify-center px-10 max-w-[700px] mx-auto h-full"
    >
      <h1 ref="title" class="force-3d text-4xl md:text-6xl font-bold mb-8 md:mb-16 tracking-tight">Reading Practice</h1>
      <p ref="intro" class="force-3d text-lg md:text-2xl mb-8 md:px-8 text-center">
        Create personalized stories for young readers. This prototype generates unique tales and illustrations to make
        reading more engaging.
      </p>
      <div ref="cta" class="force-3d flex justify-center mb-16">
        <FastButton type="primary" @click="handleCTAClick">Get started</FastButton>
      </div>
      <div ref="links" class="force-3d flex space-x-6">
        <a
          href="https://github.com/mikecreighton/reading-practice"
          target="_blank"
          class="leading-[40px] text-link hover:underline"
        >
          <i class="bi bi-github"></i>
          GitHub
        </a>
        <a href="https://x.com/mikecreighton" target="_blank" class="leading-[40px] text-link hover:underline">
          <i class="bi bi-twitter-x"></i>
          @mikecreighton
        </a>
      </div>
      <p ref="disclaimer" class="force-3d text-sm md:text-base mt-4 text-center">
        <strong>Note:</strong>
        Generative AI is used for content creation. Adult supervision is recommended due to the potential for unexpected
        outputs. But I've done my absolute best to prevent that.
      </p>
    </div>
  </div>
</template>

<script setup>
import { defineEmits, onMounted, ref } from "vue"
import FastButton from "@/components/FastButton.vue"
import gsap from "gsap"

const emit = defineEmits(["getStarted"])

const welcomeScreen = ref(null)
const content = ref(null)
const title = ref(null)
const intro = ref(null)
const links = ref(null)
const cta = ref(null)
const disclaimer = ref(null)
onMounted(() => {
  const yOffset = 24
  const yDur = 0.8
  const opacityDur = 1
  const stagger = 0.05
  const tl = gsap.timeline({ delay: 0.25 })
  const yOptions = { force3D: true, y: yOffset, duration: yDur, ease: "expo.out" }
  const opacityOptions = { opacity: 0, duration: opacityDur, ease: "power2.out" }

  tl.from(title.value, yOptions, 0)
  tl.from(title.value, opacityOptions, 0)
  tl.from(intro.value, yOptions, stagger)
  tl.from(intro.value, opacityOptions, stagger)
  tl.from(links.value, yOptions, stagger * 2)
  tl.from(links.value, opacityOptions, stagger * 2)
  tl.from(cta.value, yOptions, stagger * 3)
  tl.from(cta.value, opacityOptions, stagger * 3)
  tl.from(disclaimer.value, yOptions, stagger * 4)
  tl.from(disclaimer.value, opacityOptions, stagger * 4)
})

const handleCTAClick = () => {
  const yOffset = 12
  const yDur = 0.5
  const opacityDur = 0.45
  const stagger = 0.05
  const tl = gsap.timeline({
    onComplete: () => {
      emit("getStarted")
    },
  })
  const yOptions = { force3D: true, y: yOffset, duration: yDur, ease: "expo.inOut" }
  const opacityOptions = { opacity: 0, duration: opacityDur, ease: "power2.out" }

  tl.to(disclaimer.value, yOptions, stagger * 3)
  tl.to(disclaimer.value, opacityOptions, stagger * 3)
  tl.to(title.value, yOptions, stagger * 3)
  tl.to(title.value, opacityOptions, stagger * 3)
  tl.to(intro.value, yOptions, stagger * 2)
  tl.to(intro.value, opacityOptions, stagger * 2)
  tl.to(links.value, yOptions, stagger)
  tl.to(links.value, opacityOptions, stagger)
  tl.to(cta.value, yOptions, 0)
  tl.to(cta.value, opacityOptions, 0)

  tl.to(welcomeScreen.value, { opacity: 0, duration: 0.5, ease: "power2.inOut" })
}
</script>
