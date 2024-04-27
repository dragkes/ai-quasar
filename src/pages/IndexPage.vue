<template>
  <PageWrapper :drawer-open="drawerOpen">
    <template #drawer-content>
      <div class="drawer-content">
        <q-btn @click="() => drawerOpen = false">Close</q-btn>
        <div class="slider-container">
          <div><span>Slider 1</span>
            <q-slider v-model="slider1" label :min="0" :max="100"></q-slider>
          </div>
          <div><span>Slider 2</span>
            <q-slider v-model="slider2" label :min="0" :max="100"></q-slider>
          </div>
          <div><span>Slider 3</span>
            <q-slider v-model="slider3" label :min="0" :max="100"></q-slider>
          </div>
        </div>
        <q-btn style="width: 70%" @click="submit">Submit</q-btn>
      </div>
    </template>

    <q-page class="main-page">
      <div class="upload">
        <h5>Select image to upload</h5>
        <q-file v-model="file" class="file-input" color="teal" filled label="Upload an image">
          <template #prepend>
            <q-icon name="cloud_upload" />
          </template>
        </q-file>
        <q-img v-if="src" class="image-to-upload" :src="src"></q-img>
      </div>
    </q-page>
  </PageWrapper>
</template>

<script setup lang="ts">

import { ref, watch } from 'vue';
import { useQuasar } from 'quasar';
import PageWrapper from 'components/PageWrapper.vue';
import axios from 'axios';

const allowedTypes = ['image/jpg', 'image/jpeg', 'image/png'];

const file = ref<File | null>(null);
const src = ref<string | null>(null);
const drawerOpen = ref(false);

const slider1 = ref(0);
const slider2 = ref(0);
const slider3 = ref(0);

const $q = useQuasar();

watch(file, (newValue) => {
  console.log(newValue);
  if (newValue) {
    if (allowedTypes.find((type) => type === newValue?.type) === undefined) {
      $q.notify({
        type: 'negative',
        message: 'Uploaded file.jpg type is not supported'
      })
      console.error('Uploaded file.jpg type is not supported');
      return;
    }
    src.value = URL.createObjectURL(newValue);
    drawerOpen.value = true;
  }
})

const submit = () => {
  let data = new FormData();
  if (!file.value) {
    $q.notify({
      type: 'negative',
      message: 'Internal error'
    })
    return;
  }
  data.append('file', file.value);
  data.append('slider1',  slider1.value.toString());
  data.append('slider2',  slider2.value.toString());
  data.append('slider3',  slider3.value.toString());

  axios.post('upload', data, {
    headers: {
      'accept': 'application/json',
      'Accept-Language': 'en-US,en;q=0.8',
      'Content-Type': 'multipart/form-data',
    }
  })
    .then((response) => {
      console.log(response);
    }).catch((error) => {
    $q.notify({
      type: 'negative',
      message: 'Internal error: ' + error.message,
    });
  });
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

  .slider-container {
    margin-top: 10px;
  }

  .file-input {
    width: 400px;
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
    width: 400px;
  }
</style>
