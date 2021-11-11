$(document).ready(function() {
    $('#view_atten').DataTable( {
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print' , 'colvis'
        ],
        'columnDefs':[
            {
            'targets': [0],
            'visible': false
        }
        ]
    } );
} );