{% load i18n %}
$(function() {
    var data = {% firstof chart|safe "[]" %};

    var chart_settings = {
        culture: '{{ LANGUAGE_CODE }}',
        dataPointMaxWidth: 20,
        axisX: [],
        axisX2: [],
        axisY: [],
        axisY2: [],
        data: [],
    };

    var defaults = {
        font: "Helvetica",
        textColor: "#000000",
        dataColors: ["#000000","#008CBA","#43AC6A","#F04124","#F08A24","#A0D3E8"],
        gridColor: "#e7e7e7",
        backgroundColor: "#ffffff",
        steps: 5,
    };

    var common_axis_settings = {
        titleFontFamily: defaults.font,
        titleFontSize: 24,
        labelFontFamily: defaults.font,
        labelFontSize: 16,
        gridThickness: 1,
        lineThickness: 0,
        tickThickness: 1,
        tickLength: 5,
    };

    var common_data_settings = {
        markerType: "None",
        lineThickness: 4,
    };

    if(Array.isArray(data.x)) {
        data.x.forEach(parseAxis);
    } else if('x' in data) {
        parseAxis(data.x)
    }

    alert(JSON.stringify(chart_settings));
    $("{{ elem|escapejs }}").CanvasJSChart(chart_settings);

    // Create chart_settings according to input
    function parseAxis(axis) {

        var color = defaults.dataColors.shift() || defaults.textColor;

        var axis_settings = {
            title: axis.title || "",
            valueFormatString: axis.format || "#",
            interval: axis.interval || 1,
            titleFontColor: axis.color || color,
            labelFontColor: axis.color || color,
            tickColor: axis.color || color,
            lineColor: axis.color || color,
        };
        $.extend(axis_settings, common_axis_settings);

        if('y' in axis) { // is X-axis
            axis_settings.gridThickness = 0;
            axis_settings.intervalType = axis.interval_type || "number";

            axis.y.x_format = axis.format;

            if(axis.secondary) {
                axis.y.x_index = chart_settings.axisX2.length;
                axis.y.x_type = "secondary";
                chart_settings.axisX2.push(axis_settings);
            } else {
                axis.y.x_index = chart_settings.axisX.length;
                chart_settings.axisX.push(axis_settings);
            }

            if(Array.isArray(axis.y)) {
                axis.y.forEach(parseAxis);
            } else if('y' in axis) {
                parseAxis(axis.y);
            }
        } else if ('data' in axis) { // is Y-axis

            var max = Math.max.apply(Math,axis.data.map(function(data_point){return data_point.y;}));
            max = Math.ceil(Math.max(defaults.steps,max) / defaults.steps)*defaults.steps;

            axis_settings.maximum = max;
            axis_settings.interval = axis_settings.maximum / defaults.steps;

            var data_settings = {
                dataPoints: axis.data,
                type: axis.type || "line",
                lineColor: axis.color || color,
                valueFormatString: axis.format || [],
                xValueFormatString: axis.x_format || [],
                axisXType: axis.x_type || "primary",
                axisXIndex: axis.x_index || 0,
                color: axis.color || color,
            };
            $.extend(data_settings, common_data_settings);

            if(axis_settings.intervalType != "number") {
                data_settings.dataPoints.forEach(xToDateObj);
            }

            if(axis.secondary) {
                chart_settings.axisY2.push(axis_settings);
                data_settings.axisYType = "secondary";
            } else {
                chart_settings.axisY.push(axis_settings);
            }

            chart_settings.data.push(data_settings);
        }
    }

    // Map X values in given data point from String to JS Date Object
    function xToDateObj(data_point) {
        data_point.x = new Date(data_point.x);
    }


    /*
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
    */
});
