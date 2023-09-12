from tkinter import *
from customtkinter import *
from Managers.ErrorConfig import getParamValFromKwarg

class GUIInterface:
    current_frame = None    
    root = CTk()

    def CreateFrame(frame_target, **kwargs)->CTkFrame:
        width =         getParamValFromKwarg('width', kwargs, default=200)
        height =        getParamValFromKwarg('height', kwargs, default=200)
        border_width =  getParamValFromKwarg('border_width', kwargs)
        fg_color =      getParamValFromKwarg('fg_color', kwargs, default='transparent')
        border_color =  getParamValFromKwarg('border_color', kwargs)

        frame = CTkFrame(frame_target,
                         width=width,
                         height=height,
                         border_width=border_width,
                         fg_color=fg_color,
                         border_color=border_color)
        
        GUIInterface.SetCurrentFrame(frame)
        return frame
    
    def CreateButton(on_click, **kwargs)->CTkButton:
        width =                 getParamValFromKwarg('width', kwargs, default=140)
        height =                getParamValFromKwarg('height', kwargs, default=28)
        border_width =          getParamValFromKwarg('border_width', kwargs)
        fg_color =              getParamValFromKwarg('fg_color', kwargs)
        border_color =          getParamValFromKwarg('border_color', kwargs)
        border_spacing =        getParamValFromKwarg('border_spacing', kwargs, default=2)
        corner_radius =         getParamValFromKwarg('corner_radius', kwargs, default=10)
        hover_color =           getParamValFromKwarg('hover_color', kwargs)
        text_color =            getParamValFromKwarg('text_color', kwargs)
        text_color_disabled =   getParamValFromKwarg('text_color_disabled', kwargs)
        font =                  getParamValFromKwarg('font', kwargs)
        textvariable =          getParamValFromKwarg('textvariable', kwargs)
        image =                 getParamValFromKwarg('image', kwargs)
        state =                 getParamValFromKwarg('state', kwargs, default='normal')
        hover =                 getParamValFromKwarg('hover', kwargs)
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
        fg_color =                  getParamValFromKwarg('fg_color', kwargs, default='transparent')
        text_color =                getParamValFromKwarg('text_color', kwargs)
        font =                      getParamValFromKwarg('font', kwargs)
        textvariable =              getParamValFromKwarg('textvariable', kwargs)
        corner_radius =             getParamValFromKwarg('corner_radius', kwargs)
        placeholder_text_color =    getParamValFromKwarg('placeholder_text_color', kwargs, default='grey')
        placeholder_text =          getParamValFromKwarg('placeholder_text', kwargs)
        state =                     getParamValFromKwarg('state', kwargs, default='normal')

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
            target.rowconfigure(i, weight=rows[i])
        
        for i in range(len(cols)):
            target.columnconfigure(i, weight=cols[i])

    def UpdateEntry(entry:CTkEntry, text_var:str):
        entry.delete(0, END)
        entry.insert(0, text_var)
        
    def RetrieveCurrentInputFromTextbox(text:CTkTextbox):
        input = text.get("0.0", END)
        return input
    
    def ClearCurrentFrame():
        GUIInterface.current_frame = None

    def SetCurrentFrame(frame):
        GUIInterface.current_frame = frame

    def MainLoop(self):
        self.root.mainloop()




