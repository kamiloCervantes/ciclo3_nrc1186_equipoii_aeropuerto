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

        jqxhr.fail(function(error){
            console.log(error);
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
            $("#roles_query_results").append('<tr class="rol-results-item"><td colspan=5>No hay resultados</td></tr>');
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
            $("#recursos_query_results").append('<tr class="recurso-results-item"><td colspan=4>No hay resultados</td></tr>');
        }        
        
        $('#recursos_table').addClass('hide');
        $('#recursos_query_results').removeClass('hide');
    });   
}

/*
* Paises
*/

admin_settings.deletePais = function(e){
    e.preventDefault();
    var confirm_delete = confirm("¿Está seguro de eliminar el registro seleccionado?");

    if(confirm_delete){
        var self = $(this);
        var pais_id = self.data('pais');
        var jqxhr = $.ajax({
            url: "/admin/settings/paises?format=json",
            method: 'DELETE',
            data: {
                pais_id : pais_id
            }
        });

        jqxhr.done(function(data){
            self.closest('tr').remove();
        });
    }
}

admin_settings.loadEditPaisForm = function(e){
    e.preventDefault();
    var self = $(this);
    var pais_id = self.data('pais');
    var jqxhr = $.ajax({
        url: "/admin/settings/paises?format=json",
        method: 'GET',
        data: {
            pais_id : pais_id
        }
    });

    jqxhr.done(function(data){
        $('.editar-pais form input').val('');
        $('#btn-edit-pais').data('pais', data[0]);
        $('#nombre_pais_edit').val(data[1]);
        $('#descripcion_pais_edit').val(data[2]);

        $('.nuevo-pais').addClass('hide');
        $('.editar-pais').removeClass('hide');
    });    
}

admin_settings.cancelEditPaisForm = function(e){
    e.preventDefault();
    $('.nuevo-pais').removeClass('hide');
    $('.editar-pais').addClass('hide');
}

admin_settings.editPais = function(e){
    e.preventDefault();
    var self = $(this);
    var pais_id = self.data('pais');
    var nombre_pais = $('#nombre_pais_edit').val();
    var descripcion_pais = $('#descripcion_pais_edit').val();

    var jqxhr = $.ajax({
        url: "/admin/settings/paises?format=json",
        method: 'PUT',
        data: {
            pais_id : pais_id,
            nombre_pais : nombre_pais,
            descripcion_pais : descripcion_pais,
        }
    });

    jqxhr.done(function(data){
       location.reload();
    });    
}

admin_settings.searchPais = function(e){
    e.preventDefault();
    var self = $(this);
    var q = $('#query_pais').val() != '' ? $('#query_pais').val() : '-1';

    var jqxhr = $.ajax({
        url: "/admin/settings/paises?format=json",
        method: 'GET',
        data: {
            q : q
        }
    });

    jqxhr.done(function(data){
        $("#paises_query_results tr.pais-results-item").remove();
        if(data.length > 0){
            $.each(data, function(index,value){
                $("#paises_query_results").append('<tr class="pais-results-item"><td>'+value[0]+'</td><td>'+value[1]+'</td><td>'+(value[2])+'</td><td><a href="#" data-pais="'+value[0]+'" class="delete_pais"><i class="fa fa-trash-o mr-2 text-secondary"></i></a><a href="#" data-pais="'+value[0]+'" class="edit_pais"><i class="fa fa-pencil-square-o mr-2 text-secondary"></i></a></td></tr>');
            });
        }
        else{
            $("#paises_query_results").append('<tr class="pais-results-item"><td colspan=4>No hay resultados</td></tr>');
        }        
        
        $('#paises_table').addClass('hide');
        $('#paises_query_results').removeClass('hide');
    });   
}

/*
* Departamentos
*/

admin_settings.deleteDepartamento = function(e){
    e.preventDefault();
    var confirm_delete = confirm("¿Está seguro de eliminar el registro seleccionado?");

    if(confirm_delete){
        var self = $(this);
        var departamento_id = self.data('departamento');
        var jqxhr = $.ajax({
            url: "/admin/settings/departamentos?format=json",
            method: 'DELETE',
            data: {
                departamento_id : departamento_id
            }
        });

        jqxhr.done(function(data){
            self.closest('tr').remove();
        });
    }
}

