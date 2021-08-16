import { GlobalThemeOverrides } from "naive-ui";
import dark from "@/settings/themes/dark";
import light from "@/settings/themes/light";

const theme = {
  state: {
    dark: true,
  },
  mutations: {
    switchTheme(state: Record<string, boolean>): void {
      state.dark = !state.dark;
    },
  },
  getters: {
    getTheme(state: Record<string, boolean>): boolean {
      return state.dark;
    },
    getOverrides(state: Record<string, boolean>): GlobalThemeOverrides {
      if (state.dark) {
        return dark;
      } else {
        return light;
      }
    },
  },
  actions: {},
  namespaced: true,
};

export default theme;
