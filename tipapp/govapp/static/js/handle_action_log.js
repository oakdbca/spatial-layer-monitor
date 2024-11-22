var handle_action_log = {
    show_action_log: function(){
        console.log('in show_action_log')

        common_entity_modal.init("Action log", "info");
        common_entity_modal.init_talbe();
        let thead = common_entity_modal.get_thead();
        table.set_thead(thead, {Who:3, What:5, When:4});
        common_entity_modal.get_limit().change(()=>handle_action_log.get_action_log());
        common_entity_modal.get_search().keyup((event)=>{
            if (event.which === 13 || event.keyCode === 13){
                event.preventDefault();
                handle_action_log.get_action_log()
            }
        });
        common_entity_modal.show();

        handle_action_log.get_action_log();
    },
    get_action_log: function(params_str){
        console.log('in get_action_log')
        if(!params_str){
            console.log('in not params_str')
            params = {
                limit:  common_entity_modal.get_limit().val(),
                search: common_entity_modal.get_search().val(),
            }

            params_str = utils.make_query_params(params);
        }
    
        var catalogue_entry_id = $('#catalogue_entry_id').val();

        $.ajax({
            url: kbcatalogue.var.catalogue_data_url+catalogue_entry_id+"/logs/actions/?"+params_str,
            method: 'GET',
            dataType: 'json',
            contentType: 'application/json',
            success: function (response) {
                if(!response || !response.results){
                    table.message_tbody(common_entity_modal.get_tbody(), "No results found");
                    return;
                }
                for(let i in response.results){
                    response.results[i]['when'] = utils.convert_datetime_format(response.results[i].when, kbcatalogue_detail.var.catalogue_table_date_format); 
                    console.log(kbcatalogue_detail.var.catalogue_table_date_format)
                }
                table.set_tbody(common_entity_modal.get_tbody(), response.results, [{username:"text"}, {what:'text'}, {when:'text'}]);
                // common_pagination.init(response.count, params, kbcatalogue_detail.get_action_log, common_entity_modal.get_page_navi());
                common_pagination.init(response.count, params, handle_action_log.get_action_log, common_entity_modal.get_page_navi());
            },
            error: function (error){
                common_entity_modal.show_error_modal(error);
            }
        });
    }
}