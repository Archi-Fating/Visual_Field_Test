from tkinter import *
import random
import time

TOTAL_COLS = 12
TOTAL_ROWS = 8

REGION_COLS = 4
REGION_ROWS = 4

HIDE_COLS = 2
cell_w = None
cell_h = None
region_w = None   
region_h =None
   
def get_layout_info(test_frame, canvas):
    global cell_h,cell_w,region_h,region_w
    test_frame.update_idletasks()

    w = test_frame.winfo_width()
    h = test_frame.winfo_height()

    cell_w = w / TOTAL_COLS
    cell_h = h / TOTAL_ROWS
    
    # DRAW BLACK GRID (12 x 8)
   
    for c in range(TOTAL_COLS + 1):
        x = c * cell_w
        canvas.create_line(x, 0, x, h, fill="black")

    for r in range(TOTAL_ROWS + 1):
        y = r * cell_h
        canvas.create_line(0, y, w, y, fill="black")

    region_w = TOTAL_COLS / REGION_COLS   
    region_h = TOTAL_ROWS / REGION_ROWS   

    for rc in range(REGION_COLS):
        for rr in range(REGION_ROWS):
            x1 = rc * region_w * cell_w
            y1 = rr * region_h * cell_h
            x2 = (rc + 1) * region_w * cell_w
            y2 = (rr + 1) * region_h * cell_h

            canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="black",
                width=3
            )
    return {
        "w": w,
        "h": h,
        "cell_w": cell_w,
        "cell_h": cell_h,
        "region_w_cells": region_w,
        "region_h_cells": region_h
    }


    
min_test_limit=20
max_test_limit=120
dot_count=0
REACTION_WINDOW = 2
dot_visible=False
on_finish_callback = None
reaction_start_time = None
reaction_deadline = None
current_dot = None
dot_locked = False
results = {
    "left": {"detected": 0, "missed": 0},
    "right": {"detected": 0, "missed": 0}
}
current_dot_x = None
current_dot_y = None

dot_records={"left":{"detected":[],"missed":[]},
    "right":{"detected":[],"missed":[]}
}
extra_dots_queue = []
last_region = None
last_cell = None
space_press_count = {
    "left": 0,
    "right": 0
}
def hide_dot(dot):
    global dot_visible
    if dot and dot.winfo_exists():
        dot.place_forget()
    dot_visible = False
        
    
def start_eye_test(test_frame,eye,on_finish):
    global test_start_time, current_eye, test_running, dot_count,on_finish_callback
    
    
    current_eye = eye
    test_start_time = time.time()
    test_running = True
    dot_count = 0
    on_finish_callback = on_finish
    
    test_frame.after(500, lambda: show_random_dot(test_frame))
    #show_random_dot(test_frame, canvas)


def show_random_dot(test_frame):
    global dot_count, dot_visible, test_running
    global reaction_start_time, reaction_deadline
    global current_dot, dot_locked
    global current_dot_x, current_dot_y
    global extra_dots_queue, last_region, last_cell
    global test_start_time,use_queue

    # ---- STOP if time over ----
    if not test_running:
        return


    elapsed_time = time.time() - test_start_time

    # HARD STOP at 120 seconds (absolute maximum)
    if elapsed_time >= max_test_limit:
        print("Test finished (MAX LIMIT) for", current_eye)
        test_running = False
        extra_dots_queue.clear()
        if on_finish_callback:
            on_finish_callback()
        return

