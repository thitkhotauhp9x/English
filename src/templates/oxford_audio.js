// ==UserScript==
// @name         Oxford audio
// @namespace    http://tampermonkey.net/
// @version      2023-12-04
// @description  try to take over the world!
// @author       You
// @match        https://www.oxfordlearnersdictionaries.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=oxfordlearnersdictionaries.com
// @grant        none
// @require      https://code.jquery.com/jquery-3.6.0.min.js
// ==/UserScript==

(function() {
    'use strict';
    var sounds = $(".sound");
    sounds.each(function(){
        $(this).after("<a href='"+$(this).attr("data-src-mp3")+"'>Audio</a>");
    });
    // Your code here...
})();
