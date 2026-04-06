from tkinter import *
from tkinter import messagebox
from datetime import datetime
import random
import time
from resultframe import go_to_result
from layout_dot import get_layout_info,start_eye_test,handle_space_press
    

master = Tk()
master.title("EYE TEST")
master.attributes("-fullscreen", True)
master.configure(bg="black")


master.bind("<Escape>", lambda e: master.destroy())

print("hello world")

form_frame = Frame(master,bg="black")
instruction_frame = Frame(master, bg="black")
test_frame = Frame(master, bg="black")
instruction2_frame =Frame(master,bg="black")
result_frame = Frame(master)  


form_frame.pack(fill="both", expand=True)
master.unbind("<space>") 


container = Frame(form_frame)
container.pack(expand=True)

current_state = "form" 

first_name = StringVar()
last_name = StringVar()
dob = StringVar()
gender = IntVar()


Label(
    container,
    text="Registration Form",
    font=("Arial", 16, "bold")
).grid(row=0, column=0, columnspan=4, pady=20)

Label(container, text="First Name").grid(row=1, column=0, sticky=W, padx=10)
Label(container, text="Last Name").grid(row=2, column=0, sticky=W, padx=10)
Label(container, text="Date of Birth (MM/DD/YYYY)").grid(row=3, column=0, sticky=W, padx=10)
Label(container, text="Gender").grid(row=4, column=0, sticky=W, padx=10)

Entry(container, textvariable=first_name).grid(row=1, column=1)
Entry(container, textvariable=last_name).grid(row=2, column=1)
Entry(container, textvariable=dob).grid(row=3, column=1)

Radiobutton(container, text="Male", variable=gender, value=1).grid(row=4, column=1, sticky=W)
Radiobutton(container, text="Female", variable=gender, value=2).grid(row=4, column=2, sticky=W)
Radiobutton(container, text="Other", variable=gender, value=3).grid(row=4, column=3, sticky=W)



def submit():
    if not first_name.get():
        messagebox.showerror("Error", "Enter First Name")
        return
    elif not first_name.get().isalpha():
        messagebox.showerror("Error", "First Name should contain only alphabets")
        return

    if not last_name.get():
        messagebox.showerror("Error", "Enter Last Name")
        return
    elif not last_name.get().isalpha():
        messagebox.showerror("Error", "Last Name should contain only alphabets")
        return
    if not dob.get():
        messagebox.showerror("Error", "Enter DOB")
        return

    try:
        datetime.strptime(dob.get(), "%m/%d/%Y")
    except ValueError:
        messagebox.showerror("Error", "DOB must be MM/DD/YYYY")
        return

    if not gender.get():
        messagebox.showerror("Error", "Select Gender")
        return
    
  
    form_frame.pack_forget()
    instruction_frame.pack(fill="both", expand=True)
    master.bind("<space>", on_space_press)

Button(
    container,
    text="Submit",
    command=submit,
    width=15
).grid(row=6, column=0, columnspan=4, pady=20)


Label(instruction_frame,text="Instructions",font=("Arial", 16, "bold"),fg="white",bg="black").pack(pady=20)

instructions = """
1.A red cross will appear on the screen. 
Please keep your eyes fixed on the red cross at all times. 
2.Small gray dots will briefly appear at different places on the screen. 
3.As soon as you see a gray dot, press the SPACEBAR. 
Press only when you see a dot Try to respond as quickly as possible 
4.The test will run two times: 
First while you look at the left red cross 
Then while you look at the right red cross 
5.Do not move your eyes away from the red cross during the test. 
6.For completing test click esc
"""

Label(instruction_frame,text=instructions,justify=LEFT,fg="white",bg="black",font=("Arial", 12)).pack(padx=30)
instruction_frame.config(cursor="NONE")
test_frame.config(cursor="NONE")
instruction2_frame.config(cursor="NONE")
 


def create_cross(parent, relx, rely, anchor="center"):
    cross = Label(
        parent,
        text="X",
        font=("Arial", 24, "bold"),
        fg="red",
        bg="black"
    )
    cross.place(relx=relx, rely=rely, anchor=anchor)
    return cross



current_state = "instruction"

def on_space_press(event):
    global current_state

    if current_state == "instruction":
        instruction_frame.pack_forget()
        test_frame.pack(fill="both", expand=True)
        left_eye_test()   # start left test
        
        return


    '''if current_state == "instruction2":
        def hide_instruction2_and_start_test():
            instruction2_frame.pack_forget() 
            test_frame.pack(fill="both", expand=True)
           
            for w in test_frame.winfo_children():
                w.destroy()
            
            right_eye_test()
        
        master.after(5000, hide_instruction2_and_start_test)
        return'''

    if current_state == "instruction2":
        master.unbind("<space>")  # Disable space immediately

        def hide_instruction2_and_start_test():
            instruction2_frame.pack_forget() 
            test_frame.pack(fill="both", expand=True)

            for w in test_frame.winfo_children():
                w.destroy()

            right_eye_test()

        master.after(5000, hide_instruction2_and_start_test)
        return
    
    if current_state == "test":
        return
        
    

