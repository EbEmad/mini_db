from collections import OrderedDict
from typing import Optional

class LRUReplacer:

    def __init__(self, num_pages: int):
        self.capacity = num_pages
        self.frames = OrderedDict()

    def victim(self) -> Optional[int]:
  
        if len(self.frames) == 0:
            return None
        
        frame_id, _ = self.frames.popitem(last=False)
        return frame_id

    def pin(self, frame_id: int):

        if frame_id in self.frames:
            del self.frames[frame_id]

    def unpin(self, frame_id: int):
    
        if frame_id not in self.frames:
 
            self.frames[frame_id] = True

    def size(self) -> int:

        return len(self.frames)
