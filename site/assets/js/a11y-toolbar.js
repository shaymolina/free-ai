"use strict";(()=>{var Mt=[1,1.1,1.2,1.3,1.4,1.5,1.6],Et=[0,.05,.1,.15],Ct=[0,.1,.2,.3],Pt=[0,1.5,1.75,2],M=["highContrast","darkContrast","lightContrast","invertColors"],m=Object.freeze({textScale:1,readableFont:!1,letterSpacing:0,wordSpacing:0,lineHeight:0,pauseAnimations:!1,reduceMotion:!1,grayscale:!1,highContrast:!1,darkContrast:!1,lightContrast:!1,invertColors:!1,highlightLinks:!1,highlightHeadings:!1,readingGuide:!1,readingMask:!1,largeCursor:!1,focusHighlight:!1,hideImages:!1}),w=Object.keys(m),kt=["readableFont","pauseAnimations","reduceMotion","grayscale","highContrast","darkContrast","lightContrast","invertColors","highlightLinks","highlightHeadings","readingGuide","readingMask","largeCursor","focusHighlight","hideImages"],N={textScale:Mt,letterSpacing:Et,wordSpacing:Ct,lineHeight:Pt};function At(t){return M.includes(t)}function W(t,e){return typeof e=="number"&&N[t].includes(e)}function $(t){return typeof t=="object"&&t!==null&&!Array.isArray(t)}function R(t){if(!$(t))return m;let e={...m};for(let d of kt){let g=t[d];typeof g=="boolean"&&(e[d]=g)}let o=t.textScale;W("textScale",o)&&(e.textScale=o);let a=t.letterSpacing;W("letterSpacing",a)&&(e.letterSpacing=a);let r=t.wordSpacing;W("wordSpacing",r)&&(e.wordSpacing=r);let n=t.lineHeight;W("lineHeight",n)&&(e.lineHeight=n);let s=M.find(d=>e[d]);for(let d of M)e[d]=d===s;return Object.freeze(e)}function _(t){return M.find(e=>t[e])??null}function z(t,e){return w.every(o=>t[o]===e[o])}function me(t){return z(t,m)}function ve(t,e){return N[t].indexOf(e)}function Y(t,e,o){let a=N[t],r=Math.min(a.length-1,Math.max(0,ve(t,e)+o)),n=a[r];return n===void 0?e:n}var q=class{constructor(e=m,o=w){this.listeners=new Set;this.enabled=new Set(o),this.state=this.restrict(R(e))}get(){return this.state}isEnabled(e){return this.enabled.has(e)}subscribe(e){return this.listeners.add(e),()=>{this.listeners.delete(e)}}setPreference(e,o){if(!this.enabled.has(e))return;let a={[e]:o};if(At(e)&&o===!0)for(let r of M)r!==e&&(a[r]=!1);this.replace({...this.state,...a})}setContrastMode(e){let o={};for(let a of M)o[a]=a===e&&this.enabled.has(a);this.replace({...this.state,...o})}toggle(e){this.setPreference(e,!this.state[e])}step(e,o){switch(e){case"textScale":this.setPreference(e,Y(e,this.state.textScale,o));break;case"letterSpacing":this.setPreference(e,Y(e,this.state.letterSpacing,o));break;case"wordSpacing":this.setPreference(e,Y(e,this.state.wordSpacing,o));break;case"lineHeight":this.setPreference(e,Y(e,this.state.lineHeight,o));break}}reset(){this.replace(m)}replace(e){let o=this.restrict(R(e));if(z(o,this.state))return;let a=this.state;this.state=o;for(let r of[...this.listeners])try{r(o,a)}catch{}}restrict(e){if(this.enabled.size===w.length)return e;let o={...e};for(let a of w)this.enabled.has(a)||(o[a]=m[a]);return R(o)}};function X(t){return t||(typeof document>"u"?null:document)}function xe(t){return t?.defaultView??null}function Be(t,e){if(!t||typeof t.matchMedia!="function")return null;try{return t.matchMedia(e)}catch{return null}}function Ve(t,e){return t?typeof t.addEventListener=="function"?(t.addEventListener("change",e),()=>t.removeEventListener("change",e)):()=>{}:()=>{}}function je(t,e){return t&&typeof t.requestAnimationFrame=="function"?t.requestAnimationFrame(e):(e(),0)}function Ue(t,e){e&&t&&typeof t.cancelAnimationFrame=="function"&&t.cancelAnimationFrame(e)}function Q(){let t=typeof globalThis.crypto=="object"?globalThis.crypto:void 0;return t&&typeof t.randomUUID=="function"?t.randomUUID():`${Date.now().toString(36)}-${Math.random().toString(36).slice(2,10)}`}function Z(t){if(typeof t!="string")return!1;let e=t.trim();return/^#(?:[0-9a-f]{3,4}|[0-9a-f]{6}|[0-9a-f]{8})$/i.test(e)||/^(?:rgb|hsl)a?\(\s*[\d.%\s,/+-]+\)$/i.test(e)}function G(t,e,o,a){return typeof t!="number"||!Number.isFinite(t)?a:Math.min(o,Math.max(e,t))}function H(t){return t.body}function J(t){return t.head??t.documentElement}var Se="a11y-toolbar-preferences-v1",ae=1;function ee(t){if(t===null||t==="")return m;let e;try{e=JSON.parse(t)}catch{return m}if(!$(e))return m;let o=e.version;return o===ae?R(e.preferences):o===void 0?R(e):m}function Lt(t){return JSON.stringify({version:ae,preferences:t})}function Rt(t){if(!t)return null;try{let e=t.localStorage,o="__a11y-toolbar-probe__";return e.setItem(o,o),e.removeItem(o),e}catch{return null}}var te=class{constructor(e,o=Se){this.win=e;this.key=o;this.memory=null;this.storage=Rt(e)}get persistent(){return this.storage!==null}load(){if(!this.storage)return ee(this.memory);try{return ee(this.storage.getItem(this.key))}catch{return ee(this.memory)}}save(e){let o=Lt(e);if(this.memory=o,!!this.storage)try{this.storage.setItem(this.key,o)}catch{}}clear(){if(this.memory=null,!!this.storage)try{this.storage.removeItem(this.key)}catch{}}onExternalChange(e){let o=this.win;if(!o||!this.storage)return()=>{};let a=r=>{r.key!==this.key&&r.key!==null||e(r.key===null?m:ee(r.newValue))};return o.addEventListener("storage",a),()=>o.removeEventListener("storage",a)}};function Ht(t){return $(t)&&t.namespace==="a11y-toolbar"&&t.version===ae&&typeof t.source=="string"&&$(t.preferences)}var oe=class{constructor(e,o,a){this.win=e;this.storage=o;this.onRemote=a;this.source=Q();this.channel=null;this.stopStorage=()=>{}}get mode(){return this.channel?"broadcast":this.storage.persistent&&this.win?"storage":"none"}start(){let e=this.win?this.win.BroadcastChannel:void 0;if(typeof e=="function")try{let o=new e(`a11y-toolbar:${this.storage.key}`);o.onmessage=a=>{let r=a.data;!Ht(r)||r.source===this.source||this.onRemote(R(r.preferences))},this.channel=o;return}catch{this.channel=null}this.stopStorage=this.storage.onExternalChange(this.onRemote)}publish(e){if(!this.channel)return;let o={namespace:"a11y-toolbar",version:ae,source:this.source,preferences:e};try{this.channel.postMessage(o)}catch{}}stop(){this.channel&&(this.channel.onmessage=null,this.channel.close(),this.channel=null),this.stopStorage(),this.stopStorage=()=>{}}};var Nt="a11y-toolbar-reading-guide",It="a11y-toolbar-reading-mask-top",Kt="a11y-toolbar-reading-mask-bottom";function Te(t,e,o){let a=t.createElement("div");return a.id=e,a.className=o,a.setAttribute("aria-hidden","true"),a.setAttribute("data-a11y-toolbar-overlay",""),a}var re=class{constructor(e,o,a){this.doc=e;this.host=o;this.followFocus=a;this.y=null;this.frame=0;this.listening=!1;this.onPointer=e=>{e.clientY!==this.y&&(this.y=e.clientY,this.schedule())};this.onFocus=e=>{let o=e.target;if(!(o instanceof Element)||this.host.contains(o)||o.closest(".a11y-toolbar-root"))return;let a=o.getBoundingClientRect();this.focusRect=a,this.y=a.top+a.height/2,this.schedule()};this.focusRect=null;this.win=e.defaultView}schedule(){this.frame||(this.frame=je(this.win,()=>{this.frame=0,this.render()}))}listen(e){let o=this.win;!o||e===this.listening||(this.listening=e,e?(o.addEventListener("pointermove",this.onPointer,{passive:!0}),this.followFocus&&this.doc.addEventListener("focusin",this.onFocus)):(o.removeEventListener("pointermove",this.onPointer),this.doc.removeEventListener("focusin",this.onFocus),Ue(o,this.frame),this.frame=0))}viewportHeight(){return this.win?.innerHeight??0}},ne=class extends re{constructor(o,a,r){super(o,a,r.followFocus);this.options=r;this.el=null}update(o){if(o!==(this.el!==null))if(o){let a=Te(this.doc,Nt,"a11y-toolbar-reading-guide");a.style.setProperty("--a11y-toolbar-guide-color",this.options.color),a.style.setProperty("--a11y-toolbar-guide-thickness",`${this.options.thickness}px`),this.host.appendChild(a),this.el=a,this.y=this.y??this.viewportHeight()/2,this.render(),this.listen(!0)}else this.destroy()}render(){if(!this.el||this.y===null)return;let o=Math.round(this.y-this.options.thickness/2);this.el.style.transform=`translate3d(0, ${o}px, 0)`}destroy(){this.listen(!1),this.el?.remove(),this.el=null}},ie=class extends re{constructor(o,a,r){super(o,a,r.followFocus);this.options=r;this.top=null;this.bottom=null}update(o){if(o!==(this.top!==null))if(o){this.top=Te(this.doc,It,"a11y-toolbar-reading-mask a11y-toolbar-reading-mask-top"),this.bottom=Te(this.doc,Kt,"a11y-toolbar-reading-mask a11y-toolbar-reading-mask-bottom");for(let a of[this.top,this.bottom])a.style.setProperty("--a11y-toolbar-mask-opacity",String(this.options.opacity)),this.host.appendChild(a);this.y=this.y??this.viewportHeight()/2,this.render(),this.listen(!0)}else this.destroy()}render(){if(!this.top||!this.bottom||this.y===null)return;let o=this.viewportHeight(),a=this.focusRect?this.focusRect.height+16:0;this.focusRect=null;let r=Math.max(this.options.areaHeight,a)/2,n=Math.max(0,Math.round(this.y-r)),s=Math.min(o,Math.round(this.y+r));this.top.style.height=`${n}px`,this.bottom.style.top=`${s}px`}destroy(){this.listen(!1),this.top?.remove(),this.bottom?.remove(),this.top=null,this.bottom=null}};var we="a11y-toolbar-text-scale-styles",le="--a11y-toolbar-text-scale",We=[".a11y-toolbar-root",".a11y-toolbar-root *","[data-a11y-toolbar-overlay]","[data-a11y-toolbar-overlay] *","[data-a11y-toolbar-ignore-text-scale]","[data-a11y-toolbar-ignore-text-scale] *","svg","svg *","canvas","iframe","embed","object",".cm-editor",".cm-editor *",".CodeMirror",".CodeMirror *",".monaco-editor",".monaco-editor *"].join(", ");function Dt(t){let e=[],o=0,a=null,r="";for(let n of t){if(a)n===a&&(a=null);else if(n==='"'||n==="'")a=n;else if(n==="("||n==="[")o+=1;else if(n===")"||n==="]")o-=1;else if(n===","&&o===0){e.push(r.trim()),r="";continue}r+=n}return r.trim()&&e.push(r.trim()),e}function Ot(t){let e=/::?(?:before|after|first-line|first-letter|marker|placeholder|selection)\b.*$/i.exec(t);return e?`${t.slice(0,e.index)||"*"}:not(${We})${e[0]}`:`${t}:not(${We})`}function $t(t){let e=t.trim().toLowerCase();return!e||e.includes("rem")?!1:/\d(?:px|pt|vw|vh|vmin|vmax|cm|mm|in|pc)\b/.test(e)||e.startsWith("var(")}function _t(t){return"selectorText"in t&&"style"in t}function I(t,e){for(let o of Array.from(t)){if(_t(o)){let r=o.style.getPropertyValue("font-size");if(r&&$t(r)){let n=Dt(o.selectorText).map(Ot).join(", ");e.push(`${n}{font-size:calc(${r} * var(${le})) !important}`)}continue}if("media"in o&&"cssRules"in o&&!("styleSheet"in o)){let r=o,n=[];I(r.cssRules,n),n.length&&e.push(`@media ${r.media.mediaText}{${n.join("")}}`);continue}if("containerQuery"in o&&"conditionText"in o&&"cssRules"in o){let r=o,n=[];I(r.cssRules,n),n.length&&e.push(`@container ${r.containerName} ${r.containerQuery}{${n.join("")}}`);continue}if("conditionText"in o&&"cssRules"in o){let r=o,n=[];I(r.cssRules,n),n.length&&e.push(`@supports ${r.conditionText}{${n.join("")}}`);continue}if("styleSheet"in o){let r=o.styleSheet,n=r?Ye(r):null;n&&I(n,e);continue}let a=o;a.cssRules&&!("name"in o)&&I(a.cssRules,e)}}function Ye(t){try{return t.cssRules}catch{return null}}function zt(t){let e=[`html:not([data-a11y-toolbar-ignore-text-scale]){font-size:calc(100% * var(${le})) !important}`],o=new Set(Array.from(t.querySelectorAll('style[id^="a11y-toolbar"]')).map(a=>a.sheet));for(let a of Array.from(t.styleSheets)){if(o.has(a)||a.disabled)continue;let r=Ye(a);r&&I(r,e)}return e.join(`
`)}var se=class{constructor(e){this.doc=e;this.style=null;this.stopLoad=()=>{}}update(e){if(e===1){this.remove();return}if(!this.style){this.refresh();let o=this.doc.defaultView;if(o&&this.doc.readyState!=="complete"){let a=()=>this.refresh();o.addEventListener("load",a,{once:!0}),this.stopLoad=()=>o.removeEventListener("load",a)}}}refresh(){let e="";try{e=zt(this.doc)}catch{return}let o=this.doc.getElementById(we),a=o&&o.tagName==="STYLE"?o:this.doc.createElement("style");a.id=we,a.textContent=e,a.isConnected||J(this.doc).appendChild(a),this.style=a}remove(){this.stopLoad(),this.stopLoad=()=>{},this.style?.remove(),this.doc.getElementById(we)?.remove(),this.style=null}};var Gt="data-a11y-toolbar-",Ft="a11y-toolbar-grayscale-layer",Me="data-a11y-toolbar-backdrop",Bt="a11y-toolbar-overlays";function qe(t){return Gt+t.replace(/[A-Z]/g,e=>`-${e.toLowerCase()}`)}var Xe={textScale:le,letterSpacing:"--a11y-toolbar-letter-spacing",wordSpacing:"--a11y-toolbar-word-spacing",lineHeight:"--a11y-toolbar-line-height"};function Vt(t,e){return t==="letterSpacing"||t==="wordSpacing"?`${e}em`:String(e)}function jt(t,e){return typeof t=="boolean"?t:e==="textScale"?t!==1:t!==0}function Ut(t){let e=t?t.CSS:void 0;return!e||typeof e.supports!="function"?!1:e.supports("backdrop-filter","grayscale(1)")||e.supports("-webkit-backdrop-filter","grayscale(1)")}var ce=class{constructor(e,o){this.doc=e;this.options=o;this.guide=null;this.mask=null;this.overlayHost=null;this.grayscaleLayer=null;this.pending=null;this.onReady=()=>{let e=this.pending;this.pending=null,e&&this.apply(e)};this.root=e.documentElement,this.typography=new se(e),this.backdrop=Ut(e.defaultView)}host(){if(this.overlayHost?.isConnected)return this.overlayHost;let e=H(this.doc);if(!e)return null;let o=this.doc.createElement("div");return o.id=Bt,o.setAttribute("aria-hidden","true"),o.setAttribute("data-a11y-toolbar-overlay",""),o.style.zIndex=String(Math.max(0,this.options.zIndex-1)),e.appendChild(o),this.overlayHost=o,this.guide=new ne(this.doc,o,this.options.readingGuide),this.mask=new ie(this.doc,o,this.options.readingMask),o}dropHost(){this.guide?.destroy(),this.mask?.destroy(),this.guide=null,this.mask=null,this.overlayHost?.remove(),this.overlayHost=null}apply(e){for(let o of w)try{this.applyKey(o,e[o])}catch{}if(this.safely(()=>this.typography.update(e.textScale)),!H(this.doc)){this.pending||this.doc.addEventListener("DOMContentLoaded",this.onReady,{once:!0}),this.pending=e;return}this.safely(()=>this.updateGrayscale(e.grayscale)),this.safely(()=>{e.readingGuide||e.readingMask?(this.host(),this.guide?.update(e.readingGuide),this.mask?.update(e.readingMask)):this.dropHost()})}refreshTextScale(){this.safely(()=>this.typography.refresh())}clear(){for(let e of w){this.root.removeAttribute(qe(e));let o=Xe[e];o&&this.root.style.removeProperty(o)}this.root.removeAttribute(Me),this.root.getAttribute("style")===""&&this.root.removeAttribute("style"),this.typography.remove(),this.updateGrayscale(!1),this.dropHost(),this.doc.removeEventListener("DOMContentLoaded",this.onReady),this.pending=null}applyKey(e,o){let a=qe(e),r=Xe[e];jt(o,e)?(this.root.setAttribute(a,typeof o=="boolean"?"":String(o)),r&&typeof o=="number"&&this.root.style.setProperty(r,Vt(e,o))):(this.root.removeAttribute(a),r&&this.root.style.removeProperty(r)),this.root.getAttribute("style")===""&&this.root.removeAttribute("style")}updateGrayscale(e){if(!e||!this.backdrop){this.grayscaleLayer?.remove(),this.grayscaleLayer=null,this.root.removeAttribute(Me);return}if(this.root.setAttribute(Me,""),this.grayscaleLayer)return;let o=this.doc.createElement("div");o.id=Ft,o.setAttribute("aria-hidden","true"),o.setAttribute("data-a11y-toolbar-overlay",""),o.style.zIndex=String(Math.max(0,this.options.zIndex-1)),(H(this.doc)??this.root).appendChild(o),this.grayscaleLayer=o}safely(e){try{e()}catch{}}};var Ee="a11y-toolbar-runtime-styles",F="a11yToolbarRefs";function Qe(t,e){let o=!1,a=t.getElementById(Ee);try{if(!a||a.tagName!=="STYLE"){let r=t.createElement("style");r.id=Ee,r.textContent=e,J(t).appendChild(r),a=r}a.dataset[F]=String(Number(a.dataset[F]??"0")+1)}catch{a=null}return()=>{if(o||!a)return;o=!0;let r=Number(a.dataset[F]??"1")-1;r<=0?a.remove():a.dataset[F]=String(r)}}function Ze(t){let e=t.getElementById(Ee);return e?Number(e.dataset[F]??"0"):0}var Je=`
.a11y-toolbar-root {
  --a11y-toolbar-primary: #0b7fb3;
  --a11y-toolbar-primary-hover: color-mix(in srgb, var(--a11y-toolbar-primary) 84%, #000);
  --a11y-toolbar-primary-foreground: #fff;
  --a11y-toolbar-background: #fff;
  --a11y-toolbar-surface: #f4f7f9;
  --a11y-toolbar-foreground: #14202b;
  --a11y-toolbar-muted: #4a5864;
  --a11y-toolbar-border: #c9d3db;
  --a11y-toolbar-active-bg: #e3f1f8;
  --a11y-toolbar-active-fg: #085e85;
  --a11y-toolbar-focus: #0b7fb3;
  --a11y-toolbar-focus-inner: #fff;
  --a11y-toolbar-shadow: 0 18px 48px rgba(9, 30, 45, 0.22), 0 2px 8px rgba(9, 30, 45, 0.12);
  --a11y-toolbar-radius: 16px;
  --a11y-toolbar-radius-sm: 10px;
  --a11y-toolbar-gap: 16px;
  --a11y-toolbar-btn: 48px;
  --a11y-toolbar-font: system-ui, -apple-system, "Segoe UI", Arial, "Noto Sans Hebrew", sans-serif;
  position: fixed;
  inset: 0;
  z-index: var(--a11y-toolbar-z, 95);
  pointer-events: none;
  font-family: var(--a11y-toolbar-font);
  font-size: 15px;
  line-height: 1.45;
  letter-spacing: normal;
  word-spacing: normal;
  color: var(--a11y-toolbar-foreground);
  text-align: start;
  -webkit-text-size-adjust: 100%;
}
.a11y-toolbar-root[data-a11y-toolbar-theme="dark"] {
  --a11y-toolbar-background: #141b22;
  --a11y-toolbar-surface: #1d2731;
  --a11y-toolbar-foreground: #eef3f6;
  --a11y-toolbar-muted: #b4c1cb;
  --a11y-toolbar-border: #3b4a57;
  --a11y-toolbar-active-bg: #0f3a50;
  --a11y-toolbar-active-fg: #bfe6f8;
  --a11y-toolbar-focus: #6cc4ec;
  --a11y-toolbar-focus-inner: #141b22;
  --a11y-toolbar-shadow: 0 18px 48px rgba(0, 0, 0, 0.55);
}
@media (prefers-color-scheme: dark) {
  .a11y-toolbar-root[data-a11y-toolbar-theme="system"] {
    --a11y-toolbar-background: #141b22;
    --a11y-toolbar-surface: #1d2731;
    --a11y-toolbar-foreground: #eef3f6;
    --a11y-toolbar-muted: #b4c1cb;
    --a11y-toolbar-border: #3b4a57;
    --a11y-toolbar-active-bg: #0f3a50;
    --a11y-toolbar-active-fg: #bfe6f8;
    --a11y-toolbar-focus: #6cc4ec;
    --a11y-toolbar-focus-inner: #141b22;
    --a11y-toolbar-shadow: 0 18px 48px rgba(0, 0, 0, 0.55);
  }
}
@media (min-width: 768px) {
  .a11y-toolbar-root { --a11y-toolbar-btn: 56px; }
}
.a11y-toolbar-root *,
.a11y-toolbar-root *::before,
.a11y-toolbar-root *::after {
  box-sizing: border-box;
  font-family: inherit;
  letter-spacing: inherit;
  word-spacing: inherit;
  text-transform: none;
}
.a11y-toolbar-root :is(button, input, h2, h3, p, fieldset, legend, label) {
  margin: 0;
  font-size: inherit;
  line-height: inherit;
  color: inherit;
  text-shadow: none;
}
.a11y-toolbar-root button {
  -webkit-appearance: none;
  appearance: none;
  font: inherit;
  cursor: pointer;
  touch-action: manipulation;
  min-width: 0;
  text-decoration: none;
}
.a11y-toolbar-root :focus { outline: none; }
.a11y-toolbar-root :focus-visible {
  outline: 3px solid var(--a11y-toolbar-focus);
  outline-offset: 2px;
  box-shadow: 0 0 0 2px var(--a11y-toolbar-focus-inner);
}
.a11y-toolbar-root .a11y-toolbar-icon {
  width: 20px;
  height: 20px;
  flex: none;
  display: block;
}
.a11y-toolbar-root .a11y-toolbar-trigger {
  position: fixed;
  pointer-events: auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: var(--a11y-toolbar-btn);
  height: var(--a11y-toolbar-btn);
  padding: 0;
  border: 0;
  border-radius: 9999px;
  background: var(--a11y-toolbar-primary);
  color: var(--a11y-toolbar-primary-foreground);
  box-shadow: 0 10px 15px -3px color-mix(in srgb, var(--a11y-toolbar-primary) 30%, transparent), 0 4px 6px -4px color-mix(in srgb, var(--a11y-toolbar-primary) 30%, transparent);
  transition: transform 200ms ease, background-color 200ms ease;
}
.a11y-toolbar-root .a11y-toolbar-trigger:hover {
  transform: scale(1.05);
  background: var(--a11y-toolbar-primary-hover);
}
.a11y-toolbar-root .a11y-toolbar-trigger:focus-visible {
  outline: 3px solid var(--a11y-toolbar-primary);
  outline-offset: 2px;
  box-shadow: 0 0 0 2px #fff;
}
.a11y-toolbar-root .a11y-toolbar-trigger-icon {
  width: 24px;
  height: 24px;
  display: block;
}
@media (min-width: 768px) {
  .a11y-toolbar-root .a11y-toolbar-trigger-icon { width: 28px; height: 28px; }
}
.a11y-toolbar-root[data-a11y-toolbar-position^="bottom"] .a11y-toolbar-trigger { bottom: calc(16px + env(safe-area-inset-bottom, 0px)); }
.a11y-toolbar-root[data-a11y-toolbar-position^="top"] .a11y-toolbar-trigger { top: calc(16px + env(safe-area-inset-top, 0px)); }
.a11y-toolbar-root[data-a11y-toolbar-position$="right"] .a11y-toolbar-trigger { right: calc(16px + env(safe-area-inset-right, 0px)); }
.a11y-toolbar-root[data-a11y-toolbar-position$="left"] .a11y-toolbar-trigger { left: calc(16px + env(safe-area-inset-left, 0px)); }
.a11y-toolbar-root .a11y-toolbar-panel {
  --a11y-toolbar-offset: calc(16px + var(--a11y-toolbar-btn) + 12px);
  position: fixed;
  pointer-events: auto;
  display: flex;
  flex-direction: column;
  width: min(392px, calc(100vw - 24px));
  max-height: calc(100vh - var(--a11y-toolbar-offset) - 16px);
  max-height: calc(100dvh - var(--a11y-toolbar-offset) - 16px - env(safe-area-inset-top, 0px) - env(safe-area-inset-bottom, 0px));
  background: var(--a11y-toolbar-background);
  color: var(--a11y-toolbar-foreground);
  border: 1px solid var(--a11y-toolbar-border);
  border-radius: var(--a11y-toolbar-radius);
  box-shadow: var(--a11y-toolbar-shadow);
  overflow: hidden;
  animation: a11y-toolbar-in 180ms ease-out;
}
.a11y-toolbar-root .a11y-toolbar-panel[hidden] { display: none; }
.a11y-toolbar-root[data-a11y-toolbar-position^="bottom"] .a11y-toolbar-panel { bottom: calc(var(--a11y-toolbar-offset) + env(safe-area-inset-bottom, 0px)); transform-origin: bottom; }
.a11y-toolbar-root[data-a11y-toolbar-position^="top"] .a11y-toolbar-panel { top: calc(var(--a11y-toolbar-offset) + env(safe-area-inset-top, 0px)); transform-origin: top; }
.a11y-toolbar-root[data-a11y-toolbar-position$="right"] .a11y-toolbar-panel { right: calc(12px + env(safe-area-inset-right, 0px)); }
.a11y-toolbar-root[data-a11y-toolbar-position$="left"] .a11y-toolbar-panel { left: calc(12px + env(safe-area-inset-left, 0px)); }
@media (min-width: 768px) {
  .a11y-toolbar-root[data-a11y-toolbar-position$="right"] .a11y-toolbar-panel { right: calc(16px + env(safe-area-inset-right, 0px)); }
  .a11y-toolbar-root[data-a11y-toolbar-position$="left"] .a11y-toolbar-panel { left: calc(16px + env(safe-area-inset-left, 0px)); }
}
.a11y-toolbar-root[data-a11y-toolbar-layout="sheet"] .a11y-toolbar-panel {
  top: auto;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  max-height: 88vh;
  max-height: calc(88dvh - env(safe-area-inset-top, 0px));
  border-radius: var(--a11y-toolbar-radius) var(--a11y-toolbar-radius) 0 0;
  border-bottom: 0;
  padding-bottom: env(safe-area-inset-bottom, 0px);
  animation-name: a11y-toolbar-sheet-in;
}
@keyframes a11y-toolbar-in {
  from { opacity: 0; transform: translateY(8px) scale(0.98); }
  to { opacity: 1; transform: none; }
}
@keyframes a11y-toolbar-sheet-in {
  from { transform: translateY(24px); opacity: 0; }
  to { transform: none; opacity: 1; }
}
.a11y-toolbar-root .a11y-toolbar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 14px 10px 18px;
  padding-inline: 18px 12px;
  border-bottom: 1px solid var(--a11y-toolbar-border);
  flex: none;
}
.a11y-toolbar-root .a11y-toolbar-heading { display: flex; align-items: center; gap: 10px; min-width: 0; }
.a11y-toolbar-root .a11y-toolbar-heading-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 9999px;
  background: var(--a11y-toolbar-primary);
  color: #fff;
  flex: none;
}
.a11y-toolbar-root .a11y-toolbar-title {
  font-size: 19px;
  font-weight: 700;
  line-height: 1.25;
  color: var(--a11y-toolbar-foreground);
  border-radius: 4px;
}
.a11y-toolbar-root .a11y-toolbar-title:focus-visible { outline-offset: 4px; }
.a11y-toolbar-root .a11y-toolbar-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  flex: none;
  padding: 0;
  border: 1px solid transparent;
  border-radius: var(--a11y-toolbar-radius-sm);
  background: transparent;
  color: var(--a11y-toolbar-foreground);
}
.a11y-toolbar-root .a11y-toolbar-close:hover { background: var(--a11y-toolbar-surface); border-color: var(--a11y-toolbar-border); }
.a11y-toolbar-root .a11y-toolbar-description {
  padding: 10px 18px 0;
  font-size: 14px;
  color: var(--a11y-toolbar-muted);
  flex: none;
}
.a11y-toolbar-root .a11y-toolbar-body {
  flex: 1 1 auto;
  min-height: 0;
  overflow-y: auto;
  overscroll-behavior: contain;
  padding: 6px 18px 12px;
}
.a11y-toolbar-root .a11y-toolbar-section { padding: 12px 0; }
.a11y-toolbar-root .a11y-toolbar-section + .a11y-toolbar-section { border-top: 1px solid var(--a11y-toolbar-border); }
.a11y-toolbar-root .a11y-toolbar-section-title {
  margin: 0 0 10px;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.3;
  color: var(--a11y-toolbar-muted);
}
.a11y-toolbar-root .a11y-toolbar-section-body { display: flex; flex-direction: column; gap: 8px; }
.a11y-toolbar-root .a11y-toolbar-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 150px), 1fr));
  gap: 8px;
}
.a11y-toolbar-root .a11y-toolbar-toggle {
  position: relative;
  display: grid;
  grid-template-columns: auto 1fr;
  grid-template-rows: auto auto;
  column-gap: 10px;
  row-gap: 2px;
  align-items: center;
  min-height: 60px;
  width: 100%;
  padding: 10px 12px;
  text-align: start;
  border: 2px solid var(--a11y-toolbar-border);
  border-radius: var(--a11y-toolbar-radius-sm);
  background: var(--a11y-toolbar-background);
  color: var(--a11y-toolbar-foreground);
  transition: border-color 150ms ease, background-color 150ms ease;
}
.a11y-toolbar-root .a11y-toolbar-toggle > .a11y-toolbar-icon { grid-row: 1 / span 2; color: var(--a11y-toolbar-primary); }
.a11y-toolbar-root .a11y-toolbar-toggle:hover { border-color: var(--a11y-toolbar-primary); }
.a11y-toolbar-root .a11y-toolbar-toggle-label { font-size: 15px; font-weight: 600; line-height: 1.25; overflow-wrap: anywhere; }
.a11y-toolbar-root .a11y-toolbar-toggle-state {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  font-weight: 500;
  color: var(--a11y-toolbar-muted);
}
.a11y-toolbar-root .a11y-toolbar-check { width: 14px; height: 14px; display: none; }
.a11y-toolbar-root .a11y-toolbar-toggle[aria-pressed="true"] {
  border-color: var(--a11y-toolbar-primary);
  background: var(--a11y-toolbar-active-bg);
  color: var(--a11y-toolbar-active-fg);
}
.a11y-toolbar-root .a11y-toolbar-toggle[aria-pressed="true"] .a11y-toolbar-toggle-state { color: var(--a11y-toolbar-active-fg); font-weight: 700; }
.a11y-toolbar-root .a11y-toolbar-toggle[aria-pressed="true"] .a11y-toolbar-check { display: block; }
.a11y-toolbar-root .a11y-toolbar-stepper {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 8px 12px;
  padding: 8px 10px;
  padding-inline-start: 12px;
  border: 2px solid var(--a11y-toolbar-border);
  border-radius: var(--a11y-toolbar-radius-sm);
  background: var(--a11y-toolbar-background);
}
.a11y-toolbar-root .a11y-toolbar-stepper[data-a11y-toolbar-changed] { border-color: var(--a11y-toolbar-primary); background: var(--a11y-toolbar-active-bg); }
.a11y-toolbar-root .a11y-toolbar-stepper-label { display: inline-flex; align-items: center; gap: 10px; font-weight: 600; }
.a11y-toolbar-root .a11y-toolbar-stepper-label .a11y-toolbar-icon { color: var(--a11y-toolbar-primary); }
.a11y-toolbar-root .a11y-toolbar-stepper-controls { display: inline-flex; align-items: center; gap: 6px; margin-inline-start: auto; }
.a11y-toolbar-root .a11y-toolbar-step-button,
.a11y-toolbar-root .a11y-toolbar-step-reset {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 44px;
  height: 44px;
  padding: 0 10px;
  border: 1px solid var(--a11y-toolbar-border);
  border-radius: var(--a11y-toolbar-radius-sm);
  background: var(--a11y-toolbar-surface);
  color: var(--a11y-toolbar-foreground);
  font-size: 14px;
  font-weight: 600;
}
.a11y-toolbar-root .a11y-toolbar-step-button:hover,
.a11y-toolbar-root .a11y-toolbar-step-reset:hover { border-color: var(--a11y-toolbar-primary); }
.a11y-toolbar-root :is(.a11y-toolbar-step-button, .a11y-toolbar-step-reset)[aria-disabled="true"] {
  opacity: 0.45;
  cursor: not-allowed;
}
.a11y-toolbar-root .a11y-toolbar-step-value {
  min-width: 56px;
  text-align: center;
  font-size: 15px;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
}
.a11y-toolbar-root .a11y-toolbar-radios { border: 0; padding: 0; min-width: 0; }
.a11y-toolbar-root .a11y-toolbar-radios-legend { padding: 0; margin-bottom: 8px; font-weight: 600; font-size: 15px; }
.a11y-toolbar-root .a11y-toolbar-radios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 150px), 1fr));
  gap: 8px;
}
.a11y-toolbar-root .a11y-toolbar-radio {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 48px;
  padding: 8px 12px;
  border: 2px solid var(--a11y-toolbar-border);
  border-radius: var(--a11y-toolbar-radius-sm);
  background: var(--a11y-toolbar-background);
  cursor: pointer;
  font-weight: 600;
  line-height: 1.25;
}
.a11y-toolbar-root .a11y-toolbar-radio:hover { border-color: var(--a11y-toolbar-primary); }
.a11y-toolbar-root .a11y-toolbar-radio-input {
  position: absolute;
  opacity: 0;
  width: 1px;
  height: 1px;
  margin: 0;
  pointer-events: none;
}
.a11y-toolbar-root .a11y-toolbar-radio-mark {
  width: 20px;
  height: 20px;
  flex: none;
  border: 2px solid var(--a11y-toolbar-muted);
  border-radius: 9999px;
  background: var(--a11y-toolbar-background);
}
.a11y-toolbar-root .a11y-toolbar-radio:has(.a11y-toolbar-radio-input:checked) {
  border-color: var(--a11y-toolbar-primary);
  background: var(--a11y-toolbar-active-bg);
  color: var(--a11y-toolbar-active-fg);
}
.a11y-toolbar-root .a11y-toolbar-radio-input:checked + .a11y-toolbar-radio-mark {
  border-color: var(--a11y-toolbar-primary);
  box-shadow: inset 0 0 0 4px var(--a11y-toolbar-background);
  background: var(--a11y-toolbar-primary);
}
.a11y-toolbar-root .a11y-toolbar-radio:has(.a11y-toolbar-radio-input:focus-visible) {
  outline: 3px solid var(--a11y-toolbar-focus);
  outline-offset: 2px;
}
.a11y-toolbar-root .a11y-toolbar-footer {
  flex: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px 18px 14px;
  border-top: 1px solid var(--a11y-toolbar-border);
  background: var(--a11y-toolbar-background);
}
.a11y-toolbar-root .a11y-toolbar-reset {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  min-height: 48px;
  padding: 10px 16px;
  border: 2px solid var(--a11y-toolbar-primary);
  border-radius: var(--a11y-toolbar-radius-sm);
  background: var(--a11y-toolbar-background);
  color: var(--a11y-toolbar-active-fg);
  font-weight: 700;
}
.a11y-toolbar-root .a11y-toolbar-reset:hover { background: var(--a11y-toolbar-active-bg); }
.a11y-toolbar-root .a11y-toolbar-disclaimer { font-size: 13px; color: var(--a11y-toolbar-muted); text-align: center; }
.a11y-toolbar-root .a11y-toolbar-sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}
@media (prefers-reduced-motion: reduce) {
  .a11y-toolbar-root *,
  .a11y-toolbar-root *::before,
  .a11y-toolbar-root *::after { animation: none !important; transition: none !important; }
  .a11y-toolbar-root .a11y-toolbar-trigger:hover { transform: none; }
}
html:is([data-a11y-toolbar-reduce-motion], [data-a11y-toolbar-pause-animations]) .a11y-toolbar-root *,
html:is([data-a11y-toolbar-reduce-motion], [data-a11y-toolbar-pause-animations]) .a11y-toolbar-root *::before,
html:is([data-a11y-toolbar-reduce-motion], [data-a11y-toolbar-pause-animations]) .a11y-toolbar-root *::after {
  animation: none !important;
  transition: none !important;
}
html:is([data-a11y-toolbar-reduce-motion], [data-a11y-toolbar-pause-animations]) .a11y-toolbar-root .a11y-toolbar-trigger:hover { transform: none; }
@media (forced-colors: active) {
  .a11y-toolbar-root .a11y-toolbar-trigger { border: 2px solid ButtonText; }
  .a11y-toolbar-root .a11y-toolbar-toggle[aria-pressed="true"],
  .a11y-toolbar-root .a11y-toolbar-radio:has(.a11y-toolbar-radio-input:checked) { outline: 3px solid Highlight; }
}
@media print {
  .a11y-toolbar-root, #a11y-toolbar-overlays, #a11y-toolbar-grayscale-layer { display: none !important; }
}
`;var et=`
html[data-a11y-toolbar-readable-font] body :not(.a11y-toolbar-root, .a11y-toolbar-root *, [data-a11y-toolbar-overlay], [data-a11y-toolbar-overlay] *, svg, svg *, i, code, pre, kbd, samp, pre *, code *, [class^="icon-"], [class*=" icon-"], [class*="fa-"], .fa, .material-icons, .material-symbols-outlined, .material-symbols-rounded) {
  font-family: Arial, Helvetica, Verdana, system-ui, sans-serif !important;
}
html[data-a11y-toolbar-letter-spacing] body :not(.a11y-toolbar-root, .a11y-toolbar-root *, [data-a11y-toolbar-overlay], svg, svg *, i, [class^="icon-"], [class*=" icon-"], [class*="fa-"], .material-icons, .material-symbols-outlined) {
  letter-spacing: var(--a11y-toolbar-letter-spacing) !important;
}
html[data-a11y-toolbar-word-spacing] body :not(.a11y-toolbar-root, .a11y-toolbar-root *, [data-a11y-toolbar-overlay], svg, svg *, i, [class^="icon-"], [class*=" icon-"], [class*="fa-"], .material-icons, .material-symbols-outlined) {
  word-spacing: var(--a11y-toolbar-word-spacing) !important;
}
html[data-a11y-toolbar-line-height] body :is(p, li, dd, dt, blockquote, figcaption, caption, td, th, h1, h2, h3, h4, h5, h6, label, summary, address, article, main, section):not(.a11y-toolbar-root, .a11y-toolbar-root *) {
  line-height: var(--a11y-toolbar-line-height) !important;
}
html[data-a11y-toolbar-reduce-motion] :not(.a11y-toolbar-root, .a11y-toolbar-root *, [data-a11y-toolbar-essential-animation], [data-a11y-toolbar-essential-animation] *),
html[data-a11y-toolbar-reduce-motion] :not(.a11y-toolbar-root *, [data-a11y-toolbar-essential-animation] *)::before,
html[data-a11y-toolbar-reduce-motion] :not(.a11y-toolbar-root *, [data-a11y-toolbar-essential-animation] *)::after {
  animation-duration: 0.01ms !important;
  animation-delay: 0s !important;
  animation-iteration-count: 1 !important;
  transition-duration: 0.01ms !important;
  transition-delay: 0s !important;
  scroll-behavior: auto !important;
}
html[data-a11y-toolbar-pause-animations] :not(.a11y-toolbar-root, .a11y-toolbar-root *, [data-a11y-toolbar-essential-animation], [data-a11y-toolbar-essential-animation] *),
html[data-a11y-toolbar-pause-animations] :not(.a11y-toolbar-root *, [data-a11y-toolbar-essential-animation] *)::before,
html[data-a11y-toolbar-pause-animations] :not(.a11y-toolbar-root *, [data-a11y-toolbar-essential-animation] *)::after {
  animation-play-state: paused !important;
  transition-duration: 0.01ms !important;
  transition-delay: 0s !important;
  scroll-behavior: auto !important;
}
html[data-a11y-toolbar-pause-animations],
html[data-a11y-toolbar-reduce-motion] { scroll-behavior: auto !important; }
#a11y-toolbar-grayscale-layer {
  position: fixed;
  inset: 0;
  pointer-events: none;
  -webkit-backdrop-filter: grayscale(1);
  backdrop-filter: grayscale(1);
}
html[data-a11y-toolbar-grayscale]:not([data-a11y-toolbar-backdrop]) body > :not(.a11y-toolbar-root, [data-a11y-toolbar-overlay]) {
  filter: grayscale(1);
}
html[data-a11y-toolbar-invert-colors] {
  filter: invert(1) hue-rotate(180deg);
  background-color: #fff;
}
html[data-a11y-toolbar-invert-colors] :is(img, picture, video, canvas, iframe, embed, object, svg image, [style*="background-image"]):not(picture img),
html[data-a11y-toolbar-invert-colors] .a11y-toolbar-root,
html[data-a11y-toolbar-invert-colors] #a11y-toolbar-overlays {
  filter: invert(1) hue-rotate(180deg);
}
html[data-a11y-toolbar-high-contrast],
html[data-a11y-toolbar-dark-contrast],
html[data-a11y-toolbar-light-contrast] {
  --a11y-toolbar-c-bg: #000;
  --a11y-toolbar-c-fg: #fff;
  --a11y-toolbar-c-link: #ffeb3b;
  --a11y-toolbar-c-border: #fff;
  --a11y-toolbar-c-field: #000;
  --a11y-toolbar-c-focus: #ffeb3b;
}
html[data-a11y-toolbar-dark-contrast] {
  --a11y-toolbar-c-bg: #121212;
  --a11y-toolbar-c-fg: #f2f2f2;
  --a11y-toolbar-c-link: #8cc8ff;
  --a11y-toolbar-c-border: #9a9a9a;
  --a11y-toolbar-c-field: #1e1e1e;
  --a11y-toolbar-c-focus: #8cc8ff;
}
html[data-a11y-toolbar-light-contrast] {
  --a11y-toolbar-c-bg: #fff;
  --a11y-toolbar-c-fg: #000;
  --a11y-toolbar-c-link: #0033aa;
  --a11y-toolbar-c-border: #000;
  --a11y-toolbar-c-field: #fff;
  --a11y-toolbar-c-focus: #0033aa;
}
html:is([data-a11y-toolbar-high-contrast], [data-a11y-toolbar-dark-contrast], [data-a11y-toolbar-light-contrast]),
html:is([data-a11y-toolbar-high-contrast], [data-a11y-toolbar-dark-contrast], [data-a11y-toolbar-light-contrast]) body {
  background-color: var(--a11y-toolbar-c-bg) !important;
  color: var(--a11y-toolbar-c-fg) !important;
}
html:is([data-a11y-toolbar-high-contrast], [data-a11y-toolbar-dark-contrast], [data-a11y-toolbar-light-contrast]) body :not(.a11y-toolbar-root, .a11y-toolbar-root *, [data-a11y-toolbar-overlay], [data-a11y-toolbar-overlay] *, img, picture, video, canvas, iframe, embed, object, svg, svg *) {
  background-color: var(--a11y-toolbar-c-bg) !important;
  color: var(--a11y-toolbar-c-fg) !important;
  border-color: var(--a11y-toolbar-c-border) !important;
  text-shadow: none !important;
  box-shadow: none !important;
  -webkit-text-fill-color: currentColor !important;
}
html:is([data-a11y-toolbar-high-contrast], [data-a11y-toolbar-dark-contrast], [data-a11y-toolbar-light-contrast]) body :is(a[href], a[href] *):not(.a11y-toolbar-root *) {
  color: var(--a11y-toolbar-c-link) !important;
  text-decoration: underline !important;
}
html:is([data-a11y-toolbar-high-contrast], [data-a11y-toolbar-dark-contrast], [data-a11y-toolbar-light-contrast]) body :is(button, input, select, textarea, [role="button"]):not(.a11y-toolbar-root *) {
  background-color: var(--a11y-toolbar-c-field) !important;
  border: 1px solid var(--a11y-toolbar-c-border) !important;
}
html:is([data-a11y-toolbar-high-contrast], [data-a11y-toolbar-dark-contrast], [data-a11y-toolbar-light-contrast]) body :focus-visible:not(.a11y-toolbar-root *) {
  outline: 3px solid var(--a11y-toolbar-c-focus) !important;
  outline-offset: 2px !important;
}
html:is([data-a11y-toolbar-high-contrast], [data-a11y-toolbar-dark-contrast], [data-a11y-toolbar-light-contrast]) body svg:not(.a11y-toolbar-root *) {
  color: var(--a11y-toolbar-c-fg) !important;
}
html:is([data-a11y-toolbar-high-contrast], [data-a11y-toolbar-dark-contrast], [data-a11y-toolbar-light-contrast]) body ::placeholder {
  color: var(--a11y-toolbar-c-fg) !important;
  opacity: 0.8 !important;
}
html[data-a11y-toolbar-highlight-links] body a[href]:not(.a11y-toolbar-root *) {
  text-decoration-line: underline !important;
  text-decoration-thickness: 3px !important;
  text-underline-offset: 4px !important;
  text-decoration-skip-ink: auto;
  background-color: rgba(11, 127, 179, 0.14) !important;
  border-radius: 2px;
}
html[data-a11y-toolbar-highlight-headings] body :is(h1, h2, h3, h4, h5, h6, [role="heading"]):not(.a11y-toolbar-root *) {
  outline: 2px dashed #0b7fb3 !important;
  outline-offset: 4px !important;
  background-color: rgba(11, 127, 179, 0.08) !important;
  border-radius: 2px;
}
html[data-a11y-toolbar-large-cursor],
html[data-a11y-toolbar-large-cursor] body :not(input, textarea, select, [contenteditable=""], [contenteditable="true"], [contenteditable="plaintext-only"], [contenteditable="true"] *, a[href], a[href] *, button, button *, [role="button"], [role="button"] *, label, summary, .a11y-toolbar-root *) {
  cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='48' height='48' viewBox='0 0 48 48'%3E%3Cpath d='M6 3l30 15-13 3.5-6.5 12z' fill='%23000' stroke='%23fff' stroke-width='3' stroke-linejoin='round'/%3E%3C/svg%3E") 6 3, auto !important;
}
html[data-a11y-toolbar-large-cursor] body :is(a[href], a[href] *, button, button *, [role="button"], [role="button"] *, label, summary, select):not([disabled]) {
  cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='48' height='48' viewBox='0 0 48 48'%3E%3Cpath d='M17 22V8a3.5 3.5 0 0 1 7 0v12l2-.5a3.5 3.5 0 0 1 4 2l.5.3a3.5 3.5 0 0 1 4.5 2.2 3.5 3.5 0 0 1 4.5 3V36c0 5-4 9-9 9h-5c-3 0-5.5-1.5-7-4l-7-10a3.4 3.4 0 0 1 5.5-4z' fill='%23000' stroke='%23fff' stroke-width='2.5' stroke-linejoin='round'/%3E%3C/svg%3E") 18 4, pointer !important;
}
html[data-a11y-toolbar-focus-highlight] body :focus-visible:not(.a11y-toolbar-root *) {
  outline: 3px solid #0b7fb3 !important;
  outline-offset: 3px !important;
  box-shadow: 0 0 0 6px #fff, 0 0 0 9px #111 !important;
}
html[data-a11y-toolbar-hide-images] body :is(img, picture, svg[role="img"], [role="img"]:not(svg *)):not(.a11y-toolbar-root *, button *, a *, label *, form *, [role="button"] *, [data-a11y-toolbar-essential-image], [data-a11y-toolbar-essential-image] *, [class*="captcha" i] *, [id*="captcha" i] *, [class*="payment" i] *, [class*="stripe" i] *, [class*="paypal" i] *, .leaflet-container *, .gm-style *, [class*="mapbox" i] *) {
  visibility: hidden !important;
}
#a11y-toolbar-overlays {
  position: fixed;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}
