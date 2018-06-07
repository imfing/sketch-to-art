<template>
  <div>
    <div>
      <h1>
        About
      </h1>
    </div>
    <div class="content markdown-body">
      <about></about>
    </div>
  </div>
</template>

<script>
import About from "../assets/about.md"

export default {
  name: "AboutPage",

  components: {
    About
  },

  data() {
    return {};
  }
};
</script>

<style>
@import './../assets/github-markdown.css';

.content {
  max-width: 740px;
  margin: 0 auto;
  padding: 0rem 1rem;
  text-align: left;
}

</style>