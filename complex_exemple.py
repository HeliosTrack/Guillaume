import customtkinter
from tkintermapview import TkinterMapView
import API_meshtastic
import time, os, threading

customtkinter.set_default_color_theme("blue")


class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        button = customtkinter.CTkButton(self, text="Get info : ", width=100, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return



class DataRecorder:
    def __init__(self):
        self.recording = {}  # Stocke l'état d'enregistrement des nœuds
        self.threads = {}  # Stocke les threads d'enregistrement
        self.stop_events = {}  # Drapeaux pour arrêter proprement les threads

    def record(self, node_id):
        if node_id in self.threads and self.threads[node_id].is_alive():
            print(f"Un enregistrement est déjà en cours pour le nœud {node_id}.")
            return

        print(f"Début de l'enregistrement pour le nœud {node_id}...")

        self.stop_events[node_id] = threading.Event()  # Création du drapeau d'arrêt

        thread = threading.Thread(target=self._record_data, args=(node_id,), daemon=True)
        self.threads[node_id] = thread
        thread.start()

    def _record_data(self, node_id):
        file_path = f"data_{node_id}.csv"

        # Vérifier si le fichier existe, sinon créer l'en-tête
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write("temp,humidity,pression\n")

        while not self.stop_events[node_id].is_set():  # Vérification du drapeau d'arrêt
            telemetry_env = API_meshtastic.get_temp_humidity_pression(node_id)

            if telemetry_env:
                temp = telemetry_env.get('temp')
                humidity = telemetry_env.get('humidity')
                pression = telemetry_env.get('pression')

                # Vérification que toutes les valeurs sont valides
                if None not in [temp, humidity, pression]:
                    with open(file_path, "a") as file:
                        file.write(f"{temp},{humidity},{pression}\n")
                else:
                    print(f"Données invalides reçues pour {node_id}: {telemetry_env}")

            self.stop_events[node_id].wait(1)  # Attente 1 seconde ou arrêt immédiat

        print(f"Enregistrement terminé pour le nœud {node_id}.")

    def save(self, node_id):
        if node_id in self.threads and self.threads[node_id].is_alive():
            print(f"Arrêt de l'enregistrement pour le nœud {node_id}...")
            self.stop_events[node_id].set()  # Déclenchement du drapeau d'arrêt

            self.threads[node_id].join()  # Attente de l'arrêt du thread
            del self.threads[node_id]  # Suppression du thread terminé
            del self.stop_events[node_id]  # Suppression du drapeau d'arrêt
            print(f"Enregistrement pour {node_id} arrêté avec succès.")
        else:
            print(f"Aucun enregistrement en cours pour le nœud {node_id}.")

class App(customtkinter.CTk):

    APP_NAME = "TkinterMapView with CustomTkinter"
    WIDTH = 800
    HEIGHT = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.minsize(App.WIDTH, App.HEIGHT)
        self.cansat = {}

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.marker_list = []

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=250, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        self.frame_left.grid_rowconfigure(1, weight=1)

        # Ajout du cadre pour la liste des CanSats
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(
            master=self.frame_left, width=270, command=self.label_button_frame_event, corner_radius=0
        )
        self.scrollable_label_button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Label pour afficher les informations du CanSat sélectionné
        self.cansat_info_label = customtkinter.CTkLabel(self.frame_left, text="Sélectionnez un CanSat", anchor="w", justify="left", wraplength=220)
        self.cansat_info_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.frame_left, values=["Light", "Dark", "System"], command=self.change_appearance_mode
        )
        self.appearance_mode_optionemenu.grid(row=3, column=0, padx=20, pady=10)

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, column=0, sticky="nswe", padx=0, pady=0)

        self.entry = customtkinter.CTkEntry(master=self.frame_right, placeholder_text="Type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=12, pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_search = customtkinter.CTkButton(master=self.frame_right, text="Search", width=90, command=self.search_event)
        self.button_search.grid(row=0, column=1, sticky="w", padx=12, pady=12)

        self.map_widget.set_address("Paris")
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.appearance_mode_optionemenu.set("Dark")

        nodes = API_meshtastic.get_device()

        if nodes:
            for node_id, node_info in nodes.items():
                user = node_info.get('user', {})
                position = node_info.get('position', {})

                long_name = user.get('longName', 'Unknown')
                short_name = user.get('shortName', 'Unknown')
                latitude = position.get('latitude', None)
                longitude = position.get('longitude', None)
                altitude = position.get('altitude', None)

                if latitude is None or longitude is None:
                    latitude, longitude, altitude = 'N/A', 'N/A', 'N/A'
                else:
                    self.set_marker_event(latitude, longitude)

                self.scrollable_label_button_frame.add_item(long_name)

                self.cansat[node_id] = {
                    'longName': long_name,
                    'shortName': short_name,
                    'latitude': latitude,
                    'longitude': longitude,
                    'altitude': altitude
                }

        print(self.cansat)

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


    def label_button_frame_event(self, item):
        """Affiche les informations du CanSat sélectionné"""
        for node_id, data in self.cansat.items():
            if data['longName'] == item:
                telemetry_env = API_meshtastic.get_temp_humidity_pression(node_id)
                info_text = f"Nom: {data['longName']}\n"
                info_text += f"Abréviation: {data['shortName']}\n"
                info_text += f"Latitude: {data['latitude']}\n"
                info_text += f"Longitude: {data['longitude']}\n"
                info_text += f"Altitude: {data['altitude']}m"
                info_text += "\n\nTélémétrie environnementale:"
                info_text += f"\nTempérature: {telemetry_env['temp']}°C\n"
                info_text += f"Hygrométrie: {telemetry_env['humidity']}%\n"
                info_text += f"Pression: {telemetry_env['pression']}hPa"
                
                self.cansat_info_label.configure(text=info_text)

                start_recording = customtkinter.CTkButton(self.frame_left, text="Start Recording", width=100, height=24)
                start_recording.grid(row=4, column=0, pady=(10, 0), padx=5)
                start_recording.configure(command=lambda: DataRecorder().record(node_id))

                stop_recording = customtkinter.CTkButton(self.frame_left, text="Stop Recording", width=100, height=24)
                stop_recording.grid(row=5, column=0, pady=(10, 0), padx=5)
                stop_recording.configure(command=lambda: DataRecorder().save(node_id))

                # Ajouter un marqueur sur la carte si les coordonnées sont valides
                if isinstance(data['latitude'], float) and isinstance(data['longitude'], float):
                    marker = self.map_widget.set_marker(data['latitude'], data['longitude'], text=data['longName'])
                    self.marker_list.append(marker)

                return
            
    def set_marker_event(self, lattitude, longitude):
        self.marker_list.append(self.map_widget.set_marker(lattitude, longitude))

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start() 
    API_meshtastic.close_interface()