<script setup lang="ts">
import { useI18n } from "vue-i18n";
import { ref, reactive } from "vue";
import Motion from "../utils/motion";
import { message } from "@/utils/message";
import { updateRules } from "../utils/rule";
import type { FormInstance } from "element-plus";
import { useVerifyCode } from "../utils/verifyCode";
import { $t, transformI18n } from "@/plugins/i18n";
import { useUserStoreHook } from "@/store/modules/user";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import Lock from "@iconify-icons/ri/lock-fill";
import Iphone from "@iconify-icons/ep/iphone";
import Message from "@iconify-icons/ep/message";
import User from "@iconify-icons/ri/user-3-fill";
import { signUp } from "@/api/user";
import { getTopMenu, initRouter } from "@/router/utils";
import { useRouter } from "vue-router";

const { t } = useI18n();
const checked = ref(false);
const loading = ref(false);
const router = useRouter();
const disabled = ref(false);
const ruleForm = reactive({
  username: "",
  nickname: "",
  phone: "",
  email: "",
  password: "",
  repeatPassword: ""
});
const ruleFormRef = ref<FormInstance>();
const { isDisabled, text } = useVerifyCode();
const repeatPasswordRule = [
  {
    validator: (rule, value, callback) => {
      if (value === "") {
        callback(new Error(transformI18n($t("login.purePassWordSureReg"))));
      } else if (ruleForm.password !== value) {
        callback(
          new Error(transformI18n($t("login.purePassWordDifferentReg")))
        );
      } else {
        callback();
      }
    },
    trigger: "blur"
  }
];

const onUpdate = async (formEl: FormInstance | undefined) => {
  loading.value = true;
  if (!formEl) return;
  await formEl.validate(valid => {
    if (valid) {
      if (checked.value) {
        // 模拟请求，需根据实际开发进行修改
        signUp(ruleForm).then(res => {
          if (res.success) {
            message(transformI18n($t("login.pureRegisterSuccess")), {
              type: "success"
            });
            loading.value = false;
            useUserStoreHook()
              .loginByUsername({
                username: ruleForm.username,
                password: "admin123"
              })
              .then(res => {
                if (res.success) {
                  // 获取后端路由
                  return initRouter().then(() => {
                    disabled.value = true;
                    router
                      .push(getTopMenu(true).path)
                      .then(() => {
                        message(t("login.pureLoginSuccess"), {
                          type: "success"
                        });
                      })
                      .finally(() => (disabled.value = false));
                  });
                } else {
                  message($t("login.pureLoginFail"), { type: "error" });
                }
              })
              .finally(() => (loading.value = false));
          } else {
            message(res.msg || $t("login.pureRegisterFail"), {
              type: "error"
            });
            loading.value = false;
          }
        });
      } else {
        loading.value = false;
        message(transformI18n($t("login.pureTickPrivacy")), {
          type: "warning"
        });
      }
    } else {
      loading.value = false;
    }
  });
};

function onBack() {
  useVerifyCode().end();
  useUserStoreHook().SET_CURRENTPAGE(0);
}
</script>

<template>
  <el-form
    ref="ruleFormRef"
    :model="ruleForm"
    :rules="updateRules"
    size="large"
  >
    <Motion>
      <el-form-item
        :rules="[
          {
            required: true,
            message: transformI18n($t('login.pureUsernameReg')),
            trigger: 'blur'
          }
        ]"
        prop="username"
      >
        <el-input
          v-model="ruleForm.username"
          clearable
          :placeholder="t('login.pureUsername')"
          :prefix-icon="useRenderIcon(User)"
        />
      </el-form-item>
    </Motion>

    <Motion>
      <el-form-item
        :rules="[
          {
            required: true,
            message: transformI18n($t('login.pureNicknameReg')),
            trigger: 'blur'
          }
        ]"
        prop="nickname"
      >
        <el-input
          v-model="ruleForm.nickname"
          clearable
          :placeholder="t('login.pureNickname')"
          :prefix-icon="useRenderIcon(User)"
        />
      </el-form-item>
    </Motion>

    <Motion :delay="100">
      <el-form-item
        :rules="[
          {
            required: true,
            message: transformI18n($t('login.purePhoneReg')),
            trigger: 'blur'
          }
        ]"
        prop="phone"
      >
        <el-input
          v-model="ruleForm.phone"
          clearable
          :placeholder="t('login.purePhone')"
          :prefix-icon="useRenderIcon(Iphone)"
        />
      </el-form-item>
    </Motion>

    <Motion :delay="100">
      <el-form-item
        :rules="[
          {
            required: true,
            message: transformI18n($t('login.pureEmailReg')),
            trigger: 'blur'
          }
        ]"
        prop="email"
      >
        <el-input
          v-model="ruleForm.email"
          clearable
          :placeholder="t('login.pureEmail')"
          :prefix-icon="useRenderIcon(Message)"
        />
      </el-form-item>
    </Motion>

    <Motion :delay="200">
      <el-form-item prop="password">
        <el-input
          v-model="ruleForm.password"
          clearable
          show-password
          :placeholder="t('login.purePassword')"
          :prefix-icon="useRenderIcon(Lock)"
        />
      </el-form-item>
    </Motion>

    <Motion :delay="250">
      <el-form-item :rules="repeatPasswordRule" prop="repeatPassword">
        <el-input
          v-model="ruleForm.repeatPassword"
          clearable
          show-password
          :placeholder="t('login.pureSure')"
          :prefix-icon="useRenderIcon(Lock)"
        />
      </el-form-item>
    </Motion>

    <Motion :delay="300">
      <el-form-item>
        <el-checkbox v-model="checked">
          {{ t("login.pureReadAccept") }}
        </el-checkbox>
        <el-button link type="primary">
          {{ t("login.purePrivacyPolicy") }}
        </el-button>
      </el-form-item>
    </Motion>

    <Motion :delay="350">
      <el-form-item>
        <el-button
          class="w-full"
          size="default"
          type="primary"
          :loading="loading"
          @click="onUpdate(ruleFormRef)"
        >
          {{ t("login.pureDefinite") }}
        </el-button>
      </el-form-item>
    </Motion>

    <Motion :delay="400">
      <el-form-item>
        <el-button class="w-full" size="default" @click="onBack">
          {{ t("login.pureBack") }}
        </el-button>
      </el-form-item>
    </Motion>
  </el-form>
</template>
