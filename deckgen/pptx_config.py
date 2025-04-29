from pptx.enum.chart import XL_CHART_TYPE




def get_chart_type(chart_type):
    supported_charts = {
        "bar-horizontal": XL_CHART_TYPE.BAR_CLUSTERED,
        "bar-vertical": XL_CHART_TYPE.COLUMN_CLUSTERED,
        "line": XL_CHART_TYPE.LINE_MARKERS,
        "pie": XL_CHART_TYPE.PIE
    }

    if chart_type not in supported_charts.keys():
        raise ValueError("Unsuported Chart Type: {}".format(chart_type))
    
    return supported_charts.get(chart_type.lower(), XL_CHART_TYPE.COLUMN_CLUSTERED)


