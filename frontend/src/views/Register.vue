<template>
  <div class="register">
    <div class="register_box">
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
            <n-form-item first path="reEnteredPassword" ref="rPasswordFormItem">
              <n-input
                :disabled="!model.password"
                v-model:value="model.reEnteredPassword"
                type="password"
                placeholder="Re-enter Password"
                @keydown.enter.prevent
              />
            </n-form-item>
            <n-space justify="space-between">
              <n-button
                :disabled="
                  !model.username || !model.password || !model.reEnteredPassword
                "
                type="primary"
                icon-placement="left"
                @click="handleRegisterButtonClick"
              >
                <template #icon>
                  <n-icon>
                    <login-icon />
                  </n-icon>
                </template>
                Register
              </n-button>
              <n-button dashed @click="$router.push('login')">Login</n-button>
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
  FormItemInst,
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

    const rPasswordFormItem = ref<FormItemInst | null>(null);

    const form = ref<FormInst | null>(null);

    let model = ref<Record<string, null | string>>({
      username: null,
      password: null,
      reEnteredPassword: null,
    });

    function validatePasswordStartWith(rule: FormItemRule, value: string) {
      return (
        model.value.password &&
        model.value.password.startsWith(value) &&
        model.value.password.length >= value.length
      );
    }

    function validatePasswordSame(rule: FormItemRule, value: string) {
      return value === model.value.password;
    }

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
      reEnteredPassword: [
        {
          required: true,
          message: "Re-entered Password is required",
          trigger: ["input", "blur"],
        },
        {
          validator: validatePasswordStartWith,
          message: "Password is not same as re-entered password!",
          trigger: "input",
        },
        {
          validator: validatePasswordSame,
          message: "Password is not same as re-entered password!",
          trigger: ["blur", "password-input"],
        },
      ],
    });

    function handlePasswordInput() {
      if (model.value.reEnteredPassword) {
        if (rPasswordFormItem.value) {
          rPasswordFormItem.value.validate({ trigger: "password-input" });
        }
      }
    }

    function handleRegisterButtonClick(e: ErrorEvent) {
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
      rPasswordFormItem,
      form,
      model: model,
      rules,
      handlePasswordInput,
      handleRegisterButtonClick,
    };
  },
});
</script>

<style lang="scss" scoped>
.register {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 50em;
}
</style>
