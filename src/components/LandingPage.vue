<template>
  <div id="wrapper">
    <h1>
      Sketch to Art
    </h1>
    <div class="container">
      <div class="section">
        <h3>Start drawing</h3>
        <div class="canvas-wrapper">
          <drawing-board ref="canvas"></drawing-board>
        </div>
        <button class="btn"
                @click="clearCanvas">
          <span class="clear"></span>
          <span>Clear</span>
        </button>
      </div>

      <div class="section">
        <h3>Style</h3>
        <div class="image-container">
          <div class="image-flex">
            <div v-for="image in styleImages"
                 :key="image.id"
                 class="image-item">
              <image-item :src="image.src"
                          :id="image.id"
                          :selected="selectedId"
                          @clicked="onSelectImage"></image-item>
            </div>
          </div>
        </div>
        <div class="hint">Choose a style above</div>

        <div class="options">
          <toggle-button :value="!highReality"
                         :color="{checked: '#cb8589', unchecked: '#0984e3'}"
                         :sync="true"
                         :labels="{checked: 'More Style', unchecked: 'More Real'}"
                         :width="80"
                         :height="20"
                         @change="!toggleReality" />
          <toggle-button :value="!highQuality"
                         :color="{checked: '#00a388', unchecked: '#9b59b6'}"
                         :sync="true"
                         :labels="{checked: 'High Speed', unchecked: 'High Quality'}"
                         :width="85"
                         :height="20"
                         @change="toggleQuality" />
        </div>

        <button class="btn"
                :disabled="submitDisable"
                @click="submitDrawing">
          <span class="submit"></span>
          <span>Submit</span>
        </button>
      </div>

      <div class="section">
        <h3>Result</h3>
        <div class="result-container">
          <div class="hint"
               v-if="!resultSrc">
            Your result will be shown here.
          </div>
          <img v-if="resultSrc"
               :src="resultSrc"
               alt="">
        </div>

        <button v-if="resultSrc"
                class="btn"
                @click="toggleResult">
          <span class="toggle"></span>
          <span>Toggle result</span>
        </button>
        <button v-if="resultSrc"
                class="btn"
                @click="uploadToGallery">
          <span>Upload to Gallery</span>
        </button>
        <div v-if="resultSrc"
             class="hint">Right click or press long to save</div>
      </div>
    </div>

    <div class="overlay"
         v-if="showWaitModal">
      <div class="half-circle-spinner">
        <div class="circle circle-1"></div>
        <div class="circle circle-2"></div>
      </div>
      <div class="content">
        {{ modalContent }}
      </div>
    </div>
  </div>
</template>

<script>
import DrawingBoard from "./DrawingBoard.vue";
import ImageItem from "./ImageItem.vue";
import axios from "axios";
import Vue from "vue";
import VueSwal from "vue-swal";
import ToggleButton from "vue-js-toggle-button";

Vue.use(VueSwal);
Vue.use(ToggleButton);

const axiosPix =
  process.env.NODE_ENV === "development"
    ? axios.create({ baseURL: "http://localhost:5001" })
    : axios.create({ baseURL: "https://dip.imfing.com/pix" });

const axiosStyle =
  process.env.NODE_ENV === "development"
    ? axios.create({ baseURL: "http://localhost:5002" })
    : axios.create({ baseURL: "https://dip.imfing.com/style" });

