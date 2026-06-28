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
    Image,
)
import io
import matplotlib.pyplot as plt


def generate_report(
    route,
    metrics,
    status,
    telemetry,
    latency_history,
    loss_history,
    route_fig,
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

    content.append(Paragraph("Live Metrics", styles["Heading2"]))
    content.append(Paragraph(f"Live Latency: {telemetry['latency']} ms", styles["Normal"]))
    content.append(Paragraph(f"Live Loss: {telemetry['loss']} %", styles["Normal"]))
    content.append(Paragraph(f"Bandwidth: {telemetry['bandwidth']} Mbps", styles["Normal"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Network Status", styles["Heading2"]))
    net_status = "Low Congestion" if telemetry["latency"] < 20 else "High Congestion"
    content.append(Paragraph(f"Status: {net_status}", styles["Normal"]))
    content.append(Spacer(1, 10))
    
    content.append(Paragraph("Route Visualization", styles["Heading2"]))
    route_buf = io.BytesIO()
    route_fig.savefig(route_buf, format='png', bbox_inches='tight')
    route_buf.seek(0)
    content.append(Image(route_buf, width=400, height=300))
    content.append(Spacer(1, 10))
    
    content.append(Paragraph("Route Metrics", styles["Heading2"]))
    content.append(Paragraph(f"Route: {' -> '.join(map(str, route))}", styles["Normal"]))
    content.append(Paragraph(f"Latency: {metrics['latency']} ms", styles["Normal"]))
    content.append(Paragraph(f"Loss: {metrics['loss']} %", styles["Normal"]))
    content.append(Paragraph(f"Hops: {metrics['hops']}", styles["Normal"]))
    content.append(Paragraph(f"Estimated Reward: {metrics['reward']}", styles["Normal"]))
    content.append(Paragraph(f"Health: {status}", styles["Normal"]))
    content.append(Spacer(1, 10))
    
    content.append(Paragraph("Network Trends", styles["Heading2"]))
    
    lat_fig, lat_ax = plt.subplots(figsize=(6, 4))
    lat_ax.plot(latency_history, marker='o')
    lat_ax.set_title("Latency Trend")
    lat_ax.set_ylabel("Latency (ms)")
    lat_buf = io.BytesIO()
    lat_fig.savefig(lat_buf, format='png', bbox_inches='tight')
    lat_buf.seek(0)
    plt.close(lat_fig)
    
    content.append(Paragraph("Latency Trend", styles["Heading3"]))
    content.append(Image(lat_buf, width=300, height=200))
    content.append(Spacer(1, 10))
    
    loss_fig, loss_ax = plt.subplots(figsize=(6, 4))
    loss_ax.plot(loss_history, marker='o', color='red')
    loss_ax.set_title("Packet Loss Trend")
    loss_ax.set_ylabel("Loss (%)")
    loss_buf = io.BytesIO()
    loss_fig.savefig(loss_buf, format='png', bbox_inches='tight')
    loss_buf.seek(0)
    plt.close(loss_fig)
    
    content.append(Paragraph("Packet Loss Trend", styles["Heading3"]))
    content.append(Image(loss_buf, width=300, height=200))
    content.append(Spacer(1, 10))

    pdf.build(
        content
    )

    return filename
