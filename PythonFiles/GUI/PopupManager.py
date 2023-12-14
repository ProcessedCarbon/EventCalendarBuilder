from GUI.GUIInterface import GUIInterface
from tkcalendar import *

def PopupWithBtn(subtitle_1:str, subtitle_2:str, button_cb, textbox_content=''):
    tmp = GUIInterface.current_frame

    window = GUIInterface.CreateNewWindow(window_name='Event Clash', size='')
    window_frame = GUIInterface.CreateFrame(window)
    window_frame.grid(row=0, column=0, sticky='nsew')

    window_frame.columnconfigure(0, weight=1)
    window_frame.rowconfigure(0, weight=2)
    window_frame.rowconfigure(1, weight=1)
    window_frame.rowconfigure(2, weight=5)
    window_frame.rowconfigure(3, weight=5)

    subtitle_1_label = GUIInterface.CreateLabel(text=subtitle_1, 
                                                font=GUIInterface.getCTKFont(size=16, weight="bold"))
    subtitle_1_label.grid(row=0, column=0, sticky='nsew')

    subtitle_2_label = GUIInterface.CreateLabel(text=subtitle_2, 
                                                font=GUIInterface.getCTKFont(size=13, weight="normal"))
    subtitle_2_label.grid(row=1, column=0, sticky='nsew')

    content = GUIInterface.CreateTextbox()
    GUIInterface.UpdateTextBox(content, 'disabled', textbox_content)
    if textbox_content != '': content.grid(row=2, column=0, sticky='nsew')

    def onClick():
        button_cb()
        window.destroy()

    yes_btn = GUIInterface.CreateButton(on_click=onClick, text='Yes')
    yes_btn.grid(row=3, column=0, sticky='nsew')

    # Prevent clicking and focus of main window
    window.grab_set()
    window.focus_force()

    GUIInterface.SetCurrentFrame(tmp)

def FailedPopup(failed_msg:str):
    tmp = GUIInterface.current_frame

    window = GUIInterface.CreateNewWindow(window_name='Failed To Schedule', size='')
    window_frame = GUIInterface.CreateFrame(window)
    window_frame.grid(row=0, column=0, sticky='nsew')

    window_frame.columnconfigure(0, weight=1)
    window_frame.rowconfigure(0, weight=1)

    msg_label = GUIInterface.CreateLabel(text=failed_msg, 
                                        font=GUIInterface.getCTKFont(size=13, weight="bold"))
    msg_label.grid(row=0, column=0, sticky='nsew')

    # Prevent clicking and focus of main window
    window.grab_set()
    window.focus_force()

    GUIInterface.SetCurrentFrame(tmp)

def CreateDateWindow(size='250x250'):
    tmp = GUIInterface.current_frame

    window = GUIInterface.CreateNewWindow(window_name='Choose Date', size=size)
    
    window_frame = GUIInterface.CreateFrame(window)
    window_frame.grid(row=0, column=0, sticky='nsew')
    window_frame.columnconfigure(0, weight=1)
    window_frame.rowconfigure(0, weight=5)
    window_frame.rowconfigure(1, weight=1)

    cal = Calendar(window_frame, selectmode='day', date_pattern='y-mm-dd')
    cal.grid(row=0, column=0, sticky='nsew')

    submit_btn = GUIInterface.CreateButton(on_click=None, text='select')
    submit_btn.grid(row=1, column=0)

    # Prevent clicking and focus of main window
    window.grab_set()
    window.focus_force()

    GUIInterface.SetCurrentFrame(tmp)
    return window, cal, submit_btn