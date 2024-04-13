<template>
  <view>
    <canvas
      id="myCanvas"
      :style="{
        width: width + 'px',
        height: height + 'px',
      }"
      @touchmove="drawMove"
      @touchstart="drawStart"
      canvas-id="myCanvas"
    ></canvas>
  </view>
</template>

<script>
/**
 * 部署 web 版本，给 app 引用，nvue 不支持 canvas
 */

// get window width
const windowWidth = uni.getSystemInfoSync().windowWidth;
// get window height
const windowHeight = uni.getSystemInfoSync().windowHeight;

export default {
  data() {
    return {
      width: windowWidth,
      height: windowHeight,
      lastMove: 0,
      lastOffset: 0,
    };
  },
  onReady() {
    console.log("onLoad");
    this.draw();
  },
  methods: {
    drawMove(e) {
      let offset = e.touches[0].x - this.lastMove;
      this.draw(offset, e.touches[0]);
    },
    drawStart(e) {
      this.draw(null, e.touches[0]);
    },
    draw(chartOffset = 0, point = 0) {
      let data = [
        {
          value: 20,
          color: "#FF0000",
          label: "0",
        },
        // 100 万
        {
          value: 100,
          color: "#FF0000",
          label: "100万",
        },
        // 200 万
        {
          value: 200,
          color: "#FF0000",
          label: "200万",
        },
        // 300 万
        {
          value: 30,
          color: "#FF0000",
          label: "300万",
        },
        // 400 万
        {
          value: 40,
          color: "#FF0000",
          label: "400万",
        },
        // 500 万
        {
          value: 100,
          color: "#FF0000",
          label: "500万",
        },
      ];

      let max = Math.max(...data.map((item) => item.value));
      let unit = 150;
      max = Math.ceil(max / unit) * unit;
      data = data.map((item) => {
        item.scale = item.value / max;
        return item;
      });

      let gap = max / 5;

      let yLabels = Array.from({ length: 6 }, (v, i) => i * gap);
      const padding = 40;

      let rect = {
        x: padding,
        y: padding,
        width: this.width - padding * 2,
        height: this.height - padding,
        bottom: this.height - padding,
        right: this.width - 20,
        left: padding,
        top: 20,
      };

      let itemHeight = rect.height / yLabels.length;
      let itemWidth = rect.width / data.length;

      const dataForEach = (callback) => {
        data.forEach((item, index) => {
          let x = index * itemWidth + rect.left + itemWidth / 2 + 10;
          let y = 300 - item.value;
          let isOnPoint = false;
          if (point) {
            isOnPoint = point.x > x - 10 && point.x < x + 10;
          }
          callback({
            item,
            index,
            x,
            y,
            isOnPoint,
          });
        });
      };

      const ctx = uni.createCanvasContext("myCanvas", this);
      ctx.clearRect(0, 0, this.width, this.height);

      // draw y labels
      yLabels.forEach((item, index) => {
        ctx.setFillStyle("#ffffff");
        ctx.fillText(item, 10, rect.bottom - index * itemHeight);
      });

      // draw y axis

      for (let i = 0; i < yLabels.length; i++) {
        ctx.beginPath();
        ctx.setStrokeStyle("#20222F");
        ctx.moveTo(padding, rect.bottom - i * itemHeight);
        ctx.lineTo(rect.right, rect.bottom - i * itemHeight);
        ctx.stroke();
      }

      // draw y start line
      ctx.beginPath();
      ctx.setStrokeStyle("#5E616D");
      ctx.moveTo(padding, rect.top);
      ctx.lineTo(padding, rect.bottom);
      ctx.stroke();

      // draw x start line
      ctx.beginPath();
      ctx.setStrokeStyle("#5E616D");
      ctx.moveTo(padding, rect.bottom);
      ctx.lineTo(rect.right, rect.bottom);
      ctx.stroke();

      // draw data labels
      dataForEach(({ item, index, x, y, isOnPoint }) => {
        ctx.setFillStyle("#fff");
        // ctx.fillText(item.label, x, rect.bottom + 20);
        // rotate text 45 deg
        ctx.translate(x, rect.bottom + 30);
        ctx.rotate(-Math.PI / 4);
        ctx.fillText(item.label, 0, 0);
        ctx.rotate(Math.PI / 4);
        ctx.translate(-x, -rect.bottom - 30);
      });

      // draw data rect bar
      dataForEach(({ item, index, x, y, isOnPoint }) => {
        ctx.setFillStyle(item.color);
        // liner gradient bar
        const grd = ctx.createLinearGradient(
          x,
          rect.bottom,
          x,
          rect.bottom - item.scale * rect.height
        );
        grd.addColorStop(0, "#5525FF");
        grd.addColorStop(0.25, "#5525FF");
        grd.addColorStop(0.5, "#853EFF");
        grd.addColorStop(1, "#C25EFF");

        ctx.setFillStyle(grd);
        // rect with radius
        // ctx.fillRect(
        //   x - 10,
        //   rect.bottom - item.scale * rect.height,
        //   20,
        //   item.scale * rect.height
        // );
        this.drawRectWithRadius(
          ctx,
          x - 10,
          rect.bottom - item.scale * rect.height,
          20,
          item.scale * rect.height
        );
      });

      ctx.draw();
    },

    drawRectWithRadius(
      ctx,
      x,
      y,
      width,
      height,
      radius = {
        leftTop: 10,
        rightTop: 10,
        rightBottom: 0,
        leftBottom: 0,
      }
    ) {
      ctx.beginPath();
      ctx.moveTo(x + radius.leftTop, y);
      ctx.lineTo(x + width - radius.rightTop, y);
      ctx.arc(
        x + width - radius.rightTop,
        y + radius.rightTop,
        radius.rightTop,
        1.5 * Math.PI,
        2 * Math.PI
      );
      ctx.lineTo(x + width, y + height - radius.rightBottom);
      ctx.arc(
        x + width - radius.rightBottom,
        y + height - radius.rightBottom,
        radius.rightBottom,
        0,
        0.5 * Math.PI
      );
      ctx.lineTo(x + radius.leftBottom, y + height);
      ctx.arc(
        x + radius.leftBottom,
        y + height - radius.leftBottom,
        radius.leftBottom,
        0.5 * Math.PI,
        Math.PI
      );
      ctx.lineTo(x, y + radius.leftTop);
      ctx.arc(
        x + radius.leftTop,
        y + radius.leftTop,
        radius.leftTop,
        Math.PI,
        1.5 * Math.PI
      );
      ctx.closePath();
      ctx.fill();
    },
  },
};
</script>

<style lang="scss"></style>
