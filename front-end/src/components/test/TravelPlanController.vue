<template>
  <div style="width: 100%">
    <b-container class="bv-example-row">
      <b-row>
        <b-col cols="4">
          <b-button @click="previous" class="float-left"
                  variant="outline-info">&lt;</b-button>
        </b-col>

        <b-col cols="4">
          <b-card-text>
            {{name}}
          </b-card-text>
        </b-col>

        <b-col cols="2">
        </b-col>

        <b-col cols="2">
          <b-button @click="next" class="float-right"
                    variant="outline-success">&gt;</b-button>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "TravelPlanController",
  props: {
    name: {
      type: String,
      required: true
    },
  },
  methods: {
    previous: function (){
      this.$emit('previousTravelPlan')
    },
    next: function (){
      this.$emit('nextTravelPlan')
    },
  }
}
</script>

<style scoped>

</style>