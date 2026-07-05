PAGE_SIZE = 4096

class Page:

    def __init__(self):
        self.page_id = -1
        self.data = bytearray(PAGE_SIZE)
        self.pin_count = 0
        self.is_dirty = False

    def reset(self):
        
        self.page_id = -1
        self.data = bytearray(PAGE_SIZE)
        self.pin_count = 0
        self.is_dirty = False
