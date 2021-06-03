function getRandomID(){
    return Math.floor(100000 + Math.random() * 900000)
}

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

function appendItemToRequest(data){
  const id = getRandomID();

  let str = '<tr id="lines_'+id+'">' +
      '<td>'+data.name+'</td>' +
      '<td>'+data.category+'</td>' +
      '<td>'+data.description+'</td>' +
      '<td class="text-right"><input class="form-control-sm form-control-plaintext text-right price" id="request_lines-'+id+'-unit_price" name="request_lines-'+id+'-unit_price" type="number" value="'+data.unit_price+'" readonly></td>' +
      '<td class="text-right"><input class="form-control form-control-sm text-right qty" id="request_lines-'+id+'-qty" name="request_lines-'+id+'-qty" type="number" value="" required></td>' +
      '<td class="text-right"><input type="text" name="request_lines-'+id+'-total" class="form-control-sm form-control-plaintext text-right total" readonly value="0.00"></td>' +
      '<td>' +
      '<input class="item_id" id="request_lines-'+id+'-item_id" name="request_lines-'+id+'-item_id" type="hidden" value="'+data.id+'">' +
       '<button type="button" role="button" class="btn delete btn-danger feather icon-delete"></button>' +
      '</td>' +
      '</tr>';

  $("#requestItems").find("tbody").append(str);
  $('#addItemModal').modal("hide");
}

$(function(){

    $(".flatpickr").flatpickr({
        minDate: "today",
        altInput: true,
        defaultDate: "today",
        altFormat: "F j, Y",
        dateFormat: "Y-m-d"
    });

    $('button#addItem').on('click', function (e){
      e.preventDefault();
      $('#addItemModal').modal("show")
    });

    $('#addItemModal').on('show.bs.modal', function (e) {
        let arr = [];
        $.each($("#requestItems").find(".item_id"), function (i, v){
            arr.push($(v).val())
        });
        $('#searchItemTable').DataTable({
          "ajax": {
              "url": "/api/items?except="+arr.join(','),
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
              {"data": "name", width: "120px", className: "column-wrap"},
              {"data": "category", width: "125px", className: "column-wrap"},
              {"data": "description", width: "200px", className: "column-wrap"},
              {"data": "brand", width: "100px", className: "column-wrap"},
              {"data": "model", width: "100px", className: "column-wrap"},
              {"data": "unit_price", className: "text-right", "render": function (data, type, row, meta){
                  return  "&#8369; "+ data;
              }},
              {"data": "purchased_date", render: function (data){
                  return data == "None" ? "" : data;
              }, "visible": false, "searchable": true},
              {"data": "item_code", render: function (data){
                  return data == "None" ? "" : data;
              }, "visible": false, "searchable": true},
              {"data": "serial", "visible": false, "searchable": true},
              {"data": "supplier", "visible": false, "searchable": true}
          ],
          "ordering": false,
          "sScrollX": "100%"
      });
    });
    $('#addItemModal').on('shown.bs.modal', function (e) {
        $.fn.dataTable.tables({ visible: true, api: true }).columns.adjust().draw();
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
        let data = $(this).closest("tr").find(".item-data").val();
        data = JSON.parse(data);
        appendItemToRequest(data);
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
                    appendItemToRequest(response.data);
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

    $(document).on('click', 'button.delete', function (e){
        e.preventDefault();
        let $this = $(this)
        $this.closest("tr").remove();
    });

    $(document).on('change', 'input.qty, input.price', function (){
        let $this = $(this);
        let a = $this.val();
        let b;

        if($this.hasClass('qty')){
          b = $this.closest('tr').find('input.price').val()
        }else{
          b = $this.closest('tr').find('input.qty').val()
        }

        a = isNaN(parseFloat(a)) ? 0 : a;
        b = isNaN(parseFloat(b)) ? 0 : b;

        $this.closest('tr').find('input.total').val(get_total(a, b).toFixed(2));
    });
});