def left_eye_test():
    global left_cross, current_eye, current_state
    
    current_eye = "left"
    current_state = "test"
    
    master.unbind("<space>")
    master.bind("<space>", lambda e: handle_space_press(test_frame))
    
    canvas = Canvas(test_frame,bg="black")
    canvas.pack(fill="both", expand=True)
    
    left_cross = create_cross(
        test_frame,
        relx=0.02,
        rely=0.5,
        anchor="w"
    )
    


    test_frame.pack(fill="both", expand=True)
    get_layout_info(test_frame,canvas)
    test_frame.after(1000,lambda: start_eye_test(test_frame,"left",go_to_right_eye_instruction))
    


def go_to_right_eye_instruction():
    global current_state

    current_state = "instruction2"
    
    master.unbind("<space>")
    master.bind("<space>", on_space_press)
    
    test_frame.pack_forget()
    instruction2_frame.pack(fill="both", expand=True)

    Label(instruction2_frame,
        text="RIGHT EYE TEST INSTRUCTION",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="black"
    ).pack(pady=20)

    instructions2 = """
1. A red cross will appear on the screen.
   Please keep your eyes fixed on the red cross at all times.
2. Small gray dots will briefly appear at different places on the screen.
3. As soon as you see a gray dot, press the SPACEBAR.
   Press only when you see a dot. Try to respond as quickly as possible.
4. The test will run while you look at the RIGHT red cross.
5. Do not move your eyes away from the red cross during the test.
"""

    Label(
        instruction2_frame,
        text=instructions2,
        justify=LEFT,
        fg="white",
        bg="black",
        font=("Arial", 12, "bold")
    ).pack(padx=30, pady=10)      


def right_eye_test():
    global right_cross, current_eye, current_state
    
    
    current_eye = "right"   
    current_state = "test"
    
    
    master.unbind("<space>")
    master.bind("<space>", lambda e: handle_space_press(test_frame))
    
    
    canvas = Canvas(test_frame,bg="black")
    canvas.pack(fill="both", expand=True)
    
    right_cross = create_cross(
        test_frame,
        relx=0.98,
        rely=0.5,
        anchor="e"
    )
    
    

    test_frame.pack(fill="both", expand=True)
    get_layout_info(test_frame,canvas)
    test_frame.after(1000,lambda: start_eye_test(test_frame,"right",show_result))

def restart_test():
    global current_state, dot_count, extra_dots_queue
    from layout_dot import results, dot_records, space_press_count,extra_dots_queue
    
    # 1. Clear widgets from all frames to prevent overlapping
    for frame in [instruction_frame, test_frame, instruction2_frame, result_frame]:
        for widget in frame.winfo_children():
            widget.destroy()
    
    # 2. Reset Logic Variables
    dot_count = 0
    if extra_dots_queue:
        extra_dots_queue.clear()
    
    # 3. Reset Result Dictionaries
    for eye in ["left", "right"]:
        results[eye] = {"detected": 0, "missed": 0}
        dot_records[eye] = {"detected": [], "missed": []}
        space_press_count[eye] = 0
    
    # 4. Re-populate the first instruction frame (since we destroyed its label)
    Label(instruction_frame, text="Instructions", font=("Arial", 16, "bold"), fg="white", bg="black").pack(pady=20)
    Label(instruction_frame, text=instructions, justify=LEFT, fg="white", bg="black", font=("Arial", 12)).pack(padx=30)
    
    # 5. Reset UI state
    result_frame.pack_forget()
    current_state = "instruction"
    instruction_frame.pack(fill="both", expand=True)
    master.bind("<space>", on_space_press)   
    
last_generated_pdf_holder=[None]    
def show_result():
    from layout_dot import results,space_press_count,dot_records
    
    master.unbind("<space>") 
    
    test_frame.update_idletasks()
    test_w = test_frame.winfo_width()
    test_h = test_frame.winfo_height()
    test_frame.pack_forget()
    
    cheating_status = {
    "left": False,
    "right": False
     }

    for eye in ["left", "right"]:
        total_dots = results[eye]["detected"] + results[eye]["missed"]
        if space_press_count[eye] > total_dots:
            cheating_status[eye] = True
    go_to_result(result_frame, first_name, last_name, dob, gender,results,last_generated_pdf_holder,dot_records,test_w,test_h,cheating_status,restart_test)
    


master.mainloop()