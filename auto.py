# automated_report_generator.py
# ----------------------------------------
# Reads data from a CSV file
# Analyzes the data
# Generates a formatted PDF report using ReportLab
#
# Required Libraries:
# pip install pandas reportlab
#
# Files:
# 1. sales_data.csv
# 2. automated_report_generator.py
#
# Output:
# sales_report.pdf
# ----------------------------------------

import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus.flowables import PageBreak

# ----------------------------------------
# STEP 1: READ DATA
# ----------------------------------------

file_path = "sales_data.csv"

df = pd.read_csv(file_path)

# ----------------------------------------
# STEP 2: ANALYZE DATA
# ----------------------------------------

total_sales = df["Sales"].sum()
average_sales = df["Sales"].mean()
highest_sales = df["Sales"].max()
lowest_sales = df["Sales"].min()

top_product = (
    df.groupby("Product")["Sales"]
    .sum()
    .idxmax()
)

top_product_sales = (
    df.groupby("Product")["Sales"]
    .sum()
    .max()
)

# ----------------------------------------
# STEP 3: CREATE PDF REPORT
# ----------------------------------------

pdf_file = "sales_report.pdf"

doc = SimpleDocTemplate(
    pdf_file,
    pagesize=letter
)

styles = getSampleStyleSheet()
elements = []

# ----------------------------------------
# TITLE
# ----------------------------------------

title = Paragraph(
    "Automated Sales Report",
    styles['Title']
)

elements.append(title)
elements.append(Spacer(1, 20))

# ----------------------------------------
# SUMMARY SECTION
# ----------------------------------------

summary_title = Paragraph(
    "<b>Summary Statistics</b>",
    styles['Heading2']
)

elements.append(summary_title)
elements.append(Spacer(1, 10))

summary_data = [
    ["Metric", "Value"],
    ["Total Sales", f"${total_sales:.2f}"],
    ["Average Sales", f"${average_sales:.2f}"],
    ["Highest Sale", f"${highest_sales:.2f}"],
    ["Lowest Sale", f"${lowest_sales:.2f}"],
    ["Top Product", top_product],
    ["Top Product Sales", f"${top_product_sales:.2f}"]
]

summary_table = Table(summary_data, colWidths=[200, 200])

summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),

    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('ALIGN', (1, 1), (-1, -1), 'CENTER')
]))

elements.append(summary_table)
elements.append(Spacer(1, 30))

# ----------------------------------------
# DETAILED DATA SECTION
# ----------------------------------------

details_title = Paragraph(
    "<b>Detailed Sales Data</b>",
    styles['Heading2']
)

elements.append(details_title)
elements.append(Spacer(1, 10))

# Convert dataframe to list
table_data = [df.columns.tolist()] + df.values.tolist()

details_table = Table(table_data)

details_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.green),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),

    ('ALIGN', (0, 0), (-1, -1), 'CENTER')
]))

elements.append(details_table)

# ----------------------------------------
# BUILD PDF
# ----------------------------------------

doc.build(elements)

print("PDF report generated successfully!")
print(f"Saved as: {pdf_file}")