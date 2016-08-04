(function($){
	$(document).on('click','#id_organizacion',function(){
			var id = $(this).val();
			if (id != '1') {
				$('#id_escuela_campo').empty();
				$.ajax({
				data : {'id' : id},
				url : '/admin/escuela-campo/',
				type : 'get',
				success : function(data){
					var html = ""
					 console.log(data);
					 for (var i = 0; i < data.length; i++) {
					 	html += '<option value="'+data[i].pk+'">'+data[i].fields.nombre+'</option>'
					 };
					 $('#id_escuela_campo').html(html);
					}
				});
			};
		});

})(jQuery || django.jQuery);
