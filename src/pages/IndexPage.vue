<template>
  <PageWrapper>

    <q-page class="main-page">
      <div class="upload">
        <h3 style="margin-bottom: 0">AI image enhancer</h3>
        <h5 style="margin-top: 1em">Enhance images with AI lorem ipsum</h5>
        <q-file
          v-model="uploadedImage"
          standout
          rounded
          class="file-input"
          bg-color="red"
          label="Upload files"
          label-color="white"
        >
        </q-file>
        <div v-if="src" style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 80px ">
          <q-img  class="image-to-upload" :src="src"></q-img>
          <div style="display: flex; flex-direction: column; gap: 20px">
            <h5 style="margin: 0">Enhancing params</h5>
            <q-checkbox v-model="checkbox1">Checkbox 1</q-checkbox>
            <q-checkbox v-model="checkbox2">Checkbox 2</q-checkbox>
            <q-checkbox v-model="checkbox3">Checkbox 3</q-checkbox>
          </div>
        </div>

        <q-btn v-if="src" color="red" style="margin-top: 16px" @click="submit">Submit</q-btn>
      </div>
    </q-page>
  </PageWrapper>
</template>

<script setup lang="ts">

import { ref, watch } from 'vue';
import { useQuasar } from 'quasar';
import PageWrapper from 'components/PageWrapper.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const allowedTypes = ['image/jpg', 'image/jpeg', 'image/png'];

const uploadedImage = ref<File | null>(null);
const src = ref<string | undefined>(undefined);

const checkbox1 = ref(false);
const checkbox2 = ref(false);
const checkbox3 = ref(false);

const $q = useQuasar();
const router = useRouter();
const store = useStore();


watch(uploadedImage, (newValue) => {
  if (newValue) {
    if (allowedTypes.find((type) => type === newValue?.type) === undefined) {
      $q.notify({
        type: 'negative',
        message: 'Uploaded file.jpg type is not supported'
      });
      console.error('Uploaded file.jpg type is not supported');
      return;
    }
    src.value = URL.createObjectURL(newValue);
    store.commit('setOldImage', uploadedImage.value);
  }
});

const submit = () => {
  let data = new FormData();
  if (!uploadedImage.value) {
    $q.notify({
      type: 'negative',
      message: 'Internal error'
    });
    return;
  }
  data.append('file', uploadedImage.value);
  data.append('checkbox1', checkbox1.value.toString());
  data.append('checkbox2', checkbox2.value.toString());
  data.append('checkbox3', checkbox3.value.toString());


  $q.loading.show();
  axios.post('upload', data, {
    headers: {
      'accept': 'application/json',
      'Accept-Language': 'en-US,en;q=0.8',
      'Content-Type': 'multipart/form-data'
    },
    responseType: 'blob'
  })
    .then(async (response) => {
      $q.loading.hide();
      const newImage = new File([response.data], 'result.jpg', {
        type: 'image/jpeg'
      });
      store.commit('setNewImage', newImage);
      await router.push('/result');
    }).catch((error) => {
    $q.loading.hide();
    $q.notify({
      type: 'negative',
      message: 'Internal error: ' + error.message
    });
  });
};

defineOptions({
  name: 'IndexPage'
});
</script>

<style scoped lang="scss">


.main-page {
  display: flex;
  justify-content: center;
  flex-direction: row;
}

.drawer-content {
  padding: 8px;
}

.slider-container {
  margin-top: 10px;
}

.file-input {
  width: 400px
}

.upload {
  //margin-top: 5vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.image-to-upload {
  margin-top: 16px;
  border: 1px solid black;
  height: auto;
  width: 18vw;
}

h5 {
  font-size: max(0.8em, 1vw);
}
</style>
