from datetime import datetime as dt
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import pandas as pd
from reportlab.lib.pagesizes import letter


def create_gridlines(pdf):
    # draw horizontal lines
    for i in range(0,950,100):
        pdf.drawString(30,i,str(i))
        pdf.drawString(50,i,'-'*100)
    for i in range(30,950,100):
        pdf.drawString(i,30,str(i))
        
def print_report_header(pdf, ticker):
    """
    Prints the valuation report title and date generated as subtitle
    :param pdf: pdf canvas handler
    :param ticker: Stock ticker for title
    :return: None
    """
    # Set the title font (e.g., Helvetica, 24pt)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, 770, f'{ticker} Valuation Report')
    
    # Set the subtitle font (e.g., Helvetipdfa, 16pt)
    pdf.setFont("Helvetica", 14)
    pdf.drawString(50, 750, f'Generated on {dt.today().strftime('%d/%m/%y')}')

def print_fundamental_header(pdf):
    pdf.setFont("Helvetica", 14)
    pdf.drawString(50, 690, 'Stock Fundamentals')
    text_width = pdf.stringWidth('Stock Fundamentals', 'Helvetica', 14)
    pdf.line(50, 685, 50+text_width, 685)

def print_fundamentals(pdf,price, pe, growth):
    """
    Body text fond 12, spacing 4 after text
    :param pdf:
    :param price:
    :param pe:
    :param growth:
    :return:
    """
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 672, f'Current Stock Price: ${price}')
    pdf.drawString(50, 656, f'Current PE: {pe}')
    pdf.drawString(50, 640, f'Current growth rate: {growth}')

def print_analyst_buy(pdf, mb, earning_date, median, mbp):
    ## Print Header
    pdf.drawString(50, 570, 'Analyst Price Target')
    text_width = pdf.stringWidth('Analyst Price Target', 'Helvetica', 14)
    pdf.line(50, 565, 50+text_width, 565)
    mb_pdf = mb.copy()
    mb_pdf['Date'] = mb_pdf['Date'].dt.strftime('%d/%m/%Y')
    mb_pdf['Price Target'] = mb_pdf['Price Target'].apply(lambda x: f'${float(x):.0f}')
    mb_pdf['Old Price Target'] = mb_pdf['Old Price Target'].apply(lambda x: f'${float(x):.0f}')
    table = Table([mb_pdf.columns.tolist()] + mb_pdf.values.tolist())
    # Define the table style, setting a light green background for the header row
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),  # Header background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font bold
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # Set font size for all
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),  # Add padding to header
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)  # Set grid lines
    ])
    table.setStyle(style)
    table_width, table_height = table.wrapOn(pdf, 400, 500)
    table.drawOn(pdf, 50, 550-table_height)  # Adjust position
    
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 550-table_height-20, f'Last Earnings Date: {earning_date.strftime('%d/%m/%Y')}')
    pdf.drawString(50, 550-table_height-36, f'Max buy price based on 15%pa for 3 years: ${mbp}')


def create_pdf(ticker):
    pdf = canvas.Canvas(f'Reports/{ticker}_valuation_report.pdf',bottomup=1)
    create_gridlines(pdf)
    pdf.showPage()
    print_report_header(pdf,ticker)
    print_fundamental_header(pdf)
    return pdf

def save_pdf(pdf):
    pdf.save()


#create_pdf('AMD')
