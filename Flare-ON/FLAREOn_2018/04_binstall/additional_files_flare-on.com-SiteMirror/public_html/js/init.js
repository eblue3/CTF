/**
* @author David Trounstine
*
*/
"use strict";

var com = com || {};
com.fireeye = com.fireeye || {};
com.fireeye.flareon = (function (){
	return {
		/**
		* A function for creating name spaces
		*
		* @param {string} ns The full namespace to be created
		*/
		createNS : function (ns) {
			var nsparts = ns.split( '.' );
			var parent = this;

			for ( var i = 0; i < nsparts.length; i++ ) {
				var partname = nsparts[i];
				if ( typeof parent[partname] === 'undefined' ) {
				    parent[partname] = {};
				}
				parent = parent[partname];
			}
			return parent;
		},

		/**
		* A function to initialize the desired namespaces for this application
		*
		*/
		init : function () {
			this.model = this.createNS( 'model' );
			this.view = this.createNS( 'view' );
			this.controller = this.createNS( 'controller' );
		}
	}
})();

$(document).ready( function() {
	com.fireeye.flareon.init();
});