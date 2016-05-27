(function($){

	$(document).ready( function()
	{
    $("#id_organizacion").select2();

		var financ = $('#id_financiamiento_set-0-financiamiento').val();
		if (financ == '1') {
			$('#financiamientoproductores_set-group').show();
		}else {
			$('#financiamientoproductores_set-group').hide();
		}

		$('#id_financiamiento_set-0-financiamiento').change(function(){
			var financ = $('#id_financiamiento_set-0-financiamiento').val();
			if (financ == '1') {
				$('#financiamientoproductores_set-group').show();
			}else {
				$('#financiamientoproductores_set-group').hide();
			}
		});
  });

})(jQuery || django.jQuery);
