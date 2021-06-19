from tkinter import (
    Button,
    Canvas,
    Frame,
    Label,
    PhotoImage,
    Scrollbar,
    Tk,
    colorchooser,
    filedialog,
    ttk,
)
from threading import Timer
import os
from PIL import Image, ImageTk
import re

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


app_bg_color = "#f7f7f7"
status_bg_color = "#404144"
custom_yellow = "#FCDC7A"
custom_green = "#54EFA1"
custom_red = "#FF5555"
custom_orange = "#F7AB6D"

pixelVirtual = PhotoImage(width=1, height=1)

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
            Image.open(f"{style_path}{fn}")
            .resize((256, 144), Image.ANTIALIAS)
            .convert("RGBA")
        )
        label = Label(
            window,
            text=fn,
            image=small_img,
            relief="flat",
            borderwidth=3,
        )
        label.photo = small_img
        label.pack(padx=(2, 0))
        label.bind("<Button-1>", lambda _, arg=label.cget("text"): select_style(arg))
        labels.append(label)
        image_names.append(fn)
        x += 1


def reset_borders():
    for label in labels:
        label.config(borderwidth=3, relief="flat")


def validate_hex():
    global color, color_selected
    if hex_entry.get() == "":
        return True
    hex_code = hex_entry.get()
    hex_code = hex_code if "#" in hex_code else "#" + hex_code
    print(hex_code)
    match = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", hex_code)
    if match:
        return hex_to_rgb(hex_code)
    status_label3.config(text="Generate preview", bg=status_bg_color, fg="white")
    status_label4.config(text="Save", bg=status_bg_color, fg="white")
    return False


