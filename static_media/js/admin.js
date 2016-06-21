(function($){

	$(document).ready( function()
	{
		$("#id_organizacion").select2();
		$("#id_entrevistado").select2();
		$("#id_encuestador").select2();

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

		var socio = $('#id_organizacionasociada_set-0-socio').val();
			if (socio === '1' ) {
				$('#organizacionasociada_set-0 .field-organizacion').show();
			}else{
				$('#organizacionasociada_set-0 .field-organizacion').hide();
			};

			$('#id_organizacionasociada_set-0-socio').change(function(){
				var socio = $('#id_organizacionasociada_set-0-socio').val();
				if (socio === '1' ) {
					$('#organizacionasociada_set-0 .field-organizacion').show();
				}else{
					$('#organizacionasociada_set-0 .field-organizacion').hide();
				};
			});

	});

})(jQuery || django.jQuery);
