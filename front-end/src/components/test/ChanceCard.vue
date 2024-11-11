<script setup>
import ChanceCardItem from './ChanceCardItem.vue'
</script>

<template>
  <b-card no-body>
    <b-card-header style="font-size: 16px">Chances Information</b-card-header>
    <b-card-group deck style="margin-left: 5px; margin-right: 5px">
      <ChanceCardItem
          ref="rain"
          style="margin: 0.6rem;"
          title="Rain"
          :id="'rain-chance'"
          popoverTitle="Chance of Rain"
          popoverContent="There is a 70% chance of rain that impacts only the travel duration of the bus or taxi."
          :chance="70"
      ></ChanceCardItem>
      <ChanceCardItem
          ref="traffic"
          style="margin: 0.6rem"
          title="Traffic"
          :id="'traffic-chance'"
          popoverTitle="Probability of Traffic Jam"
          popoverContent="The pattern of traffic jams is expected to be as depicted, which is 70% accurate."
          :chance="70"
      ></ChanceCardItem>
      <ChanceCardItem
          ref="capacity"
          style="margin: 0.6rem"
          title="Seating Capacity"
          :id="'capacity-chance'"
          popoverTitle="Probability of Seating Capacity"
          popoverContent="With 70% accuracy, public transport seating capacity is expected to be according to our forecasts."
          :chance="70"
      ></ChanceCardItem>
      <ChanceCardItem
          ref="stop"
          style="margin: 0.6rem"
          v-if="showPickUpPointChance"
          title="Stop"
          :id="'stop-chance'"
          popoverTitle="Probability of Stopping at Pick-up Point"
          popoverContent="There is a 65% chance that the commuter may pick up something along her way, making her stop at the shown point on the map."
          :chance="65"
      ></ChanceCardItem>
    </b-card-group>
  </b-card>
</template>

<script>
export default {
  name: "ChanceCard",
  props: {
    chance_list: {
      type: Array,
      required: true
    },
    showPickUpPointChance: {
      type: Boolean,
      required: true
    }
  },
}
</script>

<style scoped>

</style>