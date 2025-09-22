# Customizable Macro Application Requirements Document

## 1. Project Overview

### 1.1 Purpose
Develop a Python-based customizable macro application that allows users to create and execute keyboard shortcuts for automated text insertion and actions, with configuration loaded from CSV files.

### 1.2 Target Users
- **Software developers** seeking to speed up coding workflows
- **Accountants and financial professionals** working in Excel with repetitive formulas and formatting
- **Data analysts** automating common Excel functions and pivot table operations
- **Administrative professionals** streamlining document creation and form filling
- **Writers and content creators** who frequently use boilerplate text
- **System administrators** automating repetitive tasks
- **General office workers** wanting custom shortcuts for any application

### 1.3 Key Benefits
- Reduces repetitive typing and increases productivity across all applications
- Customizable through simple CSV file configuration
- Template generation for coding patterns, Excel formulas, and document formatting
- Application-specific macro sets (different shortcuts for Excel vs Word vs IDE)
- Simple UI for toggling macros on/off and selecting active CSV configurations
- Easy to modify and share macro configurations between team members

## 2. Functional Requirements

### 2.1 Core Features

#### 2.1.1 CSV Configuration Loading
- **FR-001**: Application shall read macro configurations from CSV files
- **FR-002**: CSV format shall support two columns: Key Combination, Action/Text
- **FR-003**: Application shall validate CSV format and provide error messages for invalid entries
- **FR-004**: Users shall be able to reload CSV configurations without restarting the application
- **FR-005**: Application shall support multiple CSV files for different macro sets

#### 2.1.2 Key Combination Support
- **FR-006**: Support single key macros (e.g., F1, F2)
- **FR-007**: Support modifier key combinations (Ctrl+, Alt+, Shift+, Ctrl+Shift+, etc.)
- **FR-008**: Support function keys (F1-F12) with and without modifiers
- **FR-009**: Validate key combinations for conflicts and duplicates
- **FR-010**: Provide standardized key naming convention documentation

#### 2.1.3 Action Types
- **FR-011**: Text insertion - insert predefined text at cursor position
- **FR-012**: Template insertion - insert text with placeholder variables
- **FR-013**: Multi-line text support with proper formatting
- **FR-014**: Special character support (tabs, newlines, Unicode)
- **FR-015**: Variable substitution (e.g., {date}, {time}, {username}, {clipboard})
- **FR-016**: Excel-specific actions (formulas, cell references, formatting commands)
- **FR-017**: Application-specific text formatting (HTML tags, SQL queries, etc.)

#### 2.1.4 Macro Execution
- **FR-018**: Global hotkey detection across all applications
- **FR-019**: Application-specific macro sets (different macros for Excel, Word, IDEs, etc.)
- **FR-020**: Immediate text insertion at current cursor position
- **FR-021**: Undo support for macro insertions
- **FR-022**: Macro execution logging for debugging

#### 2.1.5 CSV Configuration Management
- **FR-023**: Load multiple CSV files simultaneously
- **FR-024**: Enable/disable individual CSV files through UI
- **FR-025**: CSV file selection and switching through simple interface
- **FR-026**: Display active CSV file name in UI
- **FR-027**: Quick reload functionality for modified CSV files

### 2.2 User Interface Requirements

#### 2.2.1 Main Interface
- **FR-028**: Simple main window with macro on/off toggle switch
- **FR-029**: CSV file selection dropdown or browser interface
- **FR-030**: Current active CSV file display
- **FR-031**: Macro count and status indicator
- **FR-032**: System tray icon for quick access when window is minimized

#### 2.2.2 Configuration Interface
- **FR-033**: Settings window for application preferences
- **FR-034**: Multiple CSV file management (load, unload, enable/disable)
- **FR-035**: Macro list viewer showing loaded key combinations and descriptions
- **FR-036**: Test macro functionality to verify configurations
- **FR-037**: Enable/disable individual macros or entire CSV files
- **FR-038**: Application-specific macro set assignment

#### 2.2.3 User Experience
- **FR-039**: One-click macro toggle (master on/off switch)
- **FR-040**: Visual feedback for macro activation status
- **FR-041**: Notification system for successful CSV loads and errors
- **FR-042**: Tooltips and help text for UI elements

### 2.3 File Management
- **FR-043**: Auto-save application settings and last loaded CSV configurations
- **FR-044**: Support for relative and absolute file paths
- **FR-045**: CSV file change detection and auto-reload option
- **FR-046**: Backup and restore functionality for macro configurations
- **FR-047**: Export functionality to share macro configurations
- **FR-048**: Multiple CSV file handling with priority/conflict resolution

## 3. Technical Requirements

### 3.1 Platform Support
- **TR-001**: Windows 10/11 primary support
- **TR-002**: Consider cross-platform compatibility (Linux, macOS) for future versions
- **TR-003**: Python 3.8+ compatibility

### 3.2 Performance Requirements
- **TR-004**: Hotkey response time < 100ms
- **TR-005**: Application startup time < 3 seconds
- **TR-006**: Memory usage < 50MB during normal operation
- **TR-007**: Support for 1000+ macro configurations without performance degradation

