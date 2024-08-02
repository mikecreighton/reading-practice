<style lang="scss" scoped>
.story-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #FFF;
    display: flex;
    align-items: center;
    justify-content: center;
    transform: translateY(100%);

    .story-modal-content {
        padding: 60px 40px 100px 40px;

        p {
            font-size: 16px;
            line-height: 1.6;
        }

        @media (min-width: 768px) {
            p {
                font-size: 30px;
            }
        }

        @media (min-width: 1200px) {
            p {
                font-size: 36px;
            }
        }
    }

    .story-modal-close-button {
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 30px;
        width: 60px;
        height: 60px;
        cursor: pointer;
        user-select: none;
        border: none;
        color: #FFF;
        text-align: center;
        background-color: #101010;
        border-radius: 12px;
        transition: background-color 0.1s ease-in-out;
        padding: 0;

        &:hover, &:focus, &:active {
            background-color: #303030;
        }
    }

    .regenerate-button {
        position: absolute;
        bottom: 40px;
        left: 50%;
        padding: 20px;
        transform: translateX(-50%);
    }

}
</style>
<template>
  <div class="story-modal">
    <div class="story-modal-content">
      <p>{{ story }}</p>
      <button class="story-modal-close-button" @click="handleCloseRequest">
        &#x2715;
      </button>
      <button class="button-labeled regenerate-button" @click="$emit('regenerate')">Regenerate</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { gsap, Power4 } from 'gsap';

const props = defineProps({
  story: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(['closeComplete', 'cancelRequest']);

onMounted(() => {
  gsap.to(".story-modal", { duration: 0.5, y: "0%", ease: Power4.easeOut });
});

const handleCloseRequest = (event) => {
  event.preventDefault();
  emit('cancelRequest');
  gsap.to(".story-modal", {
    duration: 0.5,
    y: "100%",
    ease: Power4.easeInOut,
    onComplete: () => emit('closeComplete'),
  });
};
</script>