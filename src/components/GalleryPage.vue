<template>
  <div>
    <h1>Gallery</h1>
    <p>You can see works from other people here.</p>
    <div class="images-container">
      <div class="images"
           v-viewer="{inline: false, toolbar: false, rotatable: false, transition: true}">
        <img v-for="img in showList"
             :key="img"
             :src="'https://dip.imfing.com/images/'+img"
             alt="">
      </div>
      <div>
        <button v-if="showMore"
                class="btn"
                @click="loadMore">
          <span>Load more</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Viewer from "v-viewer";
import "viewerjs/dist/viewer.css";
import Vue from "vue";
Vue.use(Viewer);

const axiosStyle = axios.create({ baseURL: "https://dip.imfing.com/style" });

export default {
  name: "GalleryPage",

  components: {
    Viewer
  },

  data() {
    return {
      imgList: "",
      showList: "",
      showNum: 10,
      showMore: false
    };
  },

  mounted: function() {
    axiosStyle.get("/getGalleryList").then(response => {
      this.imgList = response.data;
      if (this.imgList.length > this.showNum) {
        this.showList = this.imgList.slice(0, this.showNum);
        this.showMore = true;
      } else {
        this.showList = this.imgList;
      }
    });
  },

  methods: {
    loadMore() {
      if (this.showNum < this.imgList.length) {
        if (this.showNum + 10 > this.imgList.length) {
          this.showNum = this.imgList.length;
          this.showList = this.imgList;
          this.showMore = false;
        } else {
          this.showNum += 10;
          this.showList = this.imgList.slice(0, this.showNum);
        }
      } else {
        this.showMore = false;
      }
    }
  }
};
</script>

<style scoped>
.images-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.images {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin: 0 auto;
}

.images img {
  width: 150px;
  height: 150px;
  margin: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.055);
  padding: 2px;
  opacity: 1;
  transition: opacity 1s;
}

.btn {
  background-color: #008cba;
  border: none;
  border-radius: 0.3em;
  color: white;
  padding: 0.5em 1em;
  margin: 1em 0.5em;
  font-size: 1rem;
  font-family: inherit;
  font-weight: 400;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  -webkit-transition-duration: 0.4s; /* Safari */
  transition-duration: 0.4s;
  cursor: pointer;
}
</style>