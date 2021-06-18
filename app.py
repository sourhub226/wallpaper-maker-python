from tkinter import (
    Button,
    Canvas,
    Frame,
    Label,
    Scrollbar,
    Tk,
    colorchooser,
    filedialog,
)

import time
import os
from PIL import Image, ImageTk

root = Tk()

screen_width = 1222
screen_height = 620

monitor_width = root.winfo_screenwidth()
monitor_height = root.winfo_screenheight()

x_cordinate = int((monitor_width - screen_width) / 2)
y_cordinate = int((monitor_height - screen_height) / 2)

root.geometry(
    "{}x{}+{}-{}".format(screen_width, screen_height, x_cordinate, y_cordinate)
)

label_bg_color = "#f5f5f5"
app_bg_color = "white"
status_bg_color = "#404144"

root.title("Wallpaper Maker")
root.config(bg=app_bg_color)
root.resizable(False, False)


image_names = []
labels = []
x = y = style = color = 0
im = None
style_selected = color_selected = False

style_path = "styles/"
asset_path = "assets/"


def make_sidebar():
    global x, image_names, labels
    for fn in os.listdir(style_path):
        print(fn)
        small_img = ImageTk.PhotoImage(
            Image.open(f"{style_path}{fn}").resize((256, 144), Image.ANTIALIAS)
        )
        label = Label(
            window,
            text=fn,
            image=small_img,
            relief="flat",
            borderwidth=3,
            bg=label_bg_color,
        )
        label.photo = small_img
        label.pack()
        label.bind("<Button-1>", lambda _, arg=label.cget("text"): select_style(arg))
        labels.append(label)
        image_names.append(fn)
        x += 1


def reset_borders():
    for label in labels:
        label.config(borderwidth=3, relief="flat")


def select_style(arg):
    global style, style_selected, color_selected
    preview_area.delete("all")
    preview_area.create_image(0, 0, anchor="nw", image=preview_img)
    status_label2.config(text="Pick a color", bg="yellow", fg="black")
    status_label3.config(text="Generate preview", bg=status_bg_color, fg="white")
    status_label4.config(text="Save", bg=status_bg_color, fg="white")
    color_selected = False
    print(arg)
    style = arg
    reset_borders()
    selected_label = labels[image_names.index(style)]
    selected_label.config(borderwidth=3, relief="solid")
    style_selected = True
    status_label1.config(text="Style selected", bg="green", fg="white")


def make_image(style, to_save, save_as="tmp.png"):
    white_background = Image.new("RGB", (1920, 1080), "white")
    color_background = Image.new("RGBA", (1920, 1080), color)
    img = Image.open(f"{style_path}{style}")
    white_background.paste(color_background, (0, 0), color_background)
    white_background.paste(img, (0, 0), img)
    if to_save:
        white_background.save(save_as)
    return white_background


def generate_preview():
    global im, style, style_selected, color_selected, color
    preview_area.delete("all")
    if style_selected:
        if color_selected:
            im = make_image(style, False).resize((880, 495), Image.ANTIALIAS)
            im = ImageTk.PhotoImage(im)
            preview_area.create_image(8, 9, anchor="nw", image=im)
            # generated = True
            status_label3.config(text="Preview Generated", bg="green", fg="white")
            status_label4.config(text="Save", bg="yellow", fg="black")
        else:
            print("select color")
            status_label2.config(text="Please select a color", bg="red", fg="black")
    else:
        print("select style")
        status_label1.config(text="Please select a style", bg="red", fg="black")


def color_picker():
    global color, color_selected, style_selected
    status_label3.config(text="Generate preview", bg=status_bg_color, fg="white")
    status_label4.config(text="Save", bg=status_bg_color, fg="white")
    # generated = False
    if style_selected:
        selected_color = colorchooser.askcolor(color=(240, 81, 84))[0]
        if selected_color is None:
            print("color selection failed")
            status_label2.config(text="Color selection failed", bg="red", fg="black")
            return
        status_label2.config(text="Color selected", bg="green", fg="white")
        status_label3.config(text="Generate preview", bg="yellow", fg="black")
        color_selected = True
        color_list = [int(t) for t in selected_color]
        color = tuple(color_list)
        print(color)

    else:
        print("select color")
        status_label1.config(text="Please select a style", bg="red", fg="black")


