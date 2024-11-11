<template>
  <div style="width: 100%">
    <b-container class="bv-example-row">
      <b-row>
      <b-col cols="2">
        <b-button @click="showAll"
                  variant="outline-primary">All</b-button>
      </b-col>

      <b-col cols="1">
      </b-col>

      <b-col cols="2">
        <b-card-text>
          {{name}}
        </b-card-text>
      </b-col>

      <b-col cols="5">
      </b-col>

      <b-col cols="2">
        <b-button-group class="float-right">
          <b-button @click="previous"
                    variant="outline-info">&lt;</b-button>

          <b-button @click="next"
                    variant="outline-success">&gt;</b-button>
        </b-button-group>
      </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  name: "RouteController",
  props: {
    name: {
      type: String,
      required: true
    },
  },
  methods: {
    showAll: function (){
      this.$emit('showAllRoutes')
    },
    previous: function (){
      this.$emit('previousRoutes')
    },
    next: function (){
      this.$emit('nextRoutes')
    },
  }
}
</script>

<style scoped>

</style>