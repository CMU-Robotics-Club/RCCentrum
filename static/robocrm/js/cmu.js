// From cmujs by Ryhan:
// https://raw.githubusercontent.com/ryhan/cmujs/master/cmu.js
// Generated by CoffeeScript 1.6.3
(function(){var e,t,n={}.hasOwnProperty,r=function(e,t){function i(){this.constructor=e}for(var r in t)n.call(t,r)&&(e[r]=t[r]);i.prototype=t.prototype;e.prototype=new i;e.__super__=t.prototype;return e};this.API=function(){function n(n){var r;n==null&&(n={});this._id=n.id||e;this._secret=n.secret||t;this._api_endpoint="https://apis.scottylabs.org/v1/";r=new Date;this._current_semester=r.getMonth()<5?"S":"F";this._current_semester+=r.getFullYear()-2e3}var e,t;e="9c55f614-c85c-4fb9-b9db-5583351f606e";t="rtRPuoJZeGT5yiKQH6mFt9LZ1zMWFPb4z9olkJspfnPDygWukK_vjWuP";n.prototype._get=function(e){var t,n;t=""+(this._api_endpoint+e)+"?app_id="+this._id+"&app_secret_key="+this._secret;n=null;n=new XMLHttpRequest;n.open("GET",t,!1);n.send(null);return JSON.parse(n.responseText)};return n}();this.ScheduleAPI=function(t){function n(){e=n.__super__.constructor.apply(this,arguments);return e}r(n,t);n.prototype.findCourse=function(e,t){var n;t==null&&(t=this._current_semester);n=this._get("schedule/"+encodeURIComponent(t)+"/courses/"+encodeURIComponent(e));if(n!=null)return n.course};return n}(API);this.DirectoryAPI=function(e){function n(){t=n.__super__.constructor.apply(this,arguments);return t}r(n,e);n.prototype.findAndrewId=function(e){var t;t=this._get("directory/andrewid/"+encodeURIComponent(e));if(t!=null)return t.person};return n}(API);this.CMUApi=function(){function e(e){this.schedule=new ScheduleAPI(e);this.directory=new DirectoryAPI(e)}return e}()}).call(this);