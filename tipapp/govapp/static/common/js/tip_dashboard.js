var tip_dashboard = {
  dt: null,
  var: {
    page: 1,
    page_size: 10,
    thermal_files_url: "/api/thermal-files/",
    data: [],
    breadcrumb: [],
    root: '',
    location: ''
  },

  init: function () {
    const _ = tip_dashboard;
    _.var.page = 1;
    _.var.page_size = 10;
    _.var.root = $("#route_path").val();  
    _.var.location = window.location.href.split("?")[0]
    const params = new URL(document.location.toString()).searchParams;
    const path = params.get("path") ?? "";
    _.var.breadcrumb = path.split("/");

    _.renderBreadcrumb();

    // tip_dashboard.get_pending_imports();
    _.dt = $("#tip_dashboard table").DataTable({
      serverSide: true,
      ajax: function (data, callback, settings) {
        _.get_folder_data(
          {
            page: data && data.start ? data.start / data.length + 1 : 1,
            page_size: data?.length,
            search: data?.search?.value,
            draw: data?.draw,
            route_path: _.var.breadcrumb.filter((b, i) => i > 0).join("/"),
          },
          function (response) {
            const { count, results } = response;
            callback({
              data: results,
              recordsTotal: count,
              recordsFiltered: count,
            });
          },
          function (error) {}
        );
      },
      headerCallback: function (thead, data, start, end, display) {
        $(thead).addClass("table-light");
      },
      drawCallback: function (settings) {},
      columns: [
        {
          title: "Name",
          data: "name",
          render: function (data, type, row) {
            if (!row.is_dir) return utils.markup("span", data);
            const path = row.path.replace(_.var.root, "");
            const href =
              tip_dashboard.var.location +
              "?" +
              utils.make_query_params({ path });

            return utils.markup(
              "a",
              [
                `${data}&nbsp;&nbsp;`,
                utils.markup("i", "", { class: "bi bi-folder " }),
              ],
              {
                href: href,
                class:
                  "btn-folder link-opacity-50-hovericon-link icon-link-hover",
                "data-folder": `${path}${row.name}`,
                style: "--bs-icon-link-transform: translate3d(0, -.125rem, 0);",
              }
            );
          },
        },
        {
          title: "Created at",
          data: "created_at",
        },

        {
          title: "Size",
          data: "size",
          render: function (data, type, row) {
            return utils.markup("span", utils.formatFileSize(data ?? 0));
          },
        },
        {
          title: "Download",
          data: "path",
          render: function (data, type, row) {
            return utils.markup(
              "button",
              { tag: "i", class: "bi bi-download" },
              { class: "btn-download btn btn-outline-dark border border-0" }
            );
          },
        },
      ],
    });
  },

  renderBreadcrumb: function () {
    const breadcrumb = $("#dashboard-breadcrumb");
    breadcrumb.empty();
    const crumbs = tip_dashboard.var.breadcrumb ?? [];
    crumbs.unshift("");
    for (let i = 0; i < crumbs.length; i++) {
      const crumb = crumbs[i];
      const isActive = i === crumbs.length - 1;

      const href = isActive
        ? null
        : tip_dashboard.var.location +
          "?" +
          utils.make_query_params({ path: crumbs.slice(1, i + 1).join("/") });
      
      const options = {
        class: ["breadcrumb-item", isActive ? "active" : ""].join(" "),
        "data-folder": crumbs.slice(0, i + 1).join("/"),
      };
      if (isActive) options["aria-current"] = "page";
      breadcrumb.append(
        utils.markup(
          "li",

          isActive ? crumb : utils.markup("a", crumb || "root", { href }),
          options
        )
      );
    }
  },

  handle_folder_click: function (e) {
    const folder = $(this).data("folder");
    const _ = tip_dashboard;
    _.var.breadcrumb = folder.split("/");
    _.dt.draw(true);
  },

  get_folder_data: function (params, cb_success, cb_error) {
    const defaultParams = {
      page: params?.page ?? tip_dashboard.var.page,
      page_size: params?.page_size ?? tip_dashboard.var.page_size,
      route_path: params?.route_path ?? "",
    };

    const _params = {
      name__icontains: $("#file-name").val(),
    };
    params_str = utils.make_query_params(
      Object.assign({}, _params, defaultParams ?? {})
    );

    $.ajax({
      url:
        tip_dashboard.var.thermal_files_url +
        "list_thermal_folder_contents/?" +
        params_str,
      method: "GET",
      dataType: "json",
      contentType: "application/json",
      success: cb_success,
      error: cb_error,
    });
  },
};
