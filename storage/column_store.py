import os
import json
from typing import Dict
class ColumnStore:

    def __init__(self,data_dir="./data"):
        self.data_dir=data_dir
        self.wal_path=os.path.join(data_dir,"wal.log")
        self.flush_threshold=5
        os.makedirs(self.data_dir,exist_ok=True)
        self.memtable={"id":[],"name":[],"age":[],"salary":[]}
        self._recover_from_wal()

    def _apply_to_memtable(self,row_data):
        self.memtable["id"].append(row_data.get("id"))
        self.memtable['name'].append(row_data.get('name'))
        self.memtable['age'].append(row_data.get('age'))
        self.memtable['salary'].append(row_data.get('salary'))

    def _flush_to_disk(self):
        print(f"Flushing {len(self.memtable['id'])} rows to columnar disk files...")

        for col_name,col_data in self.memtable.items():
            col_path=os.path.join(self.data_dir,f"{col_name}.col")

            with open(col_path,'a') as f:
                f.write(json.dumps(col_data)+ "\n")
            
        self.memtable={"id":[],"name":[],"age":[],"salary":[]}

        
    def _recover_from_wal(self):
        if not os.path.exists(self.wal_path):
            return
        
        print("Recovering from WAL...")
        with open(self.wal_path,"r") as wal_file:
            for line in wal_file:
                row_data=json.loads(line)
                self._apply_to_memtable(row_data)

    def insert(self,row_data):
        with open(self.wal_path,'a') as wal_file:
            wal_file.write(json.dumps(row_data)+"\n")
            wal_file.flush()
            os.fsync(wal_file.fileno())
        self._apply_to_memtable(row_data)

        if len(self.memtable['id'])>=self.flush_threshold:
            self._flush_to_disk()

        
            

        
        
if __name__ == "__main__":
    db = ColumnStore()
    print("Inserting data...")
    
    db.insert({"id": 1, "name": "Alice", "age": 30})
    db.insert({"id": 2, "name": "Bob", "age": 25})
    db.insert({"id": 3, "name": "Charlie", "age": 35})
    
    db.insert({"id": 4, "name": "Diana", "age": 28})
    db.insert({"id": 5, "name": "Eve", "age": 40})
    
    db.insert({"id": 6, "name": "Frank", "age": 22}) 