.a11y-toolbar-reading-guide {
  position: absolute;
  inset-inline: 0;
  top: 0;
  height: var(--a11y-toolbar-guide-thickness, 4px);
  background: var(--a11y-toolbar-guide-color, #0b7fb3);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.9), 0 2px 8px rgba(0, 0, 0, 0.35);
  pointer-events: none;
  will-change: transform;
}
.a11y-toolbar-reading-mask {
  position: absolute;
  inset-inline: 0;
  background: rgba(0, 0, 0, var(--a11y-toolbar-mask-opacity, 0.55));
  pointer-events: none;
}
.a11y-toolbar-reading-mask-top { top: 0; height: 0; }
.a11y-toolbar-reading-mask-bottom { top: 100%; bottom: 0; }
`;var qt=`${et}
${Je}`,Xt="a11y-toolbar:preferences-change",Qt=95;function Zt(t){return{color:Z(t?.color)?t.color:"#0B7FB3",thickness:G(t?.thickness,2,16,4),followFocus:t?.followFocus??!0}}function Jt(t){return{opacity:G(t?.opacity,.2,.85,.55),areaHeight:G(t?.areaHeight,40,400,120),followFocus:t?.followFocus??!0}}function eo(t){return typeof t=="string"&&/^[\w:.-]{1,100}$/.test(t)?t:Se}var de=class{constructor(e={},o={}){this.releaseStyles=()=>{};this.unsubscribe=()=>{};this.remoteUpdate=!1;this.destroyed=!1;this.doc=X(e.document);let a=xe(this.doc);this.storage=new te(a,eo(e.storageKey));let r=e.enabledFeatures?.filter(s=>w.includes(s))??w;this.manager=new q(this.storage.load(),r),this.sync=new oe(a,this.storage,s=>{this.remoteUpdate=!0;try{this.manager.replace(s)}finally{this.remoteUpdate=!1}});let n=Math.round(G(o.zIndex,0,2e6,Qt));this.engine=this.doc?new ce(this.doc,{zIndex:n,readingGuide:Zt(e.readingGuideOptions),readingMask:Jt(e.readingMaskOptions)}):null,!(!this.doc||!this.engine)&&(this.releaseStyles=Qe(this.doc,qt),this.engine.apply(this.manager.get()),this.unsubscribe=this.manager.subscribe((s,d)=>{this.engine?.apply(s),this.remoteUpdate||(me(s)?this.storage.clear():this.storage.save(s),this.sync.publish(s)),e.onPreferenceChange?.(s,d),this.dispatch({preferences:s,previous:d})}),this.sync.start())}get isBrowser(){return this.doc!==null}get syncMode(){return this.sync.mode}get storageKey(){return this.storage.key}getPreferences(){return this.manager.get()}isEnabled(e){return this.manager.isEnabled(e)}subscribe(e){return this.manager.subscribe(e)}setPreference(e,o){this.manager.setPreference(e,o)}toggle(e){this.manager.toggle(e)}step(e,o){this.manager.step(e,o)}setContrastMode(e){this.manager.setContrastMode(e)}reset(){let e=me(this.manager.get());this.manager.reset(),e&&(this.storage.clear(),this.sync.publish(m))}refresh(){this.engine?.refreshTextScale()}destroy(){this.destroyed||(this.destroyed=!0,this.unsubscribe(),this.sync.stop(),this.doc&&(this.releaseStyles(),Ze(this.doc)===0&&this.engine?.clear()))}dispatch(e){let o=xe(this.doc);if(!(!o||typeof o.CustomEvent!="function"))try{o.dispatchEvent(new o.CustomEvent(Xt,{detail:e}))}catch{}}};var tt={accessibilityOptions:"Accessibility options",panelTitle:"Accessibility menu",panelDescription:"Adjust the display to suit you. Settings are saved in this browser.",close:"Close accessibility menu",active:"On",inactive:"Off",on:"On",off:"Off",normal:"Normal",percent:"percent",sectionText:"Text",sectionColor:"Color and contrast",sectionMotion:"Motion",sectionReading:"Reading and navigation",contrastGroup:"Contrast mode",contrastNone:"No change",textScale:"Text size",increaseText:"Increase text",decreaseText:"Decrease text",resetText:"Normal text size",readableFont:"Readable font",letterSpacing:"Letter spacing",increaseLetterSpacing:"Increase letter spacing",decreaseLetterSpacing:"Decrease letter spacing",wordSpacing:"Word spacing",increaseWordSpacing:"Increase word spacing",decreaseWordSpacing:"Decrease word spacing",lineHeight:"Line height",increaseLineHeight:"Increase line height",decreaseLineHeight:"Decrease line height",pauseAnimations:"Pause animations",reduceMotion:"Reduce motion",grayscale:"Grayscale",highContrast:"High contrast",darkContrast:"Dark contrast",lightContrast:"Light contrast",invertColors:"Invert colors",highlightLinks:"Highlight links",highlightHeadings:"Highlight headings",readingGuide:"Reading guide",readingMask:"Reading mask",largeCursor:"Large cursor",focusHighlight:"Focus highlight",hideImages:"Hide images",resetAll:"Reset all settings",resetDone:"Settings have been reset",announceEnabled:"{label}: on",announceDisabled:"{label}: off",announceTextIncreased:"Text size increased to {value} percent",announceTextDecreased:"Text size decreased to {value} percent",announceTextReset:"Text size reset to 100 percent",announceValueChanged:"{label}: {value}",announceContrastOff:"Contrast mode: no change",disclaimer:"This tool only changes how the site looks for you. It does not change the site itself."};var ot={accessibilityOptions:"\u05D0\u05E4\u05E9\u05E8\u05D5\u05D9\u05D5\u05EA \u05E0\u05D2\u05D9\u05E9\u05D5\u05EA",panelTitle:"\u05EA\u05E4\u05E8\u05D9\u05D8 \u05E0\u05D2\u05D9\u05E9\u05D5\u05EA",panelDescription:"\u05DB\u05D0\u05DF \u05D0\u05E4\u05E9\u05E8 \u05DC\u05D4\u05EA\u05D0\u05D9\u05DD \u05D0\u05EA \u05D4\u05EA\u05E6\u05D5\u05D2\u05D4 \u05DC\u05E0\u05D5\u05D7\u05D5\u05EA \u05E9\u05DC\u05DA. \u05D4\u05D4\u05D2\u05D3\u05E8\u05D5\u05EA \u05E0\u05E9\u05DE\u05E8\u05D5\u05EA \u05D1\u05D3\u05E4\u05D3\u05E4\u05DF \u05D4\u05D6\u05D4.",close:"\u05E1\u05D2\u05D9\u05E8\u05EA \u05EA\u05E4\u05E8\u05D9\u05D8 \u05D4\u05E0\u05D2\u05D9\u05E9\u05D5\u05EA",active:"\u05E4\u05E2\u05D9\u05DC",inactive:"\u05DC\u05D0 \u05E4\u05E2\u05D9\u05DC",on:"\u05E4\u05E2\u05D9\u05DC",off:"\u05DC\u05D0 \u05E4\u05E2\u05D9\u05DC",normal:"\u05E8\u05D2\u05D9\u05DC",percent:"\u05D0\u05D7\u05D5\u05D6\u05D9\u05DD",sectionText:"\u05D8\u05E7\u05E1\u05D8",sectionColor:"\u05E6\u05D1\u05E2 \u05D5\u05E0\u05D9\u05D2\u05D5\u05D3\u05D9\u05D5\u05EA",sectionMotion:"\u05EA\u05E0\u05D5\u05E2\u05D4",sectionReading:"\u05E7\u05E8\u05D9\u05D0\u05D4 \u05D5\u05E0\u05D9\u05D5\u05D5\u05D8",contrastGroup:"\u05DE\u05E6\u05D1 \u05E0\u05D9\u05D2\u05D5\u05D3\u05D9\u05D5\u05EA",contrastNone:"\u05DC\u05DC\u05D0 \u05E9\u05D9\u05E0\u05D5\u05D9",textScale:"\u05D2\u05D5\u05D3\u05DC \u05D8\u05E7\u05E1\u05D8",increaseText:"\u05D4\u05D2\u05D3\u05DC\u05EA \u05D8\u05E7\u05E1\u05D8",decreaseText:"\u05D4\u05E7\u05D8\u05E0\u05EA \u05D8\u05E7\u05E1\u05D8",resetText:"\u05D2\u05D5\u05D3\u05DC \u05D8\u05E7\u05E1\u05D8 \u05E8\u05D2\u05D9\u05DC",readableFont:"\u05D2\u05D5\u05E4\u05DF \u05E7\u05E8\u05D9\u05D0",letterSpacing:"\u05E8\u05D9\u05D5\u05D5\u05D7 \u05D0\u05D5\u05EA\u05D9\u05D5\u05EA",increaseLetterSpacing:"\u05D4\u05D2\u05D3\u05DC\u05EA \u05E8\u05D9\u05D5\u05D5\u05D7 \u05D0\u05D5\u05EA\u05D9\u05D5\u05EA",decreaseLetterSpacing:"\u05D4\u05E7\u05D8\u05E0\u05EA \u05E8\u05D9\u05D5\u05D5\u05D7 \u05D0\u05D5\u05EA\u05D9\u05D5\u05EA",wordSpacing:"\u05E8\u05D9\u05D5\u05D5\u05D7 \u05DE\u05D9\u05DC\u05D9\u05DD",increaseWordSpacing:"\u05D4\u05D2\u05D3\u05DC\u05EA \u05E8\u05D9\u05D5\u05D5\u05D7 \u05DE\u05D9\u05DC\u05D9\u05DD",decreaseWordSpacing:"\u05D4\u05E7\u05D8\u05E0\u05EA \u05E8\u05D9\u05D5\u05D5\u05D7 \u05DE\u05D9\u05DC\u05D9\u05DD",lineHeight:"\u05D2\u05D5\u05D1\u05D4 \u05E9\u05D5\u05E8\u05D4",increaseLineHeight:"\u05D4\u05D2\u05D3\u05DC\u05EA \u05D2\u05D5\u05D1\u05D4 \u05E9\u05D5\u05E8\u05D4",decreaseLineHeight:"\u05D4\u05E7\u05D8\u05E0\u05EA \u05D2\u05D5\u05D1\u05D4 \u05E9\u05D5\u05E8\u05D4",pauseAnimations:"\u05E2\u05E6\u05D9\u05E8\u05EA \u05D0\u05E0\u05D9\u05DE\u05E6\u05D9\u05D5\u05EA",reduceMotion:"\u05D4\u05E4\u05D7\u05EA\u05EA \u05EA\u05E0\u05D5\u05E2\u05D4",grayscale:"\u05D2\u05D5\u05D5\u05E0\u05D9 \u05D0\u05E4\u05D5\u05E8",highContrast:"\u05E0\u05D9\u05D2\u05D5\u05D3\u05D9\u05D5\u05EA \u05D2\u05D1\u05D5\u05D4\u05D4",darkContrast:"\u05E0\u05D9\u05D2\u05D5\u05D3\u05D9\u05D5\u05EA \u05DB\u05D4\u05D4",lightContrast:"\u05E0\u05D9\u05D2\u05D5\u05D3\u05D9\u05D5\u05EA \u05D1\u05D4\u05D9\u05E8\u05D4",invertColors:"\u05D4\u05D9\u05E4\u05D5\u05DA \u05E6\u05D1\u05E2\u05D9\u05DD",highlightLinks:"\u05D4\u05D3\u05D2\u05E9\u05EA \u05E7\u05D9\u05E9\u05D5\u05E8\u05D9\u05DD",highlightHeadings:"\u05D4\u05D3\u05D2\u05E9\u05EA \u05DB\u05D5\u05EA\u05E8\u05D5\u05EA",readingGuide:"\u05E1\u05E8\u05D2\u05DC \u05E7\u05E8\u05D9\u05D0\u05D4",readingMask:"\u05DE\u05E1\u05DB\u05EA \u05E7\u05E8\u05D9\u05D0\u05D4",largeCursor:"\u05E1\u05DE\u05DF \u05E2\u05DB\u05D1\u05E8 \u05D2\u05D3\u05D5\u05DC",focusHighlight:"\u05D4\u05D3\u05D2\u05E9\u05EA \u05DE\u05D9\u05E7\u05D5\u05D3",hideImages:"\u05D4\u05E1\u05EA\u05E8\u05EA \u05EA\u05DE\u05D5\u05E0\u05D5\u05EA",resetAll:"\u05D0\u05D9\u05E4\u05D5\u05E1 \u05DB\u05DC \u05D4\u05D4\u05D2\u05D3\u05E8\u05D5\u05EA",resetDone:"\u05D4\u05D4\u05D2\u05D3\u05E8\u05D5\u05EA \u05D0\u05D5\u05E4\u05E1\u05D5",announceEnabled:"{label}: \u05E4\u05E2\u05D9\u05DC",announceDisabled:"{label}: \u05DC\u05D0 \u05E4\u05E2\u05D9\u05DC",announceTextIncreased:"\u05D2\u05D5\u05D3\u05DC \u05D4\u05D8\u05E7\u05E1\u05D8 \u05D4\u05D5\u05D2\u05D3\u05DC \u05DC\u05BE{value} \u05D0\u05D7\u05D5\u05D6\u05D9\u05DD",announceTextDecreased:"\u05D2\u05D5\u05D3\u05DC \u05D4\u05D8\u05E7\u05E1\u05D8 \u05D4\u05D5\u05E7\u05D8\u05DF \u05DC\u05BE{value} \u05D0\u05D7\u05D5\u05D6\u05D9\u05DD",announceTextReset:"\u05D2\u05D5\u05D3\u05DC \u05D4\u05D8\u05E7\u05E1\u05D8 \u05D7\u05D6\u05E8 \u05DC\u05BE100 \u05D0\u05D7\u05D5\u05D6\u05D9\u05DD",announceValueChanged:"{label}: {value}",announceContrastOff:"\u05DE\u05E6\u05D1 \u05E0\u05D9\u05D2\u05D5\u05D3\u05D9\u05D5\u05EA: \u05DC\u05DC\u05D0 \u05E9\u05D9\u05E0\u05D5\u05D9",disclaimer:"\u05D4\u05DB\u05DC\u05D9 \u05DE\u05E9\u05E0\u05D4 \u05E8\u05E7 \u05D0\u05EA \u05D4\u05EA\u05E6\u05D5\u05D2\u05D4 \u05D0\u05E6\u05DC\u05DA. \u05D4\u05D5\u05D0 \u05DC\u05D0 \u05DE\u05E9\u05E0\u05D4 \u05D0\u05EA \u05D4\u05D0\u05EA\u05E8 \u05E2\u05E6\u05DE\u05D5."};var to={he:ot,en:tt};function at(t="he",e={}){let o=to[t],a={...o};for(let r of Object.keys(o)){let n=e[r];typeof n=="string"&&n.trim()!==""&&(a[r]=n)}return a}function B(t,e){return t.replace(/\{(\w+)\}/g,(o,a)=>e[a]??o)}function be(t){return t==="he"||t==="en"}function c(t,e,o={},a=[]){let r=t.createElement(e);if(o.className&&(r.className=o.className),o.id&&(r.id=o.id),o.text!==void 0&&(r.textContent=o.text),o.attrs)for(let[n,s]of Object.entries(o.attrs))r.setAttribute(n,s);for(let n of a)n==null||n===!1||r.appendChild(typeof n=="string"?t.createTextNode(n):n);return r}function ye(...t){return t.flatMap(e=>(e??"").split(/\s+/)).filter(e=>/^[\w-]+$/.test(e)).join(" ")}var rt="http://www.w3.org/2000/svg",l=t=>({tag:"path",d:t}),oo=[{tag:"circle",cx:16,cy:4,r:1},l("m18 19 1-7-6 1"),l("m5 8 3-3 5.5 3-2.36 3.5"),l("M4.24 14.5a5 5 0 0 0 6.88 6"),l("M13.76 17.5a5 5 0 0 0-6.88-6")],ao={accessibility:oo,close:[l("M18 6 6 18"),l("m6 6 12 12")],check:[l("M20 6 9 17l-5-5")],minus:[l("M5 12h14")],plus:[l("M5 12h14"),l("M12 5v14")],reset:[l("M3 12a9 9 0 1 0 3-6.7L3 8"),l("M3 3v5h5")],font:[l("M4 20 10 4h1l6 16"),l("M6.5 14h8"),l("M19 20v-6"),l("M16 17h6")],spacing:[l("M3 12h18"),l("m6 9-3 3 3 3"),l("m18 9 3 3-3 3")],lineHeight:[l("M10 6h11"),l("M10 12h11"),l("M10 18h11"),l("m3 8 3-3 3 3"),l("m3 16 3 3 3-3"),l("M6 5v14")],text:[l("M4 7V5h16v2"),l("M12 5v14"),l("M9 19h6")],pause:[{tag:"rect",x:6,y:5,width:4,height:14,rx:1},{tag:"rect",x:14,y:5,width:4,height:14,rx:1}],motion:[l("M3 12h4l3-8 4 16 3-8h4")],grayscale:[{tag:"circle",cx:12,cy:12,r:9},l("M12 3a9 9 0 0 1 0 18Z")],link:[l("M10 14a5 5 0 0 0 7.07 0l3-3a5 5 0 0 0-7.07-7.07l-1.5 1.5"),l("M14 10a5 5 0 0 0-7.07 0l-3 3a5 5 0 0 0 7.07 7.07l1.5-1.5")],heading:[l("M6 4v16"),l("M18 4v16"),l("M6 12h12")],guide:[l("M3 12h18"),l("M3 6h10"),l("M3 18h14")],mask:[{tag:"rect",x:3,y:3,width:18,height:18,rx:2},l("M3 9h18"),l("M3 15h18")],cursor:[l("M5 3l14 7-6 2-2 6Z")],focus:[l("M3 8V5a2 2 0 0 1 2-2h3"),l("M16 3h3a2 2 0 0 1 2 2v3"),l("M21 16v3a2 2 0 0 1-2 2h-3"),l("M8 21H5a2 2 0 0 1-2-2v-3"),{tag:"circle",cx:12,cy:12,r:3}],image:[{tag:"rect",x:3,y:3,width:18,height:18,rx:2},{tag:"circle",cx:9,cy:9,r:2},l("m21 15-5-5L5 21"),l("M3 3l18 18")]};function C(t,e,o="a11y-toolbar-icon"){let a=t.createElementNS(rt,"svg");a.setAttribute("viewBox","0 0 24 24"),a.setAttribute("fill","none"),a.setAttribute("stroke","currentColor"),a.setAttribute("stroke-width","2"),a.setAttribute("stroke-linecap","round"),a.setAttribute("stroke-linejoin","round"),a.setAttribute("aria-hidden","true"),a.setAttribute("focusable","false"),a.setAttribute("class",o);for(let r of ao[e]){let n=t.createElementNS(rt,r.tag);r.tag==="path"?n.setAttribute("d",r.d):r.tag==="circle"?(n.setAttribute("cx",String(r.cx)),n.setAttribute("cy",String(r.cy)),n.setAttribute("r",String(r.r))):(n.setAttribute("x",String(r.x)),n.setAttribute("y",String(r.y)),n.setAttribute("width",String(r.width)),n.setAttribute("height",String(r.height)),n.setAttribute("rx",String(r.rx))),a.appendChild(n)}return a}function Ce(t,e="a11y-toolbar-trigger-icon"){return C(t,"accessibility",e)}function V(t,e,o,a){let r=`a11y-toolbar-${t.uid}-section-${e}`;return c(t.doc,"section",{className:"a11y-toolbar-section",attrs:{"aria-labelledby":r}},[c(t.doc,"h3",{className:"a11y-toolbar-section-title",id:r,text:o}),c(t.doc,"div",{className:"a11y-toolbar-section-body"},a)])}function Pe(t,e,o,a){let{doc:r,t:n}=t,s=c(r,"span",{className:"a11y-toolbar-toggle-state-text",text:n.inactive}),d=c(r,"button",{className:"a11y-toolbar-toggle a11y-toolbar-nav",attrs:{type:"button","aria-pressed":"false","data-a11y-toolbar-control":e}},[C(r,o),c(r,"span",{className:"a11y-toolbar-toggle-label",text:n[e]}),c(r,"span",{className:"a11y-toolbar-toggle-state",attrs:{"aria-hidden":"true"}},[C(r,"check","a11y-toolbar-icon a11y-toolbar-check"),s])]);return d.addEventListener("click",()=>a(e)),{element:d,update(g){let v=g[e];d.setAttribute("aria-pressed",String(v)),s.textContent=v?n.active:n.inactive}}}function ke(t,e,o){return t==="textScale"?`${Math.round(e*100)}%`:e===0?o.normal:t==="lineHeight"?String(e):`+${N[t].indexOf(e)}`}function ro(t,e){switch(t){case"textScale":return{label:e.textScale,decrease:e.decreaseText,increase:e.increaseText,reset:e.resetText};case"letterSpacing":return{label:e.letterSpacing,decrease:e.decreaseLetterSpacing,increase:e.increaseLetterSpacing};case"wordSpacing":return{label:e.wordSpacing,decrease:e.decreaseWordSpacing,increase:e.increaseWordSpacing};case"lineHeight":return{label:e.lineHeight,decrease:e.decreaseLineHeight,increase:e.increaseLineHeight}}}function nt(t,e,o,a,r){let n=c(t.doc,"button",{className:"a11y-toolbar-step-button a11y-toolbar-nav",attrs:{type:"button","aria-label":o,title:o,"aria-describedby":a}},[C(t.doc,e)]);return n.addEventListener("click",()=>{n.getAttribute("aria-disabled")!=="true"&&r()}),n}function it(t,e,o,a,r){let{doc:n,t:s,uid:d}=t,g=ro(e,s),v=`a11y-toolbar-${d}-${e}-label`,p=`a11y-toolbar-${d}-${e}-value`,y=c(n,"bdi",{className:"a11y-toolbar-step-value",id:p}),f=nt(t,"minus",g.decrease,p,()=>a(e,-1)),b=nt(t,"plus",g.increase,p,()=>a(e,1));f.setAttribute("data-a11y-toolbar-control",`${e}-decrease`),b.setAttribute("data-a11y-toolbar-control",`${e}-increase`);let x=null;if(g.reset){x=c(n,"button",{className:"a11y-toolbar-step-reset a11y-toolbar-nav",text:s.normal,attrs:{type:"button","aria-label":g.reset,"data-a11y-toolbar-control":`${e}-reset`}});let P=x;P.addEventListener("click",()=>{P.getAttribute("aria-disabled")!=="true"&&r(e)})}let S=c(n,"div",{className:"a11y-toolbar-stepper",attrs:{role:"group","aria-labelledby":v,"data-a11y-toolbar-stepper":e}},[c(n,"span",{className:"a11y-toolbar-stepper-label"},[C(n,o),c(n,"span",{id:v,text:g.label})]),c(n,"span",{className:"a11y-toolbar-stepper-controls"},[f,y,b,x])]);return{element:S,update(P){let k=P[e],T=ve(e,k),j=N[e].length-1;y.textContent=ke(e,k,s),f.setAttribute("aria-disabled",String(T<=0)),b.setAttribute("aria-disabled",String(T>=j)),x?.setAttribute("aria-disabled",String(T<=0)),S.toggleAttribute("data-a11y-toolbar-changed",T>0)}}}function st(t,e,o){let{doc:a,t:r,uid:n}=t,s=`a11y-toolbar-${n}-contrast`,d=new Map,g=(y,f)=>{let b=c(a,"input",{className:"a11y-toolbar-radio-input",attrs:{type:"radio",name:s,value:y,"data-a11y-toolbar-control":`contrast-${y}`}});return b.addEventListener("change",()=>{b.checked&&o(y==="none"?null:y)}),d.set(y,b),c(a,"label",{className:"a11y-toolbar-radio"},[b,c(a,"span",{className:"a11y-toolbar-radio-mark",attrs:{"aria-hidden":"true"}}),c(a,"span",{className:"a11y-toolbar-radio-label",text:f})])},v=M.filter(y=>e.includes(y));return{element:c(a,"fieldset",{className:"a11y-toolbar-radios"},[c(a,"legend",{className:"a11y-toolbar-radios-legend",text:r.contrastGroup}),c(a,"div",{className:"a11y-toolbar-radios-grid"},[g("none",r.contrastNone),...v.map(y=>g(y,r[y]))])]),update(y){let f=_(y)??"none";for(let[b,x]of d)x.checked=b===f}}}function lt(t,e){let o=c(t.doc,"button",{className:"a11y-toolbar-reset a11y-toolbar-nav",attrs:{type:"button","data-a11y-toolbar-control":"reset"}},[C(t.doc,"reset"),c(t.doc,"span",{text:t.t.resetAll})]);return o.addEventListener("click",e),o}var ct="a11y-panel",no="a11y-toolbar-trigger";function dt(t,e,o){return c(t,"button",{className:o,id:no,attrs:{type:"button","aria-expanded":"false","aria-controls":ct,"aria-haspopup":"dialog","aria-label":e,title:e}},[Ce(t)])}function bt(t,e,o,a,r){let n=`a11y-toolbar-${r}-title`,s=`a11y-toolbar-${r}-desc`,d=c(t,"h2",{className:"a11y-toolbar-title",id:n,text:o,attrs:{tabindex:"-1"}}),g=c(t,"button",{className:"a11y-toolbar-close a11y-toolbar-nav",attrs:{type:"button","aria-label":e.close,title:e.close,"data-a11y-toolbar-control":"close"}},[C(t,"close")]),v=c(t,"div",{className:"a11y-toolbar-body"}),p=c(t,"div",{className:"a11y-toolbar-footer"}),y=c(t,"div",{className:a,id:ct,attrs:{role:"dialog","aria-modal":"false","aria-labelledby":n,"aria-describedby":s}},[c(t,"div",{className:"a11y-toolbar-header"},[c(t,"div",{className:"a11y-toolbar-heading"},[c(t,"span",{className:"a11y-toolbar-heading-icon",attrs:{"aria-hidden":"true"}},[Ce(t,"a11y-toolbar-icon")]),d]),g]),c(t,"p",{className:"a11y-toolbar-description",id:s,text:e.panelDescription}),v,p]);return y.hidden=!0,{panel:y,title:d,close:g,body:v,footer:p}}var pe=class{constructor(e){this.timer=null;this.element=c(e,"div",{className:"a11y-toolbar-sr-only",attrs:{role:"status","aria-live":"polite","aria-atomic":"true"}})}announce(e){this.timer!==null&&clearTimeout(this.timer),this.element.textContent="",this.timer=setTimeout(()=>{this.timer=null,this.element.textContent=e},60)}destroy(){this.timer!==null&&clearTimeout(this.timer),this.timer=null}};var Ae="a11y-toolbar-root",io=["bottom-right","bottom-left","top-right","top-left"],so=["light","dark","system"],yt=[["readableFont","font"]],pt=[["pauseAnimations","pause"],["reduceMotion","motion"]],ut=[["highlightLinks","link"],["highlightHeadings","heading"],["readingGuide","guide"],["readingMask","mask"],["largeCursor","cursor"],["focusHighlight","focus"],["hideImages","image"]],lo=[["textScale","text"],["letterSpacing","spacing"],["wordSpacing","spacing"],["lineHeight","lineHeight"]];function co(t,e,o){if(z(t,e))return null;if(t.textScale!==e.textScale){let s=String(Math.round(e.textScale*100));return e.textScale===1?o.announceTextReset:B(e.textScale>t.textScale?o.announceTextIncreased:o.announceTextDecreased,{value:s})}for(let s of["letterSpacing","wordSpacing","lineHeight"])if(t[s]!==e[s])return B(o.announceValueChanged,{label:o[s],value:ke(s,e[s],o)});let a=_(t),r=_(e);if(a!==r)return r?B(o.announceEnabled,{label:o[r]}):o.announceContrastOff;let n=[...yt,...pt,...ut].map(([s])=>s);for(let s of[...n,"grayscale"])if(t[s]!==e[s])return B(e[s]?o.announceEnabled:o.announceDisabled,{label:o[s]});return null}function Le(t){return{provider:t,mounted:!1,isOpen:()=>!1,open:()=>{},close:()=>{},toggle:()=>{},destroy:()=>t.destroy()}}function bo(t={},e){let o=X(t.document),a=typeof t.zIndex=="number"&&Number.isFinite(t.zIndex)?Math.round(t.zIndex):95,r=e??new de(t,{zIndex:a}),n=!e;if(!o)return Le(r);if(!t.allowMultiple&&o.getElementById(Ae))return n?Le(r):{...Le(r),destroy:()=>{}};let s=be(t.language)?t.language:"he",d=t.direction==="ltr"||t.direction==="rtl"?t.direction:s==="he"?"rtl":"ltr",g=io.includes(t.position??"bottom-right")?t.position??"bottom-right":"bottom-right",v=so.includes(t.theme??"light")?t.theme??"light":"light",p=at(s,{...t.translations,...t.panelTitle?{panelTitle:t.panelTitle}:{},...t.buttonLabel?{accessibilityOptions:t.buttonLabel}:{}}),y=Q().replace(/[^\w-]/g,"").slice(0,8),f={doc:o,t:p,uid:y},b=c(o,"div",{className:ye("a11y-toolbar-root",t.className),attrs:{dir:d,lang:s,"data-a11y-toolbar-position":g,"data-a11y-toolbar-theme":v,"data-a11y-toolbar-layout":"popover","data-a11y-toolbar-ignore-text-scale":""}});(!t.allowMultiple||!o.getElementById(Ae))&&(b.id=Ae),b.style.setProperty("--a11y-toolbar-z",String(a)),Z(t.primaryColor)&&b.style.setProperty("--a11y-toolbar-primary",t.primaryColor.trim());let x=dt(o,p.accessibilityOptions,ye("a11y-toolbar-trigger",t.buttonClassName)),S=bt(o,p,p.panelTitle,ye("a11y-toolbar-panel",t.panelClassName),y),P=new pe(o),k=[],T=(i,u)=>{let h=r.getPreferences();i();let A=r.getPreferences(),E=u??co(h,A,p);E&&(u!==void 0||!z(h,A))&&P.announce(E)},j=i=>T(()=>r.toggle(i)),ft=(i,u)=>T(()=>r.step(i,u)),ht=i=>T(()=>r.setPreference(i,1)),mt=i=>T(()=>r.setContrastMode(i)),ue=i=>i.filter(([u])=>r.isEnabled(u)).map(([u,h])=>{let A=Pe(f,u,h,j);return k.push(A),A.element}),ge=i=>i.length?c(o,"div",{className:"a11y-toolbar-grid"},i):null,Re=lo.filter(([i])=>r.isEnabled(i)).map(([i,u])=>{let h=it(f,i,u,ft,ht);return k.push(h),h.element}),fe=ge(ue(yt)),K=[];(Re.length||fe)&&K.push(V(f,"text",p.sectionText,[...Re,...fe?[fe]:[]]));let U=[],He=M.filter(i=>r.isEnabled(i));if(He.length){let i=st(f,He,mt);k.push(i),U.push(i.element)}if(r.isEnabled("grayscale")){let i=Pe(f,"grayscale","grayscale",j);k.push(i),U.push(c(o,"div",{className:"a11y-toolbar-grid"},[i.element]))}U.length&&K.push(V(f,"color",p.sectionColor,U));let Ne=ge(ue(pt));Ne&&K.push(V(f,"motion",p.sectionMotion,[Ne]));let Ie=ge(ue(ut));Ie&&K.push(V(f,"reading",p.sectionReading,[Ie]));for(let i of K)S.body.appendChild(i);let Ke=lt(f,()=>{T(()=>r.reset(),p.resetDone),t.closeOnReset?O(!0):Ke.focus()});S.footer.append(Ke,c(o,"p",{className:"a11y-toolbar-disclaimer",text:p.disclaimer})),b.append(x,S.panel,P.element);let De=i=>{for(let u of k)u.update(i)};De(r.getPreferences());let vt=r.subscribe(i=>De(i)),L=!1,D=(i,u)=>{if(i!==L){L=i,S.panel.hidden=!i,b.toggleAttribute("data-a11y-toolbar-open",i),x.setAttribute("aria-expanded",String(i)),i?S.title.focus({preventScroll:!0}):u&&x.focus({preventScroll:!0});try{t.onOpenChange?.(i)}catch{}}};function O(i=!0){D(!1,i)}x.addEventListener("click",()=>D(!L,!0)),S.close.addEventListener("click",()=>O(!0));let xt=()=>Array.from(S.panel.querySelectorAll(".a11y-toolbar-nav")),Oe=i=>{if(i.key==="Escape"&&L){i.preventDefault(),i.stopPropagation(),O(!0);return}let u=i.target;if(!(u instanceof HTMLElement)||!S.panel.contains(u)||!u.classList.contains("a11y-toolbar-nav")||i.altKey||i.ctrlKey||i.metaKey)return;let h=xt(),A=h.indexOf(u),E;i.key==="ArrowDown"?E=h[(A+1)%h.length]:i.key==="ArrowUp"?E=h[(A-1+h.length)%h.length]:i.key==="Home"?E=h[0]:i.key==="End"&&(E=h[h.length-1]),E&&(i.preventDefault(),E.focus())};b.addEventListener("keydown",Oe);let $e=i=>{!L||S.panel.contains(i.target)||x.contains(i.target)||b.getAttribute("data-a11y-toolbar-layout")==="popover"&&O(!1)};o.addEventListener("pointerdown",$e,!0);let St=o.defaultView,Tt=typeof t.mobileBreakpoint=="number"&&t.mobileBreakpoint>0?Math.round(t.mobileBreakpoint):640,_e=Be(St,`(max-width: ${Tt}px)`),ze=()=>b.setAttribute("data-a11y-toolbar-layout",_e?.matches?"sheet":"popover");ze();let wt=Ve(_e,ze),Ge=!1,he=()=>{let i=H(o);Ge||!i||(Ge=!0,i.appendChild(b),t.defaultOpen&&D(!0,!1))};H(o)?he():o.addEventListener("DOMContentLoaded",he,{once:!0});let Fe=!1;return{provider:r,mounted:!0,isOpen:()=>L,open:()=>D(!0,!1),close:(i=!0)=>O(i),toggle:()=>D(!L,!0),destroy:()=>{Fe||(Fe=!0,o.removeEventListener("DOMContentLoaded",he),o.removeEventListener("pointerdown",$e,!0),b.removeEventListener("keydown",Oe),wt(),vt(),P.destroy(),b.remove(),n&&r.destroy())}}}function gt(t={}){return bo(t)}function yo(t){let e=t instanceof HTMLScriptElement?t.dataset:{},o=Number(e.zIndex),a=e.position,r=e.theme;return{language:be(e.language)?e.language:"he",...e.direction==="rtl"||e.direction==="ltr"?{direction:e.direction}:{},...a?{position:a}:{},...r?{theme:r}:{},...e.primaryColor?{primaryColor:e.primaryColor}:{},...Number.isFinite(o)&&e.zIndex?{zIndex:o}:{},...e.storageKey?{storageKey:e.storageKey}:{}}}typeof document<"u"&&gt(yo(document.currentScript));})();
