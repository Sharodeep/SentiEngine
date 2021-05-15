from dearpygui.core import *
from dearpygui.simple import *
from engine import main

wind_val = 0


def runner(sender, data):  # runner code for the file selector
    if data[1] == "." or data[1] == "":
        display("Select valid file")
    else:
        path = open(str(data[0] + "//" + data[1]), encoding='utf-8').read()
        path = path.strip()
        if path == "":
            display("Selected file is empty")
        else:
            sent, emo, val = main(path)
            display(sent, emo, val)
            # print(sent,emo)


def filesel(sender, data):  # file selector
    open_file_dialog(runner, extensions=".txt")


def runner1(sender, data):  # runner code text input
    val_holder = get_value("Input")
    if val_holder == "" or val_holder == "Type here!!":
        display("Enter Valid Input")
    elif val_holder == "Hello there":
        easter()
    else:
        sent, emo, val = main(val_holder)
        display(sent, emo, val)


def display(val1, val2="", val3={}):  # display moudule
    display_val = "Output:\n" + val1 + "\n" + val2
    table = []
    for key, value in val3.items():
        table.append(list((key, str(value))))
    val3_key = list(val3.keys())
    val3_vals = list(val3.values())
    set_value("Output:", display_val)
    # print(val3_key,val3_vals,table) #for testing
    set_table_data(name="EmotionScore", data=table)
    add_pie_series("Plot", "PieChart", val3_vals, val3_key, 3.5, 3, 2, update_bounds=True)


def easter():  # star wars easter egg code
    global wind_val
    wind_val = wind_val + 1
    win_name = "Easter" + str(wind_val)
    pic_name = "Genral" + str(wind_val)
    add_window(win_name, width=500, height=300, x_pos=150, y_pos=200)
    add_spacing(count=8)
    add_image(pic_name, "easter1.png")
    add_spacing(count=4)
    add_text("Ah General Kenobi You're a bold one", color=[255, 255, 255])
    end()


# window settings
set_main_window_size(690, 900)
set_global_font_scale(1.25)
set_theme("Gold")
set_style_window_padding(30, 0)
set_main_window_title("DashBaord")
with window("DashBoard"):
    with tab_bar("Bartab"):
        with tab("Main"):
            print("GUI is runnning....")
            set_window_pos("DashBoard", 0, 0)
            add_drawing("logo", width=516, height=190)
            add_separator()
            add_spacing(count=12)
            add_text("Please enter input for analysing", color=[232, 163, 33])
            add_input_text("Input", width=560, default_value="Type here!!", label="", multiline=True)
            add_spacing(count=8)
            add_button("Check", callback=runner1)
            add_spacing(count=4)
            add_separator()
            add_spacing(count=8)
            add_text("Use the bellow button to select file for analysing\n(only .txt files accepted)",
                     color=[232, 163, 33])
            add_spacing(count=8)
            add_button("File Selector", callback=filesel)
            add_spacing(count=4)
            add_separator()
            add_spacing(count=8)
            add_text("Output:", color=[232, 163, 33])
        with tab("Score"):
            add_table(name="EmotionScore", headers=['Emotion', 'Score'])
        with tab("Plots"):
            add_plot("Plot", height=700, width=590)

draw_image("logo", "logo_dash.png", [0, 190], [516, 0])
start_dearpygui(primary_window="DashBoard")
print("Closing GUI")
