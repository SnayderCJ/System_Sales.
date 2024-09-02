from Utilis import green_color, blue_color, purple_color, reset_color
from datetime import datetime
from clsJson import JsonFile
import os

path, file = os.path.split(__file__)

class Company:
    next = 0    
    def __init__(self, name = "Super Maxi", ruc = "0943213456001"):
        Company.next += 1
        self._id = Company.next
        self.name = name
        self.ruc = ruc
    
    def __str__(self):
        return f"id:{self._id}\nCompañia:{self.name}\nRuc:{self.ruc}\n"
    
    json_file = JsonFile(f"{path}/data/company.json")

    def show(self):
        companies = self.json_file.read()
        for company in companies:
            date_str = datetime.now().strftime("%Y-%m-%d")
            print(f"{blue_color}Compañia: {purple_color}{company['name']:<40}{reset_color} {blue_color}Fecha: {purple_color}{date_str}{reset_color}")
            print(f"{blue_color}Ruc: {purple_color}{company['ruc']}{reset_color}")
    
    def getjson(self):
        return {
            "id": self._id,
            "name": self.name,
            "ruc": self.ruc }
    
    
if __name__ == "__main__":
    comp = Company()
    comp.show()

