$(document).ready(function() {
    $('#res_approve').DataTable( {
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print' , 'colvis'
        ],
        'columnDefs':[
            {
            'targets': [0,2,3],
            'visible': false
        }
        ]
    } );
} );