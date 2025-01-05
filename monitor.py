from monitorcontrol import get_monitors
import customtkinter as ctk
import pickle


class Monitor:

    def set_brightness(self, brightness):
        if brightness < 0:
            brightness = 0

        if brightness > 100:
            brightness = 100
        
        for monitor in get_monitors():
            with monitor:
                monitor.set_luminance(brightness)
        
    def set_contrast(self, contrast):
        if contrast < 0:
            contrast = 0

        if contrast > 100:
            contrast = 100
        
        for monitor in get_monitors():
            with monitor:
                monitor.set_contrast(contrast)

    def set_values(self, brightness=-1, contrast=-1):

        if brightness < 0 and contrast < 0:
            return
        
        if brightness > 100:
            brightness = 100
        
        if contrast > 100:
            contrast = 100

        if brightness >= 0:
            self.set_brightness(brightness)
        
        if contrast >= 0:
            self.set_contrast(contrast)


class BrightnessContrastApp:

    config_file = "config"
    config = {}
    presets = {}

    def __init__(self):
        self.root = ctk.CTk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.retrive_config()

        self.monitor = Monitor()
        self.root.title("Brightness and Contrast Settings")
        self.root.geometry(self.config["position"])
        ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"


        # ------------------------------------------------------------
        # Contrast

        contrast_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        contrast_frame.pack(pady=5)

        contrast_slider_frame = ctk.CTkFrame(contrast_frame, fg_color="transparent")
        contrast_slider_frame.pack(side="left", padx=20, pady=5)

        self.contrast_label = ctk.CTkLabel(contrast_slider_frame, text="Contrast")
        self.contrast_label.pack(side="top", pady=5)
        self.contrast_slider = ctk.CTkSlider(contrast_slider_frame, from_=0, to=100, number_of_steps=100, orientation="horizontal", command=self.update_contrast_slider)
        self.contrast_slider.set(self.config["contrast"])
        self.contrast_slider.pack()
        self.contrast_value = ctk.IntVar()
        self.update_contrast_slider(self.config["contrast"])
        self.contrast_display = ctk.CTkLabel(contrast_slider_frame, textvariable=self.contrast_value)
        self.contrast_display.pack(side="bottom", pady=5)

        # Save contrast button
        self.save_button_contrast = ctk.CTkButton(contrast_frame, text="Set", width=50, command=self.save_contrast)
        self.save_button_contrast.pack(side="right", pady=10)


        # ------------------------------------------------------------
        # Brightness

        brightness_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        brightness_frame.pack(pady=5)

        brightness_slider_frame = ctk.CTkFrame(brightness_frame, fg_color="transparent")
        brightness_slider_frame.pack(side="left", padx=20, pady=5)

        self.brightness_label = ctk.CTkLabel(brightness_slider_frame, text="Brightness")
        self.brightness_label.pack(side="top", pady=5)
        self.brightness_slider = ctk.CTkSlider(brightness_slider_frame, from_=0, to=100, number_of_steps=100, orientation="horizontal", command=self.update_brightness_slider)
        self.brightness_slider.set(self.config["brightness"])
        self.brightness_slider.pack()
        self.brightness_value = ctk.IntVar()
        self.update_brightness_slider(self.config["brightness"])
        self.brightness_display = ctk.CTkLabel(brightness_slider_frame, textvariable=self.brightness_value)
        self.brightness_display.pack(side="bottom", pady=5)

        # Save brightness button
        self.save_button_brightness = ctk.CTkButton(brightness_frame, text="Set", width=50, command=self.save_brightness)
        self.save_button_brightness.pack(side="right", pady=10)


        # ------------------------------------------------------------
        # Save button
        self.save_button = ctk.CTkButton(self.root, text="Set all", command=self.save_settings)
        self.save_button.pack(pady=10)

        # Preset field
        self.preset_label = ctk.CTkLabel(self.root, text="Presets")
        self.preset_label.pack(pady=5)

        self.preset_listbox = ctk.CTkTextbox(self.root, height=100, width=250, state="normal")
        self.preset_listbox.pack()

        self.new_preset_button = ctk.CTkButton(self.root, text="Add New Preset", command=self.add_preset)
        self.new_preset_button.pack(pady=10)

        self.message_label = ctk.CTkLabel(self.root, text="")
        self.message_label.pack(pady=5)


    def run(self):
        self.root.mainloop()

    def update_contrast_slider(self, value):
        self.contrast_value.set(round(float(value)))

    def update_brightness_slider(self, value):
        self.brightness_value.set(round(float(value)))

    def save_contrast(self):
        contrast = self.contrast_value.get()
        self.config["contrast"] = contrast
        self.monitor.set_contrast(contrast)

    def save_brightness(self):
        brightness = self.brightness_value.get()
        self.config["brightness"] = brightness
        self.monitor.set_brightness(brightness)

    def save_settings(self):
        contrast = self.contrast_value.get()
        brightness = self.brightness_value.get()
        self.config["contrast"] = contrast
        self.config["brightness"] = brightness
        self.message_label.configure(text=f"Settings Saved! Brightness: {brightness}, Contrast: {contrast}")
        
        self.monitor.set_values(brightness, contrast)

    def add_preset(self):
        contrast = self.contrast_value.get()
        brightness = self.brightness_value.get()
        preset_name = f"Preset {len(self.presets) + 1}"
        self.presets[preset_name] = (brightness, contrast)
        self.preset_listbox.insert("end", f"{preset_name}: Brightness {brightness}, Contrast {contrast}\n")
        self.message_label.configure(text=f"Preset {preset_name} added with Brightness: {brightness}, Contrast: {contrast}")
    
    def save_config(self):
        self.config["position"] = self.root.winfo_geometry()
        
        with open(self.config_file, 'wb') as file:
            pickle.dump(self.config, file)

    def retrive_config(self):
        with open(self.config_file, 'rb') as file:
            self.config = pickle.load(file)
        
        if not self.config.get("position"):
            self.config["position"] = "450x500+900+900"

        if not self.config.get("brightness"):
            self.config["brightness"] = 80
        
        if not self.config.get("contrast"):
            self.config["contrast"] = 20
        
        print("retrive_config():")
        print("Pos: ", self.config["position"])
        print("Brightness: ", self.config["brightness"])
        print("Contrast: ", self.config["contrast"])

    def on_exit(self):
        self.save_config()

        self.root.destroy()


if __name__ == "__main__":

    app = BrightnessContrastApp()
    app.run()
