from tkinter import *
from tkinter import filedialog
import shutil
from report_function import generate_eye_test_pdf
from layout_dot import dot_records
def go_to_result(result_frame,first_name,last_name,dob,gender,results,last_generated_pdf_holder,dot_records,test_w,test_h,cheating_status,restart_test):
    
    
    #result_frame.pack(fill="both", expand=True) # show frame
    
    last_generated_pdf = generate_eye_test_pdf(
        first_name.get(),
        last_name.get(),
        dob.get(),
        gender.get(),
        results,dot_records,test_w,
    test_h,cheating_status
    )
    
    # Store PDF path in the mutable container
    last_generated_pdf_holder[0] = last_generated_pdf

    result_frame.pack(fill="both", expand=True)
    
    # Clear any existing widgets
    for widget in result_frame.winfo_children():
        widget.destroy()
        
    Label(
        result_frame,
        text="Report",
        font=("Arial", 16, "bold")
    ).pack(pady=20)
    
    gender_map = {
        1: "Male",
        2: "Female",
        3: "Other"
    }
    gender_text = gender_map.get(gender.get())
    
    Label(
        result_frame,
        text=(
            f"Name: {first_name.get()} {last_name.get()}\n"
            f"Date of Birth: {dob.get()}\n"
            f"Gender: {gender_text}\n"
        ),
        font=("Arial", 12),
        justify=CENTER
    ).pack(pady=10)
    
    if cheating_status["left"]:
        Label(result_frame,
          text="⚠ Cheating detected in LEFT eye",
          fg="red").pack()

    if cheating_status["right"]:
        Label(result_frame,
          text="⚠ Cheating detected in RIGHT eye",
          fg="red").pack()
    
    content = Frame(result_frame)
    content.pack(fill="both", expand=True, padx=50)

    # Left eye results
    left_frame = Frame(content)
    left_frame.pack(side=LEFT, fill="both", expand=True)
    
    Label(
        left_frame,
        text="LEFT EYE RESULT",
        font=("Arial", 14, "bold")
    ).pack(pady=10)
    
    
    left_detected = results['left']['detected']
    left_missed = results['left']['missed']
    left_total = left_detected + left_missed
    accuracy_left = (left_detected / left_total) * 100

    
    Label(
        left_frame,
        text=(
            f"Detected dots: {results['left']['detected']}\n"
            f"Missed dots: {results['left']['missed']}\n"
            f"Accuracy: {accuracy_left:.1f}%\n"
        ),
        font=("Arial", 12),
        justify=LEFT
    ).pack()
    
    
    right_frame = Frame(content)
    right_frame.pack(side=RIGHT, fill="both", expand=True)
    
    
    Label(
        right_frame,
        text="RIGHT EYE RESULT",
        font=("Arial", 14, "bold")
    ).pack(pady=10)
    
    
    right_detected = results['right']['detected']
    right_missed = results['right']['missed']
    right_total = right_detected + right_missed
    accuracy_right = (right_detected / right_total) * 100
    Label(
        right_frame,
        text=(
            f"Detected dots: {results['right']['detected']}\n"
            f"Missed dots: {results['right']['missed']}\n"
            f"Accuracy: {accuracy_right:.1f}%\n"
            ),
        font=("Arial", 12),
        justify=LEFT
    ).pack()
        # =====================================
    # SEPARATE LEFT & RIGHT DOT MAPS
    # =====================================

    Label(
        result_frame,
        text="Dot Position Maps",
        font=("Arial", 14, "bold")
    ).pack(pady=15)

    maps_container = Frame(result_frame)
    maps_container.pack(pady=10)

    canvas_w = 400
    canvas_h = 300

    cols = 12
    rows = 8

    cell_w = canvas_w / cols
    cell_h = canvas_h / rows

    # -------- LEFT EYE GRID --------
    left_map_frame = Frame(maps_container)
    left_map_frame.pack(side=LEFT, padx=20)

    Label(left_map_frame, text="LEFT EYE", font=("Arial", 12, "bold")).pack()

    left_canvas = Canvas(left_map_frame, width=canvas_w, height=canvas_h, bg="white",highlightthickness=2,
    highlightbackground="black")
    left_canvas.pack()

    # -------- RIGHT EYE GRID --------
    right_map_frame = Frame(maps_container)
    right_map_frame.pack(side=RIGHT, padx=20)

    Label(right_map_frame, text="RIGHT EYE", font=("Arial", 12, "bold")).pack()

    right_canvas = Canvas(right_map_frame, width=canvas_w, height=canvas_h, bg="white",highlightthickness=2,
    highlightbackground="black")
    right_canvas.pack()
    def draw_cross_on_canvas(cnv, side):
        if side == "left":
            x_center = cell_w / 2
        else:
            x_center = canvas_w - (cell_w / 2)

        y_center = canvas_h / 2

        size = 8

        cnv.create_line(
        x_center - size, y_center - size,
        x_center + size, y_center + size,
        fill="red", width=3
    )

        cnv.create_line(
        x_center - size, y_center + size,
        x_center + size, y_center - size,
        fill="red", width=3
    )
    draw_cross_on_canvas(left_canvas, "left")
    draw_cross_on_canvas(right_canvas, "right")    
    

    # Function to plot dots
    def plot_dots(cnv, eye):
        screen_cell_w = test_w / cols
        screen_cell_h = test_h / rows

        pdf_cell_w = canvas_w / cols
        pdf_cell_h = canvas_h / rows

        for (x, y) in dot_records[eye]["detected"]:
            col = x / screen_cell_w
            row = y / screen_cell_h

            scaled_x = col * pdf_cell_w
            scaled_y = row * pdf_cell_h
            
            cnv.create_oval(
            scaled_x - 4, scaled_y - 4,
            scaled_x + 4, scaled_y + 4,
            fill="green"
        )

        for (x, y) in dot_records[eye]["missed"]:
            
            col = x / screen_cell_w
            row = y / screen_cell_h

            scaled_x = col * pdf_cell_w
            scaled_y = row * pdf_cell_h
            
            cnv.create_oval(
            scaled_x - 4, scaled_y - 4,
            scaled_x + 4, scaled_y + 4,
            fill="red"
        )
    plot_dots(left_canvas, "left")
    plot_dots(right_canvas, "right")
    
    
    def save_report_as():
        if not last_generated_pdf_holder[0]:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )

        if file_path:
            shutil.copy(last_generated_pdf_holder[0], file_path)
  
    


# Add the button at the bottom of go_to_result
    
    button_frame = Frame(result_frame)
    button_frame.pack(pady=20)

    Button(
        button_frame,
        text="Save Report",
        width=20,
        command=save_report_as
    ).grid(row=0, column=0, padx=15)

    Button(
        button_frame,
        text="Next Test",
        width=20,
        command=restart_test
    ).grid(row=0, column=1, padx=15)

       
       
       
       
'''def draw_grid(cnv):
        for c in range(cols + 1):
            x = c * cell_w
            cnv.create_line(x, 0, x, canvas_h)

        for r in range(rows + 1):
            y = r * cell_h
            cnv.create_line(0, y, canvas_w, y)

    draw_grid(left_canvas)
    draw_grid(right_canvas)'''