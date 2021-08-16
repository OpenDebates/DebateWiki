<template>
  <div class="login">
    <Footer />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import Footer from "@/components/Footer.vue";

export default defineComponent({
  name: "Login",
  components: {
    Footer,
  },
  setup() {
    let loggedIn = ref(true);

    return { loggedIn };
  },
});
</script>

<style lang="scss"></style>
