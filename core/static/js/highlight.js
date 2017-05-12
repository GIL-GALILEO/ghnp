(function($) {

    function add_highlights(image) {
        if (image.data('highlighted') == true) {
            return
        }
        var width = image.width();
        var height = image.height();    
        if (width > 0 && height > 0) {
            image.data('highlighted', true);
            var id = image.data('id');
            var words = image.data('words');
            var url = id+'coordinates/';
            $.getJSON(url, function(all_coordinates) {
                image.wrap('<div class="highlight_words" style="display: inline-block; position: relative; margin: 0px; padding: 0px; height: auto; width: auto;" />');
                var div = image.parents("div.highlight_words");
		        div.wrap('<div style="text-align: center" />');
                var vScale = 100 / all_coordinates["height"];
                var hScale = 100 / all_coordinates["width"];
                $.each(words.split(" "), function(index, word) {
                    var coordinates = all_coordinates["coords"][word];
                    for (var k in coordinates) {
                        var v = coordinates[k];
                        div.append("<div class='overlay' style='position: absolute; " +
                            'top: ' + (v[1] * vScale) + '%; ' +
                            'left: ' + (v[0] * hScale) + '%; ' +
                            'height: ' + (v[3] * vScale) + '%; ' +
                            'width: ' + (v[2] * hScale) + "%;' />");
                    }
                });
            });
        }
    }

    function init() {
        var highlight_words = $("img.highlight_words");
        highlight_words.load(function() {
            add_highlights($(this));
        });
        highlight_words.each(function() {
            if (this.complete) {
		        add_highlights($(this));
	        }
	    });
    }

    $(init);

})(jQuery);
