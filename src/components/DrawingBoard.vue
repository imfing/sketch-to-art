<template>
  <canvas id="canvas"
          v-on:mousedown="handleMouseDown"
          v-on:mouseup="handleMouseUp"
          v-on:mousemove="handleMouseMove"
          v-on:touchstart="handleTouchStart"
          v-on:touchend="handleTouchEnd"
          v-on:touchmove="handleTouchMove"
          :width="this.width"
          :height="this.height"></canvas>
</template>

<script>
export default {
  props: ['enabled'],

  data: function() {
    return {
      mouse: {
        current: {
          x: 0,
          y: 0
        },
        previous: {
          x: 0,
          y: 0
        },
        down: false
      },
      width: "",
      height: "",
      lineColor: "#000000",
      lineWidth: 2
    };
  },

  computed: {
    currentMouse: function() {
      var c = document.getElementById("canvas");
      var rect = c.getBoundingClientRect();

      return {
        x: this.mouse.current.x - rect.left,
        y: this.mouse.current.y - rect.top
      };
    }
  },

  methods: {
    draw: function(event) {
      if (this.mouse.down && this.enabled) {
        var c = document.getElementById("canvas");
        var ctx = c.getContext("2d");
        ctx.clearRect(0, 0, this.width, this.height);
        ctx.lineCap = "round";
        ctx.lineTo(this.currentMouse.x, this.currentMouse.y);
        ctx.strokeStyle = this.lineColor;
        ctx.lineWidth = this.lineWidth;
        ctx.stroke();
      }
    },

    handleMouseDown: function(event) {
      this.mouse.down = true;
      this.mouse.current = {
        x: event.pageX,
        y: event.pageY
      };

      var c = document.getElementById("canvas");
      var ctx = c.getContext("2d");

      ctx.moveTo(this.currentMouse.x, this.currentMouse.y);
    },
    handleMouseUp: function() {
      this.mouse.down = false;
    },
    handleMouseMove: function(event) {
      this.mouse.current = {
        x: event.pageX,
        y: event.pageY
      };

      this.draw(event);
    },

    handleTouchStart: function(event) {
      event.preventDefault();

      var c = document.getElementById("canvas");
      var ctx = c.getContext("2d");
      var touch = event.touches[0];

      this.mouse.down = true;
      this.mouse.current = {
        x: touch.clientX,
        y: touch.clientY
      };
      ctx.moveTo(this.currentMouse.x, this.currentMouse.y);
    },
    handleTouchMove: function(event) {
      event.preventDefault();
      var touch = event.touches[0];
      this.mouse.current = {
        x: touch.clientX,
        y: touch.clientY
      };

      this.draw(event);
    },
    handleTouchEnd: function(event) {
      event.preventDefault();
      this.mouse.down = false;
    },

    clearCanvas: function() {
      var c = document.getElementById("canvas");
      c.width = c.width;
    }
  },

  ready: function() {
    var c = document.getElementById("canvas");
    var ctx = c.getContext("2d");
    ctx.translate(0.5, 0.5);
    ctx.imageSmoothingEnabled = false;
  },

  mounted: function() {
    this.width = this.$el.clientWidth;
    // this.height = this.$el.clientHeight;
    this.height = this.width;
  }
};
</script>

<style scoped>
canvas {
  background: white;
  box-shadow: 0px 2px 3px rgba(0, 0, 0, 0.2);
  cursor: crosshair;
  max-width: 400px;
  width: 100%;
}
</style>