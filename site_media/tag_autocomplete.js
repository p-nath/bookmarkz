$(function() {
    $("#tags").autocomplete({
        source: "/api/tag_autocomplete/",
    });
});