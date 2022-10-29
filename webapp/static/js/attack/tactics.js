var TableExample = function () {

    var handleRecords = function () {
        var table = new Datatable();
        //debugger;

        table.init({
            src: $("#example"),
            onSuccess: function (table) {
                // execute some code after table records loaded
            },
            onError: function (table) {
                // execute some code on network or other general error
            },
            onDataLoad: function (table) {
                // execute some code on ajax data load
            },
            dataTable: {
                "responsive": true,
                "lengthChange": false,
                "autoWidth": true,
                "dom": 'Bfrtip',
                "buttons": ["copy", "csv", "excel", "pdf", "print", "colvis"],
                "pageLength": 25,//每页显示数据
                "bProcessing": true, //显示数据加载中\
                ajax: '/attack/tactics/data/',
                columns: [
                    { data: 'name' },
                    { data: 'position' },
                    { data: 'office' },
                    { data: 'salary' },
                    { data: 'salary' },
                    { data: 'salary' },
                    { data: 'salary' },
                    {
                        "className": 'dt-control',
                        "orderable": false,
                        "data": null,
                        "defaultContent": '<a class="btn btn-info btn-sm" href="#"> <i class="fas"> </i>查看 </a>',
                    },
                    {"data": null, "sClass": "center",
                                "fnCreatedCell": function (nTd, sData, oData, iRow, iCol) {
                                    var element = $(nTd).empty();
                                    var remove = $('<a href="javascript:;" class="btn btn-danger btn-sm"> <i class="fas fa-trash"> </i>删除 </a>');

                                    element.append(remove);
                                    remove.on('click', function () {
                                        var $tr = $(this).parents('tr');
                                        var con = confirm("确定删除？");
                                        if (con) {
                                            console.log(oData["id"]);
                                            $.get("/attack/tactics/delete/" + oData["id"] + "/", function (data) {
                                                if (data.success) {
                                                    $.growlService("删除成功", {type: "success"});
                                                    $tr.remove();
                                                } else {
                                                    $.growlService("删除失败", {type: "danger"})
                                                }
                                            });
                                        }
                                    });
                                }
                            }
                ],
                "fnRowCallback": function (nRow, aData, iDisplayIndex) {// 当创建了行，但还未绘制到屏幕上的时候调用，通常用于改变行的class风格

                },
                "fnInitComplete": function (oSettings, json) { //表格初始化完成后调用 在这里和服务器分页没关系可以忽略

                }

            }
        });
        function format(d) {
        // `d` is the original data object for the row
        return (
            '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
            '<tr>' +
            '<td>Full name:</td>' +
            '<td>' +
            d.name +
            '</td>' +
            '</tr>' +
            '<tr>' +
            '<td>Extension number:</td>' +
            '<td>' +
            d.extn +
            '</td>' +
            '</tr>' +
            '<tr>' +
            '<td>Extra info:</td>' +
            '<td>And any further details here (images etc)...</td>' +
            '</tr>' +
            '</table>'
        );
    }
    // Add event listener for opening and closing details
    $('#example tbody').on('click', 'td.dt-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
    };

    var handleDatePickers = function () {

        if (jQuery().datepicker) {
            $('.date-picker').datepicker({
                rtl: Metronic.isRTL(),
                orientation: "left",
                autoclose: true,
                format: "yyyy-mm-dd"
            });
            //$('body').removeClass("modal-open"); // fix bug when inline picker is used in modal
        }

        /* Workaround to restrict daterange past date select: http://stackoverflow.com/questions/11933173/how-to-restrict-the-selectable-date-ranges-in-bootstrap-datepicker */
    };


    return {

        //main function to initiate the module
        init: function () {
            handleRecords();
            handleDatePickers();
        }

    };

}();
