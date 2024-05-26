<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import store from 'src/store';
import PageWrapper from 'components/PageWrapper.vue';

const router = useRouter();
const oldImageSrc = ref<string | undefined>(undefined);
const newImageSrc = ref<string | undefined>(undefined);


onMounted(() => {
  if(store.state.oldImage && store.state.newImage) {
    oldImageSrc.value = URL.createObjectURL(store.state.oldImage);
    newImageSrc.value = URL.createObjectURL(store.state.newImage);
  } else {
    router.push('/');
  }
});

defineOptions({
  name: 'ResultPage'
});
</script>

<template>
  <PageWrapper :drawer-open = false>
    <q-page>
      <div class="result">
        <h5>See the result</h5>
        <div style="display: flex; flex-direction: row; align-items: center;">
          <div style="display: flex; flex-direction: column; align-items: center; margin-right: 1vw">
            <q-img class="image" :src="oldImageSrc"></q-img>
            <p>Before</p>
          </div>
          <div style="display: flex; flex-direction: column; align-items: center; margin-left: 1vw">
            <q-img class="image" :src="newImageSrc"></q-img>
            <p>After</p>
          </div>
        </div>
        <q-btn color="red" @click="() => {router.push('/')}">Go back</q-btn>
      </div>
    </q-page>
  </PageWrapper>
</template>

<style scoped lang="scss">
.result {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.image {
  margin-top: 16px;
  border: 1px solid black;
  height: auto;
  width: 18vw;
}

p {
  font-size: max(0.8em, 0.5vw);
}
</style>
