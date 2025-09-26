import csv
import os
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass 
class MacroConfig:
    key_combination: str
    action_text: str

class CSVConfigLoader:
    def __init__(self):
        self.loaded_configs: List[MacroConfig] = []
        self.current_csv_file: Optional[str] = None

    def load_csv_config(self, csv_file_path: str) -> bool:
        self.loaded_configs.clear()
        self.current_csv_file = None

        if not os.path.exists(csv_file_path):
            print(f"Error: File '{csv_file_path}' does not exist")
            return False

        try:
            with open(csv_file_path, 'r', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)

                for row_number, row in enumerate(reader, 1):
                    if not row or len(row) < 2:
                        continue

                    key_combination = row[0].strip()
                    action_text = row[1].strip()

                    if not key_combination or not action_text:
                        print(f"Warning: Row {row_number} has empty fields, skipping")
                        continue

                    macro = MacroConfig(
                        key_combination = key_combination,
                        action_text = action_text
                    )

                    self.loaded_configs.append(macro)

            self.current_csv_file = csv_file_path
            print(f"Successfully loaded {len(self.loaded_configs)} macros from '{csv_file_path}'")
            return True
        
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
        
    def get_macros(self) -> List[MacroConfig]:
        return self.get_macros
    
    def get_current_file(self) -> Optional[str]:
        return self.current_csv_file

    def print_macros(self):
        if not self.loaded_configs:
            print("No macros loaded")
            return
        
        print(f"\nLoaded macros from: {self.current_csv_file}")
        print("-" * 50)
        for i, macro in enumerate(self.loaded_configs, 1):
            print(f"{i}. Key: '{macro.key_combination}'-> Text: '{macro.action_text}'")

if __name__ == "__main__":
    # Create a simple test CSV file
    test_csv_content = """Ctrl+Shift+F,def function_name():
F1,=SUM(A1:A10)
Alt+T,Hello World!
Ctrl+D,import datetime"""

# Write the test file
    with open("test_macros.csv", "w") as f:
        f.write(test_csv_content)
    
    # Test our CSV loader
    loader = CSVConfigLoader()
    
    print("Testing CSV Loader...")
    success = loader.load_csv_config("test_macros.csv")
    
    if success:
        loader.print_macros()
    else:
        print("Failed to load CSV file")
    
    # Clean up the test file
    os.remove("test_macros.csv")