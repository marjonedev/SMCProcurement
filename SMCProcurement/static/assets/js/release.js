function appendItemToRelease(id, data){
    let str = '<tr id="lines_'+id+'">' +
        '<td>'+data.request+'</td>' +
        '<td>'+data.name+'</td>' +
        '<td>'+data.category+'</td>' +
        '<td>'+data.department+'</td>' +
        '<td class="text-right">'+data.price+'</td>' +
        '<td class="text-right">'+data.qty_needed+'</td>' +
        '<td class="text-right">'+data.qty_available+'</td>' +
        '<td><input class="form-control form-control-sm text-right" id="release_lines-'+id+'-quantity" name="release_lines-'+id+'-quantity" type="number" value="" min="1" max="'+data.qty_needed+'" required></td>' +
        '<td><textarea id="release_lines-'+id+'-remarks" name="release_lines-'+id+'-remarks" class="form-control"></textarea></td>' +
        '<td>' +
        '<input id="release_lines-'+id+'-item_id" name="release_lines-'+id+'-item_id" class="item_id" type="hidden" value="'+data.item_id+'">' +
        '<input id="release_lines-'+id+'-request_id" name="release_lines-'+id+'-request_id" class="request_id" type="hidden" value="'+data.request_id+'">' +
        '<input id="release_lines-'+id+'-request_item_id" name="release_lines-'+id+'-request_item_id" class="request_item_id" type="hidden" value="'+data.id+'">' +
        '<input id="release_lines-'+id+'-department_id" name="release_lines-'+id+'-department_id" class="department_id" type="hidden" value="'+data.department_id+'">' +
        '<button type="button" role="button" class="btn delete btn-danger feather icon-delete"></button>' +
        '</td>' +
        '</tr>';

    $("#releaseItems").find("tbody").append(str);
    $('#addItemModal').modal("hide");
  }

  $(function(){

    $('button#addItem').on('click', function (e){
      e.preventDefault();
      $('#addItemModal').modal("show")
    });

    $('#addItemModal').on('show.bs.modal', function (e) {

        let arr = [];
        $.each($("#releaseItems").find(".request_item_id"), function (i, v){
            arr.push($(v).val())
        });

        $('#searchItemTable').DataTable({
            "ajax": {
                "url": "/api/release_items?except="+arr.join(','),
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
                {"data": "request"},
                {"data": "name"},
                {"data": "category"},
                {"data": "department"},
                {"data": "price", className: "text-right", "render": function (data, type, row, meta){
                        return  "&#8369; "+ data;
                }},
                {"data": "qty_needed", className: "text-right", render: function (data){
                    return data == "None" ? 0 : data;
                }},
                {"data": "qty_available", className: "text-right", render: function (data){
                    return data == "None" ? 0 : data;
                }}
            ],
            "sScrollX": '100%',
            rowCallback: function( row, data, index ) {
                console.log(row, data, index)
                if(data.qty_needed < 1){
                    $(row).hide();
                }
            }
        });
    });

    $('#addItemModal').on('hidden.bs.modal', function (e) {
      $('#searchItemTable').DataTable().clear().destroy();
      $('.new-error').text("").hide();
    });

    $(document).on("click", ".select-item", function (e){
        e.preventDefault();
        let id = $(this).data("id");
        let data = $(this).closest("tr").find(".item-data").val();
        data = JSON.parse(data);
        appendItemToRelease(id, data);
    });

    $("#searchExistingForm").on("submit", function(e){ e.preventDefault(); return false; });

    $(document).on('click', 'button.delete', function (e){
        e.preventDefault();
        $(this).closest("tr").remove();
    });

    $(".flatpickr").flatpickr({
      minDate: "today",
      altInput: true,
      defaultDate: "today",
      altFormat: "F j, Y",
      dateFormat: "Y-m-d"
    });



  });