admin_settings.loadEditDepartamentoForm = function(e){
    e.preventDefault();
    var self = $(this);
    var departamento_id = self.data('departamento');
    var jqxhr = $.ajax({
        url: "/admin/settings/departamentos?format=json",
        method: 'GET',
        data: {
            departamento_id : departamento_id
        }
    });

    jqxhr.done(function(data){
        $('.editar-departamento form input').val('');
        $('#btn-edit-departamento').data('departamento', data[0]);
        $('#nombre_departamento_edit').val(data[1]);
        $('#descripcion_departamento_edit').val(data[2]);
        $('#pais_departamento_edit').val(data[3]);

        $('.nuevo-departamento').addClass('hide');
        $('.editar-departamento').removeClass('hide');
    });    
}

admin_settings.cancelEditDepartamentoForm = function(e){
    e.preventDefault();
    $('.nuevo-departamento').removeClass('hide');
    $('.editar-departamento').addClass('hide');
}

admin_settings.editDepartamento = function(e){
    e.preventDefault();
    var self = $(this);
    var departamento_id = self.data('departamento');
    var nombre_departamento = $('#nombre_departamento_edit').val();
    var descripcion_departamento = $('#descripcion_departamento_edit').val();
    var pais_departamento = $('#pais_departamento_edit').val();

    var jqxhr = $.ajax({
        url: "/admin/settings/departamentos?format=json",
        method: 'PUT',
        data: {
            departamento_id : departamento_id,
            nombre_departamento : nombre_departamento,
            descripcion_departamento : descripcion_departamento,
            pais_departamento : pais_departamento
        }
    });

    jqxhr.done(function(data){
       location.reload();
    });    
}

admin_settings.searchDepartamento = function(e){
    e.preventDefault();
    var self = $(this);
    var q = $('#query_departamento').val() != '' ? $('#query_departamento').val() : '-1';

    var jqxhr = $.ajax({
        url: "/admin/settings/departamentos?format=json",
        method: 'GET',
        data: {
            q : q
        }
    });

    jqxhr.done(function(data){
        $("#departamentos_query_results tr.departamento-results-item").remove();
        if(data.length > 0){
            $.each(data, function(index,value){
                $("#departamentos_query_results").append('<tr class="departamento-results-item"><td>'+value[0]+'</td><td>'+value[1]+'</td><td>'+(value[2])+'</td><td><a href="#" data-departamento="'+value[0]+'" class="delete_departamento"><i class="fa fa-trash-o mr-2 text-secondary"></i></a><a href="#" data-departamento="'+value[0]+'" class="edit_departamento"><i class="fa fa-pencil-square-o mr-2 text-secondary"></i></a></td></tr>');
            });
        }
        else{
            $("#departamentos_query_results").append('<tr class="departamento-results-item"><td colspan=4>No hay resultados</td></tr>');
        }        
        
        $('#departamentos_table').addClass('hide');
        $('#departamentos_query_results').removeClass('hide');
    });   

}


/*
* Municipios
*/

admin_settings.deleteMunicipio = function(e){
    e.preventDefault();
    var confirm_delete = confirm("¿Está seguro de eliminar el registro seleccionado?");

    if(confirm_delete){
        var self = $(this);
        var municipio_id = self.data('municipio');
        var jqxhr = $.ajax({
            url: "/admin/settings/municipios?format=json",
            method: 'DELETE',
            data: {
                municipio_id : municipio_id
            }
        });

        jqxhr.done(function(data){
            self.closest('tr').remove();
        });
    }
}

