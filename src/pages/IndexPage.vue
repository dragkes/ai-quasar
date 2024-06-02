<template>
  <PageWrapper>

    <q-page class="main-page">
      <div class="upload">
        <h3 style="margin-bottom: 0">AI image enhancer</h3>
        <h5 style="margin-top: 1em">Apply various effects to an image using AI</h5>
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

        <span style="opacity: 0.6">Images must be exactly 256 by 256 pixels</span>

        <div
          v-if="uploadedImageObjectUrl"
          style="display: flex; flex-direction: row; align-items: center; justify-content: center; gap: 80px ">
          <q-img class="image-to-upload" :src="uploadedImageObjectUrl"></q-img>
          <div style="display: flex; flex-direction: column; gap: 20px">
            <h5 style="margin: 0">Enhancing params</h5>
            <div>
              <q-checkbox v-model="colorize">
                Colorize
                <q-tooltip anchor="center right" self="center left">
                  Colorize monochromatic image
                </q-tooltip>
              </q-checkbox>
            </div>

            <div>
              <q-checkbox v-model="sharpen">
                Sharpen
                <q-tooltip anchor="center right" self="center left">
                  Sharpen image
                </q-tooltip>
              </q-checkbox>
            </div>

            <div>
              <q-checkbox v-model="removeGlare">
                Remove glare
                <q-tooltip anchor="center right" self="center left">
                  Remove glare defects from your image
                </q-tooltip>
              </q-checkbox>
            </div>
          </div>
        </div>

        <q-btn
          v-if="uploadedImageObjectUrl"
          :disabled="!anyCheckboxSelected()"
          color="red"
          style="margin-top: 16px"
          @click="submit"
        >
          Submit
        </q-btn>
        <span v-if="uploadedImageObjectUrl && !anyCheckboxSelected()" style="color:red;">Please choose at least one enhancement parameter</span>
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
const uploadedImageObjectUrl = ref<string | undefined>(undefined);

const colorize = ref(false);
const sharpen = ref(false);
const removeGlare = ref(false);

const $q = useQuasar();
const router = useRouter();
const store = useStore();

const anyCheckboxSelected = (): boolean => {
  return colorize.value || sharpen.value || removeGlare.value;
};

watch(uploadedImage, (newValue) => {
  if (newValue) {
    if (allowedTypes.find((type) => type === newValue?.type) === undefined) {
      $q.notify({
        type: 'negative',
        message: 'Uploaded file type is not supported'
      });
      uploadedImage.value = null;
      throw new Error('Uploaded file type is not supported');

    }

    const objectUrl = URL.createObjectURL(newValue);

    let img = new Image();
    img.src = objectUrl;

    img.onload = () => {
      if (img.height > 256 || img.width > 256) {
        $q.notify({
          type: 'negative',
          message: 'Image must be exactly 256 by 256 pixels',
          caption: `Provided image is ${img.height} by ${img.width}`
        });
        uploadedImage.value = null;
        throw new Error('Image must be exactly 256 by 256 pixels');
      }
      uploadedImageObjectUrl.value = objectUrl;

      store.commit('setOldImage', newValue);
    };
  }
});

const submit = () => {
  let data = new FormData();
  if (!uploadedImage.value) {
    return;
  }

  if (!anyCheckboxSelected()) {
    $q.notify({
      type: 'negative',
      message: 'At least one parameter must be selected'
    });
    throw new Error('At least one parameter must be selected');
  }
  data.append('file', uploadedImage.value);
  data.append('colorize', colorize.value.toString());
  data.append('sharpen', sharpen.value.toString());
  data.append('removeGlare', removeGlare.value.toString());


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
