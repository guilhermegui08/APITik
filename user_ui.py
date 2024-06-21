import api_requests
import tkinter as tk
import base64
import os.path
import csv
from tkinter import messagebox
import ssh2.session
import socket
from tkinter import scrolledtext
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os


def string_para_base64(string):
    string = string.encode('utf-8')
    escrita = base64.b64encode(string)
    return escrita.decode('utf-8')

def base64_para_string(string):
    string = string.encode('utf-8')
    escrita = base64.b64decode(string)
    return escrita.decode('utf-8')

def save_credentials(ip_address_var, username_var, password_var, listbox):
    ip_address = ip_address_var.get()
    username = username_var.get()
    password = password_var.get()
    password = string_para_base64(password)
    # Open the CSV file in append mode with newline=''
    if not os.path.exists("credentials.csv"):
        # If the file doesn't exist, create it and save the new credentials
        with open("credentials.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([ip_address, username, password])
        #print("Credentials saved successfully!")
        return
    
    # Check if the credentials already exist
    with open("credentials.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == ip_address and row[1] == username:
                # If credentials already exist, update the password
                updated_credentials = []
                with open("credentials.csv", "r") as f:
                    reader = csv.reader(f)
                    for r in reader:
                        if r[0] == ip_address and r[1] == username:
                            r[2] = password  # Update password
                        updated_credentials.append(r)
                with open("credentials.csv", "w", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(updated_credentials)
                #print("Password updated successfully!")
                return
        
    # If credentials don't exist, append them to the file
    with open("credentials.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ip_address, username, password])
    #print("Credentials saved successfully!")
    
    load_credentials(ip_address, username, listbox)

def load_credentials(ip_address_var, username_var, listbox):
    # Clear the existing items in the listbox
    listbox.delete(0, tk.END)
    
    # Check if credentials file exists
    if not os.path.exists("credentials.csv"):
        return  # Exit if the file doesn't exist
    
    # Open the CSV file for reading
    with open("credentials.csv", "r") as file:
        reader = csv.reader(file)
        # Iterate over each row in the CSV file
        for row in reader:
            ip_address_var, username_var, _ = row  # Password is not used for listbox
            listbox.insert(tk.END, f"IP= {ip_address_var}, Username= {username_var}")

def login(ip_address_var, username_var, password_var, root, listbox):
    credentials = f"{username_var.get()}:{password_var.get()}"
    authorization = string_para_base64(credentials)
    estado_pedido = api_requests.get_api(ip_address_var, authorization)
    if estado_pedido == 200:
        save_credentials(ip_address_var, username_var, password_var, listbox)
        cria_user_app(ip_address_var, username_var, authorization, password_var, root)

def cria_user_app(ip_address_var_temp,username_var_temp, authorization_temp, password_var_temp,root):
    #Função que vai buscar as estatisticas do router de 1 em 1 sgundo
    def update_labels():
        api_requests.get_system_data_periodically(ip_address_var, authorization, labels)
        
        build_time_label.config(text=f"Hora Atual: {labels[0]}")
        free_hdd_space_label.config(text=f"Disco Livre: {'{:.2f}'.format(int(labels[1]) * 0.000001) } MB")
        free_memory_label.config(text=f"Memoria Livre: {'{:.2f}'.format(int(labels[2]) * 0.000001) } MB")
        total_hdd_space_label.config(text=f"Total Disco: {'{:.2f}'.format(int(labels[3]) * 0.000001)} MB")
        total_memory_label.config(text=f"Total Memoria: {'{:.2f}'.format(int(labels[4]) * 0.000001)} MB")
        uptime_label.config(text=f"Tempo Ligado: {labels[5]}")
    
        user_window.after(1000,update_labels)

    #Criação da janela para interagir com o dispositivo
    user_window = tk.Toplevel(root)
    user_window.title(f"User: {username_var_temp.get()} - IP Address: {ip_address_var_temp.get()}")
    user_window.geometry("1280x960")

    
    ip_address_var = tk.StringVar(user_window)
    username_var = tk.StringVar(user_window)
    authorization_var = tk.StringVar(user_window)
    password_var = tk.StringVar(user_window)
    ip_address_var.set(f"{ip_address_var_temp.get()}")
    username_var.set(f"{username_var_temp.get()}")
    authorization_var.set(f"{authorization_temp}")
    authorization = authorization_var.get()
    password_var.set(f"{password_var_temp.get()}")

    #Create a frame for for labels
    labels = []
    api_requests.get_system_data_periodically(ip_address_var, authorization, labels)
    top_frame = tk.Frame(user_window, bg="light gray")
    top_frame.pack(side=tk.TOP, fill=tk.X)
    labels_frame = tk.Frame(top_frame, bg="light gray")
    labels_frame.pack(side=tk.RIGHT)
    build_time_label = tk.Label(labels_frame, text=f"Hora Atual: {labels[0]}", bg="light gray")
    build_time_label.grid(row=0, column=0, padx=5, pady=1, sticky=tk.E)
    free_hdd_space_label = tk.Label(labels_frame, text=f"Disco Livre: {labels[1]}", bg="light gray")
    free_hdd_space_label.grid(row=0, column=1, padx=5, pady=1, sticky=tk.E)
    free_memory_label = tk.Label(labels_frame, text=f"Memoria Livre: {labels[2]}", bg="light gray")
    free_memory_label.grid(row=0, column=2, padx=5, pady=1, sticky=tk.E)
    total_hdd_space_label = tk.Label(labels_frame, text=f"Total Disco: {labels[3]}", bg="light gray")
    total_hdd_space_label.grid(row=0, column=3, padx=5, pady=1, sticky=tk.E)
    total_memory_label = tk.Label(labels_frame, text=f"Total Memoria: {labels[4]}", bg="light gray")
    total_memory_label.grid(row=0, column=4, padx=5, pady=1, sticky=tk.E)
    uptime_label = tk.Label(labels_frame, text=f"Tempo Ligado: {labels[5]}", bg="light gray")
    uptime_label.grid(row=0, column=5, padx=5, pady=1, sticky=tk.E)
    
    # Create a frame for buttons
    left_frame = tk.Frame(user_window, width=200, bg="light gray")
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    button1 = tk.Button(left_frame, text="Listar Interfaces", command=lambda: api_requests.get_all_interfaces(ip_address_var, authorization, listbox, tk, user_window, old_buttons, new_buttons, labels_frame))
    button1.pack(fill=tk.X, padx=2, pady=1)
    button2 = tk.Button(left_frame, text="Listar Interfaces Wireless", command=lambda: api_requests.get_interfaces_wireless(ip_address_var, authorization, listbox, tk, user_window, old_buttons, labels_frame, new_buttons))
    button2.pack(fill=tk.X, padx=2, pady=1)
    button3 = tk.Button(left_frame, text="Listar Interfaces Bridge", command=lambda: api_requests.get_interfaces_bridge(ip_address_var, authorization, listbox, tk, user_window, labels_frame,  new_buttons, old_buttons))
    button3.pack(fill=tk.X, padx=2, pady=1)
    button13 = tk.Button(left_frame, text="Listar Portos Bridge", command=lambda: api_requests.get_portos_bridge(ip_address_var, authorization, listbox, tk, user_window, labels_frame,  new_buttons, old_buttons))
    button13.pack(fill=tk.X, padx=2, pady=1)
    button4 = tk.Button(left_frame, text="Listar Rotas", command=lambda: api_requests.get_rotas_estaticas(ip_address_var, authorization, listbox, tk, user_window, labels_frame,  new_buttons, old_buttons))
    button4.pack(fill=tk.X, padx=2, pady=1)
    button5 = tk.Button(left_frame, text="Listar endereços IP", command=lambda: api_requests.get_enderecos_ip(ip_address_var, authorization, listbox, tk, user_window, labels_frame,  new_buttons, old_buttons))
    button5.pack(fill=tk.X, padx=2, pady=1)
    button6 = tk.Button(left_frame, text="Listar Perfis de Segurança", command=lambda: api_requests.get_perfis_seguranca(ip_address_var, authorization, listbox, tk, user_window, labels_frame,  new_buttons, old_buttons))
    button6.pack(fill=tk.X, padx=2, pady=1)
    button7 = tk.Button(left_frame, text="Listar Redes Wireless", command=lambda: api_requests.get_redes_wireless(ip_address_var, authorization, listbox, tk, user_window, labels_frame,  new_buttons, old_buttons))
    button7.pack(fill=tk.X, padx=2, pady=1)
    button8= tk.Button(left_frame, text="Listar servidores de DHCP", command=lambda: api_requests.get_servidores_DHCP(ip_address_var, authorization, listbox, tk, user_window, labels_frame,  new_buttons, old_buttons))
    button8.pack(fill=tk.X, padx=2, pady=1)
    button9 = tk.Button(left_frame, text="Listar DNS", command=lambda: api_requests.get_entradas_DNS(ip_address_var, authorization, listbox, tk, user_window, labels_frame,  new_buttons, old_buttons))
    button9.pack(fill=tk.X, padx=2, pady=1)
    button14 = tk.Button(left_frame, text="Desligar", command=lambda: api_requests.desligar(ip_address_var,authorization,user_window,root))
    button14.pack(fill=tk.X, padx=2, pady=1, side=tk.BOTTOM)
    button15 = tk.Button(left_frame, text="Reiniciar", command=lambda: api_requests.reiniciar(ip_address_var,authorization,user_window,root))
    button15.pack(fill=tk.X, padx=2, pady=1, side=tk.BOTTOM)
    button12 = tk.Button(left_frame, text="Interface Web", command=lambda: open_webpage())
    button12.pack(fill=tk.X, padx=2, pady=1, side=tk.BOTTOM)
    button11 = tk.Button(left_frame, text="Terminal", command=lambda: cria_terminal_ssh())
    button11.pack(fill=tk.X, padx=2, pady=1, side=tk.BOTTOM)
    button10 = tk.Button(left_frame, text="Wireguard", command=lambda: api_requests.cria_wireguard(ip_address_var, authorization, tk, user_window))
    button10.pack(fill=tk.X, padx=2, pady=1, side=tk.BOTTOM)

    def open_webpage():
        username = username_var.get()
        password = password_var.get()
        ip_address = ip_address_var.get()
        #webbrowser.open(f"https://{ip_address_var.get()}")
        
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

        # Open the RouterOS login page
        url = f"http://{ip_address}/"
        driver.get(url)

        # Wait for the page to load
        time.sleep(2)

        # Find the username and password fields and submit button
        username_field = driver.find_element(By.ID, "name")
        password_field = driver.find_element(By.ID, "password")
        submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")

        # Enter username and password
        username_field.clear()
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Submit the form
        submit_button.click()

        # Wait for user input before closing the browser
        input("Press Enter to close the browser...")
        driver.quit()

    def cria_terminal_ssh():
        ssh_window = tk.Toplevel(user_window)
        ssh_window.title(f"Terminal: {username_var.get()}@{ip_address_var.get()}")
        ssh_window.geometry("800x600")
        parent = ssh_window
        
        last_command = tk.StringVar()
        last_command.set("")

        def carrega_comando(event=None):
            command_entry.insert(tk.END, last_command.get())

        def execute_ssh_command(event=None):
            last_command.set(command_entry.get())
            if command_entry.get() == 'clear':
                output_entry.delete("1.0", tk.END)
                command_entry.delete(0, tk.END)
                return

            ssh_host = ip_address_var.get()
            ssh_port = 22
            ssh_username = username_var.get()
            ssh_password = password_var.get()

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ssh_host, ssh_port))
            session = ssh2.session.Session()

            try:
                session.handshake(sock)
                session.userauth_password(username=ssh_username, password=ssh_password)
                channel = session.open_session()
                channel.execute(command_entry.get())
                size, data = channel.read()
                prestring = f"[{ssh_username}@{ssh_host}] > {command_entry.get()}:\n"
                #output_entry.delete("1.0", tk.END)  # Clear previous output
                output_entry.insert(tk.END, prestring + data.decode() + "\n")
                command_entry.delete(0, tk.END)

            finally:
                if 'channel' in locals():
                    channel.close()
                session.disconnect()
                sock.close()

        ssh_window.configure(bg="#eeeeec")  # Set background color to Tango White-like color
        ssh_window.bind("<Return>", execute_ssh_command)
        ssh_window.bind("<KeyRelease-Up>", carrega_comando)

        upper_frame = tk.Frame(ssh_window, bg="#eeeeec")  # Use Tango White-like color
        upper_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        lower_frame = tk.Frame(ssh_window, bg="#eeeeec")  # Use Tango White-like color
        lower_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        lef_lower_frame = tk.Frame(lower_frame, bg="#eeeeec")  # Use Tango White-like color
        lef_lower_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        right_lower_frame = tk.Frame(lower_frame, bg="#eeeeec")  # Use Tango White-like color
        right_lower_frame.pack(side=tk.RIGHT, anchor='s')

        label_font = ("Consolas", 16)

        output_label = tk.Label(upper_frame, text="Terminal OUTPUT:", bg="#eeeeec", font=label_font)  # Use Tango White-like color
        output_label.pack(side=tk.TOP, padx=5, pady=5, anchor='w')

        output_entry = scrolledtext.ScrolledText(upper_frame, height=4, width=30, font=label_font, fg="#336699")
        output_entry.pack(side=tk.BOTTOM, padx=5, pady=5, anchor='w', expand=True, fill=tk.BOTH)

        command_label = tk.Label(lef_lower_frame, bg="#eeeeec", text="Command Prompt:", font=label_font)  # Use Tango White-like color
        command_label.pack(side=tk.TOP, padx=5, pady=5, anchor='w')

        command_entry = tk.Entry(lef_lower_frame, font=label_font)  # Use Tango White-like color
        command_entry.pack(side=tk.BOTTOM, padx=5, pady=5, anchor='w', expand=True)

        enviar_button = tk.Button(right_lower_frame, text="Enviar comando", command=execute_ssh_command, font=label_font)  # Use Tango White-like color
        enviar_button.pack(side=tk.BOTTOM, padx=5, pady=5, anchor='s')

    # Create a frame for the listbox and the texbox and button
    old_buttons = [] 
    right_frame = tk.Frame(user_window)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    listbox = tk.Listbox(right_frame, font=("Arial", 12))
    listbox.pack(expand=True, fill="both", side=tk.TOP)
    labels_frame = tk.Frame(right_frame)
    labels_frame.pack(fill=tk.X)
    button_frame = tk.Frame(right_frame)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)
    criar_button = tk.Button(button_frame, text="Criar")
    editar_button = tk.Button(button_frame, text="Editar")
    apagar_button = tk.Button(button_frame, text="Apagar")
    ativar_button = tk.Button(button_frame, text="Ativar")
    desativar_button = tk.Button(button_frame, text="Desativar")
    configurar_button = tk.Button(button_frame, text="Configurar")
    new_buttons = [criar_button, editar_button, apagar_button, ativar_button, desativar_button, configurar_button]
    
    update_labels()

def cria_app():
    def on_double_click(event):
        # Get the selected item in the listbox
        index = lista.curselection()
        if index :
            item = lista.get(index)
            # Extract IP address and username from the selected item
            ip_address = item.split(",")[0].split("= ")[1].strip()
            username = item.split(",")[1].split("= ")[1].strip()
            # Retrieve password from the CSV file based on IP address and username
            with open("credentials.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == ip_address and row[1] == username:
                        password = row[2]
                        break
            # Update the entry fields with retrieved credentials
            ip_address_var.set(ip_address)
            username_var.set(username)
            password_var.set(base64_para_string(password))
    # Create the main application window
    root = tk.Tk()
    root.title("APITIK") # Define o Titulo do GUI

    # Set fixed window size # Define custom colors # Set background color
    root.geometry("1280x720")
    bg_color = "#F2F2F2"  # Light gray
    text_color = "#333333"  # Dark gray ### ELEMINAR ? 
    button_color = "#4CAF50"  # Green ### ELEMINAR ? 
    root.configure(bg=bg_color)

    #Criar um Frame na esquerda para as Credenciais 
    frame_esquerda = tk.Frame(root, bg="light gray")
    frame_esquerda.pack(side=tk.LEFT, fill=tk.Y)

    #Criar um Frame na direita para apresentar Credenciais já existentes
    frame_direita = tk.Frame(root, bg=bg_color)
    frame_direita.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    #Cria ListBox para colocar os dados das credenciais
    lista = tk.Listbox(frame_direita, font=("Arial", 16))
    lista.pack(expand=True, fill="both")
    lista.bind("<Double-Button-1>", on_double_click)  # Bind double-click event

    # Create ip address label and entry 
    ip_address_label = tk.Label(frame_esquerda, text="IP Address:", bg="light gray")
    ip_address_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    ip_address_var = tk.StringVar()
    ip_address_entry = tk.Entry(frame_esquerda, textvariable=ip_address_var)
    ip_address_entry.grid(row=0, column=1, padx=5, pady=5)

    # Create username label and entry
    username_label = tk.Label(frame_esquerda, text="Username:", bg="light gray")
    username_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    username_var = tk.StringVar()
    username_entry = tk.Entry(frame_esquerda, textvariable=username_var)
    username_entry.grid(row=1, column=1, padx=5, pady=5)

    # Create password label and entry
    password_label = tk.Label(frame_esquerda, text="Password:", bg="light gray")
    password_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    password_var = tk.StringVar()
    password_entry = tk.Entry(frame_esquerda, show="*", textvariable=password_var)
    password_entry.grid(row=2, column=1, padx=5, pady=5)

    # Create button to show values
    confirm_button = tk.Button(frame_esquerda, text="Confirmar", command=lambda: login(ip_address_var, username_var, password_var, root, lista))
    confirm_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky=tk.W)

    load_credentials(ip_address_var.get(), username_var.get(), lista)

    root.mainloop()
    return ip_address_var, username_var, password_var, root
