admin_users = {};


/*
* Users
*/

admin_users.deleteUser = function(e){
    e.preventDefault();
    var confirm_delete = confirm("¿Está seguro de eliminar el registro seleccionado?");

    if(confirm_delete){
        var self = $(this);
        var user_id = self.data('user');
        var jqxhr = $.ajax({
            url: "/admin/users?format=json",
            method: 'DELETE',
            data: {
                user_id : user_id
            }
        });

        jqxhr.done(function(data){
            self.closest('tr').remove();
        });
    }
}


admin_users.init = function(){
    $('body').on('click','.delete_user', admin_users.deleteUser);    
}


admin_users.init();