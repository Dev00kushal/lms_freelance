import tkinter as tk

def fade_in(widget, start_opacity=0, end_opacity=1, step=0.05, interval=10):
    widget.attributes("-alpha", start_opacity)
    if start_opacity < end_opacity:
        widget.after(interval, fade_in, widget, start_opacity + step, end_opacity)
