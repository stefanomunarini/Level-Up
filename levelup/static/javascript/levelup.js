$(document).ready(function() {
    $('#id_profile_picture').change(function(event) {
        updatePreview(this.files[0]);
    });

    function updatePreview(file) {
        var preview = $('.profile-pic img');
        var reader  = new FileReader();

        reader.addEventListener("load", function () {
            preview.attr('src', reader.result);
        }, false);

        if (file) {
            reader.readAsDataURL(file);
        }
    }
});