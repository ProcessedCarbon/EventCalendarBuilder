from GUI.GUIInterface import GUIInterface
from tkcalendar import *

def CreateDateWindow(size='450x450'):
    tmp = GUIInterface.current_frame

    window, on_window_close = GUIInterface.CreateNewWindow(window_name='Choose Date', size=size)
    window_frame = GUIInterface.CreateFrame(window)
    window_frame.grid(row=0, column=0, sticky='nsew')
    window_frame.columnconfigure(0, weight=1)
    window_frame.rowconfigure(0, weight=5)
    window_frame.rowconfigure(1, weight=1)

    text_color = GUIInterface.color_palette['CTkButton']['text_color'][0]
    selected_color = GUIInterface.color_palette['CTkButton']['hover_color'][1]
    bg = GUIInterface.color_palette['CTkFrame']['fg_color'][0]
    cal = Calendar(window_frame, selectmode='day', date_pattern='y-mm-dd',
                showweeknumbers=False, showothermonthdays=False,
                font = GUIInterface.getCTKFont(size=13),
                background=GUIInterface.color_palette['CTkButton']['fg_color'][0], # Header buttons
                foreground=text_color,
                bordercolor=GUIInterface.color_palette['CTkButton']['fg_color'][0],
                headersbackground=bg, # header text
                headersforeground=text_color,
                selectbackground=bg, # selected cell text
                selectforeground=selected_color,  
                normalbackground=bg, # other week day cells text
                normalforeground=text_color,
                weekendbackground=bg, # other weekend cells text
                weekendforeground=text_color,
                othermonthforeground=text_color,
                othermonthbackground=bg,
                othermonthweforeground=text_color,
                othermonthwebackground=bg,)
    cal.grid(row=0, column=0, sticky='nsew',pady=10, padx=10)

    submit_btn = GUIInterface.CreateButton(on_click=None, text='select')
    submit_btn.grid(row=1, column=0, pady=10, padx=10)

    # Prevent clicking and focus of main window
    window.grab_set()
    window.focus_force()
    GUIInterface.centerWindow(window)

    GUIInterface.current_frame = tmp
    return window, cal, submit_btn