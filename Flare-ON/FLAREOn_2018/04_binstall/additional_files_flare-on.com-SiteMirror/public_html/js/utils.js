
var model = com.fireeye.flareon.model;
var view = com.fireeye.flareon.view;
var controller = com.fireeye.flareon.controller;

controller.initDOM();

jQuery.fn.visible = function() {
	return this.css('visibility', 'visible');
};

jQuery.fn.invisible = function() {
	return this.css('visibility', 'hidden');
};

jQuery.fn.visibilityToggle = function() {
	return this.css('visibility', function(i, visibility) {
		return (visibility == 'visible') ? 'hidden' : 'visible';
	});
};

if (!String.prototype.includes) {
	String.prototype.includes = function() {
		'use strict';
		return String.prototype.indexOf.apply(this, arguments) !== -1;
	};
};