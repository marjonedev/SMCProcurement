function loadSelectCategory(){
    $.ajax({
        url: '/api/categories',
        type: 'GET',
        success: function(options) {
            $('select[name="category_id"]').selectize({
                valueField: 'id',
                labelField: 'name',
                searchField: 'name',
                preload: true,
                options: options,
                create: false,
            });
        }
    });
}
function loadSelectSupplier(){
    $.ajax({
        url: '/api/suppliers',
        type: 'GET',
        success: function(options) {
            $('select[name="supplier_id"]').selectize({
                valueField: 'id',
                labelField: 'name',
                searchField: 'name',
                preload: true,
                options: options,
                create: false,
            });
        }
    });
}

function appendItemToInventory(id, data){
        let item_code = data.item_code == "None" ? "" : data.item_code;
        let brand = data.brand == "None" ? "" : data.brand;
        let model = data.model == "None" ? "" : data.model;
        const purchased_date = (data.purchased_date == "None" || data.purchased_date == "")  ? '' : DateTime.fromISO(data.purchased_date).setLocale('us').toFormat("LLLL dd, yyyy");
        let str = '<tr id="lines_'+id+'">' +
            '<td>'+data.name+'</td>' +
            '<td>'+data.category+'</td>' +
            '<td>'+item_code+'</td>' +
            '<td>'+brand+'</td>' +
            '<td>'+model+'</td>' +
            '<td>'+ purchased_date +'</td>' +
            '<td class="text-right">&#8369; '+data.unit_price+'</td>' +
            '<td><input class="form-control form-control-sm text-right" id="inventory_items-'+id+'-unit_price" name="inventory_items-'+id+'-qty" type="number" value="" required></td>' +
            '<td>' +
            '<input id="inventory_items-'+id+'-id" name="inventory_items-'+id+'-item_id" type="hidden" value="'+id+'">' +
            '<button type="button" role="button" class="btn delete btn-danger feather icon-delete"></button>' +
            '</td>' +
            '</tr>';

        $("#inventoryItems").find("tbody").append(str);
        $('#addItemModal').modal("hide");
    }

$(function(){

    $('button#addItem').on('click', function (e){
      e.preventDefault();
      $('#addItemModal').modal("show")
    });

    $('#addItemModal').on('show.bs.modal', function (e) {
        $('#searchItemTable').DataTable({
            "ajax": {
                "url": "/api/items",
                "dataType": "json",
                "method": "POST",
                "dataSrc": "data",
                "contentType":"application/json"
            },
            "columns": [
                {"data": "id", "render": function (data, type, row, meta){
                    str = "<input class='item-data' type='hidden' value='"+JSON.stringify(row)+"'>";
                    str += "<button class='btn btn-dark btn-sm select-item' data-id='"+data+"'>Select</button>";
                    return str
                }},
                {"data": "name"},
                {"data": "category"},
                {"data": "description", "visible": false, "searchable": true},
                {"data": "item_code", render: function (data){
                    return data == "None" ? "" : data;
                }},
                {"data": "brand", "visible": false, "searchable": true},
                {"data": "model", "visible": false, "searchable": true},
                {"data": "unit_price", className: "text-right", "render": function (data, type, row, meta){
                        return  "&#8369; "+ data;
                }},
                {"data": "purchased_date", "render": function (data, type, row, meta){
                    return data == "None" ? "" : DateTime.fromISO(data).setLocale('us').toFormat("LLLL dd, yyyy");
                }},
                {"data": "serial", "visible": false, "searchable": true},
                {"data": "supplier"},
                {"data": "qty", className: "text-right", render: function (data){
                    return data == "None" ? 0 : data;
                }}
            ],
            "sScrollX": '100%'
        });
    });

    $('#addItemModal').on('hidden.bs.modal', function (e) {
      $('#searchItemTable').DataTable().clear().destroy();
      $('#createNewItemForm').trigger("reset");
      $('#existingItemTab').tab('show');
      $('.new-error').text("").hide();
    });

    $('a.new-item-tab[data-toggle="pill"]').on('shown.bs.tab', function (e) {
        $('input[name=is_existing]').val($(e.target).data('existing'))
    });

    $(document).on("click", ".select-item", function (e){
        e.preventDefault();
        let id = $(this).data("id");
        let data = $(this).closest("tr").find(".item-data").val();
        data = JSON.parse(data);
        appendItemToInventory(id, data);
    });

    $("#searchExistingForm").on("submit", function(e){ e.preventDefault(); return false; });

    $(document).on('click', 'button.delete', function (e){
        e.preventDefault();
        $(this).closest("tr").remove();
    });

    $("#createNewItemForm").on('submit', function (e){
        e.preventDefault();
        let $this = $(this);
        let data = {};
        $.each($this.serializeArray(), function(i, field) {
            data[field.name] = field.value;
        });
        data["create_item"] = 1;

        $.ajax({
            url: '/api/items/create',
            data: data,
            type: "POST",
            success: function(response){
                if(response.status == "success"){
                    appendItemToInventory(response.data.id, response.data);
                }
            },
            error: function (response){
                let data = response.responseJSON;
                if(data.status == "error"){
                    $('.new-error').text(data.message).show();
                }
            }
        });

        return false;
    });
});