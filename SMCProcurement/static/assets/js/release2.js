$(function (){
    $('select[name="request_item_id"]').selectize()
      $.ajax({
          url: '/api/items',
          type: 'GET',
          success: function(options) {
              $('select[name="item_id"]').selectize({
                  valueField: 'id',
                  labelField: 'name',
                  searchField: ['name', 'item_code', 'brand', 'model'],
                  preload: true,
                  options: options.data,
                  create: false,
                  render: {
                      option: function(item, escape) {
                          return '<div>' +
                              '<span class="title">' +
                                '<span class="name">' + escape(item.name) + '</span>' +
                                '<span class="by">(' + escape(item.qty) + ')</span>' +
                              '</span>' +
                              '<ul class="meta">' +
                                  (item.item_code != "None" ? '<li class="item_code">' + escape(item.item_code) + '</li>' : '') +
                                  (item.brand != "None" ? '<li class="brand">' + escape(item.brand) + '</li>' : '') +
                                  (item.model != "None" ? '<li class="model">' + escape(item.model) + '</li>' : '') +
                              '</ul>' +
                            '</div>';
                      }
                  }
              });
          }
      });

      function loadRequestitems(request_id){
          // if(request_id){
              $('select[name="request_item_id"]').selectize()[0].selectize.destroy();
                $('select[name="request_item_id"]').attr("required", "required");
              $.ajax({
                  url: '/api/requests/items?request_id='+request_id,
                  type: 'GET',
                  success: function(options) {
                      $('select[name="request_item_id"]').selectize({
                          valueField: 'id',
                          labelField: 'name',
                          searchField: ['name', 'description', 'unit_price'],
                          preload: true,
                          options: options.data,
                          create: false,
                          render: {
                              option: function(item, escape) {
                                  return '<div>' +
                                      '<span class="title">' +
                                        '<span class="name">' + escape(item.name) + '</span>' +
                                        '<span class="by">(' + escape(item.qty) + ')</span>' +
                                      '</span>' +
                                      (item.description != "None" ? '<span class="description">' + escape(item.description) + '</span>' : '') +
                                    '</div>';
                              }
                          },
                          onChange: function (value){

                          }
                      });
                  }
              });
          // }

      }

      $.ajax({
          url: '/api/requests',
          type: 'GET',
          success: function(options) {
              $('select[name="request_id"]').selectize({
                  valueField: 'id',
                  labelField: 'number',
                  searchField: ['number', 'status_description', 'user'],
                  preload: true,
                  options: options.data,
                  create: false,
                  render: {
                      option: function(request, escape) {
                          return '<div>' +
                              '<span class="title">' +
                                '<span class="name">' + escape(request.number) + '</span>' +
                                '<span class="by">by ' + escape(request.user) + '</span>' +
                              '</span>' +
                              '<ul class="meta">' +
                                  (request.department != "None" ? '<li class="department">' + escape(request.department) + '</li>' : '') +
                                  (request.status_description != "None" ? '<span class="badge badge-pill badge-'+request.status_name+'">' + escape(request.status_description) + '</span></li>' : '') +
                              '</ul>' +
                            '</div>';
                      }
                  },
                  onChange: function (value){
                      loadRequestitems(value)
                  }
              });
          }
      });
  });