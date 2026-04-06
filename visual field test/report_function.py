from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from layout_dot import TOTAL_COLS

def generate_eye_test_pdf(first_name, last_name, dob, gender_value,results,dot_records,test_w, test_h,cheating_status):

    file_name = f"Eye_Report_{first_name}_{last_name}.pdf"

    doc = SimpleDocTemplate(file_name, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    
    story.append(Paragraph("EYE TEST REPORT", styles["Title"]))
    story.append(Spacer(1, 20))

    
    gender_map = { 
        1: "Male",
        2: "Female",
        3: "Other"
    }

    gender_text = gender_map.get(gender_value, "Unknown")

   
    info = (
        f"Name: {first_name} {last_name}<br/>"
        f"Date of Birth: {dob}<br/>"
        f"Gender: {gender_text}"
    )
    
    story.append(Paragraph(info, styles["Normal"]))
    story.append(Spacer(1, 25))
    
    if cheating_status["left"]:
        story.append(Paragraph(
        "<font color='red'><b>⚠ Cheating detected in LEFT eye</b></font>",
        styles["Normal"]
    ))
    story.append(Spacer(1, 10))

    if cheating_status["right"]:
        story.append(Paragraph(
        "<font color='red'><b>⚠ Cheating detected in RIGHT eye</b></font>",
        styles["Normal"]
    ))
    story.append(Spacer(1, 10))
    
    
    
    left_detected = results['left']['detected']
    left_missed = results['left']['missed']
    left_total = left_detected + left_missed
    acc_left = (results['left']['detected'] / left_total) * 100
    
    right_detected = results['right']['detected']
    right_missed = results['right']['missed']
    right_total = right_detected + right_missed
    acc_right = (results['right']['detected'] / right_total) * 100

    data = [
        ["", "LEFT EYE", "RIGHT EYE"],
        ["Detected",
         results['left']['detected'],
         results['right']['detected']],

        ["Missed",
         results['left']['missed'],
         results['right']['missed']],

        ["Accuracy %",
         f"{acc_left:.1f}",
         f"{acc_right:.1f}"]
    ]

    table = Table(data, colWidths=[140, 170, 170])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))

    story.append(table)
    

    def draw_dot_map(canvas, doc):
        width, height = A4

        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawCentredString(width / 2, height - 340, "Dot Position Maps")
        grid_width = 220
        grid_height = 180

        start_y = height - 550

    # LEFT GRID POSITION
        left_start_x = 60

    # RIGHT GRID POSITION
        right_start_x = 330

        cols = 12
        rows = 8

        cell_w = grid_width / cols
        cell_h = grid_height / rows
        
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(2)

        canvas.rect(left_start_x, start_y, grid_width, grid_height)
        canvas.rect(right_start_x, start_y, grid_width, grid_height)
        
        canvas.drawString(left_start_x + 60, start_y + grid_height + 15, "LEFT EYE")
        canvas.drawString(right_start_x + 60, start_y + grid_height + 15, "RIGHT EYE")
        
        def draw_cross(center_x, center_y):
            size = 6
            canvas.setStrokeColor(colors.red)
            canvas.setLineWidth(3)

            canvas.line(center_x - size, center_y - size,
           center_x + size, center_y + size)

            canvas.line(center_x - size, center_y + size,
           center_x + size, center_y - size)



        left_cross_x = left_start_x + (grid_width / TOTAL_COLS) / 2
        left_cross_y = start_y + grid_height / 2

        draw_cross(left_cross_x, left_cross_y)

        right_cross_x = right_start_x + grid_width - (grid_width / TOTAL_COLS) / 2
        right_cross_y = start_y + grid_height / 2

        draw_cross(right_cross_x, right_cross_y)
   
        def draw_eye(eye, start_x):
            for (x, y) in dot_records[eye]["detected"]:
                canvas.setFillColor(colors.green)

                cell_w_screen = test_w / 12
                cell_h_screen = test_h / 8

                col = x / cell_w_screen
                row = y / cell_h_screen

                pdf_x = start_x + col * (grid_width / 12)
                pdf_y = start_y + grid_height - (row * (grid_height / 8))

                canvas.circle(pdf_x, pdf_y, 3, fill=1,stroke=0)

            for (x, y) in dot_records[eye]["missed"]:
                canvas.setFillColor(colors.red)

                cell_w_screen = test_w / 12
                cell_h_screen = test_h / 8

                col = x / cell_w_screen
                row = y / cell_h_screen

                pdf_x = start_x + col * (grid_width / 12)
                pdf_y = start_y + grid_height - (row * (grid_height / 8))

                canvas.circle(pdf_x, pdf_y, 3, fill=1,stroke=0)

        draw_eye("left", left_start_x)
        draw_eye("right", right_start_x)

    doc.build(story, onFirstPage=draw_dot_map)
    
    return file_name


'''def draw_grid(start_x):
            for c in range(cols + 1):
                x = start_x + c * cell_w
                canvas.line(x, start_y, x, start_y + grid_height)

            for r in range(rows + 1):
                y = start_y + r * cell_h
                canvas.line(start_x, y, start_x + grid_width, y)

    
        draw_grid(left_start_x)
        draw_grid(right_start_x)

        canvas.drawString(left_start_x + 60, start_y + grid_height + 15, "LEFT EYE")
        canvas.drawString(right_start_x + 60, start_y + grid_height + 15, "RIGHT EYE")'''