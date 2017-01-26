{% load i18n %}
$(function() {
    var data = {% firstof chart|safe "[]" %};

    {# TODO: localize culture info with Django #}

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

    //alert(JSON.stringify(chart_settings));
    $("{{ elem|escapejs }}").CanvasJSChart(chart_settings);

    // Create chart_settings according to input
    function parseAxis(axis) {

        var color = defaults.dataColors.shift() || defaults.textColor;

        var axis_settings = {
            title: axis.title || "",
            valueFormatString: axis.format || "0",
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
                valueFormatString: axis.format || "0",
                xValueFormatString: axis.x_format || "0",
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
});
