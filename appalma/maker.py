


class PageStore(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PageStore, cls).__new__(cls)
        return cls.instance
  
    def add_to_page(self, key, page=None):        
        if not hasattr(self, 'pages'):
            self.pages = {}
        if key in self.pages and self.pages[key] is not None:
            self.pages[key].play()
        else:             
            self.pages[key] = page
            page.play()

    def set_global(self, key, value):
        if not hasattr(self, 'globals'):
            self.globals = {}
        if key in self.globals:
            self.globals[key] = value
        else:
            self.globals[key] = value
    
    def get_global(self,key):
        if not hasattr(self, 'globals'):
            self.globals = {}
        if key in self.globals:
            return self.globals[key]
        else:
            return None



  
