import csv
from typing import List, Dict


class CSVUpdater:
    def __init__(self, original_csv_path: str, output_csv_path: str = None):
        self.original_csv_path = original_csv_path
        self.output_csv_path = output_csv_path or original_csv_path.replace('.csv', '_updated.csv')
        
    def append_results_to_csv(self, original_parts: List[Dict], search_results: Dict[str, List[Dict]]):
        # read original csv to get headers and structure
        with open(self.original_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            original_headers = reader.fieldnames
            original_rows = list(reader)
        
        # create new headers with additional columns
        new_headers = list(original_headers) + [
            'website', 
            'product_name_found', 
            'product_url', 
            'price', 
            'cart_url', 
            'added_to_cart'
        ]
        
        # prepare rows to write
        output_rows = []
        
        # get the part name column
        possible_columns = ['part_name', 'Part Name', 'part', 'Part', 'description', 'Description', 'item', 'Item']
        part_col = None
        for col in possible_columns:
            if col in original_headers:
                part_col = col
                break
        if not part_col:
            part_col = original_headers[0]
        
        # for each original row, create multiple rows with website results
        for original_row in original_rows:
            part_name = original_row[part_col]
            
            if part_name in search_results:
                results = search_results[part_name]
                
                if results:
                    # create a row for each website result
                    for result in results:
                        new_row = original_row.copy()
                        new_row['website'] = result.get('website', '')
                        new_row['product_name_found'] = result.get('product_name', '')
                        new_row['product_url'] = result.get('product_url', '')
                        new_row['price'] = result.get('price', '')
                        new_row['cart_url'] = result.get('cart_url', '')
                        new_row['added_to_cart'] = result.get('added_to_cart', False)
                        output_rows.append(new_row)
                else:
                    # no results found, add original row with empty new columns
                    new_row = original_row.copy()
                    for header in ['website', 'product_name_found', 'product_url', 'price', 'cart_url', 'added_to_cart']:
                        new_row[header] = ''
                    output_rows.append(new_row)
            else:
                # part not in search results, add original row with empty new columns
                new_row = original_row.copy()
                for header in ['website', 'product_name_found', 'product_url', 'price', 'cart_url', 'added_to_cart']:
                    new_row[header] = ''
                output_rows.append(new_row)
        
        # write the updated csv
        with open(self.output_csv_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=new_headers)
            writer.writeheader()
            writer.writerows(output_rows)
        
        print(f"updated csv saved to: {self.output_csv_path}")
        return self.output_csv_path


