{% load i18n %}
$(function() {
    var data = {% firstof chart|safe "[]" %};

    {# TODO: localize culture info with Django #}

    // Setup localization
    CanvasJS.addCultureInfo("{{ LANGUAGE_CODE }}", {
        decimalSeparator: "{{ DECIMAL_SEPARATOR }}",
        digitGroupSeparator: "{{ THOUSAND_SEPARATOR }}",
        zoomText: "{% trans "Zoom" %}",
        panText: "{% trans "Pan" %}",
        resetText: "{% trans "Reset" %}",
        zoomText: "{% trans "Zoom" %}",
        savePNGText: "{% trans "Save as PNG" %}",
        saveJPGText: "{% trans "Save as JPG" %}",
        menuText: "{% trans "More Options" %}",
        days: [
            "{% trans "Sunday" %}",
            "{% trans "Monday" %}",
            "{% trans "Tuesday" %}",
            "{% trans "Wednesday" %}",
            "{% trans "Thursday" %}",
            "{% trans "Friday" %}",
            "{% trans "Saturday" %}",
        ],
        shortDays: [
            "{% trans "Sun" %}",
            "{% trans "Mon" %}",
            "{% trans "Tue" %}",
            "{% trans "Wed" %}",
            "{% trans "Thu" %}",
            "{% trans "Fri" %}",
            "{% trans "Sat" %}",
        ],
        months: [
            "{% trans "January" %}",
            "{% trans "February" %}",
            "{% trans "March" context "Month name" %}",
            "{% trans "April" %}",
            "{% trans "May" context "Month name" %}",
            "{% trans "June" %}",
            "{% trans "July" %}",
            "{% trans "August" %}",
            "{% trans "September" %}",
            "{% trans "October" %}",
            "{% trans "November" %}",
            "{% trans "December" %}",
        ],
        shortMonths: [
            "{% trans "Jan" %}",
            "{% trans "Feb" %}",
            "{% trans "Mar" %}",
            "{% trans "Apr" %}",
            "{% trans "May" context "Short month name" %}",
            "{% trans "Jun" %}",
            "{% trans "Jul" %}",
            "{% trans "Aug" %}",
            "{% trans "Sep" %}",
            "{% trans "Oct" %}",
            "{% trans "Nov" %}",
            "{% trans "Dec" %}",
        ],
    });

    // Initialize chart settings object
    var chartSettings = {
        culture: "{{ LANGUAGE_CODE }}",
        dataPointMaxWidth: 20,
        axisX: [],
        axisX2: [],
        axisY: [],
        axisY2: [],
        data: [],
    };

    // Some default display values
    var defaults = {
        font: "Helvetica",
        textColor: "#000000",
        dataColors: ["#000000","#008CBA","#43AC6A","#F04124","#F08A24","#A0D3E8"], // These will be used one by one for differenct axes
        gridColor: "#e7e7e7",
        backgroundColor: "#ffffff", // Not in use
        steps: 5, // How many grid lines on Y-axes
    };

    // Settings that are shared between all axes
    var commonAxisSettings = {
        titleFontFamily: defaults.font,
        titleFontSize: 24,
        labelFontFamily: defaults.font,
        labelFontSize: 16,
        gridColor: defaults.gridColor,
        gridThickness: 1,
        lineThickness: 0,
        tickThickness: 1,
        tickLength: 5,
    };

    // Settings for drawing the data
    var commonDataSettings = {
        markerType: "None",
        lineThickness: 4,
    };

    // Parse arguments and dynamically build chartSettings object
    wrapInArr(data.x).forEach(parseXAxis);

    // Draw chart
    $("{{ elem|escapejs }}").CanvasJSChart(chartSettings);

    // HELPER FUNCTIONS

    function parseXAxis(xArgs) {

        var xAxisSettings = $.extend(dynamicAxisSettings(xArgs), commonAxisSettings);

        // Settings specific to X-axes:
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
        // Use ‘this’ argument from Array.forEach to pass the parent X-axis settings for this function
        var xAxisSettings = this;

        var yAxisSettings = $.extend(dynamicAxisSettings(yArgs), commonAxisSettings);

        // Settings specific to Y-axes:

        // Find the largest Y value in data
        var max = Math.max.apply(Math,yArgs.data.map(function(dataPoint){return dataPoint.y;}));
        // Set axis maximum as the closest multiple of defaults.steps above the maximum Y value
        yAxisSettings.maximum = Math.ceil(max / defaults.steps) * defaults.steps;
        // All Y-axes will have the same number of lines in the grid
        yAxisSettings.interval = yAxisSettings.maximum / defaults.steps;

        var dataSettings = $.extend({
            dataPoints: yArgs.data,
            type: yArgs.type || "line",
            lineColor: yArgs.color || yAxisSettings.lineColor,
            valueFormatString: yArgs.format || "0",
            xValueFormatString: xAxisSettings.valueFormatString || "0",
            axisXType: chartSettings.axisX.indexOf(xAxisSettings) > -1 ? "primary" : "secondary",
            color: yAxisSettings.lineColor,
        }, commonDataSettings);

        // Find the index of the parent X-axis
        dataSettings.axisXIndex = dataSettings.axisXType == "primary"
            ? chartSettings.axisX.indexOf(xAxisSettings)
            : chartSettings.axisX2.indexOf(xAxisSettings);

        if(yAxisSettings.intervalType != "number") {
            dataSettings.dataPoints.forEach(xToDateObj);
        }

        // Check which side the axis belongs to and what its index is,
        // and set dataSettings attributes accordingly
        if(yArgs.secondary) {
            dataSettings.axisYIndex = chartSettings.axisY2.length;
            dataSettings.axisYType = "secondary";
            chartSettings.axisY2.push(yAxisSettings);
        } else {
            dataSettings.axisYIndex = chartSettings.axisY.length;
            dataSettings.axisYType = "primary";
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