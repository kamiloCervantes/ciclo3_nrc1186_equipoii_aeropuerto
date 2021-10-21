admin_settings = {}


admin_settings.deleteRol = function(e){
    e.preventDefault();
    var confirm_delete = confirm("¿Está seguro de eliminar el registro seleccionado?");

    if(confirm_delete){
        var self = $(this);
        var rol_id = self.data('rol');
        var jqxhr = $.ajax({
            url: "/admin/settings/roles?format=json",
            method: 'DELETE',
            data: {
                rol_id : rol_id
            }
        });

        jqxhr.done(function(data){
            self.closest('tr').remove();
        });
    }
}

admin_settings.loadEditRolForm = function(e){
    e.preventDefault();
    var self = $(this);
    var rol_id = self.data('rol');
    var jqxhr = $.ajax({
        url: "/admin/settings/roles?format=json",
        method: 'GET',
        data: {
            rol_id : rol_id
        }
    });

    jqxhr.done(function(data){
        console.log(data[1]);
        $('.editar-rol form input').val('');
        $('#btn-edit-rol').data('rol', data[0]);
        $('#nombre_rol_edit').val(data[1]);
        $('#descripcion_edit').val(data[2]);
        if(data[3] > 0){
           $('#homepage_edit').val(data[3]); 
        }
        $('.nuevo-rol').addClass('hide');
        $('.editar-rol').removeClass('hide');
    });    
}

admin_settings.cancelEditRolForm = function(e){
    e.preventDefault();
    $('.nuevo-rol').removeClass('hide');
    $('.editar-rol').addClass('hide');
}

admin_settings.editRol = function(e){
    e.preventDefault();
    var self = $(this);
    var rol_id = self.data('rol');
    var nombre_rol = $('#nombre_rol_edit').val();
    var descripcion_rol = $('#descripcion_edit').val();
    var homepage_rol = $('#homepage_edit').val();
    var jqxhr = $.ajax({
        url: "/admin/settings/roles?format=json",
        method: 'PUT',
        data: {
            rol_id : rol_id,
            nombre_rol : nombre_rol,
            descripcion_rol : descripcion_rol,
            homepage_rol : homepage_rol
        }
    });

    jqxhr.done(function(data){
       location.reload();
    });    
}

admin_settings.searchRol = function(e){
    e.preventDefault();
    var self = $(this);
    var q = $('#query_rol').val();
    var jqxhr = $.ajax({
        url: "/admin/settings/roles?format=json",
        method: 'GET',
        data: {
            q : q
        }
    });

    jqxhr.done(function(data){
        $("#roles_query_results tr.rol-results-item").remove();
        if(data.length > 0){
            $.each(data, function(index,value){
                $("#roles_query_results").append('<tr class="rol-results-item"><td>'+value[0]+'</td><td>'+value[1]+'</td><td>'+value[2]+'</td><td>'+value[3]+'</td><td><a href="#" data-rol="'+value[0]+'" class="delete_rol"><i class="fa fa-trash-o mr-2 text-secondary"></i></a><a href="#" data-rol="'+value[0]+'" class="edit_rol"><i class="fa fa-pencil-square-o mr-2 text-secondary"></i></a></td></tr>');
            });
        }
        else{
            $("#roles_query_results").append('<tr><td colspan=4>No hay resultados</td></tr>');
        }        
        
        $('#roles_table').addClass('hide');
        $('#roles_query_results').removeClass('hide');
    });   
}


admin_settings.init = function(){
    $('body').on('click','.delete_rol', admin_settings.deleteRol);
    $('body').on('click', '.edit_rol', admin_settings.loadEditRolForm);
    $('#btn-cancelar-edit-rol').on('click', admin_settings.cancelEditRolForm);
    $('#btn-edit-rol').on('click', admin_settings.editRol);
    $('#roles_search_form').on('submit', admin_settings.searchRol);
}


admin_settings.init();