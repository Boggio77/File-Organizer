import os
import shutil
import wx

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='File Organizer')
        self.SetIcon(wx.Icon('C:\\Users\\boggi\\FileOrganizer\\icons8-file-48.png', wx.BITMAP_TYPE_PNG))
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour("#FFFFFF")) 
        panel.Refresh() 
        
        my_sizer = wx.BoxSizer(wx.VERTICAL)             
        self.my_btn = wx.Button(panel, label='Organize', style=wx.BORDER_NONE)
        self.my_btn.SetBackgroundColour(wx.Colour('#2EBFDC')) 
        self.my_btn.Refresh() 
        self.my_btn.Bind(wx.EVT_BUTTON, self.on_organize_button_click) 
        
        my_sizer.Add(wx.StaticText(panel), 1, wx.EXPAND)
        my_sizer.Add(self.my_btn, 0, wx.ALIGN_CENTER | wx.ALL, 5) 
        my_sizer.Add(wx.StaticText(panel), 1, wx.EXPAND) 
        
        panel.SetSizer(my_sizer)        
        self.Show()

    def on_organize_button_click(self, event):
        self.my_btn.SetBackgroundColour(wx.Colour("#2F7785"))
        self.my_btn.Refresh()

        wx.CallLater(200, self.reset_button_color)

        source_folder = r"C:\Users\boggi\Downloads" 
        destination_folders = {
            'documents': r"C:\Users\boggi\OneDrive\Documents",
            'pictures': r"C:\Users\boggi\OneDrive\Pictures",
            'others': r"C:\Users\boggi\Downloads" 
        }
        organizer = FileOrganizer(source_folder, destination_folders)
        organizer.organize_files()

    def reset_button_color(self):
        self.my_btn.SetBackgroundColour(wx.Colour('#2EBFDC')) 
        self.my_btn.Refresh()

class FileOrganizer:
    def __init__(self, source_folder, destination_folders):
        self.source_folder = source_folder
        self.destination_folders = destination_folders

    def categorize_file(self, file_path):
        file_extension = os.path.splitext(file_path)[1]
        if file_extension in ['.pdf', '.docx', '.xlsx']:
            return 'documents'
        elif file_extension in ['.jpg', '.png', '.gif']:
            return 'pictures'
        else:
            return 'others'

    def move_file(self, file_path, category):
        destination_folder = self.destination_folders.get(category)
        if destination_folder:
            shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))
        else:
            print(f"No destination folder specified for category '{category}'.")

    def organize_files(self):
        try:
            for file_name in os.listdir(self.source_folder):
                file_path = os.path.join(self.source_folder, file_name)
                if os.path.isfile(file_path):
                    category = self.categorize_file(file_path)
                    self.move_file(file_path, category)
        except FileNotFoundError:
            print(f"The specified source folder '{self.source_folder}' does not exist or is not accessible.")

if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()