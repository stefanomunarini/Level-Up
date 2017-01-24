{% load i18n %}
$(function() {
    var title = "{{ title }}";
    var titleY1 = "{{ titleY1 }}";
    var titleY2 = "{{ titleY2 }}";
    var data1 = {% firstof data1 "[]" %};
    var data2 = {% firstof data2 "[]" %};
    var color1 = "{% firstof col1 "#008CBA" %}";
    var color2 = "{% firstof col2 "#43AC6A" %}";

    var steps = 5;

    var max1 = Math.max.apply(Math,data1.map(function(o){return o.y;}));
    max1 = Math.ceil(Math.max(steps,max1) / steps)*steps;
    var max2 = Math.max.apply(Math,data2.map(function(o){return o.y;}));
    max2 = Math.ceil(Math.max(steps,max2) / steps)*steps;

    var fontFamily = "Helvetica";
    var markerType = "none";
    var lineThickness = 5;
    var gridColor = "#e7e7e7";

    $("{{ elem }}").CanvasJSChart({
        title:{
            text: title,
            fontFamily: fontFamily,
            fontSize: 24,
        },
        legend:{
            fontFamily: fontFamily,
        },
        axisX:{
            valueFormatString: "####",
            interval: 1,
            titleFontFamily: fontFamily,
            titleFontSize: 24,
            labelFontFamily: fontFamily,
            labelFontSize: 16,
            lineThickness: 0,
            lineColor: "#000000",
            labelFontColor: "#000000",

        },
        {% if data1 %}
            axisY:{
                title: titleY1,
                titleFontFamily: fontFamily,
                titleFontSize: 24,
                labelFontFamily: fontFamily,
                labelFontSize: 16,
                lineColor: color1,
                titleFontColor: color1,
                labelFontColor: color1,
                lineThickness: 0,
                gridThickness: 1,
                gridColor: gridColor,
                tickLength: 5,
                tickColor: color1,
                tickThickness: 1,
                maximum: max1,
                interval: max1 / steps,
            },
        {% endif %}
        {% if data2 %}
            axisY2:{
                title: titleY2,
                titleFontFamily: fontFamily,
                titleFontSize: 24,
                labelFontFamily: fontFamily,
                labelFontSize: 16,
                lineColor: color2,
                titleFontColor: color2,
                labelFontColor: color2,
                lineThickness: 0,
                gridThickness: 0,
                gridColor: gridColor,
                tickLength: 5,
                tickColor: color2,
                tickThickness: 1,
                maximum: max2,
                interval: max2 / steps,
            },
        {% endif %}
        data: [
            {% if data1 %}
                {
                    type: "line",
                    xValueFormatString: "####",
                    color: color1,
                    dataPoints: data1,
                    markerType: markerType,
                    lineThickness: lineThickness,
                },
            {% endif %}
            {% if data2 %}
                {
                    type: "line",
                    axisYType: "secondary",
                    xValueFormatString: "####",
                    color: color2,
                    dataPoints: data2,
                    markerType: markerType,
                    lineThickness: lineThickness,
                }
            {% endif %}
        ]
    });
});
