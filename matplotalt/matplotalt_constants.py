from enum import Enum

DescLevel = Enum('DescLevel', [('L1', 1), ('L2', 2), ('L3', 3), ('L4', 4)])
IncludeTable = Enum('IncludeTable', [('auto', 1), ('always', 2), ('never', 3)])
ChartTypeCls = Enum('ChartTypeCls', [('auto', 1), ('model', 2)])
SurfaceMethods = Enum('SurfaceMethods', [('html', 1), ('markdown', 2), ('new_cell', 3), ('img_file', 4), ('txt_file', 5)])

LINE_STYLE_TO_DESC = {
    "none": "",
    "None": "",
    "-": "",
    "solid": "",
    "--": "dashed ",
    "dashed": "dashed ",
    "-.": "dash-dotted ",
    "dashdot": "dash-dotted ",
    ":": "dotted ",
    "dotted": "dotted "
}

DEFAULT_DESC_CONFIG = {
    "stats": [],
    "trends": [],
    "sig_figs": 4,
    "max_color_desc_count": 5,
    "max_var_stats": 5,
    "max_var_trends": 5,
    "max_outliers_desc": 3,
    "include_annotation_coords": False,
    "include_warnings": False
}

CHART_TYPE_TO_DESC = {
    "other":       "An chart of unknown type",
    "line":        "A line plot",
    "scatter":     "A scatter plot",
    "bar":         "A bar chart",
    "image":       "An image",
    "heatmap":     "A heatmap",
    "boxplot":     "A boxplot",
    "sankey":      "A sankey diagram",
    "radial line": "A radial line plot",
    "pie":         "A pie chart",
    "strip":       "A strip plot",
    "choropleth":  "A choropleth map",
    "contour":     "A contour plot",
    "area":        "An area chart"
}

CHART_TYPE_TO_ID = {
    "other":      0,
    "line":       1,
    "scatter":    2,
    "bar":        3,
    "heatmap":    4,
    "boxplot":    5,
    "sankey":     6,
    "radial":     7,
    "pie":        8,
    "choropleth": 9,
    "contour":    11
}

CHART_TYPE_ANSWER_PATTERNS = [
    r"it\'s a (.*) (chart)|(diagram)|(plot)",
    r"a (.*) (chart)|(diagram)|(plot)",
    r"the (.*) (chart)|(diagram)|(plot)",
]

HEX_COLOR_TO_NAME = {
    "FF0000": "red",
    "00FFFF": "cyan",
    "0000FF": "blue",
    "4682B4": "dark blue",
    "ADD8E6": "light blue",
    "800080": "purple",
    "FFFF00": "yellow",
    "00FF00": "lime",
    "FF00FF": "magenta",
    "FFC0CB": "pink",
    "FFFFFF": "white",
    "C0C0C0": "light gray",
    "808080": "gray",
    "000000": "black",
    "FFA500": "orange",
    "5C3317": "brown",
    "800000": "maroon",
    "008000": "green",
    "808000": "olive",
    "254117": "forest green",
    "7FFFD4": "aquamarine",
}