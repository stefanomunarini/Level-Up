$(document).ready(function() {
    $('.cloudinary-image input').change(function(event) {
        var elemName = this.name;
        var preview = $('.preview[data_id=' + elemName);
        updatePreview(this.files[0], preview);
    });

    function updatePreview(file, preview) {
        var reader  = new FileReader();

        reader.addEventListener("load", function () {
            preview.attr('src', reader.result);
        }, false);

        if (file) {
            reader.readAsDataURL(file);
        }
    }
});