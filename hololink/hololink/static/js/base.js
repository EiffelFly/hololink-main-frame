$(document).ready(function () {
    $("#filter-mail-job").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#table-mail-job tbody tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

function setLanguage(language) {
    $.ajax({
        type: "POST",
        url: "{% url 'set_language' %}",
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            language: language,
        },
        success: function () {
            location.reload();
        }
    });
};