export default {
  name: "LandingPage",

  components: {
    DrawingBoard,
    ImageItem
  },

  data() {
    return {
      msg: "Welcome",
      styleImages: [
        { id: "1", src: require("@/assets/thumbs/1.jpg") },
        { id: "2", src: require("@/assets/thumbs/2.jpg") },
        { id: "3", src: require("@/assets/thumbs/3.jpg") },
        { id: "4", src: require("@/assets/thumbs/4.jpg") },
        { id: "5", src: require("@/assets/thumbs/5.jpg") },
        { id: "6", src: require("@/assets/thumbs/6.jpg") },
        { id: "7", src: require("@/assets/thumbs/7.jpg") },
        { id: "8", src: require("@/assets/thumbs/8.jpg") },
        { id: "9", src: require("@/assets/thumbs/9.jpg") }
      ],
      selectedId: 1,
      sessionId: "",

      highReality: false,
      highQuality: false,

      showStyle: true,
      resultSrc: "",
      resultPix: "",
      resultStyle: "",

      showWaitModal: false,
      modalContent: "Waiting for a few seconds...",
      submitDisable: true
    };
  },

  mounted: function() {
    // this.canvasWidth = document.body.clientWidth / 2;
    // this.canvasHeight = this.canvasWidth*(3/5);
    this.selectedId = 1;
    this.sessionId =
      "_" +
      Math.random()
        .toString(36)
        .substr(2, 9);
    axiosPix
      .get("/")
      .then(response => {
        console.log(response.data);
        return axiosStyle.get("/");
      })
      .then(response => {
        console.log(response.data);
      });
  },

  methods: {
    clearCanvas() {
      this.$refs.canvas.clearCanvas();
    },

    onSelectImage(id) {
      this.selectedId = id;
      this.submitDisable = false;
    },

    submitDrawing() {
      // Retreive canvas drawing
      var canvas = document.querySelector("#canvas");
      var context = canvas.getContext("2d");

      var w = canvas.width;
      var h = canvas.height;
      var compositeOperation = context.globalCompositeOperation;
      context.globalCompositeOperation = "destination-over";
      context.fillStyle = "white";
      context.fillRect(0, 0, w, h);

      var src = canvas.toDataURL("image/png");

      console.log("Got drawing");

      var container = this.$el.querySelector(".result-container");
      container.scrollIntoView({ behavior: "smooth" });
      // container.scrollTop = container.scrollHeight;

      // Build form data
      var pixData = new FormData();
      var styleData = new FormData();
      pixData.append("id", this.sessionId);
      pixData.append("image", src);
      styleData.append("id", this.sessionId);
      styleData.append("style", this.selectedId);
      styleData.append("highReality", this.highReality);
      styleData.append("highQuality", this.highQuality);

      // Display overlay
      this.modalContent = "Waiting for a few seconds...";
      this.showWaitModal = true;

      axiosPix({
        url: "/getPixFromData",
        method: "POST",
        data: pixData,
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
        .then(response => {
          // console.log(response.data)
          this.resultPix = response.data;
          this.resultSrc = this.resultPix;
          this.modalContent = "Styling the picture...";
          return axiosStyle({
            url: "/getStyleFromId",
            method: "POST",
            data: styleData,
            headers: {
              "Content-Type": "multipart/form-data"
            }
          });
        })
        .then(response => {
          this.showWaitModal = false;
          this.resultStyle = response.data;
          this.resultSrc = this.resultStyle;
        })
        .catch(function(response) {
          this.modalContent = "Ooops, something wrong...";
          setTimeout(function() {
            this.showWaitModal = false;
          }, 3000);
        });
    },

    toggleReality() {
      this.highReality = !this.highReality;
    },

    toggleQuality() {
      this.highQuality = !this.highQuality;
    },

    toggleResult() {
      this.showStyle = !this.showStyle;
      if (this.showStyle) {
        this.resultSrc = this.resultStyle;
      } else {
        this.resultSrc = this.resultPix;
      }
    },

    uploadToGallery() {
      this.$swal({
        text: "Save your work to public gallery?",
        buttons: true
      }).then(willUpload => {
        if (willUpload) {
          var uploadData = new FormData();
          uploadData.append("id", this.sessionId);
          // Display overlay
          this.modalContent = "Saving...";
          this.showWaitModal = true;

          axiosStyle({
            url: "/submitToGallery",
            method: "POST",
            data: uploadData,
            headers: {
              "Content-Type": "multipart/form-data"
            }
          })
            .then(response => {
              console.log(response.data);
              this.showWaitModal = false;
              this.$swal("Go to the gallery and check it out!", {
                icon: "success"
              });
            })
            .catch(function(response) {
              this.modalContent = "Ooops, something wrong...";
              setTimeout(function() {
                this.showWaitModal = false;
              }, 3000);
            });
        }
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.container {
  display: flex;
}

.section {
  margin: 1rem 2rem;
  flex-grow: 1;
  width: 35%;
}

.section .options .vue-js-switch {
  margin: 0.5rem;
}

.image-container .image-flex {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  max-width: 400px;
  margin: 0 auto;
}

.image-container .image-item {
  width: 100px;
  height: 100px;
  margin: 5px;
  padding: 2px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.055);
  transition: all 0.2s ease-in-out;
}

.image-container .image-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  overflow: hidden;
}

img.selected {
  box-sizing: border-box;
  border: 4px solid #0088cc;
}

.result-container {
  min-width: 200px;
  min-height: 200px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #ffffff;
  padding: 0.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.result-container img {
  border: 1px solid #eee;
  border-radius: 0.2rem;
  width: 100%;
  height: 100%;
  object-fit: cover;
  overflow: hidden;
}

.hint {
  font-weight: 200;
  font-size: 1rem;
  color: #95a5a6;
}

.overlay {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  color: #bdc3c7;
}

.overlay .content {
  margin: 1rem;
}

@media only screen and (max-width: 800px) {
  .container {
    flex-direction: column;
  }

  .section {
    margin: 0;
    width: 100%;
  }

  .canvas-wrapper {
    max-height: 500px;
  }
}

.canvas-wrapper {
  max-height: 400px;
  height: auto;
  padding: 10px;
}

.btn {
  background-color: #008cba;
  border: none;
  border-radius: 0.3em;
  color: white;
  padding: 0.5em 1em;
  margin: 0.5em;
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

.btn:hover {
  background: #34495e;
}

.btn.disabled,
.btn[disabled],
fieldset[disabled] .btn {
  pointer-events: none;
  cursor: not-allowed;
  box-shadow: none;
  opacity: 0.5;
}

input[type="file"] {
  display: none;
}

.upload-label {
  display: inline-block;
  border: none;
  border-radius: 0.3em;
  padding: 0.5em 1em;
  background: #008cba;
  color: white;
  font-size: 1em;
  font-weight: 400;
  font-family: inherit;
  text-align: center;
  text-decoration: none;
  transition: all 0.4s;
  cursor: pointer;
}

.upload-label:hover {
  background: #34495e;
}

.upload-label .upload {
  background: url("../assets/icons/upload.svg") no-repeat top left;
  background-size: contain;
  cursor: pointer;
  display: inline-block;
  height: 1rem;
  width: 1rem;
}

span.clear {
  background: url("../assets/icons/eraser.svg") no-repeat top left;
  background-size: contain;
  cursor: pointer;
  display: inline-block;
  height: 1rem;
  width: 1rem;
}

span.submit {
  background: url("../assets/icons/palette.svg") no-repeat top left;
  background-size: contain;
  cursor: pointer;
  display: inline-block;
  height: 1rem;
  width: 1rem;
}

span.upload {
  background: url("../assets/icons/upload.svg") no-repeat top left;
  background-size: contain;
  cursor: pointer;
  display: inline-block;
  height: 1rem;
  width: 1rem;
}

.half-circle-spinner,
.half-circle-spinner * {
  box-sizing: border-box;
}

.half-circle-spinner {
  width: 4rem;
  height: 4rem;
  border-radius: 100%;
  position: relative;
}

.half-circle-spinner .circle {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 100%;
  border: calc(60px / 10) solid transparent;
}

.half-circle-spinner .circle.circle-1 {
  border-top-color: #bdc3c7;
  animation: half-circle-spinner-animation 1s infinite;
}

.half-circle-spinner .circle.circle-2 {
  border-bottom-color: #bdc3c7;
  animation: half-circle-spinner-animation 1s infinite alternate;
}

@keyframes half-circle-spinner-animation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
