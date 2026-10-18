import tkinter as tk
window = tk.Tk()
window.title("FocusForge - Pomodoro Timer") 
#title() changes the text in the window's title bar.
window.geometry("500x400")
#geometry() sets the initial window size to 500 × 400 pixels.
window.configure(bg="#11111A")
#configure(bg="...") changes the background color to a dark charcoal-purple shade.
main_frame = tk.Frame(window, bg="#1E1E2E")
main_frame.pack(padx=20, pady=20, fill="both", expand=True)
#Frame() creates a new frame widget, which is a container for other widgets.
button_frame = tk.Frame(window, bg="#222235")
button_frame.pack(padx=20, pady=15, fill="x",expand=False)
mode_frame = tk.Frame(window, bg="#1E1E2E")
mode_frame.pack(padx=20, pady=15, fill="x", expand=False)

WORK_SECONDS = 25 * 60
BREAK_SECONDS = 5 * 60
selected_duration = WORK_SECONDS
selected_mode = "Work"
remaining_seconds = selected_duration #track the remaining time in seconds
timer_running = False #track whether the timer is currently running
timer_job = None #track the scheduled timer event
timer_label = tk.Label(main_frame, text="25:00", fg="white", bg="#424270", font=("Helvetica", 48))
timer_label.pack()
status_label = tk.Label(main_frame, text="Ready", fg="white", bg="#424270", font=("Helvetica", 14))
status_label.pack()

def choose_work():
    select_mode("Work", WORK_SECONDS)

def choose_break():
    select_mode("Rest", BREAK_SECONDS)

def select_mode(mode, duration):
    global selected_mode, selected_duration, remaining_seconds
    pause_timer()
    selected_mode = mode
    selected_duration = duration
    remaining_seconds = duration
    display_time()
    status_label.config(text=f"{mode} selected")

def display_time():
    minutes, seconds = divmod(remaining_seconds, 60) 
    #divmod() function returns the quotient and remainder when dividing the first argument by the second. In this case, it divides remaining_seconds by 60 to get the number of minutes and seconds left in the timer.
    timer_label.config(text=f"{minutes:02}:{seconds:02}") 
    #{:02} formats the minutes and seconds to always display two digits, adding a leading zero if necessary.

def tick():
    global remaining_seconds, timer_job, timer_running 
    #uses the global keyword to indicate that the function will modify the global variables remaining_seconds, timer_job, and timer_running.
    remaining_seconds -= 1
    display_time()
    if remaining_seconds > 0 and timer_running: #runs the timer if there is still time left and the timer is running.
        timer_job = window.after(1000, tick)
    else:
        timer_running = False
        timer_job = None
    if remaining_seconds == 0:
        status_label.config(text="Time's up!")

def start_timer():
    global timer_running, timer_job
    if timer_running or remaining_seconds == 0: #runs the timer only if it is not already running and there is time left.
        return
    timer_running = True #starts the timer by setting timer_running to True and scheduling the tick function to run every second using window.after().
    status_label.config(text="Timer running")
    timer_job = window.after(1000, tick) #initially schedules the tick function to run after 1000 milliseconds (1 second).

def pause_timer():
    global timer_running, timer_job
    if timer_running and remaining_seconds > 0: #runs if the timer is paused and there is still time left. It updates the status label to indicate that the timer is paused.
          status_label.config(text="Timer paused")
    timer_running = False
    if timer_job is not None: #runs if the timer is currently running and there is a scheduled timer event. It cancels the scheduled event using window.after_cancel() and sets timer_job to None to indicate that there is no longer a scheduled event.
        window.after_cancel(timer_job)
        #after_cancel() method is used to cancel a scheduled event that was previously set using the after() method. It takes the identifier of the scheduled event as an argument and cancels it, preventing it from being executed.
        timer_job = None
        #set timer_job to None to indicate that there is no longer a scheduled event.

def reset_timer():
    global remaining_seconds
    pause_timer()
    remaining_seconds = selected_duration
    display_time()
    status_label.config(text="Timer reset")

control_Frame = tk.Frame(button_frame, bg="#1E1E2E")
control_Frame.pack(anchor="center", pady=20)
start_button = tk.Button(control_Frame, text="Start", command=start_timer, fg="white", bg="#424270",padx=12, pady=6,font=("Helvetica", 12,"bold"))
pause_button = tk.Button(control_Frame, text="Pause", command=pause_timer, fg="white", bg="#424270",padx=12, pady=6,font=("Helvetica", 12,"bold"))
reset_button = tk.Button(control_Frame, text="Reset", command=reset_timer, fg="white", bg="#424270",padx=12, pady=6,font=("Helvetica", 12,"bold"))
start_button.pack(side="left", padx=5)
pause_button.pack(side="left", padx=5)
reset_button.pack(side="left", padx=5)

change_mode_label = tk.Label(mode_frame,bg="#1E1E2E")
change_mode_label.pack(anchor="center", pady=5)
work_button = tk.Button(change_mode_label, text="Work", command=choose_work, fg="white", bg="#424270",padx=12, pady=6,font=("Helvetica", 12,"bold"))
rest_button = tk.Button(change_mode_label, text="Rest", command=choose_break, fg="white", bg="#424270",padx=12, pady=6,font=("Helvetica", 12,"bold"))
work_button.pack(side="left", padx=5,pady=5)
rest_button.pack(side="left", padx=5,pady=5)

window.mainloop()