def save_img():
    global color_selected, style_selected, style
    if style_selected:
        if color_selected:
            status_label4.config(text="Choose file location", bg="orange", fg="black")
            f_location = filedialog.asksaveasfilename(
                parent=root,
                title="Save image",
                filetypes=[("png file", "*.png")],
                defaultextension=[("png file", "*.png")],
                initialdir=os.path.join(
                    os.path.join(os.environ["USERPROFILE"]), "Desktop"
                ),
                initialfile="Generated Wallpaper",
            )
            if f_location == "":
                print("save FAILED")
                status_label4.config(text="Save failed", bg="red", fg="black")
                return
            print(f_location)
            status_label4.config(text="Saving...", bg="yellow", fg="black")
            status_label4.update()
            make_image(style, True, f_location)
            time.sleep(3)
            status_label4.config(text="Saved successfully", bg="green", fg="white")
            print("saved")
        else:
            print("select color")
            status_label2.config(text="Please select a color", bg="red", fg="black")
    else:
        print("select style")
        status_label1.config(text="Please select a style", bg="red", fg="black")


frame = Frame(root)
frame.place(x=9, y=30)
style_area = Canvas(
    frame,
    width=266,
    height=screen_height - 70,
    relief="flat",
    borderwidth=3,
    bg=label_bg_color,
)
window = Frame(style_area)
scrollbar = Scrollbar(frame, orient="vertical", command=style_area.yview)
scrollbar.pack(side="right", fill="y")
style_area.pack(side="left")
style_area.configure(yscrollcommand=scrollbar.set)
style_area.create_window((0, 0), window=window, anchor="nw")
window.bind(
    "<Configure>", lambda _: style_area.configure(scrollregion=style_area.bbox("all"))
)

preview_area = Canvas(root, bg=label_bg_color, width=892, height=510)
preview_area.place(
    x=style_area.winfo_reqwidth() + scrollbar.winfo_reqwidth() + 21,
    y=screen_height - preview_area.winfo_reqheight() - 31,
)

status_label1 = Label(root, text="Select a style", width=45, bg="yellow", fg="black")
status_label1.place(x=0, y=screen_height - 21)
status_label2 = Label(
    root, text="Pick a color", width=45, bg=status_bg_color, fg="white"
)
status_label2.place(x=status_label1.winfo_reqwidth(), y=screen_height - 21)
status_label3 = Label(
    root, text="Generate preview", width=45, bg=status_bg_color, fg="white"
)
status_label3.place(
    x=status_label1.winfo_reqwidth() + status_label2.winfo_reqwidth(),
    y=screen_height - 21,
)
status_label4 = Label(root, text="Save", width=37, bg=status_bg_color, fg="white")
status_label4.place(
    x=status_label1.winfo_reqwidth()
    + status_label2.winfo_reqwidth()
    + status_label3.winfo_reqwidth(),
    y=screen_height - 21,
)

style_label = Label(root, text="Styles", bg=label_bg_color, width=41)
style_label.place(
    x=9
    + (
        style_area.winfo_reqwidth()
        - style_label.winfo_reqwidth()
        + scrollbar.winfo_reqwidth()
    )
    / 2,
    y=5,
)

color_btn = Button(
    root, text="choose color", relief="groove", bg=label_bg_color, command=color_picker
)
color_btn.place(x=332, y=20)

save_btn = Button(
    root, text="Save", relief="groove", bg=label_bg_color, command=save_img
)
save_btn.place(x=532, y=20)

generate_btn = Button(
    root, text="Generate", relief="groove", bg=label_bg_color, command=generate_preview
)
generate_btn.place(x=432, y=20)

# title_label = Label(root, text="Wallpaper Maker", font=("Arial", 20), bg="white")
# title_label.place(x=600, y=10)
preview_label = Label(root, text="Preview Area", bg=label_bg_color, width=127)
preview_label.place(
    x=(preview_area.winfo_reqwidth() - preview_label.winfo_reqwidth()) / 2
    + style_area.winfo_reqwidth()
    + 38,
    y=screen_height - 570,
)

preview_img = ImageTk.PhotoImage(Image.open(f"{asset_path}preview back.png"))
preview_area.create_image(0, 0, anchor="nw", image=preview_img)

make_sidebar()

print(root.winfo_screenheight())


root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
root.mainloop()
