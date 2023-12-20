from GUI.GUIInterface import GUIInterface
from tkcalendar import *

def PopupWithBtn(pop_up_name:str, subtitle_1:str, subtitle_2:str, button_cb, textbox_content=''):
    tmp = GUIInterface.current_frame

    window = GUIInterface.CreateNewWindow(window_name=pop_up_name, size='')
    window_frame = GUIInterface.CreateFrame(window)
    window_frame.grid(row=0, column=0, sticky='nsew')

    window_frame.columnconfigure(0, weight=1)
    window_frame.rowconfigure(0, weight=2)
    window_frame.rowconfigure(1, weight=1)
    window_frame.rowconfigure(2, weight=5)
    window_frame.rowconfigure(3, weight=5)

    subtitle_1_label = GUIInterface.CreateLabel(text=subtitle_1, 
                                                font=GUIInterface.getCTKFont(size=16, weight="bold"))
    subtitle_1_label.grid(row=0, column=0, sticky='nsew',pady=10, padx=10)

    subtitle_2_label = GUIInterface.CreateLabel(text=subtitle_2, 
                                                font=GUIInterface.getCTKFont(size=13, weight="normal"))
    subtitle_2_label.grid(row=1, column=0, sticky='nsew', pady=10, padx=10)

    content = GUIInterface.CreateTextbox()
    GUIInterface.UpdateTextBox(content, 'disabled', textbox_content)
    if textbox_content != '': content.grid(row=2, column=0, sticky='nsew', pady=10, padx=10)

    def onClick():
        button_cb()
        window.destroy()

    yes_btn = GUIInterface.CreateButton(on_click=onClick, text='Yes')
    yes_btn.grid(row=3, column=0, pady=10)

    # Prevent clicking and focus of main window
    window.grab_set()
    window.focus_force()

    GUIInterface.SetCurrentFrame(tmp)

def PopupWithTwoBtns(pop_up_name:str, subtitle_1:str, subtitle_2:str, 
                     button_cb_1, button_cb_2,
                     b1_text='Online', b2_text='Offline'):
    tmp = GUIInterface.current_frame

    window = GUIInterface.CreateNewWindow(window_name=pop_up_name, size='')
    window_frame = GUIInterface.CreateFrame(window)
    GUIInterface.CreateGrid(window_frame, rows=[2, 1, 1], cols=[1])
    window_frame.grid(row=0, column=0, sticky='nsew')

    subtitle_1_label = GUIInterface.CreateLabel(text=subtitle_1, 
                                                font=GUIInterface.getCTKFont(size=16, weight="bold"))
    subtitle_1_label.grid(row=0, column=0, sticky='nsew',pady=10, padx=10)

    subtitle_2_label = GUIInterface.CreateLabel(text=subtitle_2, 
                                                font=GUIInterface.getCTKFont(size=13, weight="normal"))
    subtitle_2_label.grid(row=1, column=0, sticky='nsew', pady=10, padx=10)

    def onClick_1():
        button_cb_1()
        window.destroy()

    def onClick_2():
        button_cb_2()
        window.destroy()

    tmp = GUIInterface.current_frame
    button_frame = GUIInterface.CreateFrame(window_frame)
    GUIInterface.CreateGrid(button_frame, rows=[1], cols=[1, 1])
    button_frame.grid(row=2, column=0, pady=10)

    yes_btn = GUIInterface.CreateButton(on_click=onClick_1, text=b1_text)
    yes_btn.grid(row=0, column=0)

    no_btn = GUIInterface.CreateButton(on_click=onClick_2, text=b2_text)
    no_btn.grid(row=0, column=1)
    GUIInterface.current_frame = tmp

    # Prevent clicking and focus of main window
    window.grab_set()
    window.focus_force()

    GUIInterface.SetCurrentFrame(tmp)

def BasicPopup(msg:str, pop_up_name='Failed'):
    tmp = GUIInterface.current_frame

    window = GUIInterface.CreateNewWindow(window_name=pop_up_name, size='')
    window_frame = GUIInterface.CreateFrame(window)
    window_frame.grid(row=0, column=0, sticky='nsew')

    window_frame.columnconfigure(0, weight=1)
    window_frame.rowconfigure(0, weight=1)

    msg_label = GUIInterface.CreateLabel(text=msg, 
                                        font=GUIInterface.getCTKFont(size=13, weight="bold"))
    msg_label.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

    # Prevent clicking and focus of main window
    window.grab_set()
    window.focus_force()

    GUIInterface.SetCurrentFrame(tmp)

def CreateDateWindow(size='450x450'):
    tmp = GUIInterface.current_frame

    window = GUIInterface.CreateNewWindow(window_name='Choose Date', size=size)
    
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
                   othermonthwebackground=bg,
                   )
    cal.grid(row=0, column=0, sticky='nsew',pady=10, padx=10)

    submit_btn = GUIInterface.CreateButton(on_click=None, text='select')
    submit_btn.grid(row=1, column=0, pady=10, padx=10)

    # Prevent clicking and focus of main window
    window.grab_set()
    window.focus_force()

    GUIInterface.SetCurrentFrame(tmp)
    return window, cal, submit_btn