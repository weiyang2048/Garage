from sweetviz import analyze
from ydata_profiling import ProfileReport
import logging
import webbrowser
import sweetviz as sv

logger = logging.getLogger(__name__)


def EDA(data, use="sweetviz", compare=None):
    """
    EDA(
        data,
        use="sweetviz",
        compare={
            "mask": data["Theme"] == "Light Theme",
            "target_col": "Scroll_Depth",
        },
    )
    """
    if use == "sweetviz":
        if compare is None:
            report = analyze(data)
        else:
            mask = compare["mask"]
            filter_name = ["masked", "unmasked"]
            target_col = compare["target_col"]
            report = sv.compare_intra(
                data,
                mask,
                filter_name,
                target_col,
            )
        report.show_html("sweetviz_report.html")
        logger.info("Sweetviz report saved to sweetviz_report.html")

    elif use == "ydata":
        report = ProfileReport(data)
        report.to_file("credit_scoring_ydata_report.html")
        logger.info("Ydata report saved to credit_scoring_ydata_report.html")
        # open in browser
        webbrowser.open("credit_scoring_ydata_report.html")
