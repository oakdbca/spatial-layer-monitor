var kbcatalogue_attribute = { 
    var: { 
         catalogue_attribute_url: "/api/catalogue/layers/attributes/",
         catalogue_attribute_type_url: "/api/catalogue/layers/attribute/type",
    },
    init_catalogue_attribute: function() {
        $( "#catalogue-attribute-limit" ).change(()=>table.refresh(this.get_catalogue_attribute));
        $( "#catalogue-attribute-order-by" ).change(()=>table.refresh(this.get_catalogue_attribute));
        $( "#catalogue-attribute-new-btn" ).click(function() {
            kbcatalogue_attribute.show_new_attribute_modal();
        });
        $( "#catalogue-attribute-order" ).on('input',function(){
            $(this).val($(this).val().replace(/\D/g, ""));
        });
        $("#log_actions_show" ).click(handle_action_log.show_action_log);

        var has_edit_access = $('#has_edit_access').val();
        if (has_edit_access == 'True') {
            kbcatalogue_attribute.var.has_edit_access = true;
        }

        // catalogue-attribute-type
        this.retrieve_att_types(()=>table.refresh(this.get_catalogue_attribute));
    },
    retrieve_att_types: function(post_callback){
        $.ajax({
            url: kbcatalogue_attribute.var.catalogue_attribute_type_url,
            type: 'GET',
            contentType: 'application/json',
            success: (response) => {
                var att_type = {}
                for(let i in response){
                    const type = response[i];
                    att_type[type.key] = type.name;
                }
                kbcatalogue_attribute.var.catalogue_attribute_type = att_type;
                post_callback();
            },
            error: (error)=> {
                common_entity_modal.show_alert("An error occured while getting catalogue attribute type.");
                // console.error(error);
            },
        });
    },
    show_new_attribute_modal: function(){
        common_entity_modal.init("New Attribute", "submit");
        let name_id = common_entity_modal.add_field(label="Name", type="text");
        let type_id = common_entity_modal.add_field(label="Type", type="select", value=null, option_map=this.var.catalogue_attribute_type);
        let order_id = common_entity_modal.add_field(label="Order", type="number");
        common_entity_modal.add_callbacks(submit_callback=(success_callback, error_callback)=> 
                                            this.write_catalogue_attribute(success_callback, error_callback, name_id, type_id, order_id),
                                            success_callback=()=>table.refresh(this.get_catalogue_attribute));
        common_entity_modal.show();
    },
    show_update_attribute_modal: function(att){
        common_entity_modal.init("Update Attribute", "submit");
        let name_id = common_entity_modal.add_field(label="Name", type="text", value=att.name);
        let type_id = common_entity_modal.add_field(label="Type", type="select", value=att.type, option_map=this.var.catalogue_attribute_type);
        let order_id = common_entity_modal.add_field(label="Order", type="number", value=att.order);
        common_entity_modal.add_callbacks(submit_callback=(success_callback, error_callback)=> 
                                            this.write_catalogue_attribute(success_callback, error_callback, name_id, type_id, order_id, att.id),
                                            success_callback=()=>table.refresh(this.get_catalogue_attribute));
        common_entity_modal.show();
    },
    show_delete_attribute_modal: function(att){
        common_entity_modal.init("Delete Attribute", "delete");
        common_entity_modal.add_field(label="Name", type="text", value=att.name);
        common_entity_modal.add_field(label="Type", type="select", value=att.type, option_map=this.var.catalogue_attribute_type);
        common_entity_modal.add_field(label="Order", type="number", value=att.order);
        common_entity_modal.add_callbacks(submit_callback=(success_callback, error_callback)=> 
                                            this.delete_catalogue_attribute(success_callback, error_callback, att.id),
                                            success_callback=()=>table.refresh(this.get_catalogue_attribute));
        common_entity_modal.show();
    },
    write_catalogue_attribute: function(success_callback, error_callback, name_id, type_id, order_id, att_id) {
        // get & validation check
        let name = utils.validate_empty_input('name', $('#'+name_id).val());
        let type = utils.validate_empty_input('type', $('#'+type_id).val());
        let order = utils.validate_empty_input('order', +$('#'+order_id).val());
        utils.validate_number('order', order);
        
        // set request
        let post_data = {
            name:   name,
            type:   type,
            order:  order,
            catalogue_entry: $('#catalogue_entry_id').val()
        };
        let csrf_token = $("#csrfmiddlewaretoken").val();
        let url = kbcatalogue_attribute.var.catalogue_attribute_url;
        let method = 'POST';
        if(att_id){
            url += att_id+'/'
            method = 'PUT';
        }
        
        $.ajax({
            url: url,
            type: method,
            headers: {'X-CSRFToken' : csrf_token},
            data: JSON.stringify(post_data),
            contentType: 'application/json',
            success: success_callback,
            error: error_callback
        });
    },
    get_catalogue_attribute: function(params_str) {
        if (!params_str){
            params = {
                catalogue_entry__in:       $('#catalogue_entry_id').val(),
                limit:                     $('#catalogue-attribute-limit').val(),
                order_by:                  $('#catalogue-attribute-order-by').val()
            }
            
            params_str = utils.make_query_params(params);
        }

        $.ajax({
            url: kbcatalogue_attribute.var.catalogue_attribute_url+"?"+params_str,
            method: 'GET',
            dataType: 'json',
            contentType: 'application/json',
            success: function (response) {
                if (response != null) {
                    if(!response){
                        $('#catalogue-attribute-tbody').html("<tr><td colspan='7' class='text-center'>No results found</td></tr>");
                        return;
                    }

                    let buttons = {};
                    if(kbcatalogue_attribute.var.has_edit_access){
                        buttons = {Update:(att)=>kbcatalogue_attribute.show_update_attribute_modal(att),
                                   Delete:(att)=>kbcatalogue_attribute.show_delete_attribute_modal(att)};
                    }

                    for(let i in response.results){
                        response.results[i].type_str = kbcatalogue_attribute.var.catalogue_attribute_type[response.results[i].type];
                    }

                    table.set_tbody($('#catalogue-attribute-tbody'), response.results,
                                    columns=[{id:"text"}, {name:"text"}, {type_str:"text"}, {order:"text"}],
                                    buttons=buttons);

                    common_pagination.init(response.count, params, kbcatalogue_attribute.get_catalogue_attribute, $('#paging_navi'));

                    // $('#catalogue-attribute-tbody').empty();
                    // if (response.results.length > 0) {
                    //     for (let i = 0; i < response.results.length; i++) {
                    //         let att = response.results[i];
                    //         let btn_update_id = 'btn-update-attribute_'+i;
                    //         let btn_delete_id = 'btn-delete-attribute_'+i;
                    //         let row = $("<tr>");
                    //         row.append("<td>"+att.id+"</td>");
                    //         row.append("<td>"+att.name+"</td>");
                    //         row.append("<td>"+att.type+"</td>");
                    //         row.append("<td>"+att.order+"</td>");
                    //         if(kbcatalogue_attribute.var.has_edit_access){
                    //             row.append("<td>" +
                    //                         "<button class='btn btn-primary btn-sm' id='"+btn_update_id+"'>Update</button> " + 
                    //                         "<button class='btn btn-primary btn-sm' id='"+btn_delete_id+"'>Delete</button>" +
                    //                         "</td");
                    //         } else {
                    //             row.append("<td></td>");
                    //         }
                    //         $('#catalogue-attribute-tbody').append(row);
                            
                    //         $('#'+btn_update_id).click(()=> kbcatalogue_attribute.show_update_attribute_modal(att));
                    //         $('#'+btn_delete_id).click(()=> kbcatalogue_attribute.show_delete_attribute_modal(att));
                    //     }
                                           
                    //     $('.publish-table-button').hide();

                    //     common_pagination.init(response.count, params, kbcatalogue_attribute.get_catalogue_attribute, +params.limit, $('#paging_navi'));

                    // } else {
                    //     $('#catalogue-attribute-tbody').html("<tr><td colspan='7' class='text-center'>No results found</td></tr>");
                    // }
                } else {
                      $('#catalogue-attribute-tbody').html("<tr><td colspan='7' class='text-center'>No results found</td></tr>");
                }      
            },
            error: function (error) {
                $('#delete-popup-error').html("Error Loading catalogue attribute data");
                $('#delete-popup-error').show();
                $('#catalogue-attribute-tbody').html('');

                console.log('Error Loading catalogue attribute data');
            },
        });    
    },
    delete_catalogue_attribute: function(success_callback, error_callback, att_id){
        $.ajax({
            url: kbcatalogue_attribute.var.catalogue_attribute_url+att_id,
            headers: {'X-CSRFToken' : $("#csrfmiddlewaretoken").val()},
            type: 'DELETE',
            success: success_callback,
            error: error_callback
        });
    },
}