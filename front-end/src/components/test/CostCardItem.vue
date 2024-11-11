<template>
  <b-card no-body style="max-width: 50%">
    <b-card-header style="font-size: 12px; padding: 5%">{{title}}</b-card-header>
    <b-card-text v-if="train !== undefined">
      <vs-icon class="transport-icon" style="margin-top: 1%" icon="train" round color="#000000"/>
      <div class="transport-text" style="margin-top: 5%">Train: {{train}}</div>
    </b-card-text>
    <b-card-text v-if="taxi !== undefined" >
      <vs-icon class="transport-icon" icon="local_taxi" round color="#000000"/>
      <div class="transport-text">Taxi: {{taxi}}</div>
    </b-card-text>
    <b-card-text v-if="bus !== undefined">
      <vs-icon class="transport-icon" icon="directions_bus" round color="#000000"/>
      <div class="transport-text">Bus: {{bus}}</div>
    </b-card-text>
  </b-card>
</template>

<script>
export default {
  name: "CostCard",
  props: {
    title: {
      type: String,
      required: true
    },
    train: String,
    taxi: String,
    bus: String,
  },
}
</script>

<style scoped>

.transport-icon {
  padding-top: 5px;
  z-index: 10;
  position: absolute;
  margin-left: 2%;
  margin-top: -4%;
}

.transport-text {
  margin-left: 18%;
  margin-bottom: 5%;
}

</style>