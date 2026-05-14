import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, ROOT)
ASSETS = os.path.join(ROOT, 'assets')

import dearpygui.dearpygui as dpg
from engine import main

wind_val = 0


def runner_file(sender, app_data):
    file_path = app_data.get('file_path_name', '')
    if not file_path or file_path.endswith('.'):
        display("Select a valid file")
        return
    try:
        text = open(file_path, encoding='utf-8').read().strip()
    except Exception as e:
        display(f"Error reading file: {e}")
        return
    if not text:
        display("Selected file is empty")
        return
    sent, emo, val = main(text)
    display(sent, emo, val)


def filesel(sender, data):
    with dpg.file_dialog(callback=runner_file, width=600, height=400, modal=True):
        dpg.add_file_extension(".txt", color=[255, 255, 0])


def runner1(sender, data):
    val_holder = dpg.get_value("Input")
    if not val_holder:
        display("Enter Valid Input")
    elif val_holder == "Hello there":
        easter()
    else:
        sent, emo, val = main(val_holder)
        display(sent, emo, val)


def display(val1, val2="", val3={}):
    display_val = "Output:\n" + val1 + "\n" + val2
    dpg.set_value("output_text", display_val)

    # Rebuild table rows (keep columns intact by only deleting rows)
    for row_tag in dpg.get_item_children("emotion_table", slot=1):
        dpg.delete_item(row_tag)
    for key, value in val3.items():
        with dpg.table_row(parent="emotion_table"):
            dpg.add_text(key)
            dpg.add_text(str(value))

    # Update pie chart
    if dpg.does_item_exist("pie_series"):
        dpg.delete_item("pie_series")
    if val3:
        keys = list(val3.keys())
        vals = [float(v) for v in val3.values()]
        dpg.add_pie_series(0.5, 0.5, 0.4, vals, keys, tag="pie_series", parent="pie_y_axis", normalize=True)

    # Update bar chart
    if dpg.does_item_exist("bar_series"):
        dpg.delete_item("bar_series")
    if val3:
        keys = list(val3.keys())
        vals = [float(v) for v in val3.values()]
        y_pos = [float(i) for i in range(len(vals))]
        dpg.add_bar_series(vals, y_pos, horizontal=True, tag="bar_series", parent="bar_y_axis")
        dpg.set_axis_ticks("bar_y_axis", tuple((k, float(i)) for i, k in enumerate(keys)))
        dpg.set_axis_limits("bar_x_axis", 0, max(vals) + 1)
        dpg.set_axis_limits("bar_y_axis", -1, len(vals))
    else:
        dpg.reset_axis_ticks("bar_y_axis")


def easter():
    global wind_val
    wind_val += 1
    with dpg.window(label="Easter Egg", width=500, height=300, pos=[150, 200]):
        dpg.add_spacer(height=20)
        dpg.add_image("easter_texture")
        dpg.add_spacer(height=10)
        dpg.add_text("Ah General Kenobi You're a bold one", color=[255, 255, 255])


dpg.create_context()

with dpg.texture_registry():
    logo_w, logo_h, _, logo_data = dpg.load_image(os.path.join(ASSETS, "logo_dash.png"))
    dpg.add_static_texture(width=logo_w, height=logo_h, default_value=logo_data, tag="logo_texture")
    easter_w, easter_h, _, easter_data = dpg.load_image(os.path.join(ASSETS, "easter1.png"))
    dpg.add_static_texture(width=easter_w, height=easter_h, default_value=easter_data, tag="easter_texture")

with dpg.window(tag="DashBoard"):
    with dpg.tab_bar():
        with dpg.tab(label="Main"):
            print("GUI is running....")
            dpg.add_image("logo_texture")
            dpg.add_separator()
            dpg.add_spacer(height=12)
            dpg.add_text("Please enter input for analysing", color=[232, 163, 33])
            dpg.add_input_text(tag="Input", width=560, hint="Type here!!")
            dpg.add_spacer(height=8)
            dpg.add_button(label="Check", callback=runner1)
            dpg.add_spacer(height=4)
            dpg.add_separator()
            dpg.add_spacer(height=8)
            dpg.add_text("Use the button below to select a file for analysing\n(only .txt files accepted)",
                         color=[232, 163, 33])
            dpg.add_spacer(height=8)
            dpg.add_button(label="File Selector", callback=filesel)
            dpg.add_spacer(height=4)
            dpg.add_separator()
            dpg.add_spacer(height=8)
            dpg.add_text("Output:", color=[232, 163, 33])
            dpg.add_text("", tag="output_text", wrap=560)

        with dpg.tab(label="Score"):
            with dpg.table(tag="emotion_table", header_row=True,
                           borders_innerH=True, borders_outerH=True,
                           borders_innerV=True, borders_outerV=True):
                dpg.add_table_column(label="Emotion")
                dpg.add_table_column(label="Score")

        with dpg.tab(label="Pie"):
            with dpg.plot(tag="pie_plot", height=700, width=590, no_mouse_pos=True):
                dpg.add_plot_legend()
                pie_x = dpg.add_plot_axis(dpg.mvXAxis, no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
                dpg.add_plot_axis(dpg.mvYAxis, no_gridlines=True, no_tick_marks=True, no_tick_labels=True,
                                  tag="pie_y_axis")
                dpg.set_axis_limits(pie_x, 0, 1)
                dpg.set_axis_limits("pie_y_axis", 0, 1)

        with dpg.tab(label="Bar"):
            with dpg.plot(tag="bar_plot", height=700, width=590):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, tag="bar_x_axis")
                dpg.add_plot_axis(dpg.mvYAxis, tag="bar_y_axis")

dpg.create_viewport(title="DashBoard", width=690, height=900)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("DashBoard", True)
dpg.start_dearpygui()
dpg.destroy_context()
print("Closing GUI")
