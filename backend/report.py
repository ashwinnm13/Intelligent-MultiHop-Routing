from datetime import (
    datetime
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


def generate_report(

    route,
    metrics,
    status,

):

    filename = (
        "route_report.pdf"
    )

    pdf = (
        SimpleDocTemplate(
            filename
        )
    )

    styles = (
        getSampleStyleSheet()
    )

    content = []

    content.append(
        Paragraph(
            "RouteFlux Report",
            styles[
                "Title"
            ]
        )
    )

    content.append(
        Spacer(
            1,
            20
        )
    )

    content.append(
        Paragraph(
            f"Generated: {datetime.now()}",
            styles[
                "Normal"
            ]
        )
    )

    content.append(
        Paragraph(
            f"Route: {' → '.join(map(str, route))}",
            styles[
                "Normal"
            ]
        )
    )

    content.append(
        Paragraph(
            f"Latency: {metrics['latency']} ms",
            styles[
                "Normal"
            ]
        )
    )

    content.append(
        Paragraph(
            f"Loss: {metrics['loss']} %",
            styles[
                "Normal"
            ]
        )
    )

    content.append(
        Paragraph(
            f"Hops: {metrics['hops']}",
            styles[
                "Normal"
            ]
        )
    )

    content.append(
        Paragraph(
            f"Health: {status}",
            styles[
                "Normal"
            ]
        )
    )

    pdf.build(
        content
    )

    return filename