admin_settings.loadEditMunicipioForm = function(e){
    e.preventDefault();
    var self = $(this);
    var municipio_id = self.data('municipio');
    var jqxhr = $.ajax({
        url: "/admin/settings/municipios?format=json",
        method: 'GET',
        data: {
            municipio_id : municipio_id
        }
    });

    jqxhr.done(function(data){
        $('.editar-municipio form input').val('');
        $('#btn-edit-municipio').data('municipio', data[0]);
        $('#nombre_municipio_edit').val(data[1]);
        $('#descripcion_municipio_edit').val(data[2]);
        $('#departamento_municipio_edit').val(data[3]);

        $('.nuevo-municipio').addClass('hide');
        $('.editar-municipio').removeClass('hide');
    });    
}

admin_settings.cancelEditMunicipioForm = function(e){
    e.preventDefault();
    $('.nuevo-municipio').removeClass('hide');
    $('.editar-municipio').addClass('hide');
}

admin_settings.editMunicipio = function(e){
    e.preventDefault();
    var self = $(this);
    var municipio_id = self.data('municipio');
    var nombre_municipio = $('#nombre_municipio_edit').val();
    var descripcion_municipio = $('#descripcion_municipio_edit').val();
    var departamento_municipio = $('#departamento_municipio_edit').val();

    var jqxhr = $.ajax({
        url: "/admin/settings/municipios?format=json",
        method: 'PUT',
        data: {
            municipio_id : municipio_id,
            nombre_municipio : nombre_municipio,
            descripcion_municipio : descripcion_municipio,
            departamento_municipio : departamento_municipio
        }
    });

    jqxhr.done(function(data){
       location.reload();
    });    
}

admin_settings.searchMunicipio = function(e){
    e.preventDefault();
    var self = $(this);
    var q = $('#query_municipio').val() != '' ? $('#query_municipio').val() : '-1';

    var jqxhr = $.ajax({
        url: "/admin/settings/municipios?format=json",
        method: 'GET',
        data: {
            q : q
        }
    });

    jqxhr.done(function(data){
        $("#municipios_query_results tr.municipio-results-item").remove();
        if(data.length > 0){
            $.each(data, function(index,value){
                $("#municipios_query_results").append('<tr class="municipio-results-item"><td>'+value[0]+'</td><td>'+value[1]+'</td><td>'+(value[2])+'</td><td><a href="#" data-municipio="'+value[0]+'" class="delete_municipio"><i class="fa fa-trash-o mr-2 text-secondary"></i></a><a href="#" data-municipio="'+value[0]+'" class="edit_municipio"><i class="fa fa-pencil-square-o mr-2 text-secondary"></i></a></td></tr>');
            });
        }
        else{
            $("#municipios_query_results").append('<tr class="municipio-results-item"><td colspan=4>No hay resultados</td></tr>');
        }        
        
        $('#municipios_table').addClass('hide');
        $('#municipios_query_results').removeClass('hide');
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
    /*
    * Paises
    */      
    $('body').on('click','.delete_pais', admin_settings.deletePais);
    $('body').on('click', '.edit_pais', admin_settings.loadEditPaisForm);
    $('#btn-cancelar-edit-pais').on('click', admin_settings.cancelEditPaisForm);
    $('#btn-edit-pais').on('click', admin_settings.editPais);
    $('#paises_search_form').on('submit', admin_settings.searchPais);
    /*
    * Departamentos
    */      
    $('body').on('click','.delete_departamento', admin_settings.deleteDepartamento);
    $('body').on('click', '.edit_departamento', admin_settings.loadEditDepartamentoForm);
    $('#btn-cancelar-edit-departamento').on('click', admin_settings.cancelEditDepartamentoForm);
    $('#btn-edit-departamento').on('click', admin_settings.editDepartamento);
    $('#departamentos_search_form').on('submit', admin_settings.searchDepartamento);
     /*
    * Municipios
    */      
    $('body').on('click','.delete_municipio', admin_settings.deleteMunicipio);
    $('body').on('click', '.edit_municipio', admin_settings.loadEditMunicipioForm);
    $('#btn-cancelar-edit-municipio').on('click', admin_settings.cancelEditMunicipioForm);
    $('#btn-edit-municipio').on('click', admin_settings.editMunicipio);
    $('#municipios_search_form').on('submit', admin_settings.searchMunicipio);
}


admin_settings.init();