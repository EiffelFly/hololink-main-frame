$(document).ready(function () {
    $("#filter-article").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#table-article tbody tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});
