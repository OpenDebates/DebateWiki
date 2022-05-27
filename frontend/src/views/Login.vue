<template>
  <div class="login">
    <div class="login_box">
      <n-form :label-width="80" :model="model" :rules="rules" ref="form">
        <n-card>
          <n-space vertical>
            <n-form-item path="username">
              <n-input
                v-model:value="model.username"
                type="text"
                placeholder="Username"
              />
            </n-form-item>
            <n-form-item path="password">
              <n-input
                v-model:value="model.password"
                type="password"
                placeholder="Password"
                @keydown.enter.prevent
              />
            </n-form-item>
            <n-space justify="space-between">
              <n-button
                type="primary"
                icon-placement="left"
                @click="handleValidateButtonClick"
              >
                <template #icon>
                  <n-icon>
                    <login-icon />
                  </n-icon>
                </template>
                Login
              </n-button>
              <n-button dashed @click="$router.push('register')"
                >Register</n-button
              >
            </n-space>
          </n-space>
        </n-card>
      </n-form>
    </div>
    <Footer />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import Footer from "@/components/Footer.vue";
import {
  NButton,
  NIcon,
  NInput,
  NSpace,
  NCard,
  FormItemRule,
  NForm,
  NFormItem,
  FormInst,
} from "naive-ui";
import { Login as LoginIcon } from "@vicons/tabler";

export default defineComponent({
  name: "GlobalLogin",
  components: {
    Footer,
    NSpace,
    NInput,
    NButton,
    NIcon,
    LoginIcon,
    NCard,
    NForm,
    NFormItem,
  },
  setup() {
    let loggedIn = ref(true);
    let username = ref("");
    let password = ref("");

    const form = ref<FormInst | null>(null);

    let model = ref({
      username: null,
      password: null,
    });

    let rules = ref({
      username: [
        {
          required: true,
          validator(rule: FormItemRule, value: string) {
            if (!value) {
              return new Error("Username is required.");
            }
            return true;
          },
          trigger: ["input", "blur"],
        },
      ],
      password: [
        {
          required: true,
          message: "Password is required.",
        },
      ],
    });

    function handleValidateButtonClick(e: ErrorEvent) {
      e.preventDefault();
      if (form.value) {
        form.value.validate((errors: unknown) => {
          if (errors) {
            console.log(errors);
          }
        });
      }
    }

    return {
      loggedIn,
      username,
      password,
      form,
      model,
      rules,
      handleValidateButtonClick,
    };
  },
});
</script>

<style lang="scss" scoped>
.login_box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50em;
}
</style>
