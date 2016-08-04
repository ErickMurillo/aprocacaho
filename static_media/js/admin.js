(function($){

	$(document).ready( function()
	{
		$("#id_organizacion").select2();
		$("#id_entrevistado").select2();
		$("#id_encuestador").select2();

		var dueno = $('#id_tenenciapropiedad_set-0-dueno_propiedad').val();
			if (dueno === '1' ) {
				$('#id_tenenciapropiedad_set-0-si').show();
				$('#tenenciapropiedad_set-0 .field-no').hide();
			}else if(dueno === '2'){
				$('#id_tenenciapropiedad_set-0-si').hide();
				$('#tenenciapropiedad_set-0 .field-no').show();
			}else{
				$('#id_tenenciapropiedad_set-0-si').hide();
				$('#tenenciapropiedad_set-0 .field-no').hide();
			};

		$('#id_tenenciapropiedad_set-0-dueno_propiedad').change(function(){
			var dueno = $('#id_tenenciapropiedad_set-0-dueno_propiedad').val();
			if (dueno === '1' ) {
				$('#id_tenenciapropiedad_set-0-si').show();
				$('#tenenciapropiedad_set-0 .field-no').hide();
			}else if(dueno === '2'){
				$('#id_tenenciapropiedad_set-0-si').hide();
				$('#tenenciapropiedad_set-0 .field-no').show();
			}else{
				$('#id_tenenciapropiedad_set-0-si').hide();
				$('#tenenciapropiedad_set-0 .field-no').hide();
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


			var certificado = $('#id_certificacion_set-0-cacao_certificado').val();
			if (certificado === '1' ) {
				$('#certificacion_set-0 .field-tipo').show();
				$('#certificacion_set-0 .field-quien_certifica').show();
				$('#certificacion_set-0 .field-paga_certificacion').show();
				$('#certificacion_set-0 .field-costo_certificacion').show();
			}else{
				$('#certificacion_set-0 .field-tipo').hide();
				$('#certificacion_set-0 .field-quien_certifica').hide();
				$('#certificacion_set-0 .field-paga_certificacion').hide();
				$('#certificacion_set-0 .field-costo_certificacion').hide()
			};

			$('#id_certificacion_set-0-cacao_certificado').change(function(){
				var certificado = $('#id_certificacion_set-0-cacao_certificado').val();
				if (certificado === '1' ) {
					$('#certificacion_set-0 .field-tipo').show();
					$('#certificacion_set-0 .field-quien_certifica').show();
					$('#certificacion_set-0 .field-paga_certificacion').show();
					$('#certificacion_set-0 .field-costo_certificacion').show();
				}else{
					$('#certificacion_set-0 .field-tipo').hide();
					$('#certificacion_set-0 .field-quien_certifica').hide();
					$('#certificacion_set-0 .field-paga_certificacion').hide();
					$('#certificacion_set-0 .field-costo_certificacion').hide()
				};
			});
	});

})(jQuery || django.jQuery);
