#!/usr/bin/env python3
"""
Creality RFID Tool - GUI Application
User-friendly interface for reading and writing RFID tags
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, colorchooser
import subprocess
import threading
import os
import sys

class CrealityRFIDGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Creality RFID Tool")
        self.root.geometry("900x700")
        
        # Get script path
        self.script_path = self.find_script()
        
        # Check if Proxmark3 is available
        self.pm3_available = self.check_pm3()
        
        # Material codes dictionary
        self.materials = {
            'HyperPLA': '01001',
            'HyperPLA-CF': '02001',
            'HyperABS': '03001',
            'CR-PLA': '04001',
            'CR-Silk': '05001',
            'CR-PETG': '06001',
            'CR-ABS': '07001',
            'Ender-PLA': '08001',
            'EN-PLA+': '09001',
            'ENDERFASTPLA': '09002',
            'HP-TPU': '10001',
            'CR-Nylon': '11001',
            'CR-PLACarbon': '13001',
            'CR-PLAMatte': '14001',
            'CR-PLAFluo': '15001',
            'CR-TPU': '16001',
            'CR-Wood': '17001',
            'HPUltraPLA': '18001',
            'HP-ASA': '19001',
            'HyperPETG': '06002',
            'GenericPLA': '00001',
            'GenericPLA-Silk': '00002',
            'GenericPETG': '00003',
            'GenericABS': '00004',
            'GenericTPU': '00005',
            'GenericPLA-CF': '00006',
            'GenericASA': '00007',
            'GenericPA': '00008',
            'GenericPA-CF': '00009',
            'GenericBVOH': '00010',
            'GenericPVA': '00011',
            'GenericHIPS': '00012',
            'GenericPET-CF': '00013',
            'GenericPETG-CF': '00014',
            'GenericPA6-CF': '00015',
            'GenericPAHT-CF': '00016',
            'GenericPPS': '00017',
            'GenericPPS-CF': '00018',
            'GenericPP': '00019',
            'GenericPET': '00020',
            'GenericPC': '00021',
        }
        
        # Color presets
        self.color_presets = {
            'Red': '0FF0000',
            'Green': '000FF00',
            'Blue': '00000FF',
            'Yellow': '0FFFF00',
            'Orange': '0FFA500',
            'Purple': '0800080',
            'Pink': '0FFC0CB',
            'White': '0FFFFFF',
            'Black': '0000000',
            'Gray': '0808080',
        }
        
        # Create UI
        self.create_widgets()
        
    def find_script(self):
        """Find the creality_rfid.py script"""
        # Check current directory
        if os.path.exists('creality_rfid.py'):
            return './creality_rfid.py'
        # Check parent directory
        if os.path.exists('../creality_rfid.py'):
            return '../creality_rfid.py'
        # Check same directory as this GUI
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, 'creality_rfid.py')
        if os.path.exists(script_path):
            return script_path
        return None
        
    def check_pm3(self):
        """Check if Proxmark3 is available"""
        try:
            subprocess.run(['pm3', '--help'], capture_output=True, timeout=2)
            return True
        except:
            try:
                subprocess.run(['proxmark3', '--help'], capture_output=True, timeout=2)
                return True
            except:
                return False
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Status bar at top
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Script status
        script_status = "✓ Script found" if self.script_path else "✗ Script not found"
        script_color = "green" if self.script_path else "red"
        ttk.Label(status_frame, text=script_status, foreground=script_color).pack(side=tk.LEFT, padx=5)
        
        # PM3 status
        pm3_status = "✓ Proxmark3 detected" if self.pm3_available else "✗ Proxmark3 not found"
        pm3_color = "green" if self.pm3_available else "red"
        ttk.Label(status_frame, text=pm3_status, foreground=pm3_color).pack(side=tk.LEFT, padx=5)
        
        if not self.script_path:
            ttk.Label(status_frame, text="Place creality_rfid_fixed.py in the same directory", 
                     foreground="red").pack(side=tk.LEFT, padx=5)
        
        # Main notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.create_write_tab()
        self.create_read_tab()
        self.create_reference_tab()
        self.create_manual_tab()
        
    def create_write_tab(self):
        """Create Write Tag tab"""
        write_frame = ttk.Frame(self.notebook)
        self.notebook.add(write_frame, text="Write Tag")
        
        # Main content frame
        content = ttk.Frame(write_frame)
        content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - inputs
        left_frame = ttk.LabelFrame(content, text="Tag Configuration", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        row = 0
        
        # Material selection
        ttk.Label(left_frame, text="Material:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.material_var = tk.StringVar(value='HyperPLA')
        material_combo = ttk.Combobox(left_frame, textvariable=self.material_var, 
                                      values=sorted(self.materials.keys()), width=25)
        material_combo.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Color selection
        ttk.Label(left_frame, text="Color:").grid(row=row, column=0, sticky=tk.W, pady=5)
        color_frame = ttk.Frame(left_frame)
        color_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        self.color_var = tk.StringVar(value='00000FF')
        self.color_entry = ttk.Entry(color_frame, textvariable=self.color_var, width=10)
        self.color_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        # Color preview
        self.color_preview = tk.Canvas(color_frame, width=30, height=20, bg='#0000FF', relief=tk.SUNKEN)
        self.color_preview.pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(color_frame, text="Pick Color", command=self.pick_color).pack(side=tk.LEFT)
        row += 1
        
        # Color presets
        ttk.Label(left_frame, text="Presets:").grid(row=row, column=0, sticky=tk.W, pady=5)
        preset_frame = ttk.Frame(left_frame)
        preset_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        for i, (name, code) in enumerate(list(self.color_presets.items())[:5]):
            ttk.Button(preset_frame, text=name, width=8,
                      command=lambda c=code: self.set_color(c)).grid(row=0, column=i, padx=2)
        
        for i, (name, code) in enumerate(list(self.color_presets.items())[5:]):
            ttk.Button(preset_frame, text=name, width=8,
                      command=lambda c=code: self.set_color(c)).grid(row=1, column=i, padx=2, pady=2)
        row += 1
        
        # Weight/Length
        ttk.Label(left_frame, text="Weight:").grid(row=row, column=0, sticky=tk.W, pady=5)
        weight_frame = ttk.Frame(left_frame)
        weight_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        self.weight_var = tk.StringVar(value='1.0 kg')
        ttk.Radiobutton(weight_frame, text="1.0 kg", variable=self.weight_var, 
                       value='1.0 kg').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(weight_frame, text="0.5 kg", variable=self.weight_var, 
                       value='0.5 kg').pack(side=tk.LEFT, padx=5)
        row += 1
        
        # Serial number
        ttk.Label(left_frame, text="Serial Number:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.serial_var = tk.StringVar(value='000001')
        ttk.Entry(left_frame, textvariable=self.serial_var, width=15).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Separator
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=10)
        row += 1
        
        # Advanced options
        ttk.Label(left_frame, text="Advanced:", font=('TkDefaultFont', 9, 'bold')).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Batch
        ttk.Label(left_frame, text="Batch:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.batch_var = tk.StringVar(value='1A5')
        ttk.Entry(left_frame, textvariable=self.batch_var, width=15).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Date
        ttk.Label(left_frame, text="Date (YYMDD):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.date_var = tk.StringVar(value='24120')
        ttk.Entry(left_frame, textvariable=self.date_var, width=15).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Supplier
        ttk.Label(left_frame, text="Supplier:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.supplier_var = tk.StringVar(value='1B3D')
        ttk.Entry(left_frame, textvariable=self.supplier_var, width=15).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Encrypted checkbox
        self.encrypted_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(left_frame, text="Tag is already encrypted", 
                       variable=self.encrypted_var).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Manual UID
        self.manual_uid_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(left_frame, text="Use manual UID (skip auto-read)", 
                       variable=self.manual_uid_var,
                       command=self.toggle_manual_uid).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Label(left_frame, text="UID:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.uid_var = tk.StringVar(value='')
        self.uid_entry = ttk.Entry(left_frame, textvariable=self.uid_var, width=15, state=tk.DISABLED)
        self.uid_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Right side - output and actions
        right_frame = ttk.Frame(content)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Output console
        output_label = ttk.Label(right_frame, text="Output:")
        output_label.pack(anchor=tk.W)
        
        self.write_output = scrolledtext.ScrolledText(right_frame, height=20, width=50)
        self.write_output.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Action buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X)
        
        self.write_button = ttk.Button(button_frame, text="Write to Tag", 
                                       command=self.write_tag, style='Accent.TButton')
        self.write_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Output", 
                  command=lambda: self.write_output.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
    def create_read_tab(self):
        """Create Read Tag tab"""
        read_frame = ttk.Frame(self.notebook)
        self.notebook.add(read_frame, text="Read Tag")
        
        content = ttk.Frame(read_frame, padding=10)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        info_frame = ttk.LabelFrame(content, text="Instructions", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, text="1. Place tag on Proxmark3 antenna\n"
                                   "2. Click 'Read Tag' button\n"
                                   "3. Tag information will be displayed below",
                 justify=tk.LEFT).pack(anchor=tk.W)
        
        # Manual UID option
        uid_frame = ttk.Frame(content)
        uid_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.read_manual_uid_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(uid_frame, text="Use manual UID:", 
                       variable=self.read_manual_uid_var,
                       command=self.toggle_read_manual_uid).pack(side=tk.LEFT)
        
        self.read_uid_var = tk.StringVar(value='')
        self.read_uid_entry = ttk.Entry(uid_frame, textvariable=self.read_uid_var, 
                                       width=20, state=tk.DISABLED)
        self.read_uid_entry.pack(side=tk.LEFT, padx=5)
        
        # Output console
        output_label = ttk.Label(content, text="Tag Data:")
        output_label.pack(anchor=tk.W)
        
        self.read_output = scrolledtext.ScrolledText(content, height=25, width=80)
        self.read_output.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Action buttons
        button_frame = ttk.Frame(content)
        button_frame.pack(fill=tk.X)
        
        self.read_button = ttk.Button(button_frame, text="Read Tag", 
                                      command=self.read_tag, style='Accent.TButton')
        self.read_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear Output", 
                  command=lambda: self.read_output.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
    
    def create_reference_tab(self):
        """Create Reference Tables tab"""
        ref_frame = ttk.Frame(self.notebook)
        self.notebook.add(ref_frame, text="Reference")
        
        content = ttk.Frame(ref_frame, padding=10)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(content)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(button_frame, text="Show Materials", 
                  command=lambda: self.show_reference('--materials')).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show Colors", 
                  command=lambda: self.show_reference('--colors')).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show All", 
                  command=lambda: self.show_reference('--all')).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=lambda: self.ref_output.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        # Output
        self.ref_output = scrolledtext.ScrolledText(content, height=30, width=80, font=('Courier', 9))
        self.ref_output.pack(fill=tk.BOTH, expand=True)
        
    def create_manual_tab(self):
        """Create Manual Commands tab"""
        manual_frame = ttk.Frame(self.notebook)
        self.notebook.add(manual_frame, text="Manual Commands")
        
        content = ttk.Frame(manual_frame, padding=10)
        content.pack(fill=tk.BOTH, expand=True)
        
        # Info
        info_frame = ttk.LabelFrame(content, text="About", padding=10)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(info_frame, text="Generate commands for manual copy/paste into Proxmark3.\n"
                                   "Useful if you want to see the exact commands or run them manually.",
                 justify=tk.LEFT).pack(anchor=tk.W)
        
        # Input frame
        input_frame = ttk.LabelFrame(content, text="Generate Commands", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # UID input
        ttk.Label(input_frame, text="UID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.manual_uid_input = tk.StringVar(value='3A14ACF1')
        ttk.Entry(input_frame, textvariable=self.manual_uid_input, width=20).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Button(input_frame, text="Generate Key", 
                  command=self.generate_key).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Button(input_frame, text="Generate Write Commands", 
                  command=self.generate_write_commands).grid(row=0, column=3, padx=5, pady=5)
        
        # Output
        output_label = ttk.Label(content, text="Generated Commands:")
        output_label.pack(anchor=tk.W)
        
        self.manual_output = scrolledtext.ScrolledText(content, height=25, width=80, font=('Courier', 9))
        self.manual_output.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Buttons
        button_frame = ttk.Frame(content)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=lambda: self.manual_output.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
    
    # Helper methods
    def toggle_manual_uid(self):
        """Toggle manual UID entry"""
        if self.manual_uid_var.get():
            self.uid_entry.config(state=tk.NORMAL)
        else:
            self.uid_entry.config(state=tk.DISABLED)
            
    def toggle_read_manual_uid(self):
        """Toggle read manual UID entry"""
        if self.read_manual_uid_var.get():
            self.read_uid_entry.config(state=tk.NORMAL)
        else:
            self.read_uid_entry.config(state=tk.DISABLED)
    
    def pick_color(self):
        """Open color picker dialog"""
        # Get current color
        current = self.color_var.get()
        if len(current) == 7 and current[0] == '0':
            current_rgb = '#' + current[1:]
        else:
            current_rgb = '#0000FF'
        
        color = colorchooser.askcolor(initialcolor=current_rgb)
        if color[1]:  # color[1] is the hex value
            # Convert #RRGGBB to 0RRGGBB
            self.set_color('0' + color[1][1:].upper())
    
    def set_color(self, color_code):
        """Set color and update preview"""
        self.color_var.set(color_code)
        # Update preview
        if len(color_code) == 7 and color_code[0] == '0':
            rgb = '#' + color_code[1:]
            self.color_preview.config(bg=rgb)
    
    def run_command(self, args, output_widget):
        """Run a command in a thread and display output"""
        if not self.script_path:
            output_widget.insert(tk.END, "[ERROR] Script not found!\n")
            output_widget.insert(tk.END, "Please place creality_rfid_fixed.py in the same directory.\n")
            return
        
        def run():
            try:
                output_widget.insert(tk.END, f"[CMD] python3 {self.script_path} {' '.join(args)}\n\n")
                output_widget.see(tk.END)
                
                process = subprocess.Popen(
                    ['python3', self.script_path] + args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                for line in process.stdout:
                    output_widget.insert(tk.END, line)
                    output_widget.see(tk.END)
                    self.root.update_idletasks()
                
                process.wait()
                
                if process.returncode == 0:
                    output_widget.insert(tk.END, "\n✓ Command completed successfully!\n")
                else:
                    output_widget.insert(tk.END, f"\n✗ Command failed with exit code {process.returncode}\n")
                
            except Exception as e:
                output_widget.insert(tk.END, f"\n[ERROR] {str(e)}\n")
            finally:
                # Re-enable buttons
                self.write_button.config(state=tk.NORMAL)
                self.read_button.config(state=tk.NORMAL)
        
        # Disable buttons during execution
        self.write_button.config(state=tk.DISABLED)
        self.read_button.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
    
    def write_tag(self):
        """Write tag using pm3write command"""
        if not self.pm3_available:
            messagebox.showerror("Error", "Proxmark3 not detected!\n\nPlease ensure Proxmark3 is connected and 'pm3' command is available.")
            return
        
        # Clear output
        self.write_output.delete(1.0, tk.END)
        
        # Build command
        args = ['pm3write']
        
        # Material
        material_name = self.material_var.get()
        material_code = self.materials.get(material_name)
        if material_code:
            args.extend(['--material', material_code])
        
        # Color
        args.extend(['--color', self.color_var.get()])
        
        # Weight
        if self.weight_var.get() == '1.0 kg':
            args.extend(['--length', '0330'])
        else:
            args.extend(['--length', '0165'])
        
        # Serial
        args.extend(['--serial', self.serial_var.get()])
        
        # Advanced
        args.extend(['--batch', self.batch_var.get()])
        args.extend(['--date', self.date_var.get()])
        args.extend(['--supplier', self.supplier_var.get()])
        
        # Encrypted
        if self.encrypted_var.get():
            args.append('--encrypted')
        
        # Manual UID
        if self.manual_uid_var.get() and self.uid_var.get():
            args.extend(['--skip-read', '--uid', self.uid_var.get()])
        
        # Run command
        self.run_command(args, self.write_output)
    
    def read_tag(self):
        """Read tag using pm3read command"""
        if not self.pm3_available:
            messagebox.showerror("Error", "Proxmark3 not detected!\n\nPlease ensure Proxmark3 is connected and 'pm3' command is available.")
            return
        
        # Clear output
        self.read_output.delete(1.0, tk.END)
        
        # Build command
        args = ['pm3read']
        
        # Manual UID
        if self.read_manual_uid_var.get() and self.read_uid_var.get():
            args.extend(['--uid', self.read_uid_var.get()])
        
        # Run command
        self.run_command(args, self.read_output)
    
    def show_reference(self, flag):
        """Show reference tables"""
        if not self.script_path:
            self.ref_output.insert(tk.END, "[ERROR] Script not found!\n")
            return
        
        self.ref_output.delete(1.0, tk.END)
        
        try:
            result = subprocess.run(
                ['python3', self.script_path, 'list', flag],
                capture_output=True,
                text=True,
                timeout=10
            )
            self.ref_output.insert(tk.END, result.stdout)
        except Exception as e:
            self.ref_output.insert(tk.END, f"[ERROR] {str(e)}\n")
    
    def generate_key(self):
        """Generate key from UID"""
        if not self.script_path:
            self.manual_output.insert(tk.END, "[ERROR] Script not found!\n")
            return
        
        uid = self.manual_uid_input.get()
        if not uid:
            messagebox.showwarning("Warning", "Please enter a UID")
            return
        
        self.manual_output.delete(1.0, tk.END)
        
        try:
            result = subprocess.run(
                ['python3', self.script_path, 'genkey', uid],
                capture_output=True,
                text=True,
                timeout=10
            )
            self.manual_output.insert(tk.END, result.stdout)
        except Exception as e:
            self.manual_output.insert(tk.END, f"[ERROR] {str(e)}\n")
    
    def generate_write_commands(self):
        """Generate write commands"""
        if not self.script_path:
            self.manual_output.insert(tk.END, "[ERROR] Script not found!\n")
            return
        
        uid = self.manual_uid_input.get()
        if not uid:
            messagebox.showwarning("Warning", "Please enter a UID")
            return
        
        self.manual_output.delete(1.0, tk.END)
        
        # Build command with current settings from write tab
        args = ['write', '-u', uid]
        
        material_name = self.material_var.get()
        material_code = self.materials.get(material_name)
        if material_code:
            args.extend(['--material', material_code])
        
        args.extend(['--color', self.color_var.get()])
        
        if self.weight_var.get() == '1.0 kg':
            args.extend(['--length', '0330'])
        else:
            args.extend(['--length', '0165'])
        
        args.extend(['--serial', self.serial_var.get()])
        args.extend(['--batch', self.batch_var.get()])
        args.extend(['--date', self.date_var.get()])
        args.extend(['--supplier', self.supplier_var.get()])
        
        if self.encrypted_var.get():
            args.append('--encrypted')
        
        try:
            result = subprocess.run(
                ['python3', self.script_path] + args,
                capture_output=True,
                text=True,
                timeout=10
            )
            self.manual_output.insert(tk.END, result.stdout)
        except Exception as e:
            self.manual_output.insert(tk.END, f"[ERROR] {str(e)}\n")
    
    def copy_to_clipboard(self):
        """Copy manual output to clipboard"""
        content = self.manual_output.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Success", "Commands copied to clipboard!")

def main():
    root = tk.Tk()
    app = CrealityRFIDGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
