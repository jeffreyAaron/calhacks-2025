import csv
from typing import List, Dict


class BOMParser:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.parts = []
        
    def parse_csv(self) -> List[Dict[str, str]]:
        # read the csv file and extract part information
        with open(self.csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.parts = [row for row in reader]
        return self.parts
    
    def get_parts(self) -> List[Dict[str, str]]:
        # return the parsed parts list
        if not self.parts:
            self.parse_csv()
        return self.parts
    
    def get_part_names(self) -> List[str]:
        # extract just the part names from the bom
        if not self.parts:
            self.parse_csv()
        # try common column names for part identification
        possible_columns = ['part_name', 'Part Name', 'part', 'Part', 'description', 'Description', 'item', 'Item']
        for col in possible_columns:
            if col in self.parts[0]:
                return [part[col] for part in self.parts]
        # if no standard column found, use the first column
        first_col = list(self.parts[0].keys())[0]
        return [part[first_col] for part in self.parts]


