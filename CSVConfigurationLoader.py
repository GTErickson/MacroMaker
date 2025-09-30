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

@dataclass
class MacroSet:
    file_path: str
    macros: List[MacroConfig]
    enabled: bool = True

class CSVConfigLoader:
    def __init__(self):
        self.macro_sets: List[MacroSet] = []
        self.loaded_files: List[str] = []
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
                self.current_csv_file = csv_file_path
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
                
                temp_macros = [] 

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

                    temp_macros.append(macro)

            macro_set = MacroSet(
                file_path=csv_file_path,
                macros=temp_macros,
                enabled=True
            )
            self.macro_sets.append(macro_set)

            print(f"Successfully loaded {len(self.macro_sets)} macros from '{csv_file_path}'")
            
            return True
        
        except Exception as e:
            self.add_error(ErrorCategory.FILE, ErrorSeverity.ERROR, 
                           f"Error reading file:  {csv_file_path}")
        return False
    
    def get_current_file(self) -> Optional[str]:
        return self.current_csv_file

    def print_macros(self):
        if not self.macro_sets:
            print("No macros loaded")
            return
        
        print(f"\nLoaded macros from: {self.current_csv_file}")
        print("-" * 50)
        for i, macro_set in enumerate(self.macro_sets, 1):
            print(f"Macro Set {1} ({macro_set.file_path})")
            for i, macro in enumerate(macro_set.macros, 1):
                print(f"{i}. Key: '{macro.key_combination}'-> Text: '{macro.action_text}'")

    def run_loader(self):
        self.macro_sets.clear()
        self.errors.clear()
        os.system('cls' if os.name == 'nt' else 'clear')

        while(True):
            print("\nCSV loader")
            print("*"*20)
            print(f"Currently loaded: {len(self.macro_sets)} file(s)")
            csv_file_path = input("Enter file path (or 'done' to finish): ")

            if csv_file_path.lower() == 'done':
                break

            success = self.load_csv_file(csv_file_path)

            for error in self.errors:
                    print(f"{error.severity.value.upper()}! {error.category.value.upper()}: {error.message}")
        
            if success:
                self.print_macros()
            else:
                print("Failed to load CSV file")


              

if __name__ == "__main__":
    # Test CSV 1: Excel/Accounting Macros
    test_csv_content1 = """Key Combination,Action/Text
    F1,=SUM(A1:A10)
    F2,"=VLOOKUP(A1,Sheet2!A:B,2,FALSE)"
    Ctrl+D,=TODAY()
    Ctrl+Shift+P,"=IF(A1>0,""Profit"",""Loss"")"
    Alt+F,=AVERAGE(B1:B20)"""

    # Test CSV 2: Programming/Code Macros
    test_csv_content2 = """Key Combination,Action/Text
    Ctrl+Shift+F,"def function_name():\n    pass"
    Alt+C,"class ClassName:\n    def __init__(self):\n        pass"
    Ctrl+I,"import datetime\nfrom typing import List"
    F5,"if __name__ == ""__main__"":\n    pass"
    Ctrl+T,"try:\n    pass\nexcept Exception as e:\n    print(e)"""

    # Test CSV 3: Email/Communication Templates
    test_csv_content3 = """Key Combination,Action/Text
    F10,"Dear [Name],\n\nThank you for your email."
    F11,"Best regards,\n[Your Name]\n[Your Title]"
    Ctrl+E,"Please let me know if you have any questions.\n\nThank you!"
    Alt+M,"I hope this message finds you well."
    Ctrl+F1,"Following up on our previous conversation regarding [Topic]."""

    # Test CSV 4: Minimal test with duplicate key (for conflict testing)
    test_csv_content4 = """Key Combination,Action/Text
    F1,This is a DUPLICATE F1 key!
    Ctrl+X,Cut this text
    Ctrl+C,Copy this text"""


    with open("excel_macros.csv", "w") as f:
        f.write(test_csv_content1)

    with open("code_macros.csv", "w") as f:
        f.write(test_csv_content2)

    with open("email_templates.csv", "w") as f:
        f.write(test_csv_content3)

    with open("duplicate_test.csv", "w") as f:
        f.write(test_csv_content4)
    
    # Test our CSV loader
    loader = CSVConfigLoader()
    
    print("Testing CSV Loader...")
    loader.run_loader()
    
    # Clean up the test file
    os.remove("excel_macros.csv")
    os.remove("code_macros.csv")
    os.remove("email_templates.csv")
    os.remove("duplicate_test.csv")