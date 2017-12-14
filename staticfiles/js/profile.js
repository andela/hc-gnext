$(function() {

    $(".member-remove").click(function() {
        var $this = $(this);

        $("#rtm-email").text($this.data("email"));
        $("#remove-team-member-email").val($this.data("email"));
        $('#remove-team-member-modal').modal("show");

        return false;
    });
    $("#report").click(function () {
        if ($(this).is(":checked")) {
            $("#div1").show();
        } else {
            $("#div1").hide();
        }
    });

});

