import type { iconType } from "./types";
import { type Component, defineComponent, h } from "vue";
import { FontIcon, IconifyIconOffline, IconifyIconOnline } from "../index";
import Iconify from "@iconify/iconify";
import { iconToHTML } from "@iconify/utils";

/**
 * 支持 `iconfont`、自定义 `svg` 以及 `iconify` 中所有的图标
 * @see 点击查看文档图标篇 {@link https://pure-admin.github.io/pure-admin-doc/pages/icon/}
 * @param icon 必传 图标
 * @param attrs 可选 iconType 属性
 * @returns Component
 */
export function useRenderIcon(icon: any, attrs?: iconType): Component {
  // iconfont
  const ifReg = /^IF-/;
  // typeof icon === "function" 属于SVG
  if (ifReg.test(icon)) {
    // iconfont
    const name = icon.split(ifReg)[1];
    const iconName = name.slice(
      0,
      name.indexOf(" ") == -1 ? name.length : name.indexOf(" ")
    );
    const iconType = name.slice(name.indexOf(" ") + 1, name.length);
    return defineComponent({
      name: "FontIcon",
      render() {
        return h(FontIcon, {
          icon: iconName,
          iconType,
          ...attrs
        });
      }
    });
  } else if (typeof icon === "function" || typeof icon?.render === "function") {
    // svg
    return attrs ? h(icon, { ...attrs }) : icon;
  } else if (typeof icon === "object") {
    return defineComponent({
      name: "OfflineIcon",
      render() {
        return h(IconifyIconOffline, {
          icon: icon,
          ...attrs
        });
      }
    });
  } else {
    // 通过是否存在 : 符号来判断是在线还是本地图标，存在即是在线图标，反之
    return defineComponent({
      name: "Icon",
      render() {
        const IconifyIcon =
          icon && icon.includes(":") ? IconifyIconOnline : IconifyIconOffline;
        return h(IconifyIcon, {
          icon: icon,
          ...attrs
        });
      }
    });
  }
}

export function useDomIcon(icon: any, attrs?: any) {
  const node = document.createElement("div");
  node.style.marginLeft = "10px";
  let iconBody = null;
  attrs = attrs || {
    rotate: 0,
    height: 24,
    width: 24
  };
  if (typeof icon === "string" && Iconify.iconExists(icon)) {
    iconBody = Iconify.renderSVG(icon, attrs);
  } else {
    const svg = iconToHTML(icon.body, attrs);
    const domParser = document.createElement("div");
    domParser.innerHTML = svg;
    iconBody = domParser.childNodes[0];
  }
  node.appendChild(iconBody);
  return node;
}
