export default class DrawUI {
  ctx;

  constructor(ctx) {
    this.ctx = ctx;
  }
  rect({ x = 0, y = 0, w = 0, h = 0, color = "#ddd", children }) {
    if (color) {
      this.ctx.setFillStyle(color);
      this.ctx.fillRect(x, y, w, h);
    }
    this.renderChildren(children, { x, y, w, h });
  }
  renderChildren(children, { x, y, w, h }) {
    if (children)
      for (let i = 0; i < children.length; i++) {
        let child = children[i];
        child(x, y, w, h);
      }
  }
  image({ x = 0, y = 0, w = 0, h = 0, url = "" }) {
    console.log({ x, y, w, h, url });
    this.ctx.drawImage(url, x, y, w, h);
  }

  clipArc({ x, y, radius, children }) {
    this.ctx.save();
    this.ctx.beginPath();
    this.ctx.arc(x, y, radius, 0, 2 * Math.PI, false);
    this.ctx.clip();
    // clip
    this.renderChildren(children, {
      x: x - radius,
      y: y - radius,
      w: radius * 2,
      h: radius * 2,
    });
    this.ctx.closePath();
    this.ctx.restore();
  }

  clipRect({ x, y, w, h, children }) {
    this.ctx.save();
    this.ctx.beginPath();
    this.ctx.rect(x, y, w, h);
    this.ctx.clip();
    this.renderChildren(children, { x, y, w, h });
    this.ctx.closePath();
    this.ctx.restore();
  }

  arc({ x = 0, y = 0, radius = 0, color = "#ddd" }) {
    this.ctx.save();
    this.ctx.setFillStyle(color);
    this.ctx.beginPath();
    this.ctx.arc(x, y, radius, 0, 2 * Math.PI);
    this.ctx.fill();
    this.ctx.closePath();
    this.ctx.restore();
  }

  /**
   * 
   * @param {*} param  : {
    align?: "left" | "center" | "right",
    baseline?: "top" | "bottom" | "middle" | "normal",
    fontSize?: number,
    color: string,
    text: string,
    x: number,
    y: number,
    fontWeight?: "normal",
    maxWidth: number,
    maxLength: number,
  }
   */
  text(param) {
    param.text = param.text.substring(0, param.maxLength || 4);
    this.ctx.setTextAlign(param.align || "left");
    this.ctx.setTextBaseline(param.baseline || "top");
    this.ctx.setFontSize(param.fontSize || 12);
    this.ctx.setFillStyle(param.color);
    this.ctx.font = `normal ${param.fontWeight} ${param.fontSize}px PingFangSC`;
    this.ctx.fillText(param.text, param.x, param.y, param.maxWidth);
  }
}
