from dearpygui.core import *
from dearpygui.simple import *
from engine import main


#display_holder =[]
def runner(sender,data):
    path = data[0]+"\\"+data[1]
    path = open(path, encoding='utf-8').read()
    sent, emo =main(path)
    display(sent,emo)
    #global display_holder
    #print(sent,emo)


def filesel(sender,data):
    open_file_dialog(runner,extensions=".txt")
def runner1(sender,data):
    val_holder = get_value("Input")
    sent,emo = main(val_holder)
    display(sent,emo)

def display(val1,val2):
        display_val = val1 +"\n"+val2
        print(display_val)
        set_value("Output:",display_val)



#window settings
set_main_window_size(650,900)
set_global_font_scale(1.25)
set_theme("Gold")
set_style_window_padding(30,0)
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
            add_button("FileSelector", callback=filesel)
            add_spacing(count=4)
            add_separator()
            add_spacing(count=8)
            add_text("Output:",color=[232,163,33])
        with tab("Plots"):
            add_plot("Plot",height=-1)



draw_image("logo", "logo_dash.png",[0,190],[516,0])
start_dearpygui(primary_window="DashBoard")
print("Closing GUI")