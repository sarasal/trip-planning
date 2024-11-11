<script setup>
import CostCardItem from './CostCardItem.vue'
</script>

<template>
  <b-card no-body>
    <b-card-header style="font-size: 16px">Cost Information</b-card-header>
    <b-card-group deck style="margin: 5px">
      <CostCardItem
          ref="transportFare"
          title="Public Transport Fare per km"
          :train="`${trainFare} €`"
          :taxi="`${taxiFare} €`"
          :bus="`${busFare} €`"
      ></CostCardItem>
      <CostCardItem
          ref="subscription"
          v-if="highMedium"
          title="Subscription Discount per km"
          :train="calculatePercentage(static_info[2].train, trainFare)"
          :taxi="calculatePercentage(static_info[2].taxi, taxiFare)"
      ></CostCardItem>
    </b-card-group>

    <b-card-group v-if="high" deck style="margin: 5px">
      <CostCardItem
          ref="peakFare"
          title="Peak-Hour Fare Rise per km"
          :train="calculatePercentage(static_info[3].train, trainFare)"
          :taxi="calculatePercentage(static_info[3].taxi, taxiFare)"
      ></CostCardItem>
      <CostCardItem
          ref="distanceBasedDiscount"
          title="Kilometer-Based Discount per km"
          :train="`${calculatePercentage(static_info[4].train, trainFare)} above 10 km trip`"
          :bus="`${calculatePercentage(static_info[4].bus, busFare)} above 4 km trip`"
      ></CostCardItem>
    </b-card-group>
  </b-card>
</template>

<script>
export default {
  name: "CostCard",
  props: {
    static_info: {
      type: Array,
      required: true
    },
    highMedium:{
      type: Boolean,
      required: true
    },
    high: {
      type: Boolean,
      required: true
    }
  },
  methods: {
    calculatePercentage: function (change, base){
      if (change === undefined){
        return undefined;
      }

      return `${Math.round(Math.abs((change/base)*100))}%`;
    }
  },
  computed: {
    trainFare: function (){
      return this.static_info[0].train;
    },
    taxiFare: function (){
      return this.static_info[0].taxi;
    },
    busFare: function (){
      return this.static_info[0].bus;
    },
  }
}
</script>

<style scoped>

</style>