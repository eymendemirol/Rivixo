# -------------------- Libraries --------------------
from tkinter import *
from tkinter import ttk
import webbrowser
import urllib.parse
import random
from pathlib import Path
import subprocess
import sys
import os

# -------------------- Resource Path Function --------------------
def resource_path(relative_path):
    """ Get the correct path for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# -------------------- Main window settings --------------------
root = Tk()
root.geometry("400x500")
root.title("rivixo")

# -------------------- Path Setup --------------------
# Correct path management for PyInstaller
base_path = Path(resource_path(""))
icon_path = resource_path("icon.png")
MOOD_DIR = Path(resource_path("rivixolist"))

# Create directory if it doesn't exist
MOOD_DIR.mkdir(exist_ok=True)

# Load icon
try:
    icon = PhotoImage(file=str(icon_path))
    root.iconphoto(False, icon)
except:
    print("Icon could not be loaded")

# -------------------- Variables --------------------
selected_mood = IntVar()
platform_selected = StringVar()
recent_songs = []
dark_mode = False

# -------------------- Theme colors --------------------
current_bg = "#ffffff"
current_fg = "black"
current_btn_bg = "#e0e0e0"
current_btn_fg = "black"

# -------------------- Create text files --------------------
for i in range(1, 11):
    file_path = MOOD_DIR / f"{i}.txt"
    if not file_path.exists():
        file_path.touch()

# -------------------- Functions --------------------
def set_error(text):
    error_label.config(text=text)

def remove_song(song, mood):
    try:
        file_path = MOOD_DIR / f"{mood}.txt"
        songs = file_path.read_text(encoding="utf-8").splitlines()
        if song in songs:
            songs.remove(song)
            file_path.write_text("\n".join(songs) + ("\n" if songs else ""), encoding="utf-8")
        set_error(f"Removed: {song} (Mood {mood})")
        refresh_recent_songs()
    except Exception as e:
        set_error(f"Error removing: {e}")

def add_song_to_file(mood_number, song_name):   
    try:
        file_path = MOOD_DIR / f"{mood_number}.txt"
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(song_name + "\n")
        set_error(f"Song added: {song_name} -> Mood {mood_number}")
    except Exception as e:
        set_error(f"Error: {e}")

def get_random_song_from_file(mood_number):
    try:
        file_path = MOOD_DIR / f"{mood_number}.txt"
        songs = file_path.read_text(encoding="utf-8").splitlines()
        if songs:
            available_songs = [s for s in songs if s not in recent_songs]
            return random.choice(available_songs if available_songs else songs)
        return None
    except Exception as e:
        set_error(f"Error: {e}")
        return None

def theme():
    global dark_mode, current_bg, current_fg, current_btn_bg, current_btn_fg
    if dark_mode:
        current_bg, current_fg, current_btn_bg, current_btn_fg = "#ffffff", "black", "#e0e0e0", "black"
        dark_mode = False
    else:
        current_bg, current_fg, current_btn_bg, current_btn_fg = "#222222", "white", "#444444", "white"
        dark_mode = True

    root.config(bg=current_bg)
    for frame in (main_frame, list_frame, platform_frame, recent_songs_frame):
        frame.config(bg=current_bg)
        for widget in frame.winfo_children():
            try:
                if isinstance(widget, Radiobutton):
                    widget.config(bg=current_bg, fg=current_fg, selectcolor=current_bg)
                elif isinstance(widget, Button):
                    widget.config(bg=current_btn_bg, fg=current_btn_fg)
                else:
                    widget.config(bg=current_bg, fg=current_fg)
            except:
                pass

def open_random_song():
    if not platform_selected.get():
        set_error("Please select a platform!")
        return

    try:
        mood_rating = int(entry.get())
        if not (1 <= mood_rating <= 10):
            set_error("Enter a number between 1-10!")
            return

        random_song_name = get_random_song_from_file(mood_rating)
        if not random_song_name:
            set_error("No song saved for that mood!")
            return

        entry.delete(0, END)
        recent_songs.append(random_song_name)
        if len(recent_songs) > 2:
            recent_songs[:] = recent_songs[-2:]

        encoded = urllib.parse.quote(random_song_name)

        if platform_selected.get() == "spotify":
            spotify_uri = f"spotify:search:{random_song_name}"
            try:
                if sys.platform.startswith("win"):
                    os.startfile(spotify_uri)
                elif sys.platform.startswith("darwin"):
                    subprocess.run(["open", spotify_uri], check=True)
                elif sys.platform.startswith("linux"):
                    subprocess.run(["xdg-open", spotify_uri], check=True)

                set_error(f"Searching in Spotify app: {random_song_name}")
            except:
                webbrowser.open(f"https://open.spotify.com/search/{encoded}", new=0)
                set_error(f"Spotify app not found, opened in web: {random_song_name}")
        else:
            youtube_url = f"https://www.youtube.com/results?search_query={encoded}"
            webbrowser.open(youtube_url, new=0)
            set_error(f"Searching on YouTube: {random_song_name}")

    except ValueError:
        set_error("Enter a valid number!")

def show_main_frame():
    list_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

def show_list_frame():
    main_frame.pack_forget()
    list_frame.pack(fill="both", expand=True)
    recent_songs_frame.pack_forget()
    show_recent_button.config(text="Show Recent Songs")

def refresh_recent_songs():
    if show_recent_button.cget("text") == "Hide Recent Songs":
        toggle_recent_songs()
        toggle_recent_songs()

def add_song_simple():
    song_name = entrylink.get()
    try:
        mood_num = int(mood_entry.get())
        if 1 <= mood_num <= 10 and song_name:
            add_song_to_file(mood_num, song_name)
            entrylink.delete(0, END)
            mood_entry.delete(0, END)
            refresh_recent_songs()
        else:
            set_error("Invalid mood or empty song name!")
    except ValueError:
        set_error("Please enter a number!")

def ad():
    webbrowser.open("https://www.tiktok.com/@popstech", new=0)
    webbrowser.open("https://www.instagram.com/eymendemirol", new=0)

def toggle_recent_songs():
    if show_recent_button.cget("text") == "Show Recent Songs":
        for widget in recent_songs_frame.winfo_children():
            widget.destroy()

        Label(recent_songs_frame, text="Recently Added Songs:", font=("Roboto", 10, "bold"),
              bg=current_bg, fg=current_fg).pack(pady=5)

        canvas = Canvas(recent_songs_frame, bg=current_bg, highlightthickness=0, height=200)
        canvas.pack(side=LEFT, fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background=current_btn_bg,
                        darkcolor=current_btn_bg,
                        lightcolor=current_btn_bg,
                        troughcolor=current_bg,
                        bordercolor=current_bg,
                        arrowcolor=current_fg)

        scrollbar = ttk.Scrollbar(recent_songs_frame, orient="vertical", command=canvas.yview, style="Vertical.TScrollbar")
        scrollbar.pack(side=RIGHT, fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = Frame(canvas, bg=current_bg)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        recent_songs_list = []
        for i in range(1, 11):
            try:
                songs = (MOOD_DIR / f"{i}.txt").read_text(encoding="utf-8").splitlines()
                for song in songs[-5:]:
                    recent_songs_list.append((song, i))
            except:
                pass

        recent_songs_list.reverse()
        for song, mood in recent_songs_list[:30]:
            row_frame = Frame(scrollable_frame, bg=current_bg)
            row_frame.pack(fill="x", padx=10, pady=2)

            Label(row_frame, text=f"• {song} (Mood: {mood})", font=("Roboto", 9),
                  bg=current_bg, fg=current_fg).pack(side=LEFT, anchor="w")
            Button(row_frame, text="Remove", font=("Roboto", 8),
                   bg=current_btn_bg, fg=current_btn_fg,
                   command=lambda s=song, m=mood: remove_song(s, m)).pack(side=RIGHT, padx=5)

        recent_songs_frame.pack(pady=10, fill="both", expand=True)
        show_recent_button.config(text="Hide Recent Songs")
    else:
        recent_songs_frame.pack_forget()
        show_recent_button.config(text="Show Recent Songs")

# -------------------- Main frame --------------------
main_frame = Frame(root)
main_frame.pack(fill="both", expand=True)

themeswitch = Button(main_frame, width=5, text="Theme", command=theme, font=("Roboto", 9))
themeswitch.place(x=350, y=8)

Label(main_frame, text="Rate Your Mood Out of 10", font=("Roboto", 12)).place(relx=0.5, rely=0.25, anchor="center")
entry = Entry(main_frame, width=6, font=("Roboto", 12))
entry.place(relx=0.5, rely=0.32, anchor="center")

platform_frame = Frame(main_frame)
platform_frame.place(relx=0.5, rely=0.42, anchor="center")
Radiobutton(platform_frame, text="Spotify", variable=platform_selected, value="spotify", font=("Roboto", 10)).pack(side=LEFT, padx=5)
Radiobutton(platform_frame, text="YouTube", variable=platform_selected, value="youtube", font=("Roboto", 10)).pack(side=LEFT, padx=5)

Button(main_frame, width=17, text="Open Suggested Song !", font=("Roboto", 10), command=open_random_song).place(relx=0.5, rely=0.52, anchor="center")
error_label = Label(main_frame, text="", font=("Roboto", 10), fg="red")
error_label.place(relx=0.5, rely=0.65, anchor="center")

Button(main_frame, width=7, text="Your List", font=("Roboto", 9), command=show_list_frame).place(x=10, y=8)
Button(main_frame, width=11, text="App Made By\nEymen Demirol", font=("Roboto", 10), command=ad).place(relx=0.5, rely=0.9, anchor="center")

# -------------------- List frame --------------------
list_frame = Frame(root)

Label(list_frame, text="Song Name:", font=("Roboto", 10)).pack(pady=10)
entrylink = Entry(list_frame, width=30, font=("Roboto", 10))
entrylink.pack()

Label(list_frame, text="Select Your Mood (1-10):", font=("Roboto", 10)).pack(pady=10)
mood_entry = Entry(list_frame, width=5, font=("Roboto", 10))
mood_entry.pack()

Button(list_frame, text="Add !", command=add_song_simple, font=("Roboto", 10)).pack(pady=20)

recent_songs_frame = Frame(list_frame, bg=current_bg)
show_recent_button = Button(list_frame, text="Show Recent Songs", command=toggle_recent_songs, font=("Roboto", 9))
show_recent_button.pack(pady=5)

Button(list_frame, text="Back", font=("Roboto", 10), command=show_main_frame).pack(pady=5)

# -------------------- Start program --------------------
root.mainloop()