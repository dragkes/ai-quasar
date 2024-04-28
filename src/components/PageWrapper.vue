<template>
  <q-layout>
    <q-drawer v-model="drawerInputModel" side="left" style="display: flex; flex-direction: column;" bordered>
      <slot name="drawer-content" style=""></slot>
    </q-drawer>
    <q-page-container>
      <slot/>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const emit = defineEmits<
  { (e: 'open-drawer', value: boolean): void }
>();

const props = defineProps({
  drawerOpen: Boolean
})

const drawerInputModel = computed({
  get() {
    return props.drawerOpen
  },
  set(newValue: boolean) {
    emit('open-drawer', newValue)
  },
});

</script>
