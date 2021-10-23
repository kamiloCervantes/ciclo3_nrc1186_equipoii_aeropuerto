admin_locations = {};


/*
* Locations
*/

admin_locations.deleteLocation = function(e){
    e.preventDefault();
    var confirm_delete = confirm("¿Está seguro de eliminar el registro seleccionado?");

    if(confirm_delete){
        var self = $(this);
        var location_id = self.data('location');
        var jqxhr = $.ajax({
            url: "/admin/locations?format=json",
            method: 'DELETE',
            data: {
                location_id : location_id
            }
        });

        jqxhr.done(function(data){
            self.closest('tr').remove();
        });
    }
}


admin_locations.init = function(){
    $('body').on('click','.delete_location', admin_locations.deleteLocation);    
}


admin_locations.init();