<template>
  <b-card
      class="circle-card"
      no-body
      :id="id"
      border-variant="info"
      header-text-variant="white"
      header-bg-variant="info"
      header-border-variant="info"
      align="center">
    <template class="circle-header" #header>
      <h5 style="font-size: 14px" >{{title}}</h5>
    </template>
    <b-card-text>
      <h2>{{chance}}%</h2>
    </b-card-text>

    <b-popover v-if="popoverTitle !== undefined && popoverContent !== undefined" :target="id" triggers="hover" placement="top">
      <template #title>{{popoverTitle}}</template>
      {{popoverContent}}
    </b-popover>
  </b-card>
</template>

<script>
export default {
  name: "ChanceCardItem",
  props: {
    title: {
      type: String,
      required: true
    },
    chance:{
      type: Number,
      required: true
    },
    id: {
      type: String,
      required: true,
    },
    popoverTitle: String,
    popoverContent: String,
  },
}
</script>

<style scoped>

.circle-card {
  border-radius: 0.30rem 0.30rem 0.30rem 0.30rem;
  margin-right: 5px;
}

.circle-card >>> div {
  border: 2px;
  border-radius: 0.20rem 0.20rem 0 0;
  padding-bottom: 0;
  padding-left: 0;
  padding-right: 0;
}

</style>