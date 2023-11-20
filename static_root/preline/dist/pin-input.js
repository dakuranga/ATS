/*! For license information please see pin-input.js.LICENSE.txt */
!function(t,e){if("object"==typeof exports&&"object"==typeof module)module.exports=e();else if("function"==typeof define&&define.amd)define([],e);else{var n=e();for(var o in n)("object"==typeof exports?exports:t)[o]=n[o]}}(self,(()=>(()=>{"use strict";var t={737:(t,e)=>{Object.defineProperty(e,"__esModule",{value:!0});var n=function(){function t(t,e,n){this.el=t,this.options=e,this.events=n,this.el=t,this.options=e,this.events={}}return t.prototype.isIOS=function(){return!!/iPad|iPhone|iPod/.test(navigator.platform)||navigator.maxTouchPoints&&navigator.maxTouchPoints>2&&/MacIntel/.test(navigator.platform)},t.prototype.isIpadOS=function(){return navigator.maxTouchPoints&&navigator.maxTouchPoints>2&&/MacIntel/.test(navigator.platform)},t.prototype.createCollection=function(t,e){var n;t.push({id:(null===(n=null==e?void 0:e.el)||void 0===n?void 0:n.id)||t.length+1,element:e})},t.prototype.fireEvent=function(t,e){if(void 0===e&&(e=null),this.events.hasOwnProperty(t))return this.events[t](e)},t.prototype.dispatch=function(t,e,n){void 0===n&&(n=null);var o=new CustomEvent(t,{detail:{payload:n},bubbles:!0,cancelable:!0,composed:!1});e.dispatchEvent(o)},t.prototype.on=function(t,e){this.events[t]=e},t.prototype.afterTransition=function(t,e){var n=function(){e(),t.removeEventListener("transitionend",n,!0)};"all 0s ease 0s"!==window.getComputedStyle(t,null).getPropertyValue("transition")?t.addEventListener("transitionend",n,!0):e()},t.prototype.onTransitionEnd=function(t,e){t.addEventListener("transitionend",(function n(o){o.target===t&&(t.removeEventListener("transitionend",n),e())}))},t.prototype.getClassProperty=function(t,e,n){return void 0===n&&(n=""),(window.getComputedStyle(t).getPropertyValue(e)||n).replace(" ","")},t.prototype.getClassPropertyAlt=function(t,e,n){void 0===n&&(n="");var o="";return t.classList.forEach((function(t){t.includes(e)&&(o=t)})),o.match(/:(.*)]/)?o.match(/:(.*)]/)[1]:n},t.prototype.htmlToElement=function(t){var e=document.createElement("template");return t=t.trim(),e.innerHTML=t,e.content.firstChild},t.prototype.classToClassList=function(t,e,n){void 0===n&&(n=" "),t.split(n).forEach((function(t){return e.classList.add(t)}))},t.prototype.debounce=function(t,e){var n,o=this;return void 0===e&&(e=200),function(){for(var i=[],r=0;r<arguments.length;r++)i[r]=arguments[r];clearTimeout(n),n=setTimeout((function(){t.apply(o,i)}),e)}},t.prototype.checkIfFormElement=function(t){return t instanceof HTMLInputElement||t instanceof HTMLTextAreaElement||t instanceof HTMLSelectElement},t.isEnoughSpace=function(t,e,n,o,i){void 0===n&&(n="auto"),void 0===o&&(o=10),void 0===i&&(i=null);var r=e.getBoundingClientRect(),s=i?i.getBoundingClientRect():null,u=window.innerHeight,a=s?r.top-s.top:r.top,l=(i?s.bottom:u)-r.bottom,c=t.clientHeight+o;return"bottom"===n?l>=c:"top"===n?a>=c:a>=c||l>=c},t.isParentOrElementHidden=function(t){return!!t&&("none"===window.getComputedStyle(t).display||this.isParentOrElementHidden(t.parentElement))},t}();e.default=n,window.HSStaticMethods={afterTransition:function(t,e){var n=function(){e(),t.removeEventListener("transitionend",n,!0)};"all 0s ease 0s"!==window.getComputedStyle(t,null).getPropertyValue("transition")?t.addEventListener("transitionend",n,!0):e()},getClassPropertyAlt:function(t,e,n){void 0===n&&(n="");var o="";return t.classList.forEach((function(t){t.includes(e)&&(o=t)})),o.match(/:(.*)]/)?o.match(/:(.*)]/)[1]:n},getClassProperty:function(t,e,n){return void 0===n&&(n=""),(window.getComputedStyle(t).getPropertyValue(e)||n).replace(" ","")}}},659:function(t,e,n){var o,i=this&&this.__extends||(o=function(t,e){return o=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(t,e){t.__proto__=e}||function(t,e){for(var n in e)Object.prototype.hasOwnProperty.call(e,n)&&(t[n]=e[n])},o(t,e)},function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Class extends value "+String(e)+" is not a constructor or null");function n(){this.constructor=t}o(t,e),t.prototype=null===e?Object.create(e):(n.prototype=e.prototype,new n)}),r=this&&this.__assign||function(){return r=Object.assign||function(t){for(var e,n=1,o=arguments.length;n<o;n++)for(var i in e=arguments[n])Object.prototype.hasOwnProperty.call(e,i)&&(t[i]=e[i]);return t},r.apply(this,arguments)};Object.defineProperty(e,"__esModule",{value:!0});var s=function(t){function e(e,n){var o=t.call(this,e,n)||this,i=e.getAttribute("data-hs-pin-input"),s=i?JSON.parse(i):{},u=r(r({},s),n);return o.items=o.el.querySelectorAll("[data-hs-pin-input-item]"),o.currentItem=null,o.currentValue=new Array(o.items.length).fill(""),o.placeholders=[],o.availableCharsRE=new RegExp((null==u?void 0:u.availableCharsRE)||"^[a-zA-Z0-9]+$"),o.init(),o}return i(e,t),e.prototype.init=function(){this.createCollection(window.$hsPinInputCollection,this),this.items.length&&this.build()},e.prototype.build=function(){this.buildInputItems()},e.prototype.buildInputItems=function(){var t=this;this.items.forEach((function(e,n){t.placeholders.push(e.getAttribute("placeholder")||""),e.hasAttribute("autofocus")&&t.onFocusIn(n),e.addEventListener("input",(function(e){return t.onInput(e,n)})),e.addEventListener("paste",(function(e){return t.onPaste(e)})),e.addEventListener("keydown",(function(e){return t.onKeydown(e,n)})),e.addEventListener("focusin",(function(){return t.onFocusIn(n)})),e.addEventListener("focusout",(function(){return t.onFocusOut(n)}))}))},e.prototype.checkIfNumber=function(t){return t.match(this.availableCharsRE)},e.prototype.autoFillAll=function(t){var e=this;Array.from(t).forEach((function(t,n){if(!(null==e?void 0:e.items[n]))return!1;e.items[n].value=t,e.items[n].dispatchEvent(new Event("input",{bubbles:!0}))}))},e.prototype.setCurrentValue=function(){this.currentValue=Array.from(this.items).map((function(t){return t.value}))},e.prototype.toggleCompleted=function(){this.currentValue.includes("")?this.el.classList.remove("active"):this.el.classList.add("active")},e.prototype.onInput=function(t,e){var n=t.target.value;if(this.currentItem=t.target,this.currentItem.value="",this.currentItem.value=n[n.length-1],!this.checkIfNumber(this.currentItem.value))return this.currentItem.value=this.currentValue[e]||"",!1;if(this.setCurrentValue(),this.currentItem.value){if(e<this.items.length-1&&this.items[e+1].focus(),!this.currentValue.includes("")){var o={currentValue:this.currentValue};this.fireEvent("completed",o),this.dispatch("completed.hs.pinInput",this.el,o)}this.toggleCompleted()}else e>0&&this.items[e-1].focus()},e.prototype.onKeydown=function(t,e){"Backspace"===t.key&&e>0&&(""===this.items[e].value?(this.items[e-1].value="",this.items[e-1].focus()):this.items[e].value=""),this.setCurrentValue(),this.toggleCompleted()},e.prototype.onFocusIn=function(t){this.items[t].setAttribute("placeholder","")},e.prototype.onFocusOut=function(t){this.items[t].setAttribute("placeholder",this.placeholders[t])},e.prototype.onPaste=function(t){var e=this;t.preventDefault(),this.items.forEach((function(n){document.activeElement===n&&e.autoFillAll(t.clipboardData.getData("text"))}))},e.getInstance=function(t,e){var n=window.$hsPinInputCollection.find((function(e){return e.element.el===("string"==typeof t?document.querySelector(t):t)}));return n?e?n:n.element:null},e}(n(737).default);window.addEventListener("load",(function(){window.$hsPinInputCollection||(window.$hsPinInputCollection=[]),document.querySelectorAll("[data-hs-pin-input]:not(.--prevent-on-load-init)").forEach((function(t){return new s(t)}))})),t.exports.HSPinInput=s,e.default=s}},e={};return function n(o){var i=e[o];if(void 0!==i)return i.exports;var r=e[o]={exports:{}};return t[o].call(r.exports,r,r.exports,n),r.exports}(659)})()));