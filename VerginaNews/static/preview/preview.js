(function($){
	'use strict';

	$(function(){

		$('#preview_panel .preview-handler').on('click', function(){
			$('#preview_panel').toggleClass('hide-panel');
		});
		
		$('#preview_panel .pw-hover-item').hover(
			function(){
				$('#preview_panel .preview-viewport').html('<img src="'+$(this).data('img')+'">');
				$('#preview_panel .preview-viewport').show();
			},
			function(){
				$('#preview_panel .preview-viewport').hide();
			}
		)
		.mousemove(function(event){
			var _max_pos = $(window).height() - $('#preview_panel .preview-viewport').height();
			if( event.clientY >= _max_pos ){
				$('#preview_panel .preview-viewport').css({ 'top': _max_pos + 'px' });
			}
			else{
				$('#preview_panel .preview-viewport').css({ 'top': event.clientY + 'px' });
			}
		});

	});

})(jQuery);