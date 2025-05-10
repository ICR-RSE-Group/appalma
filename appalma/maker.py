


class PageStore(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PageStore, cls).__new__(cls)
        return cls.instance
  
    def add_to_page(self, key, page=None):        
        if not hasattr(self, 'pages'):
            self.pages = {}
        if key in self.pages:
            self.pages[key].play()
        else:             
            self.pages[key] = page
            page.play()



  
