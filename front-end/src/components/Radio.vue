<template>
  <b-card :class="`my-card ${this.bCardColor}`">
    <b-form-group>
      <b-input-group-prepend class="bigger-txt">
        {{index+1}}. {{question}}
      </b-input-group-prepend>
      <b-form-radio-group
          v-model="selected"
          :options="options"
          class="my-input"
      ></b-form-radio-group>
    </b-form-group>
  </b-card>
</template>

<script>
export default {
  name: "Radio",
  props:{
    question: {
      type: String,
      required: true
    },
    options: {
      type: Array,
      required: true
    },
    index: {
      type: Number,
      required: true
    },
    becomeRedIfEmpty: {
      type: Boolean,
      required: true
    },
  },
  data() {
    return {
      selected: '-1',
    }
  },
  computed:{
    bCardColor: function (){
      if(this.becomeRedIfEmpty){
        if(this.selected === "-1"){
          return "my-card-red-color"
        }
        return "my-card-green-color"
      }
      return "my-card-gray-color";
    }
  },
  watch:{
    selected: function (val){
      const answer = this.options.indexOf(val);
      this.$emit('selectedChanged', {question: this.question, answer: answer, type: 'Radio', index: this.index});
    }
  },
}
</script>

<style scoped>

.my-input >>> div {
  margin-top: 1rem;
  margin-right: 3rem;
}

.my-card {
  padding: 0;
  margin-bottom: 2rem;
  border-radius: 15px 50px 30px;
}

.my-card-gray-color {
  border: 2px solid #959690FC;
  background: #e7e7e7;
}

.my-card-red-color {
  border: 2px solid #940A0AA6;
  background: #D53333A5;
}

.my-card-green-color {
  border: 2px solid #18940AA6;
  background: #55D544A5;
}

.bigger-txt {
  font-size: 24px;
}

</style>