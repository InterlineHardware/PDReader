import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter
from tkinter import ttk, scrolledtext
from src.Manager import Manager
import src.Logline as Logline
import pywinstyles
from src.Utilities import load_config, save_config


customtkinter.set_default_color_theme("dark-blue")
logger = Logline.Logger("PRODUCT DATA UI").logger

class File:
    def __init__(self, file_path):
        self.file_name = os.path.basename(file_path)
        self.file_path = file_path
        self.is_favorite = False


# Login Form

class App(customtkinter.CTk):
    def __init__(self,):
        super().__init__()
        self.withdraw()  # Hide the main window until login succeeds
        self.login = LoginWindow(master=self, on_success=self.open_main)
        self.login.protocol("WM_DELETE_WINDOW", self.quit_app)

    def open_main(self, manager):
        self.file_explorer = FileExplorerApp(master=self, manager=manager)
        
        # Bind the close event of FileExplorerApp to close the entire app
        self.file_explorer.protocol("WM_DELETE_WINDOW", self.quit_app)

    def quit_app(self):
        """Destroy the main app when FileExplorerApp closes."""
        self.destroy()

class LoginWindow(customtkinter.CTkToplevel):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.title("Login")
        self.geometry("500x250")
        self.on_success = on_success
        self.resizable(False, False)

        self.saved = load_config()  # your existing config loader
        self.credentials = None  # store credentials if login succeeds

        # Layout with 2 columns
        self.grid_columnconfigure(0, weight=1, uniform="col")
        self.grid_columnconfigure(1, weight=2, uniform="col")

        row = 0
        # Company
        customtkinter.CTkLabel(self, text="Company:").grid(row=row, column=0, padx=10, pady=15, sticky="e")
        self.entry_company = customtkinter.CTkEntry(self, width=200)
        self.entry_company.grid(row=row, column=1, padx=10, pady=5, sticky="w",)
        self.entry_company.insert(0, self.saved.get("company", ""))
        row += 1

        # Username
        customtkinter.CTkLabel(self, text="Username:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.entry_user = customtkinter.CTkEntry(self, width=200)
        self.entry_user.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        self.entry_user.insert(0, self.saved.get("username", ""))
        row += 1

        # Password
        customtkinter.CTkLabel(self, text="Password:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.entry_pass = customtkinter.CTkEntry(self, width=200, show="*")
        self.entry_pass.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        row += 1

        # Host
        customtkinter.CTkLabel(self, text="Host:").grid(row=row, column=0, padx=10, pady=5, sticky="e")
        self.entry_host = customtkinter.CTkEntry(self, width=200)
        self.entry_host.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        self.entry_host.insert(0, self.saved.get("host", ""))
        row += 1

        # Save credentials checkbox
        self.save_var = customtkinter.BooleanVar(value=True)
        self.checkbox_save = customtkinter.CTkCheckBox(self, text="Save credentials", variable=self.save_var)
        self.checkbox_save.grid(row=row, column=0, columnspan=2, pady=5)
        row += 1

        # Login button
        self.button_login = customtkinter.CTkButton(self, text="Login", command=self.try_login)
        self.button_login.grid(row=row, column=0, columnspan=2, pady=10)

    def try_login(self):
        creds = {
            "company": self.entry_company.get().strip(),
            "username": self.entry_user.get().strip(),
            "password": self.entry_pass.get().strip(),
            "host": self.entry_host.get().strip(),
        }

        if not all(creds.values()):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            # Try initializing Manager
            self.manager = Manager(**creds)
        except Exception as e:
            retry = messagebox.askretrycancel("Login Failed", f"Could not login:\n{e}\n\nRetry?")
            if retry:
                return  # let user fix credentials
            else:
                self.destroy()  # close app
                return

        # Save config if checked
        if self.save_var.get():
            save_config(creds)

        self.destroy()
        self.on_success(self.manager)
        

# Main UI 

class FileExplorerApp(customtkinter.CTkToplevel):
    
    # >> FIELDS FOR POPUP WINDOWS
    # >> The Fields for Each Popup window are stored in this dictionary with a 
    # >> Label 
    # >> Type { one of @entry, @text, @comboBox }
    # >> Default value
    
    sheet_options = {
        "Sheet Name": {"type": "entry", "default": "Product Data"},
        "Minimum Row" : {"type" : "entry", "default": "2"},
        "Maximum Row": {"type": "entry", "default": "2"},

    }

    Stage2fields = {
    "Sheet Name": {"type": "entry", "default": "Product Data"},
    "Specification Format": {"type": "combobox", "options": ["1", "2"], "default": "2"},
    
    "description": {"type": "entry", "default": "U"},
    "feat_start": {"type": "entry", "default": "V"},
    "feat_end": {"type": "entry", "default": "AE"},
    "concatFeat": {"type": "entry", "default": "AF"},
    "HTMLFeatDesc": {"type": "entry", "default": "AG"},
    
    "inc_start": {"type": "entry", "default": "MM"},
    "inc_end": {"type": "entry", "default": "MM"},
    "concatInc": {"type": "entry", "default": "MM"},
    "JSONInc": {"type": "entry", "default": "MM"},
    
    "appStart": {"type": "entry", "default": "MM"},
    "appEnd": {"type": "entry", "default": "MM"},
    "concatApp": {"type": "entry", "default": "MM"},
    "JSONApp": {"type": "entry", "default": "MM"},
    
    "specStart": {"type": "entry", "default": "AO"},
    "specEnd": {"type": "entry", "default": "BF"},
    "concatSpec": {"type": "entry", "default": "BG"},
    "JSONSpecs": {"type": "entry", "default": "BH"},
    
    "imgStart": {"type": "entry", "default": "BI"},
    "imgEnd": {"type": "entry", "default": "BP"},
    "concatImgs": {"type": "entry", "default": "BQ"},
    
    }
    
    Matrixifyfields = {
            "Sheet Name": {"type": "entry", "default": "Product Data"},
            "Minimum Row": {"type": "entry", "default": "2"},
            "Maximum Row": {"type": "entry", "default": "2"}
        }
    
    Upload_TPO_Fileds = {
            "Sheet Name": {"type": "entry", "default": "Product Data"}
        }
    
    READ_MANUAL_FIELDS = {
        "Sheet Name": {"type": "entry", "default": "Product Data"},
        "Maximum Row": {"type": "entry", "default": "2"}
    }

    WRITE_LINKS_FIELDS = {
        "Sheet Name": {"type": "entry", "default": "Product Data"},
        "Maximum Row": {"type": "entry", "default": "2"},
        "Export File" : {"type" : "open"}
    }

#---------------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------------#


    def __init__(self, manager : Manager, master):
        
        super().__init__(master)
        # tkdnd_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tkdnd2.8"))  # Example path
        # self.tk.call('lappend', 'auto_path', tkdnd_path)
        # self.tk.call('package', 'require', 'tkdnd')

        # >> Geometry for the Main Window

        
        self.title("Product Data UI")
        self.geometry("800x450")  # Adjusted window height to 450
        self.manager = manager
        # Set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Initialize selected_file as None
        self.selected_file = None

        # Create sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        # >> Headers and Tabs
        # Logo Label
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Interline", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Create a Tabview with text icons
        self.tabview = customtkinter.CTkTabview(self.sidebar_frame, width=180)
        self.tabview.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="nsew")

        # Adding tabs with text icons
        self.tabview.add("⚙️")
        self.tabview.add("🔍")
        self.tabview.add("💾") 

        #-------------------------------------------------- Buttons -----------------------------------------------------------------#

        button_width = 250  # Set a fixed width for all buttons
        button_height = 40  # Set height for thicker buttons

        # Tab 1 Buttons
        self.Stage2Button = customtkinter.CTkButton(self.tabview.tab("⚙️"), text="STAGE 2", width=button_width, height=button_height,
                                    command = lambda: CustomPopup(self,self.Stage2fields,self.process_stage2_data,self.selected_file), )
        self.Stage2Button.pack(pady=10, fill="x")

        self.PushToSpireButton = customtkinter.CTkButton(self.tabview.tab("⚙️"), text="PUSH TO SPIRE", width=button_width, height=button_height,
                                command= lambda : CustomPopup(self, self.Matrixifyfields, self.processSpirePush, self.selected_file), )
        self.PushToSpireButton.pack(pady=10, fill="x")

        self.MatrixifyButton = customtkinter.CTkButton(self.tabview.tab("⚙️"), text="MATRIXIFY", width=button_width, height=button_height,
                                command= lambda : CustomPopup(self, self.Matrixifyfields, self.processMatrixify, self.selected_file), )
        self.MatrixifyButton.pack(pady=10, fill="x")

        # Tab 2 Buttons
        self.CheckUploadButton = customtkinter.CTkButton(self.tabview.tab("🔍"), text="Check Upload",fg_color="firebrick2", 
                                                         width=button_width, height=button_height,
                                                         command = lambda : CustomPopup(self, self.Upload_TPO_Fileds, self.processUpoad, self.selected_file) )
        self.CheckUploadButton.pack(pady=10, fill="x")

        self.TPOButton = customtkinter.CTkButton(self.tabview.tab("🔍"), text="Remove From To Put Online", fg_color="firebrick2", 
                                                         width=button_width, height=button_height,
                                                         command = lambda : CustomPopup(self, self.Upload_TPO_Fileds, self.processTPO,self.selected_file) )
        self.TPOButton.pack(pady=10, fill="x")

        # Tab 3 Buttons
        self.processButton = customtkinter.CTkButton(self.tabview.tab("💾"), text="Process PD", width=button_width, height=button_height,
                                command= lambda : CustomPopup(self, self.sheet_options, self.proccessPD, self.selected_file), )
        self.processButton.pack(pady=10, fill="x")

        self.uploadButton = customtkinter.CTkButton(self.tabview.tab("💾"), text="Upload to Database", width=button_width, height=button_height,
                                    command = self.uploadFiles, )
        self.uploadButton.pack(pady=10, fill="x")

        dropdownDefaultVal = customtkinter.StringVar(value="Milwaukee Product Information")  # set initial value

        self.combobox = customtkinter.CTkComboBox(master=self.tabview.tab("💾"),
                                        values=["Milwaukee Product Information", "Milwaukee Price List", "Milwaukee IMAP"],
                                        variable=dropdownDefaultVal,
                                        width=button_width)
        self.combobox.pack(pady=10, fill="x")

        # Common Buttons
        self.openFileButton = customtkinter.CTkButton(self.sidebar_frame, text="Open File", command=self.open_selected_file, width=button_width // 2)
        self.openFileButton.grid(row=10, column=0, padx=(20, 5), pady=10, sticky="w")

        self.closeButton = customtkinter.CTkButton(self.sidebar_frame, text="Close", command=self.close_app, width=button_width // 2)
        self.closeButton.grid(row=10, column=0, padx=(5, 20), pady=10, sticky="e")
        
        #--------------------------------------------------------Frames---------------------------------------------------------------#
        
        # Create table frame with drag-and-drop area
        self.table_frame = tk.Frame(self,)
        self.table_frame.grid(row=0, column=1, sticky="nsew")

        # Create Treeview frame
        self.treeview_frame = tk.Frame(self.table_frame, padx=10, pady=50)  # Add padding
        self.treeview_frame.pack(side="left", fill="both", expand=True)

        # Treeview for displaying files with hidden file path column
        self.openedFilesWindow = ttk.Treeview(self.treeview_frame, columns=("File Name", "File Path"), show="headings", height=10)
        self.openedFilesWindow.config(selectmode='browse')
        self.openedFilesWindow.heading("File Name", text="Files")
        self.openedFilesWindow.column("File Path", width=0, stretch=tk.NO)  # Hide the File Path column
        self.openedFilesWindow.pack(fill="both", expand=True)


        # Drag-and-Drop area
        self.drop_area = customtkinter.CTkLabel(self.table_frame, text="➕ \nUpload Files", corner_radius=10, 
                                                fg_color="white", wraplength=300, padx=20, pady=20)  # Add padding
        self.drop_area.pack(expand=True, fill="both", padx=20, pady=(50, 50))  # Adjust padding to create space between widgets

        # Register drop area as a DND target
        # self.drop_area.drop_target_register(DND_FILES)
        pywinstyles.apply_dnd(self.drop_area, self.drop)
        self.drop_area.bind("<Button-1>", lambda e: self.open_file_explorer())
        self.openedFilesWindow.bind("<Button-3>", self.clear_selection)

        # Bind Treeview select event
        self.openedFilesWindow.bind("<<TreeviewSelect>>", self.on_file_select)
    
    #------------------------------------------------------------------------------------------------------------------------------------------------#
    #---------------------------------------------------- Button Functions --------------------------------------------------------------------------#

    def on_file_select(self, event):
        # Get the selected item
        selected_item = self.openedFilesWindow.selection()
        if selected_item:
            # Get the file path of the selected item from the hidden column
            self.selected_file = self.openedFilesWindow.item(selected_item)["values"][1]
            print(f"Selected file path: {self.selected_file}")
    
    def clear_selection(self, event):
        self.openedFilesWindow.selection_remove(self.openedFilesWindow.selection())
   
    def drop(self, event):
        # Extract file paths and update the Treeview
        file_paths = self.tk.splitlist(event)
        for file_path in file_paths:
            file_name = os.path.basename(file_path)  # Extract the file name
            self.openedFilesWindow.insert("", "end", values=(file_name, file_path))  # Insert both file name and path

    def open_file_explorer(self):
        file_paths = filedialog.askopenfilenames(initialdir=".")
        for file_path in file_paths:
            file_name = os.path.basename(file_path)  # Extract the file name
            self.openedFilesWindow.insert("", "end", values=(file_name, file_path))

    
    def open_selected_file(self):
        if self.selected_file:
            print("Opening selected file:", self.selected_file)
            os.startfile(self.selected_file)
        else:
            messagebox.showerror("No file selected", "Please select a file before opening.")

    def process_stage2_data(self, data : dict):
        sheet_name = data.pop("Sheet Name")
        try:
            spec_format = int(data.pop("Specification Format"))
        except Exception as err:
            messagebox.showerror(title="error", message=f"Invalid Spec Format : {err}")
        filepath = data.pop("FilePath")
        
        if not sheet_name or not spec_format:
            messagebox.showerror(title="error",message="All fields must be filled out!")
            return
         
        self.manager.convertToStage2(filepath,sheet_name, spec_format,data)

    def processMatrixify(self, data : dict):
        sheetName = data.get("Sheet Name")
        maxRow = int(data.get("Maximum Row"))
        minRow = int(data.get("Minimum Row"))
        filePath = data.get("FilePath")
        
        if not sheetName or not maxRow:
            messagebox.showerror(title="error",message="All fields must be filled out!")
            return

        self.manager.Matrxify(filePath, sheetName,minRow, maxRow)
    
    def processUpoad(self, data : dict):
        
        confirm = messagebox.askyesno(title="Confirm", message="Cofrim Upload To Web?")
        if not confirm:
            print("upload Cancelled")
            return
        
        sheetName = data.get("Sheet Name")
        filePath = data.get("FilePath")

        if not sheetName:
            messagebox.showerror(title="error",message="All fields must be filled out!")
            return

        self.manager.CheckUpload(filePath,sheetName)

    def processTPO(self, data : dict):
        
        confirm = messagebox.askyesno(title="Confirm", message="Cofrim Falsing To Put Online?")
        if not confirm:
            print("Cancelled")
            return
    
        sheetName = data.get("Sheet Name")
        filePath = data.get("FilePath")

        if not sheetName:
            messagebox.showerror(title="error",message="All fields must be filled out!")
            return

        self.manager.ToPutOnline(filePath,sheetName)

    def processSpirePush(self, data : dict):
        sheetName = data.get("Sheet Name")
        maxRow = int(data.get("Maximum Row"))
        minRow = int(data.get("Minimum Row"))
        filePath = data.get("FilePath")
        
        if not sheetName or not maxRow:
            messagebox.showerror(title="error",message="All fields must be filled out!")
            return

        self.manager.pushtoSpire(filePath, sheetName,minRow, maxRow)

    def proccessPD(self, data :dict):
        sheet_name = data.get("Sheet Name")
        try:
            min_row = int(data.get("Minimum Row"))
            max_row = int(data.get("Maximum Row"))
        except (ValueError, TypeError) as e:
            messagebox.showerror(title="error",message="Invalid Inputs")
            return
        
        if not sheet_name or not min_row or not max_row:
            messagebox.showerror(title="error",message="All fields must be filled out!")
            return
        
        self.manager.processPD(data.get("FilePath"), sheet_name, min_row, max_row)

    def uploadFiles(self):  

        if self.selected_file:
            fileReader = self.getFileReader()
            if fileReader:
                log_data = self.manager.uploadFiles(self.selected_file,fileReader)
                self.show_log_popup(log_data)
            else:
                messagebox.showinfo("Error", "No File Reader Selected")
    
    def show_log_popup(self, log_data):
        popup = tk.Toplevel(self.master)
        popup.title("Log Data")
        text_area = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=50, height=14)
        text_area.pack(expand=True, fill="both")

        # Insert the log data into the text area
        text_area.insert(tk.END, log_data)

        # Optionally make the text area read-only
        text_area.config(state=tk.DISABLED)

    def getFileReader(self):
        return self.combobox.get()
    
    def close_app(self):
        self.destroy()

    
    
#==================================================================================================================================#
#==================================================================================================================================#

# >> POPup Window with custom Entries
# >> Takes in a dictionary to specify the entries
# >> @SUBMIT -> data { label : entryValue }

class CustomPopup(customtkinter.CTkToplevel):

    MAX_HEIGHT = 600  # Maximum height for the popup window

    def __init__(self, parent, fields, submit_callback, file_path=None):
        
        
        if not file_path:
            messagebox.showinfo(title = "No File Selected", message="Please Select A File")
            return
        
        super().__init__(parent)

        self.fields = fields
        self.submit_callback = submit_callback
        self.entries = {}  # Use a dictionary to keep track of widgets
        self.file_path = file_path  # Store the file path passed during initialization

        self.title("Input Form")
        
        # Create the canvas and scrollbar
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = customtkinter.CTkFrame(self.canvas)
        
        # Create a window inside the canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Create the form based on the provided fields
        self.create_form()

        # Adjust geometry after form creation
        self.update_idletasks()  # Ensures the geometry updates after widgets are added
        window_width = max(self.scrollable_frame.winfo_reqwidth() + 40, 300)  # Add padding, minimum width of 300
        window_height = min(self.scrollable_frame.winfo_reqheight() + 60, self.MAX_HEIGHT)  # Add padding for the submit button and apply max height
        self.geometry(f"{window_width}x{window_height}")

        # Submit button
        submit_button = customtkinter.CTkButton(self.scrollable_frame, text="Submit", command=lambda: self.submit(self.file_path))
        submit_button.grid(pady=10, row=len(self.fields), columnspan=2, sticky="ew")

    def create_form(self):
        for idx, (label_text, field) in enumerate(self.fields.items()):
            label = customtkinter.CTkLabel(self.scrollable_frame, text=label_text)
            label.grid(row=idx, column=0, padx=10, pady=10, sticky="e")

            field_type = field.get('type')
            default_value = field.get('default', '')  # Get default value or empty string if not provided

            if field_type == 'entry':
                entry = tk.Entry(self.scrollable_frame)
                entry.insert(0, default_value)  # Set default value for entry
                self.entries[label_text] = entry  # Use label text as the key
                entry.bind("<Return>", self.on_enter_pressed)
            elif field_type == 'combobox':
                entry = ttk.Combobox(self.scrollable_frame, values=field.get('options', []))
                entry.set(default_value)  # Set default value for combobox
                self.entries[label_text] = entry
                entry.bind("<Return>", self.on_enter_pressed)
            elif field_type == 'text':
                entry = customtkinter.CTkTextbox(self.scrollable_frame, height=4)
                entry.insert("1.0", default_value)  # Set default value for text area
                self.entries[label_text] = entry
                entry.bind("<Return>", self.on_enter_pressed)
            elif field_type == 'open':  # Button to open file dialog
                entry = customtkinter.CTkEntry(self.scrollable_frame, textvariable=tk.StringVar(), width=100)  # Make the entry wider
                entry.grid(row=idx, column=1, padx=10, pady=(20, 0), sticky="ew")  # Place entry above the button
                button = customtkinter.CTkButton(self.scrollable_frame, text="Open File", command=lambda: self.open_file_dialog(entry))
                button.grid(row=idx, column=2, padx=10, pady=(0, 10), sticky="w")  # Button below the entry
                self.entries[label_text] = entry
                continue

            entry.grid(row=idx, column=1, padx=10, pady=10, sticky="w")


    def on_enter_pressed(self, event):
        # Find the index of the currently focused entry
        focused_widget = event.widget
        entries_list = list(self.entries.values())
        
        try:
            current_index = entries_list.index(focused_widget)
        except ValueError:
            print(f"Widget not found in the entries list: {focused_widget}")
            return
        
        next_index = current_index + 1
        if next_index < len(entries_list):
            next_widget = entries_list[next_index]
            next_widget.focus_set()
    
    def open_file_dialog(self, entry):
        file_path = filedialog.askopenfilename()  # Open file dialog
        if file_path:  # If a file was selected
            entry.configure(state='normal')  # Make entry writable
            entry.delete(0, tk.END)  # Clear existing content
            entry.insert(0, file_path)  # Insert the file path
            entry.configure(state='readonly')  # Make entry read-only
    
    def submit(self, filePath):
        # Collect the data from the entries
        data = {"FilePath": filePath}
        for label, entry in self.entries.items():
            if isinstance(entry, customtkinter.CTkTextbox):
                data[label] = entry.get("1.0", "end-1c")  # Get text from CTkTextbox
            else:
                data[label] = entry.get()

        self.submit_callback(data)
        self.destroy()

if __name__ == "__main__":

    app = FileExplorerApp()
    app.mainloop()

    

