
com.fireeye.flareon.controller = ( function() {
	function initDOM() {
		$(document)
			.click( function() {
				$( '#command_' + model.curIndex ).focus();
				$( '#command_' + model.curIndex ).select();
			})
			.on('selectstart dragstart', function( e ) {
				e.preventDefault();
				return false;
			});
		controller.getTemplate( 'home' )
			.then( function( rendered ) {
				$( document.body )
					.keydown( function( e ) {
						switch(e.which) {
							case 9: //TAB
								e.preventDefault();
								readIn( true );
								break;
							case 13: //ENTER
								e.preventDefault(); 
								readIn( false );
								break;
							case 38: //UP ARROW
								e.preventDefault(); 
								recallCmd( true );
								break;
							case 40: //DOWN ARROW
								e.preventDefault(); 
								recallCmd( false );
								break;
							default:
								break;
						}
					})
					.append( rendered );
				view.addCmd();
			});
	}

	function readIn( tab ) {
		var $input = $( '#command_' + model.curIndex );
		var val = $input.val().toLowerCase();
		if( !tab ) {
			$input.prop('disabled', true);
			if( val.length === 0){
				view.addCmd();			
			} 
			else {
				cmd = val.indexOf(' ') === -1 ? val.substr(0) : val.substr(0, val.indexOf(' '));
				if( model.lastVal[model.lastVal.length - 1] != val )
					model.lastVal.push( val );
				if( val.substr( 0, 2 ) === 'cd' )
					changeDir( val, tab, $input );
				else if ( model.cmdList[cmd.trim()] ){
					switch( val.substr( 0, 2 ) ) {
						case 'ls':
							view.lsDir();
							break;
						case 'sl':
							steamLoco( val );
							break;
						case 'he':
							view.printOut( val );
							break;
						case 'cl':
							view.cls();
							break;
					}
				}
				else {
					view.errOut( val );
				}
			}
		}
		else {
			if( val.substr( 0, 2 ) === 'cd' )
				changeDir( val, tab, $input );
			else
				tabComplete( val, false ); 
		}
	}

	function changeDir( val, tab, $input ) {
		if( val.length > 2 ) {
			var dir = val.substr(3).trim();
			if( val.substr( 2, 1 ) != ' ' ){
				view.errOut( val );
			} else {
				if( tab ){
					tabComplete( dir, true );
				}
				else {
					var d = model.curDir;
					var list = d.toLowerCase().replace( '~', 'dir').replace( '/', '_') + 'List';
					if( model.prevDir != '~' ){
						if( dir === '~' ){
							model.prevDir = model.curDir;
							model.curDir = '~';
							view.addCmd();										
						} else if( dir === '..' ){
							model.curDir = model.prevDir;
							model.prevDir = model.curDir.split('/')[0];
							if(model.curDir === model.prevDir)
								model.prevDir = '~';
							view.addCmd();	
						} else if( model[list] && model[list].hasOwnProperty(dir) ) {
							model.prevDir = model.curDir;
							model.curDir = d + '/' + model[list][dir];
							view.addCmd();									
						} else {
							view.errOut( dir, true );
						}
					} else if( model.dirList[dir] ) {
						model.prevDir = model.curDir;
						model.curDir = model.dirList[dir];
						view.addCmd();
					} else if( dir === '..' ) {
						model.curDir = model.prevDir;
						model.prevDir = '~';
						view.addCmd();
					} else if( model[list] && model[list].hasOwnProperty(dir) ) {
						model.prevDir = model.curDir;
						model.curDir = d + '/' + model[list][dir];
						view.addCmd();									
					} else {
						view.errOut( dir, true );
					}
				}
			}
		} else {
			view.addCmd();			
		}
	}

	function steamLoco( val ) {
		console.log(val);
		if( val.length > 2 ) {
			var arg = val.substr(4).toLowerCase();
			if( val.substr(2, 1) != ' ' ){
				view.errOut( val );
			} else if( val.substr(3, 1) != '-' && val.length > 3 ){
				view.errOut( val );
			} else if(val.length === 3) {
				view.sl();
			} else {
				var args = '';
				if( !arg.includes('l') && !arg.includes('a') && !arg.includes('f') ){
					view.errOut( arg, false, true )
				} else {
					if( arg.includes('l') )
						args += 'l';
					if( arg.includes('a') )
						args += 'a';
					if( arg.includes('f') )
						args += 'f';
					view.sl( args );
				}
			}
		} else {
			view.sl();
		}
	}

	function recallCmd( inc ) {
		if( inc ){
			if(model.lastValIndex++ >= model.lastVal.length)
				 model.lastValIndex = model.lastVal.length;			
		}else{
			if(model.lastValIndex-- <= 1)
				model.lastValIndex = 1; 
		}
		var i = model.lastVal.length - model.lastValIndex;
		$( '#command_' + model.curIndex ).val( model.lastVal[i] );
	}

	function tabComplete( input, isDir ) {
		var s = false;
		if( isDir ){
			var list = model[model.curDir.toLowerCase().replace( '~', 'dir').replace( '/', '_') + 'List'];
			for ( i in list ){
				if( list[i].substr( 0, input.length).toLowerCase() === input.substr( 0, input.length).toLowerCase() ){
					$( '#command_' + model.curIndex ).val( 'cd ' + list[i] );
					$( '#command_' + model.curIndex ).focus();
					s = true;
					break;
				}
			}
		} else {
			for ( c in model.cmdList ){
				if( c === input || c.substr( 0, input.length ).toLowerCase() === input.substr( 0, input.length ).toLowerCase() ){
					$( '#command_' + model.curIndex ).val( c );
					$( '#command_' + model.curIndex ).focus();
					s = true;
					break;
				}
			}
		}
		if( !s ){
			$( '#command_' + model.curIndex ).focus();
		}
	}

	function getTemplate( tmplt, vars ) {
		var def = $.Deferred();
		var vars = vars || null;
		var path = 'js/templates/'

		$.get( path + tmplt + '.mst.html', function( template ) {
			var rendered = Mustache.render( $( template ).filter( '#' + tmplt ).html(), vars );
			def.resolve( rendered );
		});
		return def.promise();
	}

	return {
		initDOM : initDOM,
		getTemplate: getTemplate
	};
} )();