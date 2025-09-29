import csv
import os
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from errors import ErrorCategory, ErrorSeverity, LoaderError

@dataclass 
class MacroConfig:
    key_combination: str
    action_text: str

class CSVConfigLoader:
    def __init__(self):
        self.loaded_macros: List[MacroConfig] = []
        self.current_csv_file: Optional[str] = None
        self.errors: List[LoaderError] = []

    def add_error(self, category: ErrorCategory, severity: ErrorSeverity, message: str, line_number: int = 0):
        error = LoaderError(category, severity, message, line_number)
        self.errors.append(error)

    def check_header(self, all_rows) -> list:
        if len(all_rows[0]) > 0:
            if (all_rows[0][0].lower() == "key combination" or 
                all_rows[0][0].lower() == "key" or 
                all_rows[0][0].lower() == "combination" or
                all_rows[0][0].lower() == "macro"):
                all_rows.pop(0)
        return all_rows

    def load_csv_file(self, csv_file_path: str) -> bool:
        self.loaded_macros.clear()
        self.errors.clear()
        self.current_csv_file = None

        if not os.path.exists(csv_file_path):
            self.add_error(ErrorCategory.FILE, ErrorSeverity.ERROR, 
                           f"CSV file cannot be opened: {csv_file_path}")
            return False
        
        if not csv_file_path.lower().endswith('.csv'):
            self.add_error(ErrorCategory.FILE, ErrorSeverity.ERROR, 
                        f"File must be a .csv file: {csv_file_path}")
            return False

        try:
            with open(csv_file_path, 'r', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                all_rows = list(reader)

                if not all_rows:
                    self.add_error(ErrorCategory.FILE, ErrorSeverity.ERROR, 
                           f"CSV file is empty: {csv_file_path}")
                    return False
    
                all_rows = self.check_header(all_rows) 

                if not all_rows:
                    self.add_error(ErrorCategory.FILE, ErrorSeverity.ERROR, 
                           f"CSV file contains only headers: {csv_file_path}")
                    return False

                for row_number, row in enumerate(all_rows, 1):
                    if not row or len(row) < 2:
                        self.add_error(ErrorCategory.ROW, ErrorSeverity.WARNING, 
                           f"Row {row_number} has missing fields, skipping")
                        continue

                    key_combination = row[0].strip()
                    action_text = row[1].strip()

                    if not key_combination or not action_text:
                        self.add_error(ErrorCategory.ROW, ErrorSeverity.WARNING, 
                           f"Row {row_number} has empty fields, skipping")
                        continue

                    if len(row) > 2:
                        self.add_error(ErrorCategory.ROW, ErrorSeverity.WARNING, 
                            f"Row {row_number} has extra columns, ignoring them")

                    macro = MacroConfig(
                        key_combination = key_combination,
                        action_text = action_text
                    )

                    self.loaded_macros.append(macro)

            self.current_csv_file = csv_file_path
            print(f"Successfully loaded {len(self.loaded_macros)} macros from '{csv_file_path}'")
            
            return True
        
        except Exception as e:
            self.add_error(ErrorCategory.FILE, ErrorSeverity.ERROR, 
                           f"Error reading file:  {csv_file_path}")
        return self.get_macros
    
    def get_current_file(self) -> Optional[str]:
        return self.current_csv_file

    def print_macros(self):
        if not self.loaded_macros:
            print("No macros loaded")
            return
        
        print(f"\nLoaded macros from: {self.current_csv_file}")
        print("-" * 50)
        for i, macro in enumerate(self.loaded_macros, 1):
            print(f"{i}. Key: '{macro.key_combination}'-> Text: '{macro.action_text}'")

    def run_loader(self):
        while(True):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("CSV loader")
            print("*"*20)
            csv_file_path = input("Enter File Path: ")
            success = self.load_csv_file(csv_file_path)

            for error in self.errors:
                    print(f"{error.severity.value.upper()}! {error.category.value.upper()}: {error.message}")
        
            if success:
                self.print_macros()
            else:
                print("Failed to load CSV file")
        
            if not (input("Would you like to load another file? (y/n) ").startswith("y")):
                return


              

if __name__ == "__main__":
    # Create a simple test CSV file
    test_csv_content = """Key Combination, Action/Text
Ctrl+Shift+F,def function_name():
F1,=SUM(A1:A10)
Alt+T,Hello World!
Ctrl+D,import datetime"""

# Write the test file
    with open("test_macros.csv", "w") as f:
        f.write(test_csv_content)
    
    # Test our CSV loader
    loader = CSVConfigLoader()
    
    print("Testing CSV Loader...")
    loader.run_loader()
    
    # Clean up the test file
    os.remove("test_macros.csv")