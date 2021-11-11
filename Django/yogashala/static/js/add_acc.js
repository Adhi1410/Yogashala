$(document).ready(function(){
    var dataTable = $('#filtertable').DataTable({
        "pageLength" : 3,
        'aoColumnDefs':[{
            'bSortable' : false,
            'aTargets':['nosort'],
        }],
        columnDefs: [
            {type: 'dd-mm-yyyy',aTargets:[2]}
        ],
        "aoColumns" :[
            null,
            null,
            null,
        ],
        "order":false,
        "bLengthChange": false,
        "dom":'<"top">ct<"top"p><"clear">'

    });
    $("#filterbox").keyup(function(){
        dataTable.search(this.value).draw();
    });
});