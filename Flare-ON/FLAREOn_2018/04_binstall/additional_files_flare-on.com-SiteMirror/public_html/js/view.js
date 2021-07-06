
com.fireeye.flareon.view = ( function() {
	function addCmd() {
		model.curIndex++;
		model.lastValIndex = 0;
		var dir = model.curDir;
		var vars = { 'dir' : dir, 'index' : model.curIndex }
		controller.getTemplate( 'cmd', vars )
			.then( function( rendered ) {
				$( '#cmd-window' ).append( rendered );
				$( '#command_' + model.curIndex ).focus();
				$( '#command_' + model.curIndex ).select();
			});
	}

	function lsDir() {
		var d = model.curDir;
		if( d === '~' )
			view.printOut( 'home_list' );
		else if( d.includes( '/' ) ){
			view.printOut( d.replace( /\//g, '-').toLowerCase() + '_list' );	
		}		
		else
			view.printOut( d.toLowerCase() + '_list' );
	}

	function printOut( input ) {
		controller.getTemplate( input )
			.then( function( rendered ) {
				$( '#cmd-window' ).append( rendered );
				view.addCmd();
			});		
	}

	function errOut( input, isDir, isArg ) {
		if( isDir )
			var $err = $('<div></div>')
						.attr('class', 'cli')
						.text('-bash: cd: ' + input + ': No such file or directory');
		else if( isArg )
			var $err = $('<div></div>')
						.attr('class', 'cli')
						.text('-bash: -' + input + ': invalid option');
		else
			var $err = $('<div></div>')
						.attr('class', 'cli')
						.text('-bash: ' + input + ': command not found');
		$( '#cmd-window' ).append( $err );
		view.addCmd();
	}

	function cls() {
		$( '#cmd-window').text('');
		view.addCmd();
	}

	function sl( args ) {
		//Concept and design elements were derived from https://github.com/mtoyoda/sl
		//License terms https://github.com/mtoyoda/sl/blob/master/LICENSE
		//Copyright 1993,1998,2014 Toyoda Masashi (mtoyoda@acm.org)

		var tmp = 'sl';
		if( args ) {
			tmp += '-'
			if( args.includes('l') )
				tmp += 'l';
			if( args.includes('a') )
				tmp += 'a';
			if( tmp === 'sl-' )
				tmp = 'sl';
		} else
			var args = '';

		controller.getTemplate( tmp )
			.then( function( rendered ) {
				$( '.cli' ).visibilityToggle();
				$( '#home-view' ).append( rendered );
				var i = 0;
				var sl_on = true;
				var choochoo = setInterval( function() {
					$( '#sl_' + i ).visibilityToggle();
					if( i < 3 ) {
						$( '#sl_' + ( i + 1 ) ).visibilityToggle();
						i++;
					} else {
						$( '#sl_0' ).visibilityToggle();
						i = 0;
					}
				}, 125 );
				if( args.includes('f') )
					$( '#sl_cmd' )
						.css({
							left: ( $( window ).width() / 1.5 ),
							top: ( $( window ).height() / 4 + $( window ).scrollTop() )
						})
						.animate({
							left: ( ( -1 * $( '#sl_cmd' ).width() ) - ( $( window ).width() / 1.5 ) ),
							top: ( $( window ).scrollTop() - 200 )
						}, 4000, 'linear', function() {
							clearInterval(choochoo);
							this.remove();
							$( '.cli' ).visibilityToggle();
							view.addCmd();
						});
				else
					$( '#sl_cmd' )
						.css({
							left: ( $( window ).width() / 1.5 ),
							top: ( $( window ).scrollTop() )
						})
						.animate({
							left: ( ( -1 * $( '#sl_cmd' ).width() ) - ( $( window ).width() / 1.5 ) ),
							top: ( $( window ).scrollTop() )
						}, 4000, 'linear', function() {
							clearInterval(choochoo);
							this.remove();
							$( '.cli' ).visibilityToggle();
							view.addCmd();
						});
			});		
	}

	return {
		addCmd : addCmd,
		lsDir: lsDir,
		printOut: printOut,
		errOut: errOut,
		cls: cls,
		sl: sl
	};
})();