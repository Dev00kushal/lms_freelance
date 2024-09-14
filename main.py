from gui.main_window import MainWindow
import ttkbootstrap as ttkb
if __name__ == "__main__":
    root = ttkb.Window(themename="flatly")
    app = MainWindow(root)
    root.mainloop()