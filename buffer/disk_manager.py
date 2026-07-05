import os
from .page import PAGE_SIZE

class DiskManager:

    def __init__(self, db_file: str):
        self.db_file = db_file
        self.next_page_id = 0
        
        if not os.path.exists(self.db_file):
          
            os.makedirs(os.path.dirname(os.path.abspath(self.db_file)), exist_ok=True)
            with open(self.db_file, "wb") as f:
                pass
        else:
       
            file_size = os.path.getsize(self.db_file)
            self.next_page_id = file_size // PAGE_SIZE

    def read_page(self, page_id: int, page_data: bytearray):
        offset = page_id * PAGE_SIZE
        with open(self.db_file, "rb") as f:
            f.seek(offset)
            data = f.read(PAGE_SIZE)
            if len(data) < PAGE_SIZE:
                data = data.ljust(PAGE_SIZE, b'\0')
            page_data[:] = data

    def write_page(self, page_id: int, page_data: bytearray):
   
        offset = page_id * PAGE_SIZE
        with open(self.db_file, "r+b") as f:
            f.seek(offset)
            f.write(page_data)
            f.flush()
            os.fsync(f.fileno())

    def allocate_page(self) -> int:

        page_id = self.next_page_id
        self.next_page_id += 1
        
        empty_data = bytearray(PAGE_SIZE)
        with open(self.db_file, "a+b") as f:
            f.write(empty_data)
            f.flush()
            os.fsync(f.fileno())
            
        return page_id
