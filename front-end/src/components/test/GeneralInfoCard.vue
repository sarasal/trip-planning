<script setup>
import CostCard from './CostCard.vue'
import ChanceCard from './ChanceCard.vue'
</script>

<template>
  <b-card title="General information" style="font-size: 12px" ref="generalInfo">
    <!--            TODO: Clear this code-->

    <b-row ref="rainHigh" v-if="highChanceRain">* There is a very high chance of rain. Rain slows down buses and taxis, leading to longer commute times by around 40%. </b-row>
    <b-row ref="rainLow" v-if="lowChanceRain">* There is a very low chance of rain. Rain slows down buses and taxis, leading to longer commute times by around 40%.</b-row>
    <b-row ref="rainFixed" v-if="highMediumDiagnose">* Today is rainy. Rain slows down buses and taxis, leading to longer commute times by around 40%.</b-row>


    <b-row ref="trafficHigh" v-if="highChanceTraffic">* There is a very high chance  with orange or red color indicating heavy or moderate traffic. Traffic jams lead to longer commute times with the bus or taxi. </b-row>
    <b-row ref="trafficLow" v-if="lowChanceTraffic">* There is a very low chance that streets will become congested, indicated by the orange and red colors on the map representing moderate and heavy traffic jams.</b-row>
    <b-row ref="trafficFixed" v-if="highMediumDiagnose">* Traffic jam is demonstrated on the map, with orange or red color indicating heavy or moderate traffic. Traffic jams lead to longer commute times with the bus or taxi.</b-row>

    <b-row ref="capacityHigh" v-if="highChanceCapacity">* There is a high possibility of not catching the intended bus or train due to limited or no seats condition, resulting in an additional travel time of 10 (for buses) to 20 minutes (for trains).</b-row>
    <b-row ref="capacityLow" v-if="lowChanceCapacity">* There is a high possibility of catching the intended bus or train, due to seat availability of buses and trains.</b-row>
    <b-row ref="capacityFixed" v-if="highMediumDiagnose">* In situations where no or limited seats are available, there is a possibility of not catching the intended bus or train, resulting in an additional travel time of 10 (for buses) to 20 minutes (for trains).</b-row>


    <b-row ref="peakFares" v-if="high">* Peak hours fall within these ranges: 6:30 - 9 AM, 4 - 6:30 PM, and 8 - 10:30 PM.</b-row>
    <b-row ref="distantBasedFare" v-if="high">* If the commuter travels at least 10 km by train or 4 km by bus, a discount based on the kilometers traveled will be applied to her fare.</b-row>
    <b-row ref="limitedTransfers" v-if="high">* The number of transfers between transport modes is limited to {{n_transfer}}.</b-row>

    <b-row ref="stopHigh" v-if="highChanceStop">* It is highly probable that the commuter might have to stop for something on her route, which could lead her to cross at the indicated point on the map.</b-row>
    <b-row ref="stopLow" v-if="lowChanceStop">* It is lowly probable that the commuter might have to stop for something on her route, which could lead her to cross at the indicated point on the map.</b-row>
    <b-row ref="stopFixed" v-if="highDiagnose">* The commuter has to stop for something on her route, which could lead her to cross at the indicated point on the map. </b-row>

    <br />

    <b-row> *** The streets depicted on a map may not align with actual travel routes.</b-row>
    <b-row> *** Each of the features related to tasks is established without any influence on one another.</b-row>
    <b-row> *** There aren't any preferences toward particular transportation modes or routes.</b-row>
    <br />

    <CostCard ref="costCard" :static_info="static_info" :high="high" :highMedium="highMedium"></CostCard>
<!--    <CostCard ref="costCard" :static_info="static_info" :showIfHighComplexity="highComplexity" :showSubscription="showSubscription"></CostCard>-->
<!--    <ChanceCard ref="chanceCard" style="margin-top: 1rem" v-if="showChance" :chance_list="chance_list" :showPickUpPointChance="showPickUpPointChance"></ChanceCard>-->


  </b-card>
</template>

<script>
export default {
  name: "GeneralInfoCard",
  props: {
    chance_list: {
      type: Array,
      required: true
    },
    static_info: {
      type: Array,
      required: true
    },
    task_type: {
      type: String,
      required: true
    },
    complexity: {
      type: String,
      required: true
    },
    n_transfer: {
      type: String,
      required: true,
    }
  },
  computed:{
    highChanceRain: function(){
      return parseInt(this.chance_list[0]['chance']) >= 60 && this.task_type === 'prognostic' && this.complexity !== 'low';
    },
    lowChanceRain: function(){
      return parseInt(this.chance_list[0]['chance']) < 60 && this.task_type === 'prognostic' && this.complexity !== 'low';
    },
    highChanceCapacity: function(){
      return parseInt(this.chance_list[2]['chance']) >= 60 && this.task_type === 'prognostic' && this.complexity !== 'low';
    },
    lowChanceCapacity: function(){
      return parseInt(this.chance_list[2]['chance']) < 60 && this.task_type === 'prognostic' && this.complexity !== 'low';
    },
    highChanceTraffic: function(){
      return parseInt(this.chance_list[1]['chance']) >= 60 && this.task_type === 'prognostic' && this.complexity !== 'low';
    },
    lowChanceTraffic: function(){
      return parseInt(this.chance_list[1]['chance']) < 60 && this.task_type === 'prognostic' && this.complexity !== 'low';
    },
    highChanceStop: function(){
      return parseInt(this.chance_list[3]['chance']) >= 60 && this.task_type === 'prognostic' && this.complexity === 'high';
    },
    lowChanceStop: function(){
      return parseInt(this.chance_list[3]['chance']) < 60 && this.task_type === 'prognostic' && this.complexity === 'high';
    },
    highMedium: function () {
      return  this.complexity !== 'low';
    },
    high: function () {
      return  this.complexity === 'high';
    },
    highMediumDiagnose: function () {
      return this.task_type === 'diagnostic' && this.complexity !== 'low';
    },
    highDiagnose: function () {
      return this.complexity === 'high' && this.task_type === 'diagnostic';
    },
  }
}
</script>

<style scoped>

</style>