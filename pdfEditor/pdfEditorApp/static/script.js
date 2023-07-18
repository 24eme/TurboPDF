$(document).ready(function() {
    $('#pdf-input').change(function(e) {
        var file = e.target.files[0];
        var fileReader = new FileReader();

        fileReader.onload = function() {
            var typedarray = new Uint8Array(this.result);
            PDFJS.getDocument(typedarray).then(function(pdf) {
                pdf.getPage(1).then(function(page) {
                    var scale = 1.5;
                    var viewport = page.getViewport({ scale: scale });

                    var canvas = document.createElement('canvas');
                    var context = canvas.getContext('2d');
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;

                    var renderContext = {
                        canvasContext: context,
                        viewport: viewport
                    };

                    page.render(renderContext).then(function() {
                        $('#pdf-container').empty();
                        $('#pdf-container').append(canvas);
                    });
                });
            });
        };

        fileReader.readAsArrayBuffer(file);
    });
});
