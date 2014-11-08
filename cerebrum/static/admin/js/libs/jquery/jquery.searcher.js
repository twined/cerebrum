/*! jQuery Searcher Plugin - v0.1.0 - 2014-08-18
 * https://github.com/lloiser/jquery-searcher/
 * Copyright (c) 2014 Lukas Beranek; Licensed MIT 
*/
(function(){"use strict";function a(a){function b(b,c){this.element=b,this.options=a.extend({},f,c),this._create()}function c(a){return a.replace(/([.*+?^=!:${}()|\[\]\/\\])/g,"\\$1")}var d="searcher",e="plugin_"+d,f={itemSelector:"tbody > tr",textSelector:"td",inputSelector:"",caseSensitive:!1,toggle:function(b,c){a(b).toggle(c)}};b.prototype={dispose:function(){this._$input.unbind("."+d);var a=this.options,b=a.toggle||f.toggle;this._$element.find(a.itemSelector).each(function(){b(this,!0)})},_create:function(){var b=this.options;this._$element=a(this.element),this._fn=a.proxy(this._onValueChange,this);var c="input."+d+" change."+d+" keyup."+d;this._$input=a(b.inputSelector).bind(c,this._fn),this._lastValue="";var e=b.toggle||f.toggle;this._$element.find(b.itemSelector).each(function(){e(this,!0)})},_onValueChange:function(){var b=this.options,d=b.textSelector,e=b.toggle||f.toggle,g="gm"+(b.caseSensitive?"":"i"),h=new RegExp("("+c(this._$input.val())+")",g);h.toString()!==this._lastValue&&(this._lastValue=h.toString(),this._$element.find(b.itemSelector).each(function(){var b=a(this),c=d?b.find(d):b,f=!1;c=c.each(function(){return f=f||!!a(this).text().match(h),!f}),e(this,f)}))}},a.fn[d]=function(c){return this.each(function(){var d=a.data(this,e);d&&"dispose"===c?(d.dispose(),a.removeData(this,e)):d?a.extend(d.options,c):"object"==typeof c&&a.data(this,e,new b(this,c))})}}"function"==typeof define&&define.amd?define(["jquery"],a):"object"==typeof exports?module.exports=a:a(jQuery)}).call(this);