def hex_to_rgb(hex_code):
    global color, color_selected
    color_selected = True
    if len(hex_code) == 4:
        hex_code = "#{}".format("".join(2 * c for c in hex_code.lstrip("#")))
    print(hex_code)
    color = tuple(int(hex_code.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    print(color)
    status_label2.config(text="Color selected", bg=custom_green, fg="black")
    return True


def select_style(arg):
    global style, style_selected, color_selected
    preview_area.delete("all")
    preview_area.create_image(0, 0, anchor="nw", image=preview_img)
    status_label2.config(text="Pick a color", bg=custom_yellow, fg="black")
    status_label3.config(text="Generate preview", bg=status_bg_color, fg="white")
    status_label4.config(text="Save", bg=status_bg_color, fg="white")
    color_selected = False
    print(arg)
    style = arg
    reset_borders()
    selected_label = labels[image_names.index(style)]
    selected_label.config(borderwidth=3, relief="solid")
    style_selected = True
    status_label1.config(text="Style selected", bg=custom_green, fg="black")


def make_image(style, to_save, save_as="tmp.png"):
    global color
    white_background = Image.new("RGB", (1920, 1080), "white")
    color_background = Image.new("RGBA", (1920, 1080), color)
    img = Image.open(f"{style_path}{style}").convert("RGBA")
    white_background.paste(color_background, (0, 0), color_background)
    white_background.paste(img, (0, 0), img)
    if to_save:
        white_background.save(save_as)
    return white_background


def generate_preview():
    global im, style, style_selected, color_selected, color
    preview_area.delete("all")
    # color_selected=False
    if style_selected:
        if validate_hex():
            im = make_image(style, False).resize((880, 495), Image.ANTIALIAS)
            im = ImageTk.PhotoImage(im)
            preview_area.create_image(8, 9, anchor="nw", image=im)
            # generated = True
            status_label3.config(text="Preview Generated", bg=custom_green, fg="black")
            status_label4.config(text="Save", bg=custom_yellow, fg="black")
        else:
            print("select color")
            status_label2.config(
                text="Please select a valid color", bg=custom_red, fg="black"
            )
    else:
        print("select style")
        status_label1.config(text="Please select a style", bg=custom_red, fg="black")


def color_picker():
    global color, color_selected, style_selected
    status_label3.config(text="Generate preview", bg=status_bg_color, fg="white")
    status_label4.config(text="Save", bg=status_bg_color, fg="white")
    # generated = False
    if style_selected:
        color_selected = False
        status_label2.config(text="Pick a color", bg=custom_yellow, fg="black")
        # hex_entry.config(state="active")
        hex_entry.delete(0, "end")
        selected_color = colorchooser.askcolor(color=(240, 81, 84))[0]
        if selected_color is None:
            print("color selection failed")
            # status_label2.config(
            #     text="Color selection failed", bg=custom_red, fg="black"
            # )
            return
        # hex_entry.config(state="disabled")
        status_label2.config(text="Color selected", bg=custom_green, fg="black")
        status_label3.config(text="Generate preview", bg=custom_yellow, fg="black")
        color_selected = True
        color_list = [int(t) for t in selected_color]
        color = tuple(color_list)
        print(color)

    else:
        print("select color")
        status_label1.config(text="Please select a style", bg=custom_red, fg="black")


def save_img():
    global color_selected, style_selected, style
    if style_selected:
        if color_selected:
            status_label4.config(
                text="Choose file location", bg=custom_orange, fg="black"
            )
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
                status_label4.config(text="Save failed", bg=custom_red, fg="black")
                return
            print(f_location)
            status_label4.config(text="Saving...", bg=custom_yellow, fg="black")
            status_label4.update()
            make_image(style, True, f_location)
            # time.sleep(3)
            Timer(
                3,
                lambda: status_label4.config(
                    text="Saved successfully", bg=custom_green, fg="black"
                ),
            ).start()
            print("saved")
        else:
            print("select color")
            status_label2.config(
                text="Please select a valid color", bg=custom_red, fg="black"
            )
    else:
        print("select style")
        status_label1.config(text="Please select a style", bg=custom_red, fg="black")


frame = Frame(root)
frame.place(x=9, y=30)
style_area = Canvas(
    frame,
    width=266,
    height=screen_height - 70,
    relief="flat",
    borderwidth=3,
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

preview_area = Canvas(root, width=892, height=510)
preview_area.place(
    x=style_area.winfo_reqwidth() + scrollbar.winfo_reqwidth() + 21,
    y=screen_height - preview_area.winfo_reqheight() - 31,
)

status_label1 = Label(
    root, text="Select a style", width=45, bg=custom_yellow, fg="black"
)
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


style_label = Label(root, text="- Styles -", width=41)
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
    root,
    text="Choose color",
    relief="groove",
    command=color_picker,
    image=pixelVirtual,
    width=100,
    height=33,
    compound="c",
)
color_btn.place(x=style_area.winfo_reqwidth() + 40, y=5)

generate_btn = Button(
    root,
    text="Generate",
    relief="groove",
    command=generate_preview,
    image=pixelVirtual,
    width=100,
    height=33,
    compound="c",
)
generate_btn.place(x=screen_width - 230, y=5)

save_btn = Button(
    root,
    text="Save",
    command=save_img,
    relief="groove",
    image=pixelVirtual,
    width=100,
    height=33,
    compound="c",
)
save_btn.place(x=screen_width - 120, y=5)


or_label = Label(
    root,
    text="or",
    image=pixelVirtual,
    width=35,
    height=33,
    compound="c",
)
or_label.place(x=style_area.winfo_reqwidth() + color_btn.winfo_reqwidth() + 45, y=5)

hex_label = Label(
    root,
    text="Enter HEX color code (#) ->",
    image=pixelVirtual,
    width=150,
    height=33,
    compound="c",
)
hex_label.place(
    x=style_area.winfo_reqwidth()
    + color_btn.winfo_reqwidth()
    + or_label.winfo_reqwidth()
    + 50,
    y=5,
)

hex_entry = ttk.Entry(
    root,
)
hex_entry.place(
    x=style_area.winfo_reqwidth()
    + color_btn.winfo_reqwidth()
    + or_label.winfo_reqwidth()
    + hex_label.winfo_reqwidth()
    + 55,
    y=5,
    width=100,
    height=39,
)

preview_label = Label(root, text="- Preview Area -", width=127)
preview_label.place(
    x=(preview_area.winfo_reqwidth() - preview_label.winfo_reqwidth()) / 2
    + style_area.winfo_reqwidth()
    + 38,
    y=screen_height - 570,
)

preview_img = ImageTk.PhotoImage(
    Image.open(f"{asset_path}preview back.png").convert("RGBA")
)
preview_area.create_image(0, 0, anchor="nw", image=preview_img)

make_sidebar()

print(root.winfo_screenheight())


root.protocol("WM_DELETE_WINDOW", root.destroy)
root.mainloop()
