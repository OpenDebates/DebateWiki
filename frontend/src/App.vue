<template>
  <n-config-provider
    style="width: 100%; height: 100%"
    :theme="getTheme"
    :theme-overrides="themeOverrides"
  >
    <n-notification-provider>
      <router-view />
      <n-global-style />
    </n-notification-provider>
  </n-config-provider>
</template>

<script lang="ts">
import { computed, defineComponent } from "vue";
import {
  darkTheme,
  NConfigProvider,
  NGlobalStyle,
  NNotificationProvider,
} from "naive-ui";
import { useStore } from "vuex";

export default defineComponent({
  name: "GlobalApp",
  components: {
    NConfigProvider,
    NNotificationProvider,
    NGlobalStyle,
  },
  setup() {
    const store = useStore();
    const themeOverrides = store.state.theme.getOverrides;
    const getTheme = computed(() =>
      store.state.theme.dark ? darkTheme : undefined
    );
    return { themeOverrides, getTheme };
  },
});
</script>

<style lang="scss"></style>
