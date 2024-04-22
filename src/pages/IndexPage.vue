<template>
  <PageWrapper :drawer-open="drawerOpen">
    <template #drawer-content>
      <div class="drawer-content">
        <q-btn @click="() => drawerOpen = false">Close</q-btn>
        <div style="margin-top: 8px">
          <span>Slider 1</span>
          <q-slider v-model="slider1" :min="0" :max="100" >asdad</q-slider>
        </div>
      </div>
    </template>

    <q-page class="main-page">
      <div class="upload">
        <h5>Select image to upload</h5>
        <q-file class="file-input" color="teal" filled v-model="test" label="Upload an image">
          <template #prepend>
            <q-icon name="cloud_upload" />
          </template>
        </q-file>
        <q-img class="image-to-upload" v-if="src" :src="src"></q-img>
      </div>
    </q-page>
  </PageWrapper>
</template>

<script setup lang="ts">

import { ref, watch } from 'vue';
import { useQuasar } from 'quasar';
import PageWrapper from 'components/PageWrapper.vue';

const allowedTypes = ['image/jpg', 'image/jpeg', 'image/png'];

const test = ref<File | null>(null);
const src = ref<string | null>(null);
const drawerOpen = ref(false);

const slider1 = ref(0);

const $q = useQuasar();

watch(test, (newValue) => {
  console.log(newValue);
  if (newValue) {
    if (allowedTypes.find((type) => type === newValue?.type) === undefined) {
      $q.notify({
        type: 'negative',
        message: 'Uploaded file type is not supported'
      })
      console.error('Uploaded file type is not supported');
      return;
    }
    src.value = URL.createObjectURL(newValue);
    drawerOpen.value = true;
  }
})

const submit = () => {
  //TODO submit data to backend
}

defineOptions({
  name: 'IndexPage'
});
</script>

<style scoped lang="scss">
  .main-page{
    display: flex;
    justify-content: center;
    flex-direction: row;
  }

  .drawer-content {
    padding: 8px;
  }

  .file-input {
    width: 400px;
  }

  .upload {
    margin-top: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .image-to-upload {
    margin-top: 16px;
    border: 1px solid black;
    height: auto;
    width: 400px;
  }
</style>
