<template>
  <img :src="this.src"
       :class="classThumbnail(this.selected, this.id)"
       alt=""
       @click="onSelect">
</template>

<script>
export default {
  props: ["id", "src", "selected"],

  methods: {
    onSelect() {
      this.$emit("clicked", this.id);
    },

    classThumbnail(selectedId, imageId) {
      if (selectedId === imageId) {
        return `selected`
      }
      return ``
    }
  }
};
</script>

<style scoped>
</style>