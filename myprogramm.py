import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
import json
import re
import os
import shutil
from typing import Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='ce_configurator.log', filemode='w')


class Configurator:
    def __init__(self, root):
        self.style = None
        self.root = root
        self.root.title("CE Configurator")
        self.root.geometry("800x600")
        self.root.resizable(False, False)


        self.config = self.load_config()
        self.difficulty = tk.StringVar(value="normal")
        self.ai_army_size = tk.StringVar(value="6")
        self.points_to_win = tk.StringVar(value="24000")
        self.ammo_regen = tk.StringVar(value="No regen")
        self.damage_mode = tk.StringVar(value="Mod Damage")
        self.setup_styles()
        self.setup_ui()

    def load_config(self) -> Dict[str, Any]:
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.create_default_config()
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure colors
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        self.style.configure("TRadiobutton", background="#f0f0f0", font=("Helvetica", 10))
        self.style.configure("TButton", background="#4CAF50", foreground="white", font=("Helvetica", 10, "bold"))
        self.style.map("TButton", background=[('active', '#45a049')])

        # Custom styles
        self.style.configure("Title.TLabel", font=("Helvetica", 16, "bold"))
        self.style.configure("Subtitle.TLabel", font=("Helvetica", 12, "bold"))
        self.style.configure("Section.TFrame", background="#e0e0e0")
    def create_default_config(self) -> Dict[str, Any]:
        config = {
            "base_dir": os.path.dirname(os.path.abspath(__file__)),
            "backup_dir": os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups"),
            "periods": ["normal", "early", "mid", "late"],
            "files_to_update": [
                "units_fin.set", "units_fin2.set", "units_ger.set", "units_ger2.set",
                "units_rus.set", "units_rus2.set", "bot.wave_system.lua", "bot.lua",
                "dcg_easy.inc", "dcg_normal.inc", "dcg_hard.inc", "dcg_heroic.inc",
                "unit_research_fin.set", "unit_research_fin2.set", "unit_research_ger.set",
                "unit_research_ger2.set", "unit_research_rus.set", "unit_research_rus2.set"
            ]
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        return config

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Title
        ttk.Label(main_frame, text="CE Configurator", style="Title.TLabel").grid(column=0, row=0, columnspan=3,
                                                                                 pady=(0, 20))

        # Left Column
        left_frame = ttk.Frame(main_frame, style="Section.TFrame", padding="10")
        left_frame.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(0, 10))

        ttk.Label(left_frame, text="Game Settings", style="Subtitle.TLabel").grid(column=0, row=0, columnspan=2,
                                                                                  pady=(0, 10))

        # Difficulty selection
        ttk.Label(left_frame, text="Difficulty:").grid(column=0, row=1, sticky=tk.W, pady=5)
        difficulties = [("Performance (Easy)", "performance"), ("Normal", "normal"),
                        ("Hard", "hard"), ("Unfair", "unfair")]
        for i, (text, value) in enumerate(difficulties):
            ttk.Radiobutton(left_frame, text=text, variable=self.difficulty,
                            value=value).grid(column=1, row=i + 1, sticky=tk.W, pady=2)

        # AI Army Size
        ttk.Label(left_frame, text="AI Army Size:").grid(column=0, row=5, sticky=tk.W, pady=5)
        ttk.Entry(left_frame, textvariable=self.ai_army_size, width=10).grid(column=1, row=5, sticky=tk.W)
        ttk.Button(left_frame, text="Update", command=self.update_ai_army_size).grid(column=2, row=5, padx=5)

        # Points to Win
        ttk.Label(left_frame, text="Points to Win:").grid(column=0, row=6, sticky=tk.W, pady=5)
        ttk.Entry(left_frame, textvariable=self.points_to_win, width=10).grid(column=1, row=6, sticky=tk.W)
        ttk.Button(left_frame, text="Update", command=self.update_points_to_win).grid(column=2, row=6, padx=5)

        # Right Column
        right_frame = ttk.Frame(main_frame, style="Section.TFrame", padding="10")
        right_frame.grid(column=1, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))

        ttk.Label(right_frame, text="Advanced Settings", style="Subtitle.TLabel").grid(column=0, row=0, columnspan=2,
                                                                                       pady=(0, 10))

        # Ammo Regeneration
        ttk.Label(right_frame, text="Ammo Regeneration:").grid(column=0, row=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(right_frame, text="No Regeneration", variable=self.ammo_regen,
                        value="No regen").grid(column=1, row=1, sticky=tk.W)
        ttk.Radiobutton(right_frame, text="Regeneration", variable=self.ammo_regen,
                        value="Regen").grid(column=1, row=2, sticky=tk.W)
        ttk.Button(right_frame, text="Update", command=self.update_ammo_regen).grid(column=2, row=1, rowspan=2, padx=5)

        # Damage Settings
        ttk.Label(right_frame, text="Damage Settings:").grid(column=0, row=3, sticky=tk.W, pady=5)
        ttk.Radiobutton(right_frame, text="Modded Damage", variable=self.damage_mode,
                        value="Mod Damage").grid(column=1, row=3, sticky=tk.W)
        ttk.Radiobutton(right_frame, text="Vanilla Damage", variable=self.damage_mode,
                        value="Vanilla Damage").grid(column=1, row=4, sticky=tk.W)
        ttk.Button(right_frame, text="Update", command=self.update_damage_settings).grid(column=2, row=3, rowspan=2,
                                                                                         padx=5)

        # Buttons for options that still open new windows
        button_frame = ttk.Frame(main_frame, style="TFrame", padding="10")
        button_frame.grid(column=0, row=2, columnspan=2, sticky=(tk.W, tk.E), pady=20)

        buttons = [
            ("Set War Period", self.open_period_window),
            ("Player Army Size", self.player_army_size),
            ("Preparation Time", self.preparation_time),
            ("Resources at Start", self.resources_starting),
            ("Resource Income", self.resource_income),
            ("AI Defense Research", self.ai_fortifications),
            ("AI Research Speed", self.ai_researches)
        ]

        for i, (text, command) in enumerate(buttons):
            ttk.Button(button_frame, text=text, command=command).grid(column=i % 3, row=i // 3, padx=5, pady=5,
                                                                      sticky=(tk.W, tk.E))

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        # Help Button
        ttk.Button(main_frame, text="Help", command=self.show_help).grid(column=0, row=3, columnspan=2, pady=20)

        # Footer
        ttk.Label(main_frame, text="Made by MrCookie for Conquest Enhanced mod. Code available on GitHub.",
                  font=("Helvetica", 8)).grid(column=0, row=4, columnspan=2, pady=10)

    def update_ai_army_size(self):
        try:
            size = float(self.ai_army_size.get())
            if 1 <= size <= 10:
                self.save_numeric_setting("BotResources", str(size), r"BotResources +\d+")
                messagebox.showinfo("Success", "AI Army Size updated successfully!")
            else:
                messagebox.showerror("Error", "AI Army Size must be between 1 and 10")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for AI Army Size")

    def update_points_to_win(self):
        try:
            points = int(self.points_to_win.get())
            if points > 0:
                file_path = "./resource/set/multiplayer/games/campaign_capture_the_flag.set"
                self.save_numeric_setting_to_file(file_path, "winpoints", str(points), r"winpoints *?\d+")
                messagebox.showinfo("Success", "Points to Win updated successfully!")
            else:
                messagebox.showerror("Error", "Points to Win must be a positive integer")
        except ValueError:
            messagebox.showerror("Error", "Invalid input for Points to Win")

    def update_ammo_regen(self):
        file_path = "./resource/properties/resupply.inc"
        try:
            with open(file_path, "r") as file:
                content = file.read()

            if self.ammo_regen.get() == "Regen":
                content = content.replace("{regenerationPeriod 0};", "{regenerationPeriod 5};")
            else:
                content = content.replace("{regenerationPeriod 5};", "{regenerationPeriod 0};")

            with open(file_path, "w") as file:
                file.write(content)

            messagebox.showinfo("Success", "Ammo regeneration settings updated successfully!")
        except Exception as e:
            logging.error(f"Error updating ammo regeneration settings: {str(e)}")
            messagebox.showerror("Error", "Failed to update ammo regeneration settings")

    def update_damage_settings(self):
        try:
            source_file = "./configurator files/moddedballistics.set" if self.damage_mode.get() == "Mod Damage" else "./configurator files/vanillaballistics.set"
            target_file = "./resource/set/ballistics.set"
            shutil.copy2(source_file, target_file)
            messagebox.showinfo("Success", f"{self.damage_mode.get()} settings applied successfully!")
        except Exception as e:
            logging.error(f"Error updating damage settings: {str(e)}")
            messagebox.showerror("Error", "Failed to update damage settings")

    def save_numeric_setting(self, setting: str, value: str, pattern: str):
        file_to_read = self.get_difficulty_file()
        self.save_numeric_setting_to_file(file_to_read, setting, value, pattern)

    def save_numeric_setting_to_file(self, file_path: str, setting: str, value: str, pattern: str):
        try:
            with open(file_path, "r") as file:
                content = file.read()

            content = re.sub(pattern, f"{setting} {value}", content)

            with open(file_path, "w") as file:
                file.write(content)

        except Exception as e:
            logging.error(f"Error updating {setting}: {str(e)}")
            messagebox.showerror("Error", f"Failed to update {setting}")

    def get_difficulty_file(self):
        difficulty_files = {
            "performance": "./resource/set/dynamic_campaign/dcg_easy.inc",
            "normal": "./resource/set/dynamic_campaign/dcg_normal.inc",
            "hard": "./resource/set/dynamic_campaign/dcg_hard.inc",
            "unfair": "./resource/set/dynamic_campaign/dcg_heroic.inc"
        }
        return difficulty_files.get(self.difficulty.get(), difficulty_files["normal"])

    def open_period_window(self):
        period_window = tk.Toplevel(self.root)
        period_window.title("Choose War Period")
        period_window.geometry('400x350')

        ttk.Label(period_window, text="Select War Period", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2,
                                                                                        pady=10)

        periods = [
            ("All War (1939-1945)", "normal"),
            ("Early War (1939-1941)", "early"),
            ("Mid War (1941-1943)", "mid"),
            ("Late War (1943-1945)", "late")
        ]

        for i, (text, period) in enumerate(periods):
            ttk.Button(period_window, text=text, command=lambda p=period: self.set_period(p, period_window)).grid(
                row=i + 1, column=0, columnspan=2, pady=5)

        ttk.Button(period_window, text="Cancel", command=period_window.destroy).grid(row=len(periods) + 1, column=0,
                                                                                     columnspan=2, pady=10)

        warning_text = "Warning: Setting the war period will reset difficulty files.\nAny previous changes will be lost."
        ttk.Label(period_window, text=warning_text, foreground="red", wraplength=350).grid(row=len(periods) + 2,
                                                                                           column=0, columnspan=2,
                                                                                           pady=10)

    def set_period(self, period: str, window: tk.Toplevel):
        try:
            self.backup_files()
            self.update_files(period)
            messagebox.showinfo("Success", f"{period.capitalize()} war period set successfully!")
            window.destroy()
        except Exception as e:
            logging.error(f"Error setting {period} period: {str(e)}")
            messagebox.showerror("Error", f"Failed to set {period} period. Check the log for details.")
            self.rollback()

    def backup_files(self):
        backup_dir = self.config['backup_dir']
        os.makedirs(backup_dir, exist_ok=True)
        file_locations = {}

        for file in self.config['files_to_update']:
            if file in file_locations:
                src = file_locations[file]
            else:
                for root, _, files in os.walk(os.path.join(self.config['base_dir'], "resource")):
                    if file in files:
                        src = os.path.join(root, file)
                        file_locations[file] = src
                        break
                else:
                    logging.warning(f"File not found, skipping backup: {file}")
                    continue

            dst = os.path.join(backup_dir, file)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            try:
                shutil.copy2(src, dst)
            except PermissionError:
                raise Exception(f"Permission denied when trying to backup {src}")

    def update_files(self, period: str):
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Updating Files")
        progress = ttk.Progressbar(progress_window, length=300, mode='determinate')
        progress.pack(pady=10)
        status_label = ttk.Label(progress_window, text="Updating files...")
        status_label.pack()

        total_files = len(self.config['files_to_update'])
        file_locations = {}

        for i, file in enumerate(self.config['files_to_update']):
            if file in file_locations:
                src = file_locations[file]
            else:
                for root, _, files in os.walk(
                        os.path.join(self.config['base_dir'], "configurator files", f"{period}war")):
                    if file in files:
                        src = os.path.join(root, file)
                        file_locations[file] = src
                        break
                else:
                    logging.warning(f"File not found, skipping update: {file}")
                    continue

            dst = os.path.join(self.config['base_dir'], "resource", file)
            try:
                with open(src, "r") as source_file, open(dst, "w") as dest_file:
                    dest_file.write(source_file.read())
            except PermissionError:
                raise Exception(f"Permission denied when trying to update {dst}")

            progress['value'] = (i + 1) / total_files * 100
            status_label.config(text=f"Updating {file}...")
            progress_window.update()

        progress_window.destroy()

    def rollback(self):
        backup_dir = self.config['backup_dir']
        for file in self.config['files_to_update']:
            src = os.path.join(backup_dir, file)
            dst = os.path.join(self.config['base_dir'], "resource", file)
            if os.path.exists(src):
                try:
                    shutil.copy2(src, dst)
                except Exception as e:
                    logging.error(f"Error during rollback of {file}: {str(e)}")
        messagebox.showinfo("Rollback", "Changes have been rolled back due to an error.")

    def player_army_size(self):
        player_size_window = tk.Toplevel(self.root)
        player_size_window.title("Player Army Size")
        player_size_window.geometry('700x250')

        each_stage_size = tk.StringVar()
        whole_budget = tk.StringVar()

        file_to_read = self.get_difficulty_file()

        with open(file_to_read, "r") as length_file:
            whole_file = length_file.read()
            stage_cp = re.search(r"\{StageCP ([^\}]+)\}", whole_file)
            if stage_cp:
                each_stage_size.set(stage_cp.group(1))

            start_budget = re.search(r'\{Start "([^"]+)"\}', whole_file)
            if start_budget:
                whole_budget.set(start_budget.group(1))

        ttk.Label(player_size_window,
                  text="Size of each stage (keep the space between each number, should be 7 numbers):").grid(row=1,
                                                                                                             column=0,
                                                                                                             padx=10,
                                                                                                             pady=5)
        ttk.Entry(player_size_window, textvariable=each_stage_size, width=50).grid(row=2, column=0, padx=10, pady=5)

        ttk.Label(player_size_window,
                  text="Total points for buying stages (in mod, you're supposed to only have enough for 5):").grid(
            row=3, column=0, padx=10, pady=5)
        ttk.Entry(player_size_window, textvariable=whole_budget, width=50).grid(row=4, column=0, padx=10, pady=5)

        ttk.Button(player_size_window, text="Save Changes",
                   command=lambda: self.save_player_army_size(file_to_read, each_stage_size.get(),
                                                              whole_budget.get(), player_size_window)).grid(row=5,
                                                                                                            column=0,
                                                                                                            pady=10)

    def save_player_army_size(self, file_path: str, stage_size: str, budget: str, window: tk.Toplevel):
        try:
            with open(file_path, "r") as file:
                content = file.read()

            content = re.sub(r"\{StageCP [^\}]+\}", f"{{StageCP {stage_size}}}", content)
            content = re.sub(r'\{Start "[^"]+"\}', f'{{Start "{budget}"}}', content)

            with open(file_path, "w") as file:
                file.write(content)

            messagebox.showinfo("Success", "Player army size updated successfully!")
            window.destroy()
        except Exception as e:
            logging.error(f"Error updating player army size: {str(e)}")
            messagebox.showerror("Error", "Failed to update player army size. Check the log for details.")

    def preparation_time(self):
        prep_window = tk.Toplevel(self.root)
        prep_window.title("Preparation Time")
        prep_window.geometry('800x400')

        times = {
            "oneFlagOffsetTime": tk.StringVar(),
            "twoFlagOffsetTime": tk.StringVar(),
            "threeFlagOffsetTime": tk.StringVar(),
            "fourFlagOffsetTime": tk.StringVar(),
            "fiveFlagOffsetTime": tk.StringVar()
        }

        file_path = "./resource/conquest_configuration/bot.conquest_configuration.lua"

        with open(file_path, "r") as file:
            content = file.read()
            for key in times:
                match = re.search(rf"{key} = (\d+)", content)
                if match:
                    times[key].set(match.group(1))

        row = 0
        for key, var in times.items():
            ttk.Label(prep_window, text=f"Time for {key}:").grid(row=row, column=0, padx=10, pady=5)
            ttk.Spinbox(prep_window, from_=1, to=10000, textvariable=var).grid(row=row, column=1, padx=10, pady=5)
            row += 1

        ttk.Button(prep_window, text="Save Changes",
                   command=lambda: self.save_preparation_time(file_path, times, prep_window)).grid(row=row,
                                                                                                   column=0,
                                                                                                   columnspan=2,
                                                                                                   pady=10)

    def save_preparation_time(self, file_path: str, times: Dict[str, tk.StringVar], window: tk.Toplevel):
        try:
            with open(file_path, "r") as file:
                content = file.read()

            for key, var in times.items():
                content = re.sub(rf"{key} = \d+", f"{key} = {var.get()}", content)

            with open(file_path, "w") as file:
                file.write(content)

            messagebox.showinfo("Success", "Preparation times updated successfully!")
            window.destroy()
        except Exception as e:
            logging.error(f"Error updating preparation times: {str(e)}")
            messagebox.showerror("Error", "Failed to update preparation times. Check the log for details.")

    def resources_starting(self):
        resources_window = tk.Toplevel(self.root)
        resources_window.title("Starting Resources")
        resources_window.geometry('400x250')

        resources = {
            "Research Points": tk.StringVar(),
            "Manpower Points": tk.StringVar(),
            "Star Call Points": tk.StringVar(),
            "Ammo Points": tk.StringVar()
        }

        file_to_read = self.get_difficulty_file()

        with open(file_to_read, "r") as file:
            content = file.read()
            for resource, var in resources.items():
                match = re.search(rf"{resource.replace(' ', '')}.*?StartVal (\d+)", content, re.DOTALL)
                if match:
                    var.set(match.group(1))

        row = 0
        for resource, var in resources.items():
            ttk.Label(resources_window, text=f"Starting {resource}:").grid(row=row, column=0, padx=10, pady=5)
            ttk.Spinbox(resources_window, from_=1, to=100000, textvariable=var).grid(row=row, column=1, padx=10,
                                                                                     pady=5)
            row += 1

        ttk.Button(resources_window, text="Save Changes",
                   command=lambda: self.save_resources_starting(file_to_read, resources, resources_window)).grid(
            row=row, column=0, columnspan=2, pady=10)

    def save_resources_starting(self, file_path: str, resources: Dict[str, tk.StringVar], window: tk.Toplevel):
        try:
            with open(file_path, "r") as file:
                content = file.read()

            for resource, var in resources.items():
                content = re.sub(rf"({resource.replace(' ', '')}).*?StartVal \d+", rf"\1\nStartVal {var.get()}",
                                 content, flags=re.DOTALL)

            with open(file_path, "w") as file:
                file.write(content)

            messagebox.showinfo("Success", "Starting resources updated successfully!")
            window.destroy()
        except Exception as e:
            logging.error(f"Error updating starting resources: {str(e)}")
            messagebox.showerror("Error", "Failed to update starting resources. Check the log for details.")

    def resource_income(self):
        income_window = tk.Toplevel(self.root)
        income_window.title("Resource Income Multiplier")
        income_window.geometry('400x200')

        risk_levels = {
            "Low Risk": tk.StringVar(),
            "Standard Risk": tk.StringVar(),
            "High Risk": tk.StringVar()
        }

        file_to_read = self.get_difficulty_file()

        with open(file_to_read, "r") as file:
            content = file.read()
            rewards = re.findall(r"\{Rewards ([^}]+)\}", content)
            for i, var in enumerate(risk_levels.values()):
                if i < len(rewards):
                    var.set(rewards[i])

        row = 0
        for risk, var in risk_levels.items():
            ttk.Label(income_window, text=f"{risk}:").grid(row=row, column=0, padx=10, pady=5)
            ttk.Spinbox(income_window, from_=1.00, to=100.00, textvariable=var, format="%.2f", increment=0.1).grid(
                row=row, column=1, padx=10, pady=5)
            row += 1

        ttk.Button(income_window, text="Save Changes",
                   command=lambda: self.save_resource_income(file_to_read, risk_levels, income_window)).grid(
            row=row, column=0, columnspan=2, pady=10)

    def save_resource_income(self, file_path: str, risk_levels: Dict[str, tk.StringVar], window: tk.Toplevel):
        try:
            with open(file_path, "r") as file:
                content = file.read()

            rewards = [var.get() for var in risk_levels.values()]
            content = re.sub(r"\{Rewards [^}]+\}", lambda m: f"{{Rewards {rewards.pop(0)}}}", content)

            with open(file_path, "w") as file:
                file.write(content)

            messagebox.showinfo("Success", "Resource income multipliers updated successfully!")
            window.destroy()
        except Exception as e:
            logging.error(f"Error updating resource income multipliers: {str(e)}")
            messagebox.showerror("Error",
                                 "Failed to update resource income multipliers. Check the log for details.")

    def ai_fortifications(self):
        fort_window = tk.Toplevel(self.root)
        fort_window.title("AI Defense Research Speed")
        fort_window.geometry('700x200')

        levels = {
            "Second Level": tk.StringVar(),
            "Third Level": tk.StringVar()
        }

        file_to_read = self.get_difficulty_file()

        with open(file_to_read, "r") as file:
            content = file.read()
            for level, var in levels.items():
                match = re.search(rf"{level}.*?unlock games (\d+)", content, re.DOTALL)
                if match:
                    var.set(match.group(1))

        row = 0
        for level, var in levels.items():
            ttk.Label(fort_window, text=f"Missions for {level} defense:").grid(row=row, column=0, padx=10, pady=5)
            ttk.Spinbox(fort_window, from_=1, to=100, textvariable=var).grid(row=row, column=1, padx=10, pady=5)
            row += 1

        ttk.Button(fort_window, text="Save Changes",
                   command=lambda: self.save_ai_fortifications(file_to_read, levels, fort_window)).grid(row=row,
                                                                                                        column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=10)

    def save_ai_fortifications(self, file_path: str, levels: Dict[str, tk.StringVar], window: tk.Toplevel):
        try:
            with open(file_path, "r") as file:
                content = file.read()

            for level, var in levels.items():
                content = re.sub(rf"({level}).*?unlock games \d+", rf"\1\nunlock games {var.get()}", content,
                                 flags=re.DOTALL)

            with open(file_path, "w") as file:
                file.write(content)

            messagebox.showinfo("Success", "AI defense research speed updated successfully!")
            window.destroy()
        except Exception as e:
            logging.error(f"Error updating AI defense research speed: {str(e)}")
            messagebox.showerror("Error", "Failed to update AI defense research speed. Check the log for details.")

    def ai_researches(self):
        research_window = tk.Toplevel(self.root)
        research_window.title("AI Research Speed")
        research_window.geometry('400x200')

        ai_prog = tk.StringVar(value="normal")

        progressions = [
            ("Normal AI progression", "normal"),
            ("30% slower AI progression", "slow30"),
            ("60% slower AI progression", "slow60"),
            ("Faster AI progression", "fast")
        ]

        for i, (text, value) in enumerate(progressions):
            ttk.Radiobutton(research_window, text=text, variable=ai_prog, value=value).grid(row=i, column=0,
                                                                                            padx=10, pady=5,
                                                                                            sticky="w")

        ttk.Button(research_window, text="Save Changes",
                   command=lambda: self.save_ai_researches(ai_prog.get(), research_window)).grid(
            row=len(progressions), column=0, pady=10)

    def save_ai_researches(self, progression: str, window: tk.Toplevel):
        file_to_read = self.get_difficulty_file()
        try:
            with open(file_to_read, "r") as file:
                content = file.read()

            progressions = {
                "normal": '{ResearchStages "0:1 1:2 2:3 3:4 4:5 5:6 6:7 7:8 8:9 9:10 10:11 11:12 12:13 13:14 14:15 15:16 16:17 17:18 18:19 19:20"}',
                "slow30": '{ResearchStages "0:1 1:1 2:2 3:2 4:3 5:4 6:5 7:6 8:7 9:8 10:9 11:10 12:11 13:12 14:13 15:14 16:15 17:16 18:17 19:18 20:19 21:20"}',
                "slow60": '{ResearchStages "0:1 1:1 2:2 3:2 4:2 5:3 6:3 7:4 8:4 9:5 10:5 11:6 12:7 13:8 14:9 15:9 16:10 17:11 18:12 19:13 20:14 21:15 22:16 23:17 24:18 25:19 25:20"}',
                "fast": '{ResearchStages "0:2 1:2 2:4 3:4 4:6 5:6 6:8 7:8 8:10 9:10 10:12 11:13 12:14 13:15 14:16 15:18 16:19 17:20"}'
            }

            for prog, stages in progressions.items():
                content = content.replace(stages, progressions[progression])

            with open(file_to_read, "w") as file:
                file.write(content)

            messagebox.showinfo("Success", "AI research speed updated successfully!")
            window.destroy()
        except Exception as e:
            logging.error(f"Error updating AI research speed: {str(e)}")
            messagebox.showerror("Error", "Failed to update AI research speed. Check the log for details.")

    def show_help(self):
        help_text = """
        CE Configurator Help:

        1. Difficulty Selection:
           Choose the difficulty level using the radio buttons at the top.

        2. Main Window Controls:
           - AI Army Size: Set the multiplier for AI army size (normally between 6 and 7).
           - Points to Win: Set the number of points required to win (24000 is about 30-35 minutes).
           - Ammo Regeneration: Choose whether supply trucks regenerate ammo or not.
           - Damage Settings: Toggle between modded and vanilla damage models.

        3. Additional Settings (separate windows):
           - Set War Period: Choose the time period for the game (affects unit availability).
           - Player Army Size: Modify the player's army size and budget for each stage.
           - Preparation Time: Set the time before AI arrives in different scenarios.
           - Resources at Start: Adjust starting resources for the player.
           - Resource Income: Modify resource income multipliers based on risk levels.
           - AI Defense Research Speed: Change how quickly AI researches defenses.
           - AI Research Speed: Adjust the speed of AI research progression.

        4. File Operations:
           - The configurator automatically selects the correct files based on the chosen difficulty.
           - Backups are created before making changes. In case of errors, changes are rolled back.

        5. After Making Changes:
           - Always check the game to ensure the desired effect.
           - If you encounter any issues, check the log file (ce_configurator.log) for details.

        6. Additional Information:
           - For more detailed information, please refer to the mod description.
           - If you need further assistance, contact the mod author on Discord.

        Remember to use these settings responsibly to maintain game balance and enjoyment.
        """
        messagebox.showinfo("CE Configurator Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = Configurator(root)
    root.mainloop()