### 3.3 Dependencies and Libraries
- **TR-008**: `pynput` or `keyboard` for global hotkey detection
- **TR-009**: `pandas` or built-in `csv` module for CSV processing
- **TR-010**: `pystray` for system tray functionality
- **TR-011**: `tkinter` for GUI components (built-in with Python)
- **TR-012**: `watchdog` for file system monitoring (optional)

## 4. Non-Functional Requirements

### 4.1 Reliability
- **NFR-001**: Application shall recover gracefully from CSV format errors
- **NFR-002**: Hotkey conflicts shall be detected and reported
- **NFR-003**: Application shall handle special characters and Unicode properly
- **NFR-004**: Memory leaks shall be prevented during extended operation

### 4.2 Usability
- **NFR-005**: CSV format shall be intuitive for non-technical users
- **NFR-006**: Error messages shall be clear and actionable
- **NFR-007**: Application shall provide example CSV files and documentation
- **NFR-008**: Setup and configuration shall be completable in under 5 minutes

### 4.3 Security
- **NFR-009**: Application shall not store sensitive information in logs
- **NFR-010**: CSV files shall be validated to prevent code injection
- **NFR-011**: File access permissions shall be properly handled

## 5. CSV File Specification

### 5.1 Format Requirements
```csv
Key Combination,Action/Text,Application
Ctrl+Shift+F,def function_name():\n    pass,code
F1,=SUM(A1:A10),excel
Alt+T,import datetime\nnow = datetime.datetime.now(),python
Ctrl+D,=TODAY(),excel
F2,"Dear [Customer Name],\n\nThank you for your inquiry.",general
```

### 5.2 Supported Key Formats
- Single keys: `A`, `1`, `F1`, `Space`, `Enter`, `Tab`
- Modifiers: `Ctrl+`, `Alt+`, `Shift+`, `Win+`
- Combinations: `Ctrl+Shift+A`, `Alt+F1`, `Ctrl+Alt+T`

### 5.3 Action Format
- Plain text insertion
- `\n` for newlines, `\t` for tabs
- Variable placeholders: `{date}`, `{time}`, `{clipboard}`, `{username}`
- Excel formulas and functions
- HTML/XML tags and structures
- SQL queries and database commands

### 5.4 Application Column (Optional)
- `excel` - Active only in Microsoft Excel
- `word` - Active only in Microsoft Word
- `code` - Active in code editors (VS Code, Notepad++, etc.)
- `general` or blank - Active in all applications

## 6. User Stories

### 6.1 Developer Use Cases
- As a Python developer, I want to press `Ctrl+Shift+F` to insert a function template
- As a web developer, I want to press `Alt+H` to insert HTML boilerplate
- As a SQL developer, I want to press `Ctrl+Q` to insert common query structures

### 6.2 Excel/Accounting Use Cases
- As an accountant, I want to press `F1` to insert `=SUM()` formulas quickly
- As a financial analyst, I want to press `Ctrl+D` to insert today's date
- As a data analyst, I want to press `Alt+P` to insert pivot table formulas
- As an Excel user, I want to press `Ctrl+Shift+V` to insert VLOOKUP templates

### 6.3 General User Cases
- As a user, I want a simple toggle to turn all macros on or off
- As a user, I want to select which CSV file is active from a dropdown
- As a user, I want to see which macros are currently loaded and active
- As an office worker, I want to press `F2` to insert email signatures and templates

## 7. Implementation Phases

### Phase 1: Core Functionality (MVP)
- Basic CSV loading and parsing
- Simple text insertion macros
- System tray application
- Windows support

### Phase 2: Enhanced Features
- Template variables and substitution
- Application-specific macro sets
- GUI configuration interface
- File monitoring and auto-reload

### Phase 3: Advanced Features
- Macro recording functionality
- Cloud sync for configurations
- Plugin system for custom actions
- Cross-platform support

## 8. Testing Requirements

### 8.1 Unit Testing
- CSV parsing and validation
- Key combination parsing
- Text insertion functionality
- Variable substitution

### 8.2 Integration Testing
- End-to-end macro execution
- System tray integration
- File system interactions
- Cross-application hotkey detection

### 8.3 User Acceptance Testing
- Real-world usage scenarios
- Performance under heavy macro usage
- Usability testing with sample CSV files

## 9. Deployment and Distribution

### 9.1 Packaging
- Standalone executable using PyInstaller
- Installer package for easy setup
- Portable version requiring no installation

### 9.2 Documentation
- User manual with CSV format examples
- Developer guide for extending functionality
- Troubleshooting guide for common issues

## 10. Future Considerations

### 10.1 Potential Enhancements
- GUI macro editor with CSV export
- Macro sharing community/marketplace
- Advanced scripting capabilities
- Integration with popular IDEs and editors
- Mobile companion app for macro management

### 10.2 Scalability
- Cloud-based macro synchronization
- Team/organization macro sharing
- Analytics for most-used macros
- AI-suggested macros based on usage patterns