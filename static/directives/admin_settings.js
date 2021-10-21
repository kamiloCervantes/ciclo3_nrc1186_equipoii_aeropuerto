admin_settings = {}

/*
* Roles
*/

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
    var q = $('#query_rol').val() != '' ? $('#query_rol').val() : '-1';
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
            $("#roles_query_results").append('<tr><td colspan=5>No hay resultados</td></tr>');
        }        
        
        $('#roles_table').addClass('hide');
        $('#roles_query_results').removeClass('hide');
    });   
}

/*
* Recursos
*/

admin_settings.deleteRecurso = function(e){
    e.preventDefault();
    var confirm_delete = confirm("¿Está seguro de eliminar el registro seleccionado?");

    if(confirm_delete){
        var self = $(this);
        var recurso_id = self.data('recurso');
        var jqxhr = $.ajax({
            url: "/admin/settings/recursos?format=json",
            method: 'DELETE',
            data: {
                recurso_id : recurso_id
            }
        });

        jqxhr.done(function(data){
            self.closest('tr').remove();
        });
    }
}

admin_settings.loadEditRecursoForm = function(e){
    e.preventDefault();
    var self = $(this);
    var recurso_id = self.data('recurso');
    var jqxhr = $.ajax({
        url: "/admin/settings/recursos?format=json",
        method: 'GET',
        data: {
            recurso_id : recurso_id
        }
    });

    jqxhr.done(function(data){
        $('.editar-recurso form input').val('');
        $('#btn-edit-recurso').data('recurso', data[0]);
        $('#nombre_recurso_edit').val(data[1]);
        $('#descripcion_recurso_edit').val(data[2]);
        $('#codigo_recurso_edit').val(data[3]);
        $('#ruta_relativa_edit').val(data[4]);

        $('.nuevo-recurso').addClass('hide');
        $('.editar-recurso').removeClass('hide');
    });    
}

admin_settings.cancelEditRecursoForm = function(e){
    e.preventDefault();
    $('.nuevo-recurso').removeClass('hide');
    $('.editar-recurso').addClass('hide');
}

admin_settings.editRecurso = function(e){
    e.preventDefault();
    var self = $(this);
    var recurso_id = self.data('recurso');
    var nombre_recurso = $('#nombre_recurso_edit').val();
    var descripcion_recurso = $('#descripcion_recurso_edit').val();
    var codigo_recurso = $('#codigo_recurso_edit').val();
    var ruta_relativa = $('#ruta_relativa_edit').val();

    var jqxhr = $.ajax({
        url: "/admin/settings/recursos?format=json",
        method: 'PUT',
        data: {
            recurso_id : recurso_id,
            nombre_recurso : nombre_recurso,
            descripcion_recurso : descripcion_recurso,
            codigo_recurso : codigo_recurso,
            ruta_relativa : ruta_relativa
        }
    });

    jqxhr.done(function(data){
       location.reload();
    });    
}

admin_settings.searchRecurso = function(e){
    e.preventDefault();
    var self = $(this);
    var q = $('#query_recurso').val() != '' ? $('#query_recurso').val() : '-1';

    var jqxhr = $.ajax({
        url: "/admin/settings/recursos?format=json",
        method: 'GET',
        data: {
            q : q
        }
    });

    jqxhr.done(function(data){
        $("#recursos_query_results tr.recurso-results-item").remove();
        if(data.length > 0){
            $.each(data, function(index,value){
                $("#recursos_query_results").append('<tr class="recurso-results-item"><td>'+value[0]+'</td><td>'+value[1]+'</td><td>'+(value[2] == null ? 'None' : value[2])+'</td><td>'+value[3]+'</td><td><a href="#" data-recurso="'+value[0]+'" class="delete_recurso"><i class="fa fa-trash-o mr-2 text-secondary"></i></a><a href="#" data-recurso="'+value[0]+'" class="edit_recurso"><i class="fa fa-pencil-square-o mr-2 text-secondary"></i></a></td></tr>');
            });
        }
        else{
            $("#recursos_query_results").append('<tr><td colspan=4>No hay resultados</td></tr>');
        }        
        
        $('#recursos_table').addClass('hide');
        $('#recursos_query_results').removeClass('hide');
    });   
}


admin_settings.init = function(){
    /*
    * Roles
    */
    $('body').on('click','.delete_rol', admin_settings.deleteRol);
    $('body').on('click', '.edit_rol', admin_settings.loadEditRolForm);
    $('#btn-cancelar-edit-rol').on('click', admin_settings.cancelEditRolForm);
    $('#btn-edit-rol').on('click', admin_settings.editRol);
    $('#roles_search_form').on('submit', admin_settings.searchRol);
    /*
    * Recursos
    */      
    $('body').on('click','.delete_recurso', admin_settings.deleteRecurso);
    $('body').on('click', '.edit_recurso', admin_settings.loadEditRecursoForm);
    $('#btn-cancelar-edit-recurso').on('click', admin_settings.cancelEditRecursoForm);
    $('#btn-edit-recurso').on('click', admin_settings.editRecurso);
    $('#recursos_search_form').on('submit', admin_settings.searchRecurso);
}


admin_settings.init();