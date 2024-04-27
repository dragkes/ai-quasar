<template>
  <q-layout>
    <q-drawer v-model="props.drawerOpen" side="left" style="display: flex; flex-direction: column" bordered>
      <slot name="drawer-content" style=""></slot>
    </q-drawer>
    <q-page-container>
      <slot/>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">

const props = defineProps({
  drawerOpen: Boolean
})

</script>
