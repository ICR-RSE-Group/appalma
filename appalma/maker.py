


class PageStore(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PageStore, cls).__new__(cls)
        return cls.instance
  
    def ssh_success(self):
        ssh = self.get_global("ssh")
        return ssh

    def add_to_page(self, key, page=None):        
        if not hasattr(self, 'pages'):
            self.pages = {}
        #if key in self.pages and page is not None:
        #    self.pages[key] = page
        #    self.pages[key].play()
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
        
    def clean(self):
        if hasattr(self, 'globals'):
            self.globals = {}
        if hasattr(self, 'pages'):
            self.pages = {}



  
