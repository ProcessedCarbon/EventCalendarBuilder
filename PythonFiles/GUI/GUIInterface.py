from tkinter import *
from customtkinter import *
from Managers.ErrorConfig import getParamValFromKwarg
import Managers.DirectoryManager as dir_manager

class GUIInterface:
    current_frame = None    
    root = CTk()
    monitor_width = root.winfo_screenwidth()
    monitor_height = root.winfo_screenheight()
    gui_path = dir_manager.getCurrentFileDirectory(__file__)
    default_theme_path = dir_manager.getFilePath(gui_path, 'ColorThemes')
    color_palette = {}

    def getAppWindowSize():
        return GUIInterface.root.winfo_screenwidth(), GUIInterface.root.winfo_screenheight()

    def CreateFrame(frame_target, **kwargs)->CTkFrame:
        width =         getParamValFromKwarg('width', kwargs, default=200)
        height =        getParamValFromKwarg('height', kwargs, default=200)
        border_width =  getParamValFromKwarg('border_width', kwargs)
        fg_color =      getParamValFromKwarg('fg_color', kwargs)
        border_color =  getParamValFromKwarg('border_color', kwargs)
        bg_color =      getParamValFromKwarg('bg_color', kwargs, default='transparent')

        frame = CTkFrame(frame_target,
                         width=width,
                         height=height,
                         border_width=border_width,
                         fg_color=fg_color,
                         border_color=border_color,
                         bg_color=bg_color)
        
        GUIInterface.SetCurrentFrame(frame)
        return frame
    
    def CreateScrollableFrame(frame_target, **kwargs)->CTkScrollableFrame:
        width =         getParamValFromKwarg('width', kwargs, default=200)
        height =        getParamValFromKwarg('height', kwargs, default=200)
        corner_radius = getParamValFromKwarg('height', kwargs)
        border_width =  getParamValFromKwarg('border_width', kwargs)
        fg_color =      getParamValFromKwarg('fg_color', kwargs)
        border_color =  getParamValFromKwarg('border_color', kwargs)
        scrollbar_fg_color = getParamValFromKwarg('scrollbar_fg_color', kwargs)
        scrollbar_button_color = getParamValFromKwarg('scrollbar_button_color', kwargs)
        scrollbar_button_hover_color = getParamValFromKwarg('scrollbar_button_hover_color', kwargs)
        label_fg_color = getParamValFromKwarg('label_fg_color', kwargs)
        label_text_color = getParamValFromKwarg('label_text_color', kwargs)
        label_text = getParamValFromKwarg('label_text_color', kwargs)
        label_font = getParamValFromKwarg('label_font', kwargs)
        label_anchor = getParamValFromKwarg('label_anchor', kwargs, default='center')
        orientation = getParamValFromKwarg('orientation', kwargs, default='vertical')
        bg_color = getParamValFromKwarg('bg_color', kwargs, default='transparent')

        scrollable_frame = CTkScrollableFrame(frame_target,
                                              width=width,
                                              height=height,
                                              corner_radius=corner_radius,
                                              border_width=border_width,
                                              fg_color=fg_color,
                                              border_color=border_color,
                                              scrollbar_fg_color=scrollbar_fg_color,
                                              scrollbar_button_color=scrollbar_button_color,
                                              scrollbar_button_hover_color=scrollbar_button_hover_color,
                                              label_fg_color=label_fg_color,
                                              label_text_color=label_text_color,
                                              label_text=label_text,
                                              label_font=label_font,
                                              label_anchor=label_anchor,
                                              orientation=orientation,
                                              bg_color=bg_color)
        return scrollable_frame

    def CreateButton(on_click=None, **kwargs)->CTkButton:
        width =                 getParamValFromKwarg('width', kwargs, default=140)
        height =                getParamValFromKwarg('height', kwargs, default=28)
        border_width =          getParamValFromKwarg('border_width', kwargs)
        fg_color =              getParamValFromKwarg('fg_color', kwargs)
        border_color =          getParamValFromKwarg('border_color', kwargs)
        border_spacing =        getParamValFromKwarg('border_spacing', kwargs, default=2)
        corner_radius =         getParamValFromKwarg('corner_radius', kwargs, default=10)
        hover_color =           getParamValFromKwarg('hover_color', kwargs, tuple(GUIInterface.color_palette['CTkButton']['hover_color']))
        text_color =            getParamValFromKwarg('text_color', kwargs)
        text_color_disabled =   getParamValFromKwarg('text_color_disabled', kwargs)
        font =                  getParamValFromKwarg('font', kwargs, default=GUIInterface.getCTKFont(weight="bold"))
        textvariable =          getParamValFromKwarg('textvariable', kwargs)
        image =                 getParamValFromKwarg('image', kwargs)
        state =                 getParamValFromKwarg('state', kwargs, default='normal')
        hover =                 getParamValFromKwarg('hover', kwargs, True)
        compound =              getParamValFromKwarg('compound', kwargs, default='left')
        anchor =                getParamValFromKwarg('anchor', kwargs, default='center')
        text =                  getParamValFromKwarg('text', kwargs, default='Button')


        myButton = CTkButton(GUIInterface.current_frame, 
                             text=text, 
                             command=on_click, 
                             corner_radius=corner_radius,
                             width=width,
                             height=height,
                             border_width=border_width,
                             fg_color=fg_color,
                             border_color=border_color,
                             hover_color=hover_color,
                             text_color=text_color,
                             text_color_disabled=text_color_disabled,
                             font=font,
                             textvariable=textvariable,
                             image=image,
                             state=state,
                             hover=hover,
                             compound=compound,
                             anchor=anchor,
                             border_spacing=border_spacing)
        return myButton
        
    def CreateLabel(text:str, **kwargs)->CTkLabel:
        width =             getParamValFromKwarg('width', kwargs, default=0)
        height =            getParamValFromKwarg('height', kwargs, default=28)
        fg_color =          getParamValFromKwarg('fg_color', kwargs, default='transparent')
        text_color =        getParamValFromKwarg('text_color', kwargs)
        font =              getParamValFromKwarg('font', kwargs)
        textvariable =      getParamValFromKwarg('textvariable', kwargs)
        corner_radius =     getParamValFromKwarg('corner_radius', kwargs)
        anchor =            getParamValFromKwarg('anchor', kwargs, default='center')
        compound =          getParamValFromKwarg('compound', kwargs, default='center')
        justify =           getParamValFromKwarg('justify', kwargs, default='center')
        padx =              getParamValFromKwarg('padx', kwargs, default=1)
        pady =              getParamValFromKwarg('pady', kwargs, default=1)

        myLabel = CTkLabel(GUIInterface.current_frame, 
                           text=text,
                           width=width,
                           height=height,
                           fg_color=fg_color,
                           text_color=text_color,
                           font=font,
                           textvariable=textvariable,
                           corner_radius=corner_radius,
                           anchor=anchor,
                           compound=compound,
                           justify=justify,
                           padx=padx,
                           pady=pady)
        return myLabel

    def CreateEntry(**kwargs)->CTkEntry:
        width =                     getParamValFromKwarg('width', kwargs, default=140)
        height =                    getParamValFromKwarg('height', kwargs, default=28)
        fg_color =                  getParamValFromKwarg('fg_color', kwargs)
        text_color =                getParamValFromKwarg('text_color', kwargs)
        font =                      getParamValFromKwarg('font', kwargs)
        textvariable =              getParamValFromKwarg('textvariable', kwargs)
        corner_radius =             getParamValFromKwarg('corner_radius', kwargs)
        placeholder_text_color =    getParamValFromKwarg('placeholder_text_color', kwargs, default='grey')
        placeholder_text =          getParamValFromKwarg('placeholder_text', kwargs)
        state =                     getParamValFromKwarg('state', kwargs, default='normal')
        bg_color =                  getParamValFromKwarg('bg_color', kwargs, default='transparent')

        textInput = CTkEntry(GUIInterface.current_frame, 
                             width=width,
                             height=height,
                             fg_color=fg_color,
                             text_color=text_color,
                             font=font,
                             textvariable=textvariable,
                             corner_radius=corner_radius,
                             placeholder_text_color=placeholder_text_color,
                             placeholder_text=placeholder_text,
                             state=state)
        return textInput
    
    def CreateTextbox(**kwargs)->CTkTextbox:
        width =                         getParamValFromKwarg('width', kwargs, default=200)
        height =                        getParamValFromKwarg('height', kwargs, default=200)
        fg_color =                      getParamValFromKwarg('fg_color', kwargs)
        text_color =                    getParamValFromKwarg('text_color', kwargs)
        font =                          getParamValFromKwarg('font', kwargs)
        corner_radius =                 getParamValFromKwarg('corner_radius', kwargs)
        state =                         getParamValFromKwarg('state', kwargs)
        border_width =                  getParamValFromKwarg('border_width', kwargs)
        border_spacing =                getParamValFromKwarg('border_spacing', kwargs, default=3)
        border_color =                  getParamValFromKwarg('border_color', kwargs)
        scrollbar_button_color =        getParamValFromKwarg('scrollbar_button_color', kwargs)
        scrollbar_button_hover_color =  getParamValFromKwarg('scrollbar_button_color', kwargs)
        activate_scrollbars =           getParamValFromKwarg('activate_scrollbars', kwargs, default=True)
        wrap =                          getParamValFromKwarg('wrap', kwargs, default='char')

        text = CTkTextbox(GUIInterface.current_frame, 
                          height=height, 
                          width=width,
                          fg_color=fg_color,
                          text_color=text_color,
                          font=font,
                          corner_radius=corner_radius,
                          state=state,
                          border_width=border_width,
                          border_spacing=border_spacing,
                          border_color=border_color,
                          scrollbar_button_color=scrollbar_button_color,
                          scrollbar_button_hover_color=scrollbar_button_hover_color,
                          activate_scrollbars=activate_scrollbars,
                          wrap=wrap)
        return text
    
    def CreateComboBox(values:list[str], **kwargs)->CTkComboBox:
        width =                         getParamValFromKwarg('width', kwargs, default=140)
        height =                        getParamValFromKwarg('height', kwargs, default=28)
        fg_color =                      getParamValFromKwarg('fg_color', kwargs)
        text_color =                    getParamValFromKwarg('text_color', kwargs)
        text_color_disabled =           getParamValFromKwarg('text_color_disabled', kwargs)
        font =                          getParamValFromKwarg('font', kwargs)
        corner_radius =                 getParamValFromKwarg('corner_radius', kwargs)
        state =                         getParamValFromKwarg('state', kwargs, default='readonly')
        border_width =                  getParamValFromKwarg('border_width', kwargs)
        border_color =                  getParamValFromKwarg('border_color', kwargs)
        button_color =                  getParamValFromKwarg('button_color', kwargs)
        button_hover_color =            getParamValFromKwarg('button_hover_color', kwargs)
        dropdown_fg_color =             getParamValFromKwarg('dropdown_fg_color', kwargs)
        dropdown_hover_color =          getParamValFromKwarg('dropdown_hover_color', kwargs)
        dropdown_text_color =           getParamValFromKwarg('dropdown_text_color', kwargs)
        dropdown_font =                 getParamValFromKwarg('dropdown_font', kwargs)
        hover =                         getParamValFromKwarg('hover', kwargs)
        command =                       getParamValFromKwarg('command', kwargs)
        variable =                      getParamValFromKwarg('variable', kwargs)
        justify =                       getParamValFromKwarg('justify', kwargs, default='left')

        combobox = CTkComboBox(GUIInterface.current_frame, 
                               values=values, 
                               state=state,
                               width=width,
                               height=height,
                               fg_color=fg_color,
                               text_color=text_color,
                               text_color_disabled=text_color_disabled,
                               font=font,
                               corner_radius=corner_radius,
                               border_width=border_width,
                               border_color=border_color,
                               button_color=button_color,
                               button_hover_color=button_hover_color,
                               dropdown_fg_color=dropdown_fg_color,
                               dropdown_hover_color=dropdown_hover_color,
                               dropdown_text_color=dropdown_text_color,
                               dropdown_font=dropdown_font,
                               hover=hover,
                               command=command,
                               variable=variable,
                               justify=justify)
        combobox.set(values[0])
        return combobox

    def CreateGrid(target:CTkFrame, rows=list[int], cols=list[int]):
        for i in range(len(rows)):
            target.grid_rowconfigure(i, weight=rows[i])
        
        for i in range(len(cols)):
            target.grid_columnconfigure(i, weight=cols[i])

    def CreateEntryWithLabel(label:str, **kwargs)->list[CTkFrame, CTkLabel, CTkEntry]:
        entry_width =       getParamValFromKwarg('entry_width', kwargs)
        default_text =      getParamValFromKwarg('default_text', kwargs)
        entry_state =       getParamValFromKwarg('entry_state', kwargs)
        placeholder_text =  getParamValFromKwarg('placeholder_text', kwargs)

        tmp_frame = GUIInterface.current_frame
        entry_frame = GUIInterface.CreateFrame(frame_target=GUIInterface.current_frame, 
                                               border_width=0,
                                               fg_color='transparent')

        entry_frame.columnconfigure(0, weight=1)
        entry_frame.columnconfigure(1, weight=3)

        # Entry label
        label = GUIInterface.CreateLabel(text=label,font=GUIInterface.getCTKFont(weight="bold"))
        label.grid(row=0, column=0)

        # Entry
        entry = GUIInterface.CreateEntry(width=entry_width, 
                                         textvariable=default_text, 
                                         state=entry_state,
                                         placeholder_text=placeholder_text)
        
        entry.grid(row=0, column=1, sticky='e')

        GUIInterface.SetCurrentFrame(tmp_frame)

        return entry_frame, label ,entry
    
    def CreateOptionMenuWithLabel(label:str, dropdown:list[str])->list[CTkFrame,CTkLabel,CTkComboBox]:    
        tmp_frame = GUIInterface.current_frame
        combo_frame = GUIInterface.CreateFrame(frame_target=GUIInterface.current_frame,
                                               border_width=0,
                                               fg_color='transparent')

        combo_frame.columnconfigure(0, weight=1)
        combo_frame.columnconfigure(1, weight=3)

        # Entry label
        label = GUIInterface.CreateLabel(text=label,font=GUIInterface.getCTKFont(weight="bold"))
        label.grid(row=0, column=0)

        # Entry
        combobox = GUIInterface.CreateOptionMenu(values=dropdown)
        combobox.grid(row=0, column=1, sticky='e')

        GUIInterface.SetCurrentFrame(tmp_frame)

        return combo_frame, label, combobox 

    def CreateNewWindow(window_name:str, size='250x250'):
        window = Toplevel(GUIInterface.root)
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        window.title(window_name)
        if size != '': window.geometry(size)

        def onCloseCallBack():
            window.destroy()
            window.grab_release()
        
        window.protocol("WM_DELETE_WINDOW", onCloseCallBack)
        window.bind("<FocusOut>", lambda event : onCloseCallBack)

        return window
    
    def centerWindow(window):
        '''
        Should be ran after all UI elements of the window has been placed
        '''
        w_width, w_height, x_disp, y_disp = GUIInterface.getWindowDisplacement(window)
        window.geometry(f'{w_width}x{w_height}+{x_disp}+{y_disp}')

    def getWindowDisplacement(window)->[int,int,int,int]:
        w_width, w_height = GUIInterface.getWindowInfo(window)

        screen_width, screen_height = GUIInterface.getAppWindowSize()
        # Coordinates of the upper left corner of the window to make the window appear in the center
        x = int((screen_width/2) - (w_width/2))
        y = int((screen_height/2) - (w_height/2))

        return w_width, w_height, x, y
    
    def CreateOptionMenu(**kwargs):
        width =                         getParamValFromKwarg('width', kwargs, default=140)
        height =                        getParamValFromKwarg('height', kwargs, default=28)
        corner_radius =                        getParamValFromKwarg('corner_radius', kwargs)
        bg_color =                        getParamValFromKwarg('bg_color', kwargs, default='transparent')
        fg_color =                        getParamValFromKwarg('fg_color', kwargs)
        button_color =                        getParamValFromKwarg('button_color', kwargs)
        button_hover_color =                        getParamValFromKwarg('button_hover_color', kwargs)
        text_color =                        getParamValFromKwarg('text_color', kwargs)
        text_color_disabled =                        getParamValFromKwarg('text_color_disabled', kwargs)
        dropdown_fg_color =                        getParamValFromKwarg('dropdown_fg_color', kwargs)
        dropdown_hover_color =                        getParamValFromKwarg('dropdown_hover_color', kwargs)
        dropdown_text_color =                        getParamValFromKwarg('dropdown_text_color', kwargs)
        font =                        getParamValFromKwarg('font', kwargs)
        dropdown_font =                        getParamValFromKwarg('dropdown_font', kwargs)
        values =                        getParamValFromKwarg('values', kwargs)
        variable =                        getParamValFromKwarg('variable', kwargs)
        state =                        getParamValFromKwarg('state', kwargs, default=NORMAL)
        hover =                        getParamValFromKwarg('hover', kwargs, default=True)
        command =                        getParamValFromKwarg('command', kwargs)
        dynamic_resizing =                        getParamValFromKwarg('dynamic_resizing', kwargs, default=True)
        anchor =                        getParamValFromKwarg('anchor', kwargs, default='w')

        option_menu = CTkOptionMenu(master=GUIInterface.current_frame,
                                    width=width,
                                    height=height,
                                    corner_radius=corner_radius,
                                    bg_color=bg_color,
                                    fg_color=fg_color,
                                    button_color=button_color,
                                    button_hover_color=button_hover_color,
                                    text_color=text_color,
                                    text_color_disabled=text_color_disabled,
                                    dropdown_fg_color=dropdown_fg_color,
                                    dropdown_hover_color=dropdown_hover_color,
                                    dropdown_text_color=dropdown_text_color,
                                    font=font,
                                    dropdown_font=dropdown_font,
                                    values=values,
                                    variable=variable,
                                    state=state,
                                    hover=hover,
                                    command=command,
                                    dynamic_resizing=dynamic_resizing,
                                    anchor=anchor)
        return option_menu

    def getCTKFont(**kwargs):
        family = getParamValFromKwarg('family', kwargs)
        size = getParamValFromKwarg('size', kwargs)
        weight = getParamValFromKwarg('weight', kwargs)
        slant = getParamValFromKwarg('slant', kwargs, 'roman')
        underline = getParamValFromKwarg('slant', kwargs, False)
        overstrike = getParamValFromKwarg('slant', kwargs, False)


        return CTkFont(family=family,
                       size=size,
                       weight=weight,
                       slant=slant,
                       underline=underline,
                       overstrike=overstrike
                       )

    def getWindowInfo(window)->[int,int]:
        window.update()
        return window.winfo_width(), window.winfo_height()

    def UpdateEntry(entry:CTkEntry, text_var:str):
        og_state = entry.cget("state")
        entry.configure(state='normal')
        entry.delete(0, END)
        entry.insert(0, text_var)
        entry.configure(state=og_state)

    def UpdateTextBox(textbox:CTkTextbox, state:str, text:str):
        textbox.configure(state='normal')
        textbox.delete("0.0", END)
        textbox.insert("0.0", text)
        textbox.configure(state=state)
        
    def RetrieveCurrentInputFromTextbox(text:CTkTextbox)->str:
        input = text.get("0.0", END)
        return input
    
    def ClearCurrentFrame():
        GUIInterface.current_frame = None

    def ClearTextBox(textbox:CTkTextbox):
        textbox.delete("0.0", END)

    def SetCurrentFrame(frame):
        GUIInterface.current_frame = frame
    
    def SetAppearanceMode(new_appearance_mode:str):
        set_appearance_mode(new_appearance_mode)

    def ChangeGUIScaling(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        set_widget_scaling(new_scaling_float)

    def SetDefaultColorTheme(theme=''):
        try:
            path = dir_manager.getFilePath(GUIInterface.default_theme_path, theme)
            if path == '': set_default_color_theme('blue')
            else: 
                set_default_color_theme(path)
                GUIInterface.setColorPalette(theme)
        except: set_default_color_theme('blue')

    def setColorPalette(theme=''):
        try:
            curr_path = dir_manager.getCurrentFileDirectory(__file__)
            theme_dir = dir_manager.getFilePath(curr_path, 'ColorThemes')
            GUIInterface.color_palette = dir_manager.ReadJSON(dir_path=theme_dir, file_name=theme)
        except: pass

    def MainLoop(self):
        self.root.mainloop()
        
