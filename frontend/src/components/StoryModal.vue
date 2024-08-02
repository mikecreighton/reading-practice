<style lang="scss" scoped>
.modal {
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

    .modal-content {
        width: 80%;
        padding: 100px 40px 160px 40px;

        p {
            font-size: 36px;
            line-height: 1.6;
            margin-bottom: 0px;
        }
    }

    // mobile
    @media (max-width: 768px) {

        align-items: flex-start;
        padding-top: 100px;

        .modal-content {

            width: 90%;

            p {
                font-size: 24px;
                line-height: 1.6;
            }

        }
    }
    @media (max-width: 480px) {
        padding-top: 0;

        .modal-content {
            width: 100%;

            p {
                font-size: 18px;
                line-height: 1.6;
            }

        }
    }

    .modal-close-button {
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

        &:hover {
            background-color: #303030;
        }
    }

    .modal-regenerate-button {
        position: absolute;
        bottom: 40px;
        left: 50%;
        padding: 20px;
        transform: translateX(-50%);
    }

}
</style>
<template>
  <div class="modal">
    <div class="modal-content">
      <p>{{ story }}</p>
      <button class="modal-close-button" @click="handleCloseRequest">
        &#x2715;
      </button>
      <button
        class="button-labeled modal-regenerate-button"
        @click="$emit('regenerate')"
      >
        Regenerate
      </button>
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
  gsap.to(".modal", { duration: 0.5, y: "0%", ease: Power4.easeOut });
});

const handleCloseRequest = (event) => {
  event.preventDefault();
  emit('cancelRequest');
  gsap.to(".modal", {
    duration: 0.5,
    y: "100%",
    ease: Power4.easeInOut,
    onComplete: () => emit('closeComplete'),
  });
};
</script>