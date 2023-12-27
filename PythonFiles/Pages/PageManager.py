class PageManager:
    pages = []
    current_page = None

    def __init__(self) -> None:
        pass

    def AddPage(page):
        PageManager.pages.append(page)
    
    def SwitchPages(page:int=0, callback=None):
        if len(PageManager.pages) < 1:
            print(f"[{__name__}] NO PAGES FOUND!")
            return
        
        if page > len(PageManager.pages) - 1:
            print(f"[{__name__}] MISSING PAGES, PAGE NOT FOUND!")
            return
        
        if PageManager.current_page != None:
            PageManager.current_page.OnExit()
                
        if callback != None:
            callback()

        PageManager.current_page = PageManager.pages[page]
        PageManager.current_page.OnEntry()
        PageManager.current_page.SwitchTo()
