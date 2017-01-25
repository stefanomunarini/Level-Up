{% load i18n %}
$(function() {
    var dataLeft = JSON.parse("{% firstof chart.y_left.data|escapejs "[]" %}");
    var dataRight = JSON.parse("{% firstof chart.y_right.data|escapejs "[]" %}");

    var steps = 5;

    var maxLeft = Math.max.apply(Math,dataLeft.map(function(o){return o.y;}));
    maxLeft = Math.ceil(Math.max(steps,maxLeft) / steps)*steps;
    var maxRight = Math.max.apply(Math,dataRight.map(function(o){return o.y;}));
    maxRight = Math.ceil(Math.max(steps,maxRight) / steps)*steps;

    {# If X-values are dates #}
    {% if chart.x_interval_type != "number" %}
        function x_to_date_object(o) { o.x = new Date(o.x); }
        dataLeft.forEach(x_to_date_object);
        dataRight.forEach(x_to_date_object);
    {% endif %}

    {# Display settings #}
    var fontFamily = "Helvetica";
    var markerType = "none";
    var lineThickness = 4;
    var markerSize = lineThickness*1.5;
    var markerBorderThickness = lineThickness/2;
    var markerColor = "#ffffff";
    var gridColor = "#e7e7e7";

    {# TODO: localize culture info with Django #}

    $("{{ elem|escapejs }}").CanvasJSChart({
        culture: '{{ LANGUAGE_CODE }}',
        dataPointMaxWidth: 20,
        axisX:{
            interval: 1,
            xValueFormatString: "{{ x_format|escapejs }}",
            intervalType: "{% firstof chart.x_interval_type|escapejs "number" %}",
            titleFontFamily: fontFamily,
            titleFontSize: 24,
            labelFontFamily: fontFamily,
            labelFontSize: 16,
            lineThickness: 0,
            lineColor: "#000000",
            labelFontColor: "#000000",

        },
        {% if chart.y_left %}
            axisY:{
                title: "{{ chart.y_left.title|escapejs }}",
                titleFontFamily: fontFamily,
                titleFontSize: 24,
                labelFontFamily: fontFamily,
                labelFontSize: 16,
                lineColor: "{{ chart.y_left.color|escapejs }}",
                titleFontColor: "{{ chart.y_left.color|escapejs }}",
                labelFontColor: "{{ chart.y_left.color|escapejs }}",
                lineThickness: 0,
                gridThickness: 1,
                gridColor: gridColor,
                tickLength: 5,
                tickColor: "{{ chart.y_left.color|escapejs }}",
                tickThickness: 1,
                maximum: maxLeft,
                interval: maxLeft / steps,
            },
        {% endif %}
        {% if chart.y_right %}
            axisY2:{
                title: "{{ chart.y_right.title|escapejs }}",
                titleFontFamily: fontFamily,
                titleFontSize: 24,
                labelFontFamily: fontFamily,
                labelFontSize: 16,
                lineColor: "{{ chart.y_right.color|escapejs }}",
                titleFontColor: "{{ chart.y_right.color|escapejs }}",
                labelFontColor: "{{ chart.y_right.color|escapejs }}",
                lineThickness: 0,
                gridThickness: 0,
                gridColor: gridColor,
                tickLength: 5,
                tickColor: "{{ chart.y_right.color|escapejs }}",
                tickThickness: 1,
                maximum: maxRight,
                interval: maxRight / steps,
            },
        {% endif %}
        data: [
            {
                type: "{{ chart.y_left.type|escapejs }}",
                valueFormatString: "{{ chart.y_left.format|escapejs }}",
                xValueFormatString: "{{ chart.x_format|escapejs }}",
                color: "{{ chart.y_left.color|escapejs }}",
                dataPoints: dataLeft,
                markerType: markerType,
                markerSize: markerSize,
                markerColor: markerColor,
                markerBorderColor: "{{ chart.y_left.color|escapejs }}",
                markerBorderThickness: markerBorderThickness,
                lineThickness: lineThickness,
            },
            {
                type: "{{ chart.y_left.type|escapejs }}",
                axisYType: "secondary",
                valueFormatString: "{{ chart.y_right.format|escapejs }}",
                xValueFormatString: "{{ chart.x_format|escapejs }}",
                color: "{{ chart.y_right.color|escapejs }}",
                dataPoints: dataRight,
                markerType: markerType,
                markerSize: markerSize,
                markerColor: markerColor,
                markerBorderColor: "{{ chart.y_right.color|escapejs }}",
                markerBorderThickness: markerBorderThickness,
                lineThickness: lineThickness,
            }
        ]
    });
});
