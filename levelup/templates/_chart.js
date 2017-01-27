{% load i18n %}
$(function() {
    var data = {% firstof chart|safe "[]" %};

    {# TODO: localize culture info with Django #}

    // Initialize chart settings object
    var chartSettings = {
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

    var commonAxisSettings = {
        titleFontFamily: defaults.font,
        titleFontSize: 24,
        labelFontFamily: defaults.font,
        labelFontSize: 16,
        gridThickness: 1,
        lineThickness: 0,
        tickThickness: 1,
        tickLength: 5,
    };

    var commonDataSettings = {
        markerType: "None",
        lineThickness: 4,
    };

    // Parse arguments and dynamically build chart settings object
    wrapInArr(data.x).forEach(parseXAxis);

    // Draw chart
    $("{{ elem|escapejs }}").CanvasJSChart(chartSettings);

    // HELPER FUNCTIONS

    function parseXAxis(xArgs) {

        var xAxisSettings = $.extend(dynamicAxisSettings(xArgs), commonAxisSettings);

        xAxisSettings.gridThickness = 0;
        xAxisSettings.intervalType = xArgs.interval_type || "number";

        if(xArgs.secondary) {
            chartSettings.axisX2.push(xAxisSettings);
        } else {
            chartSettings.axisX.push(xAxisSettings);
        }

        wrapInArr(xArgs.y).forEach(parseYAxis, xAxisSettings);

    }

    function parseYAxis(yArgs) {
        var xAxisSettings = this;

        var yAxisSettings = $.extend(dynamicAxisSettings(yArgs), commonAxisSettings);

        // Find the largest Y value in data
        var max = Math.max.apply(Math,yArgs.data.map(function(dataPoint){return dataPoint.y;}));
        // Set axis maximum as the closest multiple of defaults.steps above the maximum Y value
        yAxisSettings.maximum = Math.ceil(max / defaults.steps) * defaults.steps;
        // All Y-axis will have same number of steps in the grid
        yAxisSettings.interval = yAxisSettings.maximum / defaults.steps;

        var dataSettings = {
            dataPoints: yArgs.data,
            type: yArgs.type || "line",
            lineColor: yArgs.color || yAxisSettings.lineColor,
            valueFormatString: yArgs.format || "0",
            xValueFormatString: xAxisSettings.valueFormatString || "0",
            axisXType: chartSettings.axisX.indexOf(xAxisSettings) > -1 ? "primary" : "secondary",
            color: yAxisSettings.lineColor,
        };
        dataSettings.axisXIndex = dataSettings.axisXType == "primary"
            ? chartSettings.axisX.indexOf(xAxisSettings)
            : chartSettings.axisX2.indexOf(xAxisSettings);
        $.extend(dataSettings, commonDataSettings);

        if(yAxisSettings.intervalType != "number") {
            dataSettings.dataPoints.forEach(xToDateObj);
        }

        if(yArgs.secondary) {
            chartSettings.axisY2.push(yAxisSettings);
            dataSettings.axisYType = "secondary";
        } else {
            chartSettings.axisY.push(yAxisSettings);
        }

        chartSettings.data.push(dataSettings);
    }

    function dynamicAxisSettings(args) {
        var color = defaults.dataColors.shift() || defaults.textColor;
        return {
            title: args.title || "",
            valueFormatString: args.format || "0",
            interval: args.interval || 1,
            titleFontColor: args.color || color,
            labelFontColor: args.color || color,
            tickColor: args.color || color,
            lineColor: args.color || color,
        };
    }

    // Map X values in given data point from String to JS Date Object
    function xToDateObj(dataPoint) {
        dataPoint.x = new Date(dataPoint.x);
    }

    // If the argument is an array, it will be returned as is, otherwise an array is returned
    // with the argument as its first element.
    function wrapInArr(o) {
        if(Array.isArray(o)) {
            return o;
        } else {
            return [o];
        }
    }
});