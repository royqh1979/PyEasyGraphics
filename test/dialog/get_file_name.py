import easygraphics.dialog as dlg

dd = dlg.get_directory_name("Choose a directory")
print(dd)
filename = dlg.get_open_file_name("Choose a file to open", dlg.FileFilter.ImageFiles)
print(filename)
name2 = dlg.get_file_names("Choose files", dlg.FileFilter.ImageFiles)
print(name2)
name2 = dlg.get_save_file_name("Save", dlg.FileFilter.ImageFiles)
print(name2)
