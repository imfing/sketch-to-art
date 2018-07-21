<template>
  <div id="wrapper">
    <h1>
      Sketch to Art
    </h1>
    <div class="container">
      <div class="section">
        <h3>Start drawing</h3>
        <div class="canvas-wrapper">
          <drawing-board ref="canvas"
                         :enabled="!userContent"></drawing-board>
        </div>
        <form id="upload-file"
              method="post"
              enctype="multipart/form-data">
          <label for="imageUpload"
                 class="upload-label">
            Choose...
          </label>
          <input type="file"
                 name="file"
                 @change="contentUpload"
                 id="imageUpload"
                 accept=".png, .jpg, .jpeg">
        </form>
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
                          @clicked="onSelectStyle"></image-item>
            </div>
          </div>
        </div>
        <div class="style-hint">
          Choose a style or
          <form id="upload-style"
                method="post"
                enctype="multipart/form-data">
            <label for="styleUpload"
                   class="upload-label">
              upload yours
            </label>
            <input type="file"
                   name="file"
                   @change="styleUpload"
                   id="styleUpload"
                   accept=".png, .jpg, .jpeg">
          </form>
        </div>

        <div v-if="userStyle"
             class="upload-style">
          <div class="remove"
               @click="removeUserStyle">Remove</div>
          <img :src="userStyleSrc"
               alt="">
        </div>

        <div class="options">
          <toggle-button :value="highReality"
                         :color="{checked: '#cb8589', unchecked: '#0984e3'}"
                         :sync="true"
                         :labels="{checked: 'More Real', unchecked: 'More Style'}"
                         :width="80"
                         :height="20"
                         @change="toggleReality" />
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

        <button v-if="showToggle"
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

      userContent: false,
      userStyle: false,
      userStyleSrc: "",

      highReality: true,
      highQuality: false,

      showStyle: true,
      showToggle: false,
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

    let that = this;
    axiosPix
      .get("/")
      .catch(function(error) {
        that.$swal({
          title: "Something wrong...",
          text:
            "Server not responding, check your Internet connection first. You can view details in the About page. To experience the app, please contact the author for help.",
          icon: "warning",
          buttons: {
            cancel: "Got it"
          }
        });
        console.log("pix server error");
      })
      .then(response => {
        console.log(response.data);
        return axiosStyle.get("/");
      })
      .catch(function(error) {
        console.log("style server error");
      })
      .then(response => {
        console.log(response.data);
      });
  },

  methods: {
    clearCanvas() {
      this.$refs.canvas.clearCanvas();
      this.userContent = false;
    },

    onSelectStyle(id) {
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
      var container = this.$el.querySelector(".result-container");
      container.scrollIntoView({ behavior: "smooth" });

      // Build form data
      var pixData = new FormData();
      var styleData = new FormData();
      pixData.append("id", this.sessionId);
      pixData.append("image", src);

      styleData.append("id", this.sessionId);
      styleData.append("style", this.selectedId);
      styleData.append("highReality", this.highReality);
      styleData.append("highQuality", this.highQuality);
      styleData.append("userContent", this.userContent);
      styleData.append("userStyle", this.userStyle);
      styleData.append("contentData", src);
      styleData.append("styleData", this.userStyleSrc);

      // Use custom image
      if (this.userContent) {
        this.modalContent = "Stylizing your picture...";
        this.showWaitModal = true;

        axiosStyle({
          url: "/stylize-with-data",
          method: "POST",
          data: styleData,
          headers: {
            "Content-Type": "multipart/form-data"
          }
        }).then(response => {
          this.showWaitModal = false;
          this.resultStyle = response.data;
          this.resultSrc = this.resultStyle;
          this.showToggle = false;
        });
      } else {
        // Use sketch
        this.modalContent = "Waiting for a few seconds...";
        this.showWaitModal = true;

        axiosPix({
          url: "/pix-translate-data",
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
              url: "/stylize-with-data",
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
            this.showToggle = true;
          });
      }
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
            url: "/submit-to-gallery",
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
    },

    contentUpload(e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;

      var reader = new FileReader();

      reader.onload = e => {
        var canvas = document.querySelector("#canvas");
        var ctx = canvas.getContext("2d");

        var w = canvas.width;
        var h = canvas.height;
        ctx.clearRect(0, 0, w, h);

        var img = new Image();
        img.onload = function() {
          ctx.drawImage(img, 0, 0, w, h);
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(files[0]);
      e.target.value = "";
      this.userContent = true;
    },

    styleUpload(e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;

      var reader = new FileReader();
      var vm = this;

      reader.onload = e => {
        var canvas = document.createElement("canvas");
        var ctx = canvas.getContext("2d");
        var imgSize = 256;
        var image = new Image();

        canvas.width = imgSize;
        canvas.height = imgSize;

        var imgData;

        image.onload = function() {
          ctx.drawImage(image, 0, 0, imgSize, imgSize);
          let imgData = canvas.toDataURL("image/png");
          vm.setUserStyleSrc(imgData);
        };
        image.src = e.target.result;
      };
      reader.readAsDataURL(files[0]);
      e.target.value = "";
    },

    setUserStyleSrc(data) {
      this.userStyleSrc = data;
      this.userStyle = true;
      this.submitDisable = false;

      var submit = this.$el.querySelector(".submit");
      submit.scrollIntoView({ behavior: "smooth" });
    },

    removeUserStyle() {
      this.userStyle = false;
      this.userStyleSrc = "";
      this.submitDisable = true;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#wrapper h1 {
  margin: 1rem 0rem;
}

#wrapper h3 {
  margin-top: 0.2rem;
  margin-bottom: 0.8rem;
}

.container {
  display: flex;
}

.section {
  margin: 0.5rem 1rem;
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
  width: 25%;
  margin: 3px;
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

.style-hint form {
  display: inline;
}

.style-hint {
  font-weight: 200;
  font-size: 0.8rem;
  color: #95a5a6;
}

.style-hint .upload-label {
  text-decoration: underline;
}

.upload-label {
  cursor: pointer;
  font-weight: 200;
  font-size: 0.8rem;
  color: #95a5a6;
}

.upload-style img {
  width: 120px;
  height: 120px;
  margin: 0.2rem;
  padding: 2px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.055);
  transition: all 0.2s ease-in-out;
}

.upload-style .remove {
  cursor: pointer;
  font-weight: 200;
  font-size: 0.8rem;
  color: #95a5a6;
  text-decoration: underline;
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
