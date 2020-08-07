import sys
import pathlib
import os

class DayZLogCleaner():
    def __init__(self):
        os.system("mode con: cols=55 lines=20")
        os.system("TITLE DayZ Log Cleaner")
        os.system('color 0A')
        
        self.log_path = pathlib.Path.home() / "AppData/Local/DayZ"
        self.log_extensions = {"mdmp", "RPT", "log"}
    
    def is_log_file(self, file) -> "bool":
        return file.split(".")[-1] in self.log_extensions and os.path.isfile(file)
        
    def convert_size(self, size,precision = 2) -> "str":
        suffixes = [' B',' KB',' MB',' GB',' TB']
        suffixIndex = 0
        while size > 1024 and suffixIndex < 4:
            suffixIndex += 1 #increment the index of the suffix
            size = size/1024.0 #apply the division
        return "%.*f%s"%(precision,size,suffixes[suffixIndex])
    
    def pre_compute(self) -> None:
        self.logs_to_delete = []
        delete_size = 0
        log_count = 0
        
        for f in os.listdir(self.log_path):
            abs_file_path = os.path.join(self.log_path, f)
            if self.is_log_file(abs_file_path):
                self.logs_to_delete.append(abs_file_path)
                delete_size += os.stat(abs_file_path).st_size
                log_count += 1
        self.log_stats = f"Found {log_count} log files ({self.convert_size(delete_size)})."
    
    def delete_logs(self) -> "bool":
        self.error = 0
        for f in self.logs_to_delete:
            try:
                os.remove(f)
            except:
                self.error += 1
    
    def confirm_delete(self) -> "bool":
        resp = input("Are you sure you want to delete ALL DayZ log files? [Y/n]").strip()
        if len(resp) > 0 and resp.lower() not in {"yes", "y"}:
            print("Aborting...")
            return False
        else:
            print("Deleting Logs...")
            return True
    
    def exit(self):
        print("Exitting...")
        os.system('pause')
    
    def run(self) -> None:
        os.system('cls')
        if not pathlib.Path.exists(self.log_path):
            print(f"[!] DayZ Log folder not found. ({self.log_path} does not exist.)")
            self.exit()
            return
        
        self.pre_compute()
        print(self.log_stats)
        
        if self.logs_to_delete and self.confirm_delete():
            self.delete_logs()
            if(self.error):
                print(f"[!] Unable to delete {self.error} files. Make sure your game isn't running!")
            print("Done!.")
        self.exit()
        
if __name__ == "__main__":
    cleaner = DayZLogCleaner()
    if sys.platform == "win32":
        cleaner.run()
    else:
        print(f"[!] Unsupported OS: {sys.platform}")
        cleaner.exit()
        
        