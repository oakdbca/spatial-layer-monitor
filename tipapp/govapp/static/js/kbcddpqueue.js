var kbcddpweb = { 
    var: {
        cddpqueue_list:"/api/publish/cddp-contents/"
    },
    init_dashboard: function() { 
        $( "#cddp-queue-limit" ).change(function() {
            common_pagination.var.current_page=0;
            kbcddpweb.get_cddpqueue();
        });

        kbcddpweb.get_cddpqueue();
    },
    set_tbody: function (tbody, list, columns, buttons=null){
        tbody.empty();

        for(let i in list){
            let row = this._make_row(list[i], columns);
            if(buttons){
                row.append(this._make_button_cell(buttons, tbody.attr("id")+'-row-'+i, list[i]));
            }
            tbody.append(row);
        }
    },
    get_cddpqueue: function(params_str){
        if (!params_str){
            params = {
                limit: $('#cddp-queue-limit').val(),
            }

            params_str = utils.make_query_params(params);
        }

        const tbody = $('#cddp-queue-tbody');
        let url = kbcddpweb.var.cddpqueue_list;
        url += "?limit="+$('#cddp-queue-limit').val();
        url += "&offset="+0; 
        
        $.ajax({
            url: kbcddpweb.var.cddpqueue_list+"?"+params_str,
            method: 'GET',
            dataType: 'json',
            contentType: 'application/json',
            headers: {'X-CSRFToken' : $("#csrfmiddlewaretoken").val()},
            success: (response) => {
                for(let i in response.results){
                    if(response.results[i].status == 'FAILED') response.results[i].success = false;
                    else if(response.results[i].status == 'PUBLISHED') response.results[i].success = true;
                    else response.results[i].success = null;
                }

                tbody.empty()
                for(let i in response.results){
                    let filepath_html = '<td class="fielpath"><a style="text-decoration: none;" href="/api/publish/cddp-contents/retrieve-file/?filepath=' + response.results[i]['filepath'] + '">' + response.results[i]['filepath'] + '</a></td>'
                    let created_at_html = '<td class="created_at">' + response.results[i]['created_at'] + '</td>'
                    let size_html = '<td>' + response.results[i]['size_kb'] + '</td>'
                    let row = '<tr data-filepath="' + response.results[i]['filepath'] + '">' + filepath_html + created_at_html + size_html + '</tr>'
                    tbody.append(row)
                }

                if(response.results == 0){
                    table.message_tbody(tbody, "No results found");
                }
                common_pagination.init(response.count, params, kbcddpweb.get_cddpqueue, $('#paging_navi'));
            },
            error: (error)=> {
                table.message_tbody(tbody, "No results found");
                common_entity_modal.show_alert("An error occured while getting cddp queue.");
            },
        });
    },
}
