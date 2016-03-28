(function($){

	$(document).ready( function() 
	{
		var dueno = $('#id_tenenciapropiedad_set-0-dueno_propiedad').val();
			if (dueno === '1' ) {
				$('#id_tenenciapropiedad_set-0-si').show();
				$('#id_tenenciapropiedad_set-0-no').hide();
			}else if(dueno === '2'){
				$('#id_tenenciapropiedad_set-0-si').hide();
				$('#id_tenenciapropiedad_set-0-no').show();
			}else{
				$('#id_tenenciapropiedad_set-0-si').hide();
				$('#id_tenenciapropiedad_set-0-no').hide();
			};

		$('#id_tenenciapropiedad_set-0-dueno_propiedad').change(function(){
			var valor_tipo = $('#id_tenenciapropiedad_set-0-dueno_propiedad').val();
			if (valor_tipo == '1' ) {
				$('#id_tenenciapropiedad_set-0-si').show();
				$('#id_tenenciapropiedad_set-0-no').hide();
			}else{
				$('#id_tenenciapropiedad_set-0-si').hide();
				$('#id_tenenciapropiedad_set-0-no').show();
			};
		});
	});

})(jQuery || django.jQuery);