(function($) {

    function printUrl(viewer, page_url) {

        var image = viewer.tileSources[0]; // get image object
        var zoom = viewer.viewport.getZoom(); // get zoom level
        var size = new OpenSeadragon.Rect(0, 0, image.width, image.height); // build osd rect
        var container = viewer.viewport.getContainerSize(); // get size of osd window?
        var fit_source = fitWithinBoundingBox(size, container); // returns OSD.Point
        var total_zoom = fit_source.x / image.width; // compute zoom factor for scaled dimensions?
        var container_zoom = fit_source.x / container.x; // ???
        var level =  (zoom * total_zoom) / container_zoom; // ???
        var box = getDisplayRegion(
            viewer,
            new OpenSeadragon.Point(
                parseInt(image.width * level),
                parseInt(image.height*  level)
             )
        ); // compute displayed region
        var scaledBox = new OpenSeadragon.Rect(
            parseInt(box.x / level),
            parseInt(box.y / level),
            parseInt(box.width / level),
            parseInt(box.height / level)
        ); // ???
        var d = fitWithinBoundingBox(
            box, new OpenSeadragon.Point(681, 817)
        ); // ???
        return page_url + 'print/image_' + d.x + 'x' + d.y + '_from_' +  scaledBox.x + ',' + scaledBox.y + '_to_' + scaledBox.getBottomRight().x + ',' + scaledBox.getBottomRight().y;
    }

    function fitWithinBoundingBox(size, container) {
        if (size.width / size.height > container.x / container.y) {
            return new OpenSeadragon.Point(
                container.x,
                parseInt(size.height * container.x/ size.width)
            );
        } else {
            return new OpenSeadragon.Point(
                parseInt(size.width * container.y / size.height),
                container.y
            );
        }
    }

    function getDisplayRegion(viewer, source) {
        // Determine portion of scaled image that is being displayed
        var box = new OpenSeadragon.Rect(0, 0, source.x, source.y);
        var container = viewer.viewport.getContainerSize();
        var bounds = viewer.viewport.getBounds();
        // If image is offset to the left
        if (bounds.x > 0){
            box.x = box.x - viewer.viewport.pixelFromPoint(new OpenSeadragon.Point(0,0)).x;
        }
        // If full image doesn't fit
        if (box.x + source.x > container.x) {
            box.width = container.x - viewer.viewport.pixelFromPoint(new OpenSeadragon.Point(0,0)).x;
            if (box.width > container.x) {
                box.width = container.x;
            }
        }
        // If image is offset up
        if (bounds.y > 0) {
            box.y = box.y - viewer.viewport.pixelFromPoint(new OpenSeadragon.Point(0,0)).y;
        }
        // If full image doesn't fit
        if (box.y + source.y > container.y) {
            box.height = container.y - viewer.viewport.pixelFromPoint(new OpenSeadragon.Point(0,0)).y;
            if (box.height > container.y) {
                box.height = container.y;
            }
        }
        return box;
    }

    function addOverlay(viewer, x1, y1, x2, y2) {
        var div = document.createElement("div");
        var rect = new OpenSeadragon.Rect(x1, y1, x2, y2);
        div.className = "overlay";
        viewer.addOverlay(div, rect);
    }

    function addOverlays(viewer, coordinates_url) {
        var params = $.deparam.fragment();
        var words = params["words"] || "";
        $.getJSON(coordinates_url, function(all_coordinates) {
            var scale = 1 / all_coordinates["width"];
            $.each(words.split(" "), function(index, word) {
                if (word !== "") {
                    var coordinates = all_coordinates["coords"][word];
                    if(coordinates !== undefined){
                        $.each(coordinates, function(index, value) {
                            addOverlay(viewer,
                                       value[0]*scale,
                                       value[1]*scale,
                                       value[2]*scale,
                                       value[3]*scale);
                        });
                    }
                }
            });
        });
    }

    function initPage() {

        var $page_data = $('#page_data');
        var width = $page_data.data("width");
        var height = $page_data.data("height");
        var page_url = $page_data.data("page_url");
        var static_url = $page_data.data("static_url");
        var iiif_url = $page_data.data("iiif_url");
        var coordinates_url = $page_data.data("coordinates_url");

        var viewer = OpenSeadragon({
            id: "viewer_container",
            prefixUrl:          static_url,
            showNavigator:      false,
            minZoomLevel:       1,
            defaultZoomLevel:   1,
            tileSources:   [{
                              "@context": "http://iiif.io/api/image/2/context.json",
                              "@id": iiif_url,
                              "height": height,
                              "width": width,
                              "profile": [ "http://iiif.io/api/image/2/level2.json" ],
                              "protocol": "http://iiif.io/api/image",
                              "tiles": [{
                                "scaleFactors": [ 1, 2, 4, 8, 16, 32 ],
                                "width": 1024
                              }]
                            }]
        });

        viewer.addHandler("open", addOverlays(viewer, coordinates_url));

        $('#clip').on('click', function(e){
           window.open(printUrl(viewer, page_url));
           e.preventDefault();
           return false;
        });

    }

    $(initPage);


})(jQuery);