# Stop at 60 seconds ONLY if no misses happened
    if elapsed_time >= min_test_limit and results[current_eye]["missed"] == 0:
        print("Test finished (NO MISSES) for", current_eye)
        test_running = False
        if on_finish_callback:
            on_finish_callback()
        return

    if extra_dots_queue:
        rc, rr, col, row = extra_dots_queue.pop(0)
        last_region = (rc, rr)
        last_cell = (col, row)
        use_queue = True

    else:
        if current_eye == "left":
            if dot_count <= 2:
                rc = random.randint(0, REGION_COLS - 4)
                rr = random.randint(0, REGION_ROWS - 1)
            elif dot_count %3==0:
                rc = random.randint(3, REGION_COLS - 1)
                rr = random.randint(0, REGION_ROWS - 1)
            else:
                rc = random.randint(1, REGION_COLS - 1)
                rr = random.randint(1, REGION_ROWS - 1)
            print(f"LEFT EYE: dot_count={dot_count} → region=({rc},{rr})")
        elif current_eye == "right":
            if dot_count <= 2:
                rc = random.randint(3, REGION_COLS - 1)
                rr = random.randint(0, REGION_ROWS - 1)
            elif dot_count %3==0:
                rc = random.randint(0, REGION_COLS - 4)
                rr = random.randint(0, REGION_ROWS - 1)
            else:
                rc = random.randint(0, REGION_COLS - 2)
                rr = random.randint(0, REGION_ROWS - 2)
            print(f"RIGHT EYE: dot_count={dot_count} → region=({rc},{rr})")
        last_region = (rc, rr)


        col_start = int(rc * region_w)
        col_end   = int((rc + 1) * region_w) - 1
        row_start = int(rr * region_h)
        row_end   = int((rr + 1) * region_h) - 1

        col = random.randint(col_start, col_end)
        row = random.randint(row_start, row_end)

        last_cell = (col, row)

    x = (col + 0.5) * cell_w
    y = (row + 0.5) * cell_h

    dot = Label(
        test_frame,
        text="●",
        font=("Arial", 20, "bold"),
        fg="gray",
        bg="black"
    )

    dot.place(x=x, y=y, anchor="center")

    current_dot_x = x
    current_dot_y = y

    dot_count += 1
    dot_visible = True
    dot_locked = False
    current_dot = dot

    reaction_start_time = time.time()
    reaction_deadline = reaction_start_time + REACTION_WINDOW

    test_frame.after(200, lambda: hide_dot(dot))
       
    test_frame.after(2000, lambda: check_missed())
    if test_running:
        if dot_count == 8:
            test_frame.after(4000, lambda: show_random_dot(test_frame))
        else:
            test_frame.after(2500, lambda: show_random_dot(test_frame))
        
def check_missed():
    global dot_locked, extra_dots_queue,reaction_start_time
    if not test_running:
        return
    
    if reaction_start_time is None:
        return
    
    if time.time() - test_start_time >= max_test_limit:
        return
    
    if not dot_locked:
        results[current_eye]["missed"] += 1
        record_missed_dot()
        dot_locked = True

        # Generate 4 NEW cells inside same region
        if last_region:
            rc, rr = last_region

            info = {
                "region_w": TOTAL_COLS // REGION_COLS,
                "region_h": TOTAL_ROWS // REGION_ROWS
            }

            region_w = info["region_w"]
            region_h = info["region_h"]

            col_start = int(rc * region_w)
            col_end   = int((rc + 1) * region_w) - 1

            row_start = int(rr * region_h)
            row_end   = int((rr + 1) * region_h) - 1

            used_cells = set()

            # generate 4 different cells
            while len(used_cells) < 4:
                col = random.randint(col_start, col_end)
                row = random.randint(row_start, row_end)

                if (col, row) != last_cell:
                    used_cells.add((col, row))

            # store full cell info
            for cell in used_cells:
                extra_dots_queue.append((rc, rr, cell[0], cell[1]))

    print(
    f"[DOT {dot_count}] "
    f"Eye={current_eye.upper()} | "
    f"MISS (timeout) at {time.time():.3f}"
)

    reaction_start_time = None
    
        
def handle_space_press(test_frame):
    global reaction_start_time, reaction_deadline, dot_locked,space_press_count
    
    space_press_count[current_eye] += 1
    
    if reaction_start_time is None or dot_locked:
        return

    current_time = time.time()

    # Within 2 sec → detected
    if current_time <= reaction_deadline:
        results[current_eye]["detected"] += 1
        record_detected_dot()
        dot_locked = True

    # After 2 sec but before next dot → late press → missed
    else:
        results[current_eye]["missed"] += 1
        record_missed_dot()
        dot_locked = True       
        
    reaction_time = (current_time - reaction_start_time) * 1000

    print(
    f"[DOT {dot_count}] "
    f"Eye={current_eye.upper()} | "
    f"Detected at {current_time:.3f} | "
    f"Reaction Time={reaction_time:.1f} ms"
)
    print(f"[DOT RECORDS{dot_records}]")
    print(f"space count",space_press_count)
    reaction_start_time = None
    
def record_detected_dot():
    dot_records[current_eye]["detected"].append(
        (current_dot_x, current_dot_y)
    )

def record_missed_dot():
    dot_records[current_eye]["missed"].append(
        (current_dot_x, current_dot_y)
    )

