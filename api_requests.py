import requests
from tkinter import messagebox
from tkinter import ttk
import ipaddress
import random

def show_in_list(list, listbox, tk):
    listbox.delete(0, tk.END)
    for item in list:
        listbox.insert(tk.END, f"{item}")

def get_api(ip_address_var, authorization):
    try:
        url = f"http://{ip_address_var.get()}/rest/system/resource?.proplist=''"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        messagebox.showinfo("Message", "Cliente autenticado com Sucesso!")
        return response.status_code
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}")
        return response.status_code


def get_all_interfaces(ip_address_var, authorization, listbox, tk, parent, old_buttons, new_buttons, labels_frame):
    for button in old_buttons:
        button.grid_forget()
        del button

    bridge_label = tk.Label(labels_frame, text="", height=0)
    bridge_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(bridge_label)
    
    new_buttons[3].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[3].config(command=lambda: ativar_interface(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[3])
    new_buttons[4].grid(row=0, column=2, padx=2, pady=2, sticky=tk.SW)
    new_buttons[4].config(command=lambda: desativar_interface(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[4])

    def on_double_click(event):
        # Get the selected item in the listbox
        index = listbox.curselection()
        if index :
            item = listbox.get(index)
            item = item.strip()
            try:
                id_value = item.split("ID:")[1].split(";")[0].strip()
                url = f"http://{ip_address_var.get()}/rest/interface/{id_value}"
                headers = {'Authorization': 'Basic '+ authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                interface_data = response.json()
                string_text_box = ""
                for data in interface_data:
                    string_text_box += f"{data} : {interface_data[data]} \n"
                messagebox.showinfo(f"{item}", string_text_box, parent=parent )
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}")

    try:
        url = f"http://{ip_address_var.get()}/rest/interface"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        interfaces = response.json()
        interface_names = []
        for interface in interfaces:
            interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Tipo: {interface['type']}; Desativada: {interface['disabled']}")
        show_in_list(interface_names, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}")

def ativar_interface(ip_address_var_temp, authorization, listbox, tk, parent):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhuma interface!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var_temp.get()}/rest/interface/set"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {
                ".id": id_value,
                "disabled": False
            }
            response = requests.post(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Interface ativada", "Interface ativada com sucesso", parent=parent )
            url = f"http://{ip_address_var_temp.get()}/rest/interface"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            for interface in interfaces:
                interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Tipo: {interface['type']}; Desativada: {interface['disabled']}")
            show_in_list(interface_names, listbox, tk)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def desativar_interface(ip_address_var_temp, authorization, listbox, tk, parent):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhuma interface!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var_temp.get()}/rest/interface/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {
                #".id": id_value,
                "disabled": True
            }
            response = requests.put(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Interface desativada", "Interface desativada com sucesso", parent=parent )
            url = f"http://{ip_address_var_temp.get()}/rest/interface"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            for interface in interfaces:
                interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Tipo: {interface['type']}; Desativada: {interface['disabled']}")
            show_in_list(interface_names, listbox, tk)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def get_interfaces_wireless(ip_address_var, authorization, listbox, tk, parent, old_buttons, labels_frame, new_buttons):
    for button in old_buttons:
        button.grid_forget()
        del button

    bridge_label = tk.Label(labels_frame, text="", height=0)
    bridge_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(bridge_label)

    new_buttons[3].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[3].config(command=lambda: ativar_interface_wireless(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[3])
    new_buttons[4].grid(row=0, column=2, padx=2, pady=2, sticky=tk.SW)
    new_buttons[4].config(command=lambda: desativar_interface_wireless(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[4])

    def on_double_click(event):
        # Get the selected item in the listbox
        index = listbox.curselection()
        if index :
            item = listbox.get(index)
            item = item.strip()
            try:
                id_value = item.split("ID:")[1].split(";")[0].strip()
                url = f"http://{ip_address_var.get()}/rest/interface/{id_value}"
                headers = {'Authorization': 'Basic '+ authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                interface_data = response.json()
                string_text_box = ""
                for data in interface_data:
                    string_text_box += f"{data} : {interface_data[data]} \n"
                messagebox.showinfo(f"{item}", string_text_box, parent=parent )
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    try:
        url = f"http://{ip_address_var.get()}/rest/interface/wireless"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        interfaces = response.json()
        interface_names = []
        for interface in interfaces:
            interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Mac-Address: {interface['mac-address']}; Desativada: {interface['disabled']}")
        show_in_list(interface_names, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def ativar_interface_wireless(ip_address_var_temp, authorization, listbox, tk, parent):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhuma interface Wireless!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var_temp.get()}/rest/interface/wireless/set"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {
                ".id": id_value,
                "disabled": False
            }
            response = requests.post(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Interface ativada", "Interface ativada com sucesso", parent=parent )
            url = f"http://{ip_address_var_temp.get()}/rest/interface/wireless"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            for interface in interfaces:
                interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Mac-Address: {interface['mac-address']}; Desativada: {interface['disabled']}")
            show_in_list(interface_names, listbox, tk)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def desativar_interface_wireless(ip_address_var_temp, authorization, listbox, tk, parent):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhuma interface Wireless!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var_temp.get()}/rest/interface/wireless/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {
                #".id": id_value,
                "disabled": True
            }
            response = requests.put(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Interface desativada", "Interface desativada com sucesso", parent=parent )
            url = f"http://{ip_address_var_temp.get()}/rest/interface/wireless"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            for interface in interfaces:
                interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Mac-Address: {interface['mac-address']}; Desativada: {interface['disabled']}")
            show_in_list(interface_names, listbox, tk)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def get_interfaces_bridge(ip_address_var, authorization, listbox, tk, parent, labels_frame, new_buttons, old_buttons):
    for button in old_buttons:
        button.grid_forget()
        del button
    
    name_label = tk.Label(labels_frame, text="Nome:*")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(name_label)
    name_entry = tk.Entry(labels_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    old_buttons.append(name_entry)
    desativar_value = tk.BooleanVar()
    desativar_button = tk.Checkbutton(labels_frame, text="Interface desativada", variable=desativar_value)
    desativar_button.grid(row=1, column=0, padx=5, pady=5)
    old_buttons.append(desativar_button)
    comment_label = tk.Label(labels_frame, text="Comentário:")
    comment_label.grid(row=0, column=2, padx=5, pady=5)
    old_buttons.append(comment_label)
    comment_entry = tk.Entry(labels_frame)
    comment_entry.grid(row=0, column=3, padx=5, pady=5)
    old_buttons.append(comment_entry)

    new_buttons[0].grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    new_buttons[0].config(command=lambda: criar_interfaces_bridge(ip_address_var, authorization, listbox, name_entry, tk, parent,desativar_value,desativar_button,comment_entry))
    old_buttons.append(new_buttons[0])
    new_buttons[1].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[1].config(command=lambda: editar_interfaces_bridge(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[1])
    new_buttons[2].grid(row=0, column=2, padx=2, pady=2, sticky=tk.SW)
    new_buttons[2].config(command=lambda: eliminar_interfaces_bridge(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[2])

    def on_double_click(event):
        # Get the selected item in the listbox
        index = listbox.curselection()
        if index :
            item = listbox.get(index)
            item = item.strip()
            try:
                id_value = item.split("ID:")[1].split(";")[0].strip()
                url = f"http://{ip_address_var.get()}/rest/interface/bridge/{id_value}"
                headers = {'Authorization': 'Basic '+ authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                interface_data = response.json()
                string_text_box = ""        
                for data in interface_data:
                    string_text_box += f"{data} : {interface_data[data]} \n" 
                messagebox.showinfo(f"{item}", string_text_box, parent=parent )
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    try:
        url = f"http://{ip_address_var.get()}/rest/interface/bridge"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        interfaces = response.json()
        interface_names = []
        for interface in interfaces:
            interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Mac-Address{interface['mac-address']}; Desativada: {interface['disabled']}")
        show_in_list(interface_names, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def criar_interfaces_bridge(ip_address_var, authorization, listbox, name_entry, tk, parent, desativar_value,desativar_button,comment_entry):
    text = name_entry.get().replace(" ", "")
    if not text:
        messagebox.showerror("Erro","Não foi dado nenhum nome, a caixa de texto encontra-se vazia!", parent=parent)
        return
    

    comment_entry_valor = comment_entry.get().strip()

    desativado = False
    if desativar_value.get():
        desativado = True

    try:
        url = f"http://{ip_address_var.get()}/rest/interface/bridge/add"
        headers = {'Authorization': 'Basic '+ authorization}
        payload = {
            'name' : text,
            'disabled': desativado,
        }
        if comment_entry_valor:
            payload['comment'] = comment_entry_valor
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        if response.status_code == 200:
            messagebox.showinfo(text,f"Interface criada com sucesso!", parent=parent)
            name_entry.delete(0, tk.END)
            desativar_button.deselect()
            comment_entry.delete(0,tk.END)
            url = f"http://{ip_address_var.get()}/rest/interface/bridge"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            for interface in interfaces:
                interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Mac-Address{interface['mac-address']}; Desativada: {interface['disabled']}")
            show_in_list(interface_names, listbox, tk)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def editar_interfaces_bridge(ip_address_var_temp, authorization, listbox, tk, parent):
    def update_bridge(disabled, interface_names, ports_ids):
        try:
            url = f"http://{ip_address_var.get()}/rest/interface/bridge/set"
            headers = {'Authorization': 'Basic '+ authorization}
            if disabled == 'false' and ativar_value.get() == True:
                disabled = True
            if disabled == 'true' and ativar_value.get() == True:
                disabled = False
            payload = {
                ".id": bridge_id, 
                "name": name_entry.get().replace(" ", ""),
                "disabled": disabled,
            }
            if comentario_entry.get("1.0", "end-1c").replace(" ", ""):
                payload['comment'] =  comentario_entry.get("1.0", "end-1c")
            response = requests.post(url, headers=headers, json=payload, verify=False)
            response.raise_for_status()
            response = response.json()

            url = f"http://{ip_address_var.get()}/rest/interface/bridge/port/add"
            count = 0
            for interface in adicionar_interfaces:
                if interface.get():
                    payload = {
                        "interface": interface_names[count],
                        "bridge": name_entry.get().replace(" ", ""),
                    }
                    response = requests.post(url, headers=headers, json=payload, verify=False)
                    response.raise_for_status()
                count += 1
            
            url = f"http://{ip_address_var.get()}/rest/interface/bridge/port/remove"
            count = 0
            for interface in remover_interfaces:
                if interface.get():
                    payload = {
                        ".id": ports_ids[count]
                    }
                    response = requests.post(url, headers=headers, json=payload, verify=False)
                    response.raise_for_status()
                count += 1

            messagebox.showinfo("Sucesso", "Interface bridge atualizada com sucesso!", parent=parent)
            url = f"http://{ip_address_var.get()}/rest/interface/bridge"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            for interface in interfaces:
                interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Mac-Address{interface['mac-address']}; Desativada: {interface['disabled']}")
            show_in_list(interface_names, listbox, tk)
            close()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
    
    def close():
        bridge_window.destroy()

    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhuma Interface Bridge!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()

        bridge_window = tk.Toplevel(parent)
        bridge_window.title(f"{item.title()}")
        bridge_window.geometry("640x480")
        parent = bridge_window
        ip_address_var = tk.StringVar(bridge_window)
        authorization_var = tk.StringVar(bridge_window)
        ip_address_var.set(f"{ip_address_var_temp.get()}")
        authorization_var.set(f"{authorization}")
        authorization = authorization_var.get()

        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var.get()}/rest/interface/bridge/{id_value}"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interface_data = response.json()
            print(interface_data)
            name = interface_data['name']
            bridge_id = interface_data['.id'] 
            disabled = interface_data['disabled']
            comentario_valor = ""
            if 'comment' in interface_data:
                comentario_valor = interface_data['comment']
            url = f"http://{ip_address_var.get()}/rest/interface"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            encontrou = 0
            for interface in interfaces:
                for key in interface:
                    if key == 'slave':
                        encontrou = 1
                if encontrou == 0 and interface['type'] != 'bridge' and interface['type'] != 'loopback' and interface['type'] != 'wg': 
                    interface_names.append(interface['name'])
                encontrou = 0
            print(name)
            url = f"http://{ip_address_var.get()}/rest/interface/bridge/port"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            bridge_ports_data = response.json()
            bridge_specific_ports = [port for port in bridge_ports_data if port['bridge'] == name]
            ports_names = []
            ports_ids = []
            for interface in bridge_specific_ports:
                ports_names.append(interface['interface'])
                ports_ids.append(interface['.id'])
        except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
        
        for item in interface_names:
            if item in ports_names:
                interface_names.remove(item)

        entry_frame = tk.Frame(bridge_window)
        entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        name_label = tk.Label(entry_frame, text="Nome:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(entry_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(tk.END, name)
        comentario_label = tk.Label(entry_frame, text="Comentário:")
        comentario_label.grid(row=0, column=3, padx=5, pady=5, sticky=tk.N)
        comentario_entry = tk.Text(entry_frame, height=4, width=30)
        comentario_entry.grid(row=0, column=5, padx=5, pady=5)
        comentario_entry.insert(tk.END, comentario_valor)
        ativar_value = tk.BooleanVar()
        if disabled == 'true':
            ativar_button = tk.Checkbutton(entry_frame, text="Ativar", variable=ativar_value)
            ativar_button.grid(row=1, column=0, padx=5, pady=5)
        else:
            ativar_button = tk.Checkbutton(entry_frame, text="Desativar", variable=ativar_value)
            ativar_button.grid(row=1, column=0, padx=5, pady=5)

        remover_label = tk.Label(entry_frame, text="Remover interfaces:")
        remover_label.grid(row=2, column=0, padx=5, pady=5)
        remover_interfaces = []
        for i in range(0,len(ports_names)):
            remover_interfaces.append(tk.BooleanVar())
        pos = 0
        for item in ports_names:
            tk.Checkbutton(entry_frame, text=item, variable=remover_interfaces[pos]).grid(row=pos+3, column=0, padx=5, pady=5)
            pos += 1

        adicionar_label = tk.Label(entry_frame, text="Adicionar interfaces:")
        adicionar_label.grid(row=2, column=1, padx=5, pady=5)
        adicionar_interfaces = []
        for i in range(0,len(interface_names)):
             adicionar_interfaces.append(tk.BooleanVar())
        pos = 0
        for item in interface_names:
            tk.Checkbutton(entry_frame, text=item, variable=adicionar_interfaces[pos]).grid(row=pos+3, column=1, padx=5, pady=5)
            pos += 1

        button_frame = tk.Frame(bridge_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        right_button_frame = tk.Frame(button_frame)
        right_button_frame.pack(side=tk.RIGHT)
        ok_button = tk.Button(right_button_frame, text="Ok", command=lambda: update_bridge(disabled, interface_names, ports_ids))
        ok_button.grid(row=0, column=0, padx=2, pady=2)
        close_button = tk.Button(right_button_frame, text="Fechar", command=close)
        close_button.grid(row=0, column=1, padx=2, pady=2)

def eliminar_interfaces_bridge(ip_address_var, authorization, listbox, tk, parent):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhuma interface Bridge!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        confirmacao = messagebox.askquestion(f"Eliminar interface bridge {item}",f'Tem a certeza que pretende eliminar a interface bridge "{item}" ?', parent=parent)
        if confirmacao == "no":
            return
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var.get()}/rest/interface/bridge/{id_value}"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interface_data = response.json()
            item = interface_data['name']
            url = f"http://{ip_address_var.get()}/rest/interface/bridge/port"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            bridge_ports_data = response.json()
            bridge_specific_ports = [port for port in bridge_ports_data if port['bridge'] == item]
            ports_names = []
            ports_ids = []
            for interface in bridge_specific_ports:
                ports_names.append(interface['interface'])
                ports_ids.append(interface['.id'])
            
            url = f"http://{ip_address_var.get()}/rest/interface/bridge/port/remove"
            count = 0
            for interface in ports_ids:
                payload = {
                    ".id": interface
                }
                response = requests.post(url, headers=headers, json=payload, verify=False)
                response.raise_for_status()
                count += 1
            
            url = f"http://{ip_address_var.get()}/rest/interface/{item}"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interface_data = response.json()
            interface_id = interface_data['.id']

            
            url = f"http://{ip_address_var.get()}/rest/interface/bridge/remove"
            headers = {'Authorization': 'Basic '+ authorization}
            params = {
                '.id' : interface_id
            }
            response = requests.post(url, headers=headers, json=params,verify=False)

            messagebox.showinfo("Sucesso", "Bridge interface deleted successfully", parent=parent)
            url = f"http://{ip_address_var.get()}/rest/interface/bridge"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            for interface in interfaces:
                interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Mac-Address{interface['mac-address']}; Desativada: {interface['disabled']}")
            show_in_list(interface_names, listbox, tk)
        except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def get_portos_bridge(ip_address_var, authorization, listbox, tk, parent, labels_frame, new_buttons, old_buttons):
    for button in old_buttons:
        button.grid_forget()
        del button
    
    def on_double_click(event):
        # Get the selected item in the listbox
        index = listbox.curselection()
        if index :
            item = listbox.get(index)
            item = item.strip()
            try:
                id_value = item.split("ID:")[1].split(";")[0].strip()
                url = f"http://{ip_address_var.get()}/rest/interface/bridge/port/{id_value}"
                headers = {'Authorization': 'Basic '+ authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                interface_data = response.json()
                string_text_box = ""        
                for data in interface_data:
                    string_text_box += f"{data} : {interface_data[data]} \n" 
                messagebox.showinfo(f"{item}", string_text_box, parent=parent )
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    try:
        url = f"http://{ip_address_var.get()}/rest/interface/bridge/port"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        interfaces = response.json()
        print(interfaces)
        interface_names = []
        for interface in interfaces:
            interface_names.append(f"ID: {interface['.id']}; Interface: {interface['interface']}; Bridge: {interface['bridge']}; Desativada: {interface['disabled']}")
        show_in_list(interface_names, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
        url = f"http://{ip_address_var.get()}/rest/interface/bridge"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        interfaces = response.json()
        bridge_names = []
        for interface in interfaces:
            bridge_names.append(interface['name'])
        url = f"http://{ip_address_var.get()}/rest/interface"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        interfaces = response.json()
        interface_names = []
        encontrou = 0
        for interface in interfaces:
            for key in interface:
                if key == 'slave':
                    encontrou = 1
            if encontrou == 0 and interface['type'] != 'bridge' and interface['type'] != 'loopback' and interface['type'] != 'wg':
                interface_names.append(interface['name'])
            encontrou = 0
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
    
    type_label = tk.Label(labels_frame, text="Interface:*")
    type_label.grid(row=0, column=0, padx=5, pady=5)
    options = interface_names
    selected_option = 0
    combobox = 0
    if len(interface_names) > 0:
        pre_filled_value = interface_names[0]
        selected_option = tk.StringVar()
        combobox = ttk.Combobox(labels_frame, textvariable=selected_option, values=options)
        try:
            pre_filled_index = options.index(pre_filled_value)
            combobox.current(pre_filled_index)
        except ValueError:
            pass
        combobox.grid(row=0, column=1, padx=5, pady=5)
    else:
        options = ["Não há interfaces disponíveis!"]
        pre_filled_value = options[0]
        selected_option = tk.StringVar()
        combobox = ttk.Combobox(labels_frame, textvariable=selected_option, values=options)
        try:
            pre_filled_index = options.index(pre_filled_value)
            combobox.current(pre_filled_index)
        except ValueError:
            pass
        combobox.grid(row=0, column=1, padx=5, pady=5)
    old_buttons.append(type_label)
    old_buttons.append(combobox)

    bridge_label = tk.Label(labels_frame, text="Bridge:*")
    bridge_label.grid(row=1, column=0, padx=5, pady=5)
    options2 = bridge_names
    selected_option2 = 0
    combobox2 = 0
    if len(bridge_names) > 0:
        pre_filled_value2 = bridge_names[0]
        selected_option2 = tk.StringVar()
        combobox2 = ttk.Combobox(labels_frame, textvariable=selected_option2, values=options2)
        try:
            pre_filled_index2 = options.index(pre_filled_value2)
            combobox.current(pre_filled_index2)
        except ValueError:
            pass
        combobox2.grid(row=1, column=1, padx=5, pady=5)
    else:
        options2 = ["Não há briges disponíveis!"]
        pre_filled_value2 = options[0]
        selected_option2 = tk.StringVar()
        combobox2 = ttk.Combobox(labels_frame, textvariable=selected_option2, values=options2)
        try:
            pre_filled_index2 = options.index(pre_filled_value2)
            combobox.current(pre_filled_index2)
        except ValueError:
            pass
        combobox2.grid(row=1, column=1, padx=5, pady=5)
    old_buttons.append(bridge_label)
    old_buttons.append(combobox2)

    comment_label = tk.Label(labels_frame, text="Comentário:")
    comment_label.grid(row=0, column=2, padx=5, pady=5)
    old_buttons.append(comment_label)
    comment_entry = tk.Entry(labels_frame)
    comment_entry.grid(row=0, column=3, padx=5, pady=5)
    old_buttons.append(comment_entry)

    desativar_value = tk.BooleanVar()
    desativar_button = tk.Checkbutton(labels_frame, text="Porto desativado", variable=desativar_value)
    desativar_button.grid(row=1, column=2, padx=5, pady=5)
    old_buttons.append(desativar_button)

    new_buttons[0].grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    new_buttons[0].config(command=lambda: criar_portos_bridge(ip_address_var, authorization, listbox, tk, parent, comment_entry, desativar_value, desativar_button, selected_option, selected_option2, labels_frame, combobox))
    old_buttons.append(new_buttons[0])
    new_buttons[1].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[1].config(command=lambda: editar_portos_bridge(ip_address_var, authorization, listbox, tk, parent, labels_frame, combobox, selected_option))
    old_buttons.append(new_buttons[1])
    new_buttons[2].grid(row=0, column=2, padx=2, pady=2, sticky=tk.SW)
    new_buttons[2].config(command=lambda: eliminar_porto_bridge(ip_address_var, authorization, listbox, tk, parent, combobox, labels_frame, selected_option))
    old_buttons.append(new_buttons[2])

def eliminar_porto_bridge(ip_address_var, authorization, listbox, tk, parent, combobox, labels_frame, selected_option):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhum Porto bridge!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            confirmacao = messagebox.askquestion(f"Eliminar Porto Bridge {id_value}?",f"Tem a certeza que pretende eliminar o Porto bridge {id_value} ?", parent=parent)
            if confirmacao == "no":
                return
            delete_url = f"http://{ip_address_var.get()}/rest/interface/bridge/port/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.delete(delete_url, headers=headers, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Porto Bridge Apagado", f"Porto Bridge {id_value} apagada com Sucesso", parent=parent)
            url = f"http://{ip_address_var.get()}/rest/interface/bridge/port"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            for interface in interfaces:
                interface_names.append(f"ID: {interface['.id']}; Interface: {interface['interface']}; Bridge: {interface['bridge']}; Desativada: {interface['disabled']}")
            show_in_list(interface_names, listbox, tk)
            url = f"http://{ip_address_var.get()}/rest/interface"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            encontrou = 0
            for interface in interfaces:
                for key in interface:
                    if key == 'slave':
                        encontrou = 1
                if encontrou == 0 and interface['type'] != 'bridge' and interface['type'] != 'loopback' and interface['type'] != 'wg':
                    interface_names.append(interface['name'])
                encontrou = 0
            options = interface_names
            if len(interface_names) > 0:
                pre_filled_value = interface_names[0]
                combobox['textvariable'] = selected_option
                combobox['values'] = options
                try:
                    pre_filled_index = options.index(pre_filled_value)
                    combobox.current(pre_filled_index)
                except ValueError:
                    pass
            combobox.grid(row=0, column=1, padx=5, pady=5)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def criar_portos_bridge(ip_address_var, authorization, listbox, tk, parent, comment_entry, desativar_value, desativar_button, selected_option, selected_option2, labels_frame, combobox):
    interface_value = selected_option.get()
    if interface_value == "Não há interfaces disponíveis!":
        messagebox.showerror("Erro","Não há interfaces disponíveis!", parent=parent)
        return
    bridge_value = selected_option2.get()
    if bridge_value == "Não há briges disponíveis!":
        messagebox.showerror("Erro","Não há bridges disponíveis!", parent=parent)
        return
    
    comment_valor = comment_entry.get()
    desativado = False
    if desativar_value.get():
        desativado = True

    try:
        dns_entry_data = {
            "interface": interface_value, 
            "disabled": desativado,
            "bridge" : bridge_value
        }
        if comment_valor:
            dns_entry_data['comment'] = comment_valor
        url = f"http://{ip_address_var.get()}/rest/interface/bridge/port/add"
        headers = {'Authorization': 'Basic ' + authorization}
        response = requests.post(url, headers=headers, json=dns_entry_data, verify=False)
        if response.status_code == 200:
            messagebox.showinfo("Porto bridge criado", "Porto bridge criado com sucesso", parent=parent )
        url = f"http://{ip_address_var.get()}/rest/interface/bridge/port"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        interfaces = response.json()
        interface_names = []
        for interface in interfaces:
            interface_names.append(f"ID: {interface['.id']}; Interface: {interface['interface']}; Bridge: {interface['bridge']}; Desativada: {interface['disabled']}")
        show_in_list(interface_names, listbox, tk)
        url = f"http://{ip_address_var.get()}/rest/interface"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        interfaces = response.json()
        interface_names = []
        encontrou = 0
        for interface in interfaces:
            for key in interface:
                if key == 'slave':
                    encontrou = 1
            if encontrou == 0 and interface['type'] != 'bridge' and interface['type'] != 'loopback' and interface['type'] != 'wg':
                interface_names.append(interface['name'])
            encontrou = 0
        options = interface_names
        if len(interface_names) > 0:
            pre_filled_value = interface_names[0]
            combobox['textvariable'] = selected_option
            combobox['values'] = options
            try:
                pre_filled_index = options.index(pre_filled_value)
                combobox.current(pre_filled_index)
            except ValueError:
                pass
            combobox.grid(row=0, column=1, padx=5, pady=5)
        else:
            options = ["Não há interfaces disponíveis!"]
            pre_filled_value = options[0]
            selected_option = tk.StringVar()
            combobox['textvariable'] = selected_option
            combobox['values'] = options
            try:
                pre_filled_index = options.index(pre_filled_value)
                combobox.current(pre_filled_index)
            except ValueError:
                pass
            combobox.grid(row=0, column=1, padx=5, pady=5)
        comment_entry.delete(0, tk.END)
        desativar_button.deselect()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def editar_portos_bridge(ip_address_var_temp, authorization, listbox, tk, parent, labels_frame, combobox1, selected_option1):
    def update_porto_bridge(id_value):
        try:
            interface_value = selected_option.get()
            bridge_value = selected_option2.get()
            url = f"http://{ip_address_var.get()}/rest/interface/bridge/port/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {
                "interface": interface_value,
                "bridge": bridge_value
            }
            if comentario_entry.get("1.0", "end-1c").replace(" ", ""):
                data['comment'] =  comentario_entry.get("1.0", "end-1c")
            if ativar_value.get() and disabled:
                data['disabled'] = False
            if ativar_value.get() and not disabled:
                data['disabled'] = True
            response = requests.put(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Porto Bridge atualizado!", "Porto Bridge atualizado com sucesso.", parent=parent )
            url = f"http://{ip_address_var.get()}/rest/interface/bridge/port"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            for interface in interfaces:
                interface_names.append(f"ID: {interface['.id']}; Interface: {interface['interface']}; Bridge: {interface['bridge']}; Desativada: {interface['disabled']}")
            show_in_list(interface_names, listbox, tk)
            url = f"http://{ip_address_var.get()}/rest/interface"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            encontrou = 0
            for interface in interfaces:
                for key in interface:
                    if key == 'slave':
                        encontrou = 1
                if encontrou == 0 and interface['type'] != 'bridge' and interface['type'] != 'loopback' and interface['type'] != 'wg':
                    interface_names.append(interface['name'])
                encontrou = 0
            options1 = interface_names
            if len(interface_names) > 0:
                pre_filled_value1 = interface_names[0]
                combobox['textvariable'] = selected_option1
                combobox['values'] = options1
                try:
                    pre_filled_index1 = options1.index(pre_filled_value1)
                    combobox1.current(pre_filled_index1)
                except ValueError:
                    pass
                combobox1.grid(row=0, column=1, padx=5, pady=5)
            close()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    def close():
        address_window.destroy()

    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum porto bridge!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()

        address_window = tk.Toplevel(parent)
        address_window.title(f"{item.title()}")
        address_window.geometry("640x480")
        parent = address_window
        ip_address_var = tk.StringVar(address_window)
        authorization_var = tk.StringVar(address_window)
        ip_address_var.set(f"{ip_address_var_temp.get()}")
        authorization_var.set(f"{authorization}")
        authorization = authorization_var.get()

        disabled = False
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var.get()}/rest/interface/bridge/port/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            dns_entry = response.json()
            comment_valor = ""
            if 'comment' in dns_entry:
                comment_valor = dns_entry['comment']
            if dns_entry['disabled'] == 'true':
                disabled = True
            interface_valor = dns_entry['interface']
            bridge_valor = dns_entry['bridge']
            url = f"http://{ip_address_var.get()}/rest/interface/bridge"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            bridge_names = []
            for interface in interfaces:
                bridge_names.append(interface['name'])
            url = f"http://{ip_address_var.get()}/rest/interface"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            interface_names.append(interface_valor)
            encontrou = 0
            for interface in interfaces:
                for key in interface:
                    if key == 'slave':
                        encontrou = 1
                if encontrou == 0 and interface['type'] != 'bridge' and interface['type'] != 'loopback' and interface['type'] != 'wg':
                    interface_names.append(interface['name'])
                encontrou = 0
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

        entry_frame = tk.Frame(address_window)
        entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        interface_label = tk.Label(entry_frame, text="Interface:")
        interface_label.grid(row=0, column=0, padx=5, pady=5)
        options = interface_names
        pre_filled_value = interface_valor
        selected_option = tk.StringVar()
        combobox = ttk.Combobox(entry_frame, textvariable=selected_option, values=options)
        combobox.set(bridge_valor)
        pre_filled_index = options.index(pre_filled_value)
        combobox.current(pre_filled_index)
        combobox.grid(row=0, column=1, padx=5, pady=5)

        bridge_label = tk.Label(entry_frame, text="Bridge:")
        bridge_label.grid(row=1, column=0, padx=5, pady=5)
        options2 = bridge_names
        pre_filled_value2 = bridge_valor
        selected_option2 = tk.StringVar()
        combobox2 = ttk.Combobox(entry_frame, textvariable=selected_option2, values=options2)
        combobox2.set(bridge_valor)
        pre_filled_index2 = options2.index(pre_filled_value2)
        combobox2.current(pre_filled_index2)
        combobox2.grid(row=1, column=1, padx=5, pady=5)

        comentario_label = tk.Label(entry_frame, text="Comentário:")
        comentario_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N)
        comentario_entry = tk.Text(entry_frame, height=4, width=30)
        comentario_entry.grid(row=2, column=1, padx=5, pady=5)
        comentario_entry.insert(tk.END, comment_valor)

        ativar_value = tk.BooleanVar()
        if not disabled:
            ativar_button = tk.Checkbutton(entry_frame, text="Desativar", variable=ativar_value)
            ativar_button.grid(row=3, column=0, padx=5, pady=5)
        else:
            ativar_button = tk.Checkbutton(entry_frame, text="Ativar", variable=ativar_value)
            ativar_button.grid(row=3, column=0, padx=5, pady=5)

        button_frame = tk.Frame(address_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        right_button_frame = tk.Frame(button_frame)
        right_button_frame.pack(side=tk.RIGHT)
        ok_button = tk.Button(right_button_frame, text="Ok", command=lambda: update_porto_bridge(id_value))
        ok_button.grid(row=0, column=0, padx=2, pady=2)
        close_button = tk.Button(right_button_frame, text="Fechar", command=close)
        close_button.grid(row=0, column=1, padx=2, pady=2)

def get_perfis_seguranca(ip_address_var, authorization, listbox, tk, parent, labels_frame, new_buttons, old_buttons):
    for button in old_buttons:
        button.grid_forget()
        del button
    
    name_label = tk.Label(labels_frame, text="Nome*:")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(name_label)
    name_entry = tk.Entry(labels_frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    old_buttons.append(name_entry)
    password_label = tk.Label(labels_frame, text="WPA2 Pre-Shared Key*:")
    password_label.grid(row=1, column=0, padx=5, pady=5)
    old_buttons.append(password_label)
    password_entry = tk.Entry(labels_frame)
    password_entry.grid(row=1, column=1, padx=5, pady=5)
    old_buttons.append(password_entry)
    desativar_pmkid = tk.BooleanVar()
    desativar_pmkid_button = tk.Checkbutton(labels_frame, text="Desativar PMKID", variable=desativar_pmkid)
    desativar_pmkid_button.grid(row=0, column=2, padx=5, pady=5)
    old_buttons.append(desativar_pmkid_button)
    autentication_mac = tk.BooleanVar()
    autentication_mac_button = tk.Checkbutton(labels_frame, text="MAC Authentication", variable=autentication_mac)
    autentication_mac_button.grid(row=1, column=2, padx=5, pady=5)
    old_buttons.append(autentication_mac_button)
    comentario_label = tk.Label(labels_frame, text="Comentário:")
    comentario_label.grid(row=0, column=4, padx=5, pady=5)
    old_buttons.append(comentario_label)
    comentario_entry = tk.Entry(labels_frame)
    comentario_entry.grid(row=0, column=5, padx=5, pady=5)
    old_buttons.append(comentario_entry)

    new_buttons[0].grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    new_buttons[0].config(command=lambda: criar_perfis_seguranca(ip_address_var, authorization, listbox, tk, parent, name_entry, password_entry, desativar_pmkid, desativar_pmkid_button, autentication_mac, autentication_mac_button, comentario_entry))
    new_buttons[1].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[1].config(command=lambda: editar_perfis_seguranca(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[1])
    new_buttons[2].grid(row=0, column=2, padx=2, pady=2, sticky=tk.SW)
    new_buttons[2].config(command=lambda: eliminar_perfil_seguranca(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[2])

    def on_double_click(event):
        index = listbox.curselection()
        if index :
            item = listbox.get(index)
            item = item.strip()
            try:
                id_value = item.split("ID:")[1].split(";")[0].strip()
                url = f"http://{ip_address_var.get()}/rest/interface/wireless/security-profiles/{id_value}"
                headers = {'Authorization': 'Basic '+ authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                rota_estatica = response.json()
                string_text_box = ""
                for item in rota_estatica:
                    string_text_box += f"{item} : {rota_estatica[item]} \n" 
                messagebox.showinfo(f"{item}", string_text_box, parent=parent )
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    try:
        url = f"http://{ip_address_var.get()}/rest/interface/wireless/security-profiles"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        perfis_segurança = response.json()
        string_perfis_seguranca = []
        for perfil in perfis_segurança:
            string_perfis_seguranca.append(f"ID: {perfil['.id']}; Modo de Autenticação: {perfil['authentication-types']}; Nome: {perfil['name']};")
        show_in_list(string_perfis_seguranca, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def criar_perfis_seguranca(ip_address_var, authorization, listbox, tk, parent, name_entry, password_entry, desativar_pmkid, desativar_pmkid_button, autentication_mac, autentication_mac_button, comentario_entry):
    name_valor = name_entry.get().replace(" ", "")
    if not name_valor:
        messagebox.showerror("Erro","Não foi dado nenhum nome, a caixa de texto encontra-se vazia!", parent=parent)
        return
    password_valor = password_entry.get().replace(" ", "")
    if not password_valor:
        messagebox.showerror("Erro","O campo WPA2 Pre-Shared Key não foi preenchido!", parent=parent)
        return
    pmkid_desativado = False
    if desativar_pmkid.get():
        pmkid_desativado = True
    mac_desativado = False
    if autentication_mac.get():
        mac_desativado = True
    try:
        url = f"http://{ip_address_var.get()}/rest/interface/wireless/security-profiles/add"
        headers = {'Authorization': 'Basic '+ authorization}
        data = {
            "name" : name_valor,
            "wpa2-pre-shared-key" : password_valor,
            "mode" : 'dynamic-keys',
            "authentication-types" : 'wpa2-psk',
            "disable-pmkid" : pmkid_desativado,
            "radius-mac-authentication" : mac_desativado,
            "eap-methods" : "passthrough",
            "group-ciphers" : "aes-ccm",
            "management-protection" : "disabled",
            "radius-mac-caching" : "disabled",
            "radius-mac-format" : "XX:XX:XX:XX:XX:XX",
            "radius-mac-mode" : "as-username",
            "tls-mode" : "no-certificates",
            "unicast-ciphers" : "aes-ccm"
        }
        if comentario_entry.get().replace(" ", ""):
            data['comment'] = comentario_entry.get().replace(" ", "")
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        if response.status_code == 200:
            messagebox.showinfo("Perfil de Segurança criado", "Perfil de Segurança criado com sucesso", parent=parent )
        url = f"http://{ip_address_var.get()}/rest/interface/wireless/security-profiles"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        perfis_segurança = response.json()
        string_perfis_seguranca = []
        for perfil in perfis_segurança:
            string_perfis_seguranca.append(f"ID: {perfil['.id']}; Modo de Autenticação: {perfil['authentication-types']}; Nome: {perfil['name']};")
        show_in_list(string_perfis_seguranca, listbox, tk)
        name_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        comentario_entry.delete(0, tk.END)
        autentication_mac_button.deselect()
        desativar_pmkid_button.deselect()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def editar_perfis_seguranca(ip_address_var_temp, authorization, listbox, tk, parent):
    def update_perfil_seguranca(id_value):
        try:
            url = f"http://{ip_address_var.get()}/rest/interface/wireless/security-profiles/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {}
            if nome_entry.get().replace(" ", ""):
                data['name'] = nome_entry.get().replace(" ", "")
            if comentario_entry.get("1.0", "end-1c").replace(" ", ""):
                data['comment'] =  comentario_entry.get("1.0", "end-1c")
            if password_entry.get().replace(" ", ""):
                data['wpa2-pre-shared-key'] = password_entry.get().replace(" ", "")
            if pmkid_value.get() and desativar_pmkid:
                data['disable-pmkid'] = False
            if pmkid_value.get() and not desativar_pmkid:
                data['disable-pmkid'] = True
            if mac_value.get() and mac_authentication:
                data['radius-mac-authentication'] = False
            if mac_value.get() and not mac_authentication:
                data['radius-mac-authentication'] = True
            response = requests.put(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Perfil de segurança atualizado", "Perfil de segurança atualizado com sucesso", parent=parent )
            url = f"http://{ip_address_var.get()}/rest/interface/wireless/security-profiles"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            perfis_segurança = response.json()
            string_perfis_seguranca = []
            for perfil in perfis_segurança:
                string_perfis_seguranca.append(f"ID: {perfil['.id']}; Modo de Autenticação: {perfil['authentication-types']}; Nome: {perfil['name']};")
            show_in_list(string_perfis_seguranca, listbox, tk)
            close()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    def close():
        rota_window.destroy()

    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum Perfil de Segurança!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()

        rota_window = tk.Toplevel(parent)
        rota_window.title(f"{item.title()}")
        rota_window.geometry("640x480")
        parent = rota_window
        ip_address_var = tk.StringVar(rota_window)
        authorization_var = tk.StringVar(rota_window)
        ip_address_var.set(f"{ip_address_var_temp.get()}")
        authorization_var.set(f"{authorization}")
        authorization = authorization_var.get()

        desativar_pmkid = False
        mac_authentication = False
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var.get()}/rest/interface/wireless/security-profiles/{id_value}"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            perfil_seguranca = response.json()
            nome_valor = perfil_seguranca['name']
            modo_valor = perfil_seguranca['mode']
            autenticacao_tipo_valor = perfil_seguranca['authentication-types']
            if autenticacao_tipo_valor != 'wpa2-psk':
                messagebox.showerror("Erro","Não é possível editar este perfil de segurança!\n A aplicação apenas suporta perfis wpa2-psk.", parent=parent)
                close()
                return
            password_valor = perfil_seguranca['wpa2-pre-shared-key']
            comment_valor = ""
            if 'comment' in perfil_seguranca:
                comment_valor = perfil_seguranca['comment']
            if perfil_seguranca['radius-mac-authentication'] == 'true':
                mac_authentication = True
            if perfil_seguranca['disable-pmkid'] == 'true':
                desativar_pmkid = True
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

        entry_frame = tk.Frame(rota_window)
        entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        nome_label = tk.Label(entry_frame, text="Nome:")
        nome_label.grid(row=0, column=0, padx=5, pady=5)
        nome_entry = tk.Entry(entry_frame)
        nome_entry.grid(row=0, column=1, padx=5, pady=5)
        nome_entry.insert(tk.END, nome_valor)
        modo_label = tk.Label(entry_frame, text="Modo:")
        modo_label.grid(row=1, column=0, padx=5, pady=5)
        modo_label = tk.Label(entry_frame, text=modo_valor)
        modo_label.grid(row=1, column=1, padx=5, pady=5)
        autenticacao_tipo_label = tk.Label(entry_frame, text="Authentication Types:")
        autenticacao_tipo_label.grid(row=2, column=0, padx=5, pady=5)
        autenticacao_tipo_label = tk.Label(entry_frame, text=autenticacao_tipo_valor)
        autenticacao_tipo_label.grid(row=2, column=1, padx=5, pady=5)
        password_label = tk.Label(entry_frame, text="WPA2 Pre-Shared Key:")
        password_label.grid(row=3, column=0, padx=5, pady=5)
        password_entry = tk.Entry(entry_frame)
        password_entry.grid(row=3, column=1, padx=5, pady=5)
        password_entry.insert(tk.END, password_valor)
        comentario_label = tk.Label(entry_frame, text="Comentário:")
        comentario_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.N)
        comentario_entry = tk.Text(entry_frame, height=4, width=30)
        comentario_entry.grid(row=4, column=1, padx=5, pady=5)
        comentario_entry.insert(tk.END, comment_valor)

        pmkid_value = tk.BooleanVar()
        if not desativar_pmkid:
            ativar_button = tk.Checkbutton(entry_frame, text="Desativar PMKID", variable=pmkid_value)
            ativar_button.grid(row=5, column=0, padx=5, pady=5)
        else:
            ativar_button = tk.Checkbutton(entry_frame, text="Ativar PMKID", variable=pmkid_value)
            ativar_button.grid(row=5, column=0, padx=5, pady=5)
        mac_value = tk.BooleanVar()
        if not mac_authentication:
            ativar_button = tk.Checkbutton(entry_frame, text="Ativar MAC Authentication", variable=mac_value)
            ativar_button.grid(row=6, column=0, padx=5, pady=5)
        else:
            ativar_button = tk.Checkbutton(entry_frame, text="Desativar MAC Authentication", variable=mac_value)
            ativar_button.grid(row=6, column=0, padx=5, pady=5)

        button_frame = tk.Frame(rota_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        right_button_frame = tk.Frame(button_frame)
        right_button_frame.pack(side=tk.RIGHT)
        ok_button = tk.Button(right_button_frame, text="Ok", command=lambda: update_perfil_seguranca(id_value))
        ok_button.grid(row=0, column=0, padx=2, pady=2)
        close_button = tk.Button(right_button_frame, text="Fechar", command=close)
        close_button.grid(row=0, column=1, padx=2, pady=2)

def eliminar_perfil_seguranca(ip_address_var, authorization, listbox, tk, parent):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum Perfil de Segurança!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            confirmacao = messagebox.askquestion(f"Eliminar Perfil de Segurança {id_value}",f"Tem a certeza que pretende eliminar o perfil de segurança {id_value} ?", parent=parent)
            if confirmacao == "no":
                return
            url = f"http://{ip_address_var.get()}/rest/interface/wireless"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            print(interfaces)
            for interface in interfaces:
                interface_names.append(interface['security-profile'])
            url = f"http://{ip_address_var.get()}/rest/interface/wireless/security-profiles/{id_value}"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            perfil_seguranca = response.json()
            nome = perfil_seguranca['name']
            if nome in interface_names:
                messagebox.showerror("Erro","Não é possível eliminar!\n Este perfil de segurança encontra-se associado a uma rede.", parent=parent)
                return
            url = f"http://{ip_address_var.get()}/rest/interface/wireless/security-profiles/remove"
            headers = {'Authorization': 'Basic '+ authorization}
            payload = {
                ".id": id_value,
            }
            response = requests.post(url, headers=headers, json=payload, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Sucesso", "Perfil de segurança eliminado com sucesso!", parent=parent)
            url = f"http://{ip_address_var.get()}/rest/interface/wireless/security-profiles"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            perfis_segurança = response.json()
            print(perfis_segurança)
            string_perfis_seguranca = []
            for perfil in perfis_segurança:
                string_perfis_seguranca.append(f"ID: {perfil['.id']}; Modo de Autenticação: {perfil['authentication-types']}; Nome: {perfil['name']};")
            show_in_list(string_perfis_seguranca, listbox, tk)
        except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def get_redes_wireless(ip_address_var, authorization, listbox, tk, parent, labels_frame, new_buttons, old_buttons):
    for button in old_buttons:
        button.grid_forget()
        del button

    bridge_label = tk.Label(labels_frame, text="", height=0)
    bridge_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(bridge_label)

    new_buttons[1].grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    new_buttons[1].config(command=lambda: editar_rede_wireless(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[1])
    new_buttons[3].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[3].config(command=lambda: ativar_rede_wireless(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[3])
    new_buttons[4].grid(row=0, column=2, padx=2, pady=2, sticky=tk.SW)
    new_buttons[4].config(command=lambda: desativar_rede_wireless(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[4])

    def on_double_click(event):
        # Get the selected item in the listbox
        index = listbox.curselection()
        if index :
            item = listbox.get(index)
            item = item.strip()
            try:
                id_value = item.split("ID:")[1].split(";")[0].strip()
                url = f"http://{ip_address_var.get()}/rest/interface/wireless/{id_value}"
                headers = {'Authorization': 'Basic '+ authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                interface_data = response.json()
                string_text_box = ""
                for data in interface_data:
                    string_text_box += f"{data} : {interface_data[data]} \n"
                messagebox.showinfo(f"{item}", string_text_box, parent=parent )
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    try:
        url = f"http://{ip_address_var.get()}/rest/interface/wireless"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        interfaces = response.json()
        interface_names = []
        print(interfaces)
        for interface in interfaces:
            interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Band: {interface['band']}; Perfil de segurança: {interface['security-profile']}; SSID: {interface['ssid']}; Desativado: {interface['disabled']}")
        show_in_list(interface_names, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def ativar_rede_wireless(ip_address_var_temp, authorization, listbox, tk, parent):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhuma rede wireless!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var_temp.get()}/rest/interface/wireless/set"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {
                ".id": id_value,
                "disabled": False
            }
            response = requests.post(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Rede wireless ativada", "Rede wireless ativada com sucesso", parent=parent )
            url = f"http://{ip_address_var_temp.get()}/rest/interface/wireless"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            print(interfaces)
            for interface in interfaces:
                interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Band: {interface['band']}; Perfil de segurança: {interface['security-profile']}; SSID: {interface['ssid']}; Desativado: {interface['disabled']}")
            show_in_list(interface_names, listbox, tk)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def desativar_rede_wireless(ip_address_var_temp, authorization, listbox, tk, parent):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhuma rede wireless!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var_temp.get()}/rest/interface/wireless/set"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {
                ".id": id_value,
                "disabled": True
            }
            response = requests.post(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Rede wireless desativada", "Rede wireless desativada com sucesso", parent=parent )
            url = f"http://{ip_address_var_temp.get()}/rest/interface/wireless"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            print(interfaces)
            for interface in interfaces:
                interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Band: {interface['band']}; Perfil de segurança: {interface['security-profile']}; SSID: {interface['ssid']}; Desativado: {interface['disabled']}")
            show_in_list(interface_names, listbox, tk)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def editar_rede_wireless(ip_address_var_temp, authorization, listbox, tk, parent):
    def update_rede_wireless(id_value):
        try:
            band_value = selected_option1.get()
            security_profile_value = selected_option2.get()
            url = f"http://{ip_address_var.get()}/rest/interface/wireless/set"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {
                ".id": id_value,
                "name": nome_entry.get().replace(" ", ""),
                "band": band_value,
                "security-profile": security_profile_value,
                "ssid": ssid_entry.get().replace(" ", ""),
                "mac-address": mac_entry.get().replace(" ", ""),
            }
            if comentario_entry.get("1.0", "end-1c").replace(" ", ""):
                data['comment'] =  comentario_entry.get("1.0", "end-1c")
            if disabled_value.get() and desativada:
                data['disabled'] = False
            if disabled_value.get() and not desativada:
                data['disabled'] = True
            if hide_value.get() and hide_ssid:
                data['hide-ssid'] = False
            if hide_value.get() and not hide_ssid:
                data['hide-ssid'] = True
            response = requests.post(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Rede wireless atualizada", "Rede wireless atualizada atualizada com sucesso", parent=parent )
            url = f"http://{ip_address_var.get()}/rest/interface/wireless"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            interface_names = []
            print(interfaces)
            for interface in interfaces:
                interface_names.append(f"ID: {interface['.id']}; Nome: {interface['name']}; Band: {interface['band']}; Perfil de segurança: {interface['security-profile']}; SSID: {interface['ssid']}; Desativado: {interface['disabled']}")
            show_in_list(interface_names, listbox, tk)
            close()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    def close():
        rota_window.destroy()

    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhuma rede wireless!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()

        rota_window = tk.Toplevel(parent)
        rota_window.title(f"{item.title()}")
        rota_window.geometry("640x480")
        parent = rota_window
        ip_address_var = tk.StringVar(rota_window)
        authorization_var = tk.StringVar(rota_window)
        ip_address_var.set(f"{ip_address_var_temp.get()}")
        authorization_var.set(f"{authorization}")
        authorization = authorization_var.get()

        desativada = False
        hide_ssid = False
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var.get()}/rest/interface/wireless/{id_value}"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interface = response.json()
            name_valor = interface['name']
            comentario_valor = ""
            if 'comment' in interface:
                comentario_valor = interface['comment']
            if interface['disabled'] == 'true':
                desativada = True
            tipo_valor = interface['interface-type']
            mtu_valor = interface['mtu']
            mac_address_valor = interface['mac-address']
            modo_valor = interface['mode']
            band_valor = interface['band']
            ssid_valor = interface['ssid']
            security_profile_valor = interface['security-profile']
            if interface['hide-ssid'] == 'true':
                hide_ssid = True
            url = f"http://{ip_address_var.get()}/rest/interface/wireless/security-profiles"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            perfis_seguranca = response.json()
            perfis_seguranca_array = []
            for perfil in perfis_seguranca:
                perfis_seguranca_array.append(f"{perfil['name']}")
            if security_profile_valor not in perfis_seguranca_array:
                security_profile_valor = 'default'
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
        
        entry_frame = tk.Frame(rota_window)
        entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        nome_label = tk.Label(entry_frame, text="Nome:")
        nome_label.grid(row=0, column=0, padx=5, pady=5)
        nome_entry = tk.Entry(entry_frame)
        nome_entry.grid(row=0, column=1, padx=5, pady=5)
        nome_entry.insert(tk.END, name_valor)
        tipo_label = tk.Label(entry_frame, text="Tipo:")
        tipo_label.grid(row=1, column=0, padx=5, pady=5)
        tipo_label = tk.Label(entry_frame, text=tipo_valor)
        tipo_label.grid(row=1, column=1, padx=5, pady=5)
        mtu_label = tk.Label(entry_frame, text="MTU:")
        mtu_label.grid(row=2, column=0, padx=5, pady=5)
        mtu_label = tk.Label(entry_frame, text=mtu_valor)
        mtu_label.grid(row=2, column=1, padx=5, pady=5)
        mac_label = tk.Label(entry_frame, text="MAC Address:")
        mac_label.grid(row=3, column=0, padx=5, pady=5)
        mac_entry = tk.Entry(entry_frame)
        mac_entry.grid(row=3, column=1, padx=5, pady=5)
        mac_entry.insert(tk.END, mac_address_valor)
        comentario_label = tk.Label(entry_frame, text="Comentário:")
        comentario_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.N)
        comentario_entry = tk.Text(entry_frame, height=4, width=30)
        comentario_entry.grid(row=4, column=1, padx=5, pady=5)
        comentario_entry.insert(tk.END, comentario_valor)
        mode_label = tk.Label(entry_frame, text="Mode:")
        mode_label.grid(row=5, column=0, padx=5, pady=5)
        mode_label = tk.Label(entry_frame, text=modo_valor)
        mode_label.grid(row=5, column=1, padx=5, pady=5)
        
        band_label = tk.Label(entry_frame, text="Band:")
        band_label.grid(row=6, column=0, padx=5, pady=5)
        if band_valor[0] == '5':
            options1 = ["5GHz-A".lower(), "5GHz-only-N".lower(), "5GHz-A/N".lower(), "5GHz-A/N/AC".lower(), "5GHz-only-AC".lower(), "5GHz-N/AC".lower()]
        if band_valor[0] == '2':
            options1 = ["2GHz-B".lower(), "2GHz-only-G".lower(), "2GHz-B/G".lower(), "2GHz-only-N".lower(), "2GHz-B/G/N".lower(), "2GHz-G/N".lower()]
        pre_filled_value1 = band_valor
        selected_option1 = tk.StringVar()
        combobox = ttk.Combobox(entry_frame, textvariable=selected_option1, values=options1)
        combobox.set(band_valor)
        pre_filled_index = options1.index(pre_filled_value1)
        combobox.current(pre_filled_index)
        combobox.grid(row=6, column=1, padx=5, pady=5)

        ssid_label = tk.Label(entry_frame, text="SSID:")
        ssid_label.grid(row=7, column=0, padx=5, pady=5)
        ssid_entry = tk.Entry(entry_frame)
        ssid_entry.grid(row=7, column=1, padx=5, pady=5)
        ssid_entry.insert(tk.END, ssid_valor)

        perfil_label = tk.Label(entry_frame, text="Perfil de Segurança:")
        perfil_label.grid(row=8, column=0, padx=5, pady=5)
        options2 = perfis_seguranca_array
        pre_filled_value2 = security_profile_valor
        selected_option2 = tk.StringVar()
        combobox = ttk.Combobox(entry_frame, textvariable=selected_option2, values=options2)
        combobox.set(security_profile_valor)
        pre_filled_index = options2.index(pre_filled_value2)
        combobox.current(pre_filled_index)
        combobox.grid(row=8, column=1, padx=5, pady=5)

        disabled_value = tk.BooleanVar()
        if desativada:
            ativar_button = tk.Checkbutton(entry_frame, text="Ativar rede", variable=disabled_value)
            ativar_button.grid(row=10, column=0, padx=5, pady=5)
        else:
            ativar_button = tk.Checkbutton(entry_frame, text="Desativar rede", variable=disabled_value)
            ativar_button.grid(row=10, column=0, padx=5, pady=5)
        
        hide_value = tk.BooleanVar()
        if hide_ssid:
            ativar_button = tk.Checkbutton(entry_frame, text="Mostrar SSID", variable=hide_value)
            ativar_button.grid(row=9, column=0, padx=5, pady=5)
        else:
            ativar_button = tk.Checkbutton(entry_frame, text="Esconder SSID", variable=hide_value)
            ativar_button.grid(row=9, column=0, padx=5, pady=5)

        button_frame = tk.Frame(rota_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        right_button_frame = tk.Frame(button_frame)
        right_button_frame.pack(side=tk.RIGHT)
        ok_button = tk.Button(right_button_frame, text="Ok", command=lambda: update_rede_wireless(id_value))
        ok_button.grid(row=0, column=0, padx=2, pady=2)
        close_button = tk.Button(right_button_frame, text="Fechar", command=close)
        close_button.grid(row=0, column=1, padx=2, pady=2)

    

def get_rotas_estaticas(ip_address_var, authorization, listbox, tk, parent, labels_frame, new_buttons, old_buttons):
    for button in old_buttons:
        button.grid_forget()
        del button
    
    ip_destino_label = tk.Label(labels_frame, text="IP destino*:")
    ip_destino_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(ip_destino_label)

    ip_destino_entry = tk.Entry(labels_frame)
    ip_destino_entry.grid(row=0, column=1, padx=5, pady=5)
    old_buttons.append(ip_destino_entry)
    
    gateway_label = tk.Label(labels_frame, text="Gateway*:")
    gateway_label.grid(row=1, column=0, padx=5, pady=5)
    old_buttons.append(gateway_label)
    
    gateway_entry = tk.Entry(labels_frame)
    gateway_entry.grid(row=1, column=1, padx=5, pady=5)
    old_buttons.append(gateway_entry)
    
    desativar_value = tk.BooleanVar()
    desativar_button = tk.Checkbutton(labels_frame, text="Rota desativada", variable=desativar_value)
    desativar_button.grid(row=2, column=0, padx=5, pady=5)
    old_buttons.append(desativar_button)

    comment_label = tk.Label(labels_frame, text="Comentário:")
    comment_label.grid(row=0, column=2, padx=5, pady=5)
    old_buttons.append(comment_label)

    comment_entry = tk.Entry(labels_frame)
    comment_entry.grid(row=0, column=3, padx=5, pady=5)
    old_buttons.append(comment_entry)

    new_buttons[0].grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    new_buttons[0].config(command=lambda: criar_rotas_estaticas(ip_address_var, authorization, listbox, tk, parent, ip_destino_entry, gateway_entry, desativar_value, desativar_button,comment_entry))
    old_buttons.append(new_buttons[0])
    new_buttons[1].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[1].config(command=lambda: editar_rotas_estaticas(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[1])
    new_buttons[2].grid(row=0, column=2, padx=2, pady=2, sticky=tk.SW)
    new_buttons[2].config(command=lambda: eliminar_rotas_estaticas(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[2])
    
    def on_double_click(event):
        index = listbox.curselection()
        if index :
            item = listbox.get(index)
            item = item.strip()
            try:
                id_value = item.split("ID:")[1].split(";")[0].strip()
                url = f"http://{ip_address_var.get()}/rest/ip/route/{id_value}"
                headers = {'Authorization': 'Basic '+ authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                rota_estatica = response.json()
                string_text_box = ""
                for item in rota_estatica:
                    string_text_box += f"{item} : {rota_estatica[item]} \n" 
                messagebox.showinfo(f"{item}", string_text_box, parent=parent )
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    try:
        url = f"http://{ip_address_var.get()}/rest/ip/route?"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        interfaces = response.json()
        string_rotas_estaticas = []
        for interface in interfaces:
            if 'static' in interface:
                string_rotas_estaticas.append(f"ID: {interface['.id']}; Static: {interface['static']}; Rede: {interface['dst-address']}; Gateway: {interface['gateway']}; Inativa: {interface['inactive']}")
            else:
                string_rotas_estaticas.append(f"ID: {interface['.id']}; Rede: {interface['dst-address']}; Gateway: {interface['gateway']}; Inativa: {interface['inactive']}")
        show_in_list(string_rotas_estaticas, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def criar_rotas_estaticas(ip_address_var, authorization, listbox, tk, parent, ip_destination, gateway, desativar_value, desativar_button,comment_entry):
    ip_destino_valor = ip_destination.get().replace(" ", "")
    if not ip_destino_valor:
        messagebox.showerror("Erro","Não foi dado nenhum IP de destino, a caixa de texto encontra-se vazia!", parent=parent)
        return
    gateway_valor = gateway.get().replace(" ", "")
    if not gateway_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Gateway, a caixa de texto encontra-se vazia!", parent=parent)
        return
    
    comment_entry_valor = comment_entry.get().strip()
    
    desativado = False
    if desativar_value.get():
        desativado = True
    try:
        url = f"http://{ip_address_var.get()}/rest/ip/route/add"
        headers = {'Authorization': 'Basic '+ authorization}
        data = {
            "dst-address" : ip_destino_valor,
            "gateway" : gateway_valor,
            "disabled" : desativado,
        }
        if comment_entry_valor:
            data['comment'] = comment_entry_valor
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        if response.status_code == 200:
            messagebox.showinfo("Rota Criada", "Rota criada com sucesso", parent=parent )
        url = f"http://{ip_address_var.get()}/rest/ip/route"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        interfaces = response.json()
        string_rotas_estaticas = []
        for interface in interfaces:
            if 'static' in interface:
                string_rotas_estaticas.append(f"ID: {interface['.id']}; Static: {interface['static']}; Rede: {interface['dst-address']}; Gateway: {interface['gateway']}; Inativa: {interface['inactive']}")
            else:
                string_rotas_estaticas.append(f"ID: {interface['.id']}; Rede: {interface['dst-address']}; Gateway: {interface['gateway']}; Inativa: {interface['inactive']}")
        show_in_list(string_rotas_estaticas, listbox, tk)
        gateway.delete(0, tk.END)
        ip_destination.delete(0, tk.END)
        desativar_button.deselect()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def editar_rotas_estaticas(ip_address_var_temp, authorization, listbox, tk, parent):
    def update_rota_estatica(id_value):
        try:
            url = f"http://{ip_address_var.get()}/rest/ip/route/set"
            headers = {'Authorization': 'Basic '+ authorization}
            payload = {
                ".id": id_value,
                "dst-address": dst_entry.get().replace(" ", ""),
                "gateway": gateway_entry.get().replace(" ", ""),
            }
            if comentario_entry.get("1.0", "end-1c").replace(" ", ""):
                payload['comment'] =  comentario_entry.get("1.0", "end-1c")
            if active and ativar_value.get():
                payload["disabled"] = True
                print("quero desativar")
            elif ativar_value.get():
                payload["disabled"] = "false"
                print("quero ativar")
            response = requests.post(url, headers=headers, json=payload, verify=False)
            response.raise_for_status()
            if response.status_code == 200:
                messagebox.showinfo("Rota editada", "Rota editada com sucesso!", parent=parent )
            url = f"http://{ip_address_var.get()}/rest/ip/route"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            string_rotas_estaticas = []
            for interface in interfaces:
                if 'static' in interface:
                    string_rotas_estaticas.append(f"ID: {interface['.id']}; Static: {interface['static']}; Rede: {interface['dst-address']}; Gateway: {interface['gateway']}; Inativa: {interface['inactive']}")
                else:
                    string_rotas_estaticas.append(f"ID: {interface['.id']}; Rede: {interface['dst-address']}; Gateway: {interface['gateway']}; Inativa: {interface['inactive']}")
            show_in_list(string_rotas_estaticas, listbox, tk)
            close()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
    
    def close():
        rota_window.destroy()

    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhuma Rota Estática!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()

        rota_window = tk.Toplevel(parent)
        rota_window.title(f"{item.title()}")
        rota_window.geometry("640x480")
        parent = rota_window
        ip_address_var = tk.StringVar(rota_window)
        authorization_var = tk.StringVar(rota_window)
        ip_address_var.set(f"{ip_address_var_temp.get()}")
        authorization_var.set(f"{authorization}")
        authorization = authorization_var.get()

        active = False
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var.get()}/rest/ip/route/{id_value}"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interface = response.json()
            rota_id = interface['.id']
            dst_address = interface['dst-address']
            gateway = interface['gateway']
            if 'active' in interface:
                active = interface['active']
            comentario_valor = ""
            if 'comment' in interface:
                comentario_valor = interface['comment']
            if 'static' not in interface:
                messagebox.showerror("Erro","Não é possível editar esta rota!\n A aplicação apenas suporta rotas estáticas.", parent=parent)
                close()
                return
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

        entry_frame = tk.Frame(rota_window)
        entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        dst_label = tk.Label(entry_frame, text="Endereço de Destino:")
        dst_label.grid(row=0, column=0, padx=5, pady=5)
        dst_entry = tk.Entry(entry_frame)
        dst_entry.grid(row=0, column=1, padx=5, pady=5)
        dst_entry.insert(tk.END, dst_address)
        gateway_label = tk.Label(entry_frame, text="Gateway:")
        gateway_label.grid(row=1, column=0, padx=5, pady=5)
        gateway_entry = tk.Entry(entry_frame)
        gateway_entry.grid(row=1, column=1, padx=5, pady=5)
        gateway_entry.insert(tk.END, gateway)
        comentario_label = tk.Label(entry_frame, text="Comentário:")
        comentario_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.N)
        comentario_entry = tk.Text(entry_frame, height=4, width=30)
        comentario_entry.grid(row=4, column=1, padx=5, pady=5)
        comentario_entry.insert(tk.END, comentario_valor)
        
        ativar_value = tk.BooleanVar()
        if active:
            ativar_button = tk.Checkbutton(entry_frame, text="Desativar", variable=ativar_value)
            ativar_button.grid(row=2, column=0, padx=5, pady=5)
        else:
            ativar_button = tk.Checkbutton(entry_frame, text="Ativar", variable=ativar_value)
            ativar_button.grid(row=2, column=0, padx=5, pady=5)

        button_frame = tk.Frame(rota_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        right_button_frame = tk.Frame(button_frame)
        right_button_frame.pack(side=tk.RIGHT)
        ok_button = tk.Button(right_button_frame, text="Ok", command=lambda: update_rota_estatica(id_value))
        ok_button.grid(row=0, column=0, padx=2, pady=2)
        close_button = tk.Button(right_button_frame, text="Fechar", command=close)
        close_button.grid(row=0, column=1, padx=2, pady=2)

def eliminar_rotas_estaticas(ip_address_var, authorization, listbox, tk, parent):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhuma Rota Estática!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            confirmacao = messagebox.askquestion(f"Eliminar Rota Estática {id_value}",f"Tem a certeza que pretende eliminar a rota estática {id_value} ?", parent=parent)
            if confirmacao == "no":
                return
            url = f"http://{ip_address_var.get()}/rest/ip/route/remove"
            headers = {'Authorization': 'Basic '+ authorization}
            payload = {
                ".id": id_value,
            }
            response = requests.post(url, headers=headers, json=payload, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Sucesso", "Static route deleted successfully", parent=parent)
            url = f"http://{ip_address_var.get()}/rest/ip/route"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces = response.json()
            string_rotas_estaticas = []
            for interface in interfaces:
                if 'static' in interface:
                    string_rotas_estaticas.append(f"ID: {interface['.id']}; Static: {interface['static']}; Rede: {interface['dst-address']}; Gateway: {interface['gateway']}; Inativa: {interface['inactive']}")
                else:
                    string_rotas_estaticas.append(f"ID: {interface['.id']}; Rede: {interface['dst-address']}; Gateway: {interface['gateway']}; Inativa: {interface['inactive']}")
            show_in_list(string_rotas_estaticas, listbox, tk)
        except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def get_enderecos_ip(ip_address_var, authorization, listbox, tk, parent, labels_frame, new_buttons, old_buttons):
    for button in old_buttons:
        button.grid_forget()
        del button
    
    address_label = tk.Label(labels_frame, text="Endereço*:")
    address_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(address_label)
    address_entry = tk.Entry(labels_frame)
    address_entry.grid(row=0, column=1, padx=5, pady=5)
    old_buttons.append(address_entry)
    interface_label = tk.Label(labels_frame, text="Interface*:")
    interface_label.grid(row=1, column=0, padx=5, pady=5)
    old_buttons.append(interface_label)
    interface_entry = tk.Entry(labels_frame)
    interface_entry.grid(row=1, column=1, padx=5, pady=5)
    old_buttons.append(interface_entry)
    desativar_value = tk.BooleanVar()
    desativar_button = tk.Checkbutton(labels_frame, text="Endereço desativado", variable=desativar_value)
    desativar_button.grid(row=2, column=0, padx=5, pady=5)
    old_buttons.append(desativar_button)
    rede_label = tk.Label(labels_frame, text="Rede:")
    rede_label.grid(row=0, column=2, padx=5, pady=5)
    old_buttons.append(rede_label)
    rede_entry = tk.Entry(labels_frame)
    rede_entry.grid(row=0, column=3, padx=5, pady=5)
    old_buttons.append(rede_entry)
    netmask_label = tk.Label(labels_frame, text="Máscara de rede:")
    netmask_label.grid(row=1, column=2, padx=5, pady=5)
    old_buttons.append(netmask_label)
    netmask_entry = tk.Entry(labels_frame)
    netmask_entry.grid(row=1, column=3, padx=5, pady=5)
    old_buttons.append(netmask_entry)
    comment_label = tk.Label(labels_frame, text="Comentário:")
    comment_label.grid(row=2, column=2, padx=5, pady=5)
    old_buttons.append(comment_label)
    comment_entry = tk.Entry(labels_frame)
    comment_entry.grid(row=2, column=3, padx=5, pady=5)
    old_buttons.append(comment_entry)

    new_buttons[0].grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    new_buttons[0].config(command=lambda: criar_enderecos_ip(ip_address_var, authorization, listbox, tk, parent, address_entry, interface_entry, comment_entry, rede_entry, netmask_entry, desativar_value, desativar_button))
    old_buttons.append(new_buttons[0])
    new_buttons[1].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[1].config(command=lambda: editar_enderecos_ip(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[1])
    new_buttons[2].grid(row=0, column=2, padx=2, pady=2, sticky=tk.SW)
    new_buttons[2].config(command=lambda: eliminar_enderecos_ip(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[2])

    def on_double_click(event):
        index = listbox.curselection()
        if index :
            item = listbox.get(index)
            item = item.strip()
            try:
                id_value = item.split("ID:")[1].split(";")[0].strip()
                url = f"http://{ip_address_var.get()}/rest/ip/address/{id_value}"
                headers = {'Authorization': 'Basic '+ authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                ip_address = response.json()
                string_text_box = ""
                for item in ip_address:
                    string_text_box += f"{item} : {ip_address[item]} \n" 
                messagebox.showinfo(f"{item}", string_text_box, parent=parent )
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    try:
        url = f"http://{ip_address_var.get()}/rest/ip/address"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        ip_addresses = response.json()
        string_listbox = []
        for ip in ip_addresses:
            string_listbox.append(f"ID: {ip['.id']}; Endereço: {ip['address']}; Desativado: {ip['disabled']}; Dinâmico: {ip['dynamic']}; Interface: {ip['interface']}")
        show_in_list(string_listbox, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def criar_enderecos_ip(ip_address_var, authorization, listbox, tk, parent, address_entry, interface_entry, comment_entry, rede_entry, netmask_entry, desativar_value, desativar_button):
    address_entry_valor = address_entry.get().replace(" ", "")
    if not address_entry_valor:
        messagebox.showerror("Erro", "Não foi dado nenhum endereço de IP, a caixa de texto encontra-se vazia!", parent=parent)
        return
    interface_entry_valor = interface_entry.get().replace(" ", "")
    if not interface_entry_valor:
        messagebox.showerror("Erro", "Não foi dada nenhuma interface, a caixa de texto encontra-se vazia!", parent=parent)
        return
    
    comment_entry_valor = comment_entry.get().strip()
    rede_entry_valor = rede_entry.get().strip()
    netmask_entry_valor = netmask_entry.get().strip()

    desativado = False
    if desativar_value.get():
        desativado = True

    try:
        url = f"http://{ip_address_var.get()}/rest/ip/address/add"
        headers = {'Authorization': 'Basic ' + authorization}
        data = {
            "address": address_entry_valor,
            "interface": interface_entry_valor,
            "disabled": desativado,
        }
        if comment_entry_valor:
            data['comment'] = comment_entry_valor
        if rede_entry_valor:
            data['network'] = rede_entry_valor
        if netmask_entry_valor:
            data['netmask'] = netmask_entry_valor
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        if response.status_code == 200:
            messagebox.showinfo("Endereço de IP criado", "Endereço de IP criado com sucesso", parent=parent )
        url = f"http://{ip_address_var.get()}/rest/ip/address"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        ip_addresses = response.json()
        string_listbox = []
        for ip in ip_addresses:
            string_listbox.append(f"ID: {ip['.id']}; Endereço: {ip['address']}; Desativado: {ip['disabled']}; Dinâmico: {ip['dynamic']}; Interface: {ip['interface']}")
        show_in_list(string_listbox, listbox, tk)
        address_entry.delete(0, tk.END)
        interface_entry.delete(0, tk.END)
        comment_entry.delete(0, tk.END)
        netmask_entry.delete(0, tk.END)
        rede_entry.delete(0, tk.END)
        desativar_button.deselect()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def editar_enderecos_ip(ip_address_var_temp, authorization, listbox, tk, parent):
    def update_endereco_ip(id_value):
        try:
            url = f"http://{ip_address_var.get()}/rest/ip/address/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {
                "address": ip_entry.get().replace(" ", ""),
                "interface": interface_entry.get().replace(" ", ""),
                "network": rede_entry.get().replace(" ", ""),
            }
            if comentario_entry.get("1.0", "end-1c").replace(" ", ""):
                data['comment'] =  comentario_entry.get("1.0", "end-1c")
            if mascara_entry.get().replace(" ", ""):
                data['netmask'] = mascara_entry.get().replace(" ", "")
            if ativar_value.get() and disabled:
                data['disabled'] = False
            if ativar_value.get() and not disabled:
                data['disabled'] = True
            response = requests.put(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Endereço de IP atualizado", "Endereço de IP atualizado com sucesso", parent=parent )
            url = f"http://{ip_address_var.get()}/rest/ip/address"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            ip_addresses = response.json()
            string_listbox = []
            for ip in ip_addresses:
                string_listbox.append(f"ID: {ip['.id']}; Endereço: {ip['address']}; Desativado: {ip['disabled']}; Dinâmico: {ip['dynamic']}; Interface: {ip['interface']}")
            show_in_list(string_listbox, listbox, tk)
            close()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    def close():
        address_window.destroy()

    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhum endereço de IP!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()

        address_window = tk.Toplevel(parent)
        address_window.title(f"{item.title()}")
        address_window.geometry("640x480")
        parent = address_window
        ip_address_var = tk.StringVar(address_window)
        authorization_var = tk.StringVar(address_window)
        ip_address_var.set(f"{ip_address_var_temp.get()}")
        authorization_var.set(f"{authorization}")
        authorization = authorization_var.get()

        disabled = False
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var.get()}/rest/ip/address/{id_value}"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            ip_address = {}
            ip_address = response.json()
            ip_address_valor = ip_address['address']
            rede_valor = ip_address['network']
            mascara_valor = ""
            if 'netmask' in ip_address:
                mascara_valor = ip_address['netmask']
            interface_valor = ip_address['interface']
            comentario_valor = ""
            if 'comment' in ip_address:
                comentario_valor = ip_address['comment']
            if ip_address['disabled'] == 'true':
                disabled = True
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
        
        entry_frame = tk.Frame(address_window)
        entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        ip_label = tk.Label(entry_frame, text="Endereço de IP:")
        ip_label.grid(row=0, column=0, padx=5, pady=5)
        ip_entry = tk.Entry(entry_frame)
        ip_entry.grid(row=0, column=1, padx=5, pady=5)
        ip_entry.insert(tk.END, ip_address_valor)
        rede_label = tk.Label(entry_frame, text="Rede:")
        rede_label.grid(row=1, column=0, padx=5, pady=5)
        rede_entry = tk.Entry(entry_frame)
        rede_entry.grid(row=1, column=1, padx=5, pady=5)
        rede_entry.insert(tk.END, rede_valor)
        mascara_label = tk.Label(entry_frame, text="Máscara:")
        mascara_label.grid(row=2, column=0, padx=5, pady=5)
        mascara_entry = tk.Entry(entry_frame)
        mascara_entry.grid(row=2, column=1, padx=5, pady=5)
        mascara_entry.insert(tk.END, mascara_valor)
        interface_label = tk.Label(entry_frame, text="Interface:")
        interface_label.grid(row=3, column=0, padx=5, pady=5)
        interface_entry = tk.Entry(entry_frame)
        interface_entry.grid(row=3, column=1, padx=5, pady=5)
        interface_entry.insert(tk.END, interface_valor)
        comentario_label = tk.Label(entry_frame, text="Comentário:")
        comentario_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.N)
        comentario_entry = tk.Text(entry_frame, height=4, width=30)
        comentario_entry.grid(row=4, column=1, padx=5, pady=5)
        comentario_entry.insert(tk.END, comentario_valor)
        
        ativar_value = tk.BooleanVar()
        if not disabled:
            ativar_button = tk.Checkbutton(entry_frame, text="Desativar", variable=ativar_value)
            ativar_button.grid(row=5, column=0, padx=5, pady=5)
        else:
            ativar_button = tk.Checkbutton(entry_frame, text="Ativar", variable=ativar_value)
            ativar_button.grid(row=5, column=0, padx=5, pady=5)

        button_frame = tk.Frame(address_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        right_button_frame = tk.Frame(button_frame)
        right_button_frame.pack(side=tk.RIGHT)
        ok_button = tk.Button(right_button_frame, text="Ok", command=lambda: update_endereco_ip(id_value))
        ok_button.grid(row=0, column=0, padx=2, pady=2)
        close_button = tk.Button(right_button_frame, text="Fechar", command=close)
        close_button.grid(row=0, column=1, padx=2, pady=2)

def eliminar_enderecos_ip(ip_address_var, authorization, listbox, tk, parent):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhum endereço de IP!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            confirmacao = messagebox.askquestion(f"Eliminar endereço de IP {id_value}",f"Tem a certeza que pretende eliminar o endereço de IP {id_value} ?", parent=parent)
            if confirmacao == "no":
                return
            delete_url = f"http://{ip_address_var.get()}/rest/ip/address/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.delete(delete_url, headers=headers, verify=False)
            response.raise_for_status()
            messagebox.showinfo("IP Address Deleted", "IP address deleted successfully", parent=parent)
            url = f"http://{ip_address_var.get()}/rest/ip/address"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            ip_addresses = response.json()
            string_listbox = []
            for ip in ip_addresses:
                string_listbox.append(f"ID: {ip['.id']}; Endereço: {ip['address']}; Desativado: {ip['disabled']}; Dinâmico: {ip['dynamic']}; Interface: {ip['interface']}")
            show_in_list(string_listbox, listbox, tk)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}")

def get_servidores_DHCP(ip_address_var, authorization, listbox, tk, parent, labels_frame, new_buttons, old_buttons):
    

    def on_entry_click(event, entry, text):
        """function that gets called whenever entry is clicked"""
        if entry.get() == text:
            entry.delete(0, "end") # delete all the text in the entry
            entry.insert(0, '') #Insert blank for user input
            entry.config(fg = 'black')

    def on_focusout(event, entry, text):
        if entry.get() == '':
            entry.insert(0, text)
            entry.config(fg = 'grey')
    
    for button in old_buttons:
        button.grid_forget()
        del button
    
    name_server_dhcp_label = tk.Label(labels_frame, text="Nome Servidor DHCP* :")
    name_server_dhcp_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(name_server_dhcp_label)
    
    name_server_dhcp_entry = tk.Entry(labels_frame)
    name_server_dhcp_entry.insert(0,"Ex: Servidor DHCP")
    name_server_dhcp_entry.bind('<FocusIn>', lambda event: on_entry_click(event,name_server_dhcp_entry,"Ex: Servidor DHCP"))
    name_server_dhcp_entry.bind('<FocusOut>', lambda event: on_focusout(event,name_server_dhcp_entry,"Ex: Servidor DHCP"))
    name_server_dhcp_entry.config(fg='grey')
    name_server_dhcp_entry.grid(row=0, column=1, padx=5, pady=5)
    old_buttons.append(name_server_dhcp_entry)
    
    interface_label = tk.Label(labels_frame, text="Interface de saida* :")
    interface_label.grid(row=1, column=0, padx=5, pady=5)
    old_buttons.append(interface_label)
    
    interface_entry = tk.Entry(labels_frame)
    interface_entry.insert(0,"Ex: ether1")
    interface_entry.bind('<FocusIn>', lambda event: on_entry_click(event,interface_entry,"Ex: ether1"))
    interface_entry.bind('<FocusOut>', lambda event: on_focusout(event,interface_entry,"Ex: ether1"))
    interface_entry.config(fg='grey')
    interface_entry.grid(row=1, column=1, padx=5, pady=5)
    old_buttons.append(interface_entry)

    network_label = tk.Label(labels_frame, text="Rede :")
    network_label.grid(row=0, column=2, padx=5, pady=5 )
    old_buttons.append(network_label)

    network_entry = tk.Entry(labels_frame)
    network_entry.insert(0,"Ex: 192.168.1.0/24")
    network_entry.bind('<FocusIn>', lambda event: on_entry_click(event,network_entry,"Ex: 192.168.1.0/24"))
    network_entry.bind('<FocusOut>', lambda event: on_focusout(event,network_entry,"Ex: 192.168.1.0/24"))
    network_entry.config(fg='grey')
    network_entry.grid(row=0, column=3, padx=5, pady=5)
    old_buttons.append(network_entry)

    gateway_label = tk.Label(labels_frame, text="Gateway :")
    gateway_label.grid(row=1, column=2, padx=5, pady=5 )
    old_buttons.append(gateway_label)

    gateway_entry = tk.Entry(labels_frame)
    gateway_entry.insert(0,"Ex: 192.168.1.254")
    gateway_entry.bind('<FocusIn>', lambda event: on_entry_click(event,gateway_entry,"Ex: 192.168.1.254"))
    gateway_entry.bind('<FocusOut>', lambda event: on_focusout(event,gateway_entry,"Ex: 192.168.1.254"))
    gateway_entry.config(fg='grey')
    gateway_entry.grid(row=1, column=3, padx=5, pady=5)
    old_buttons.append(gateway_entry)

    dns_label = tk.Label(labels_frame, text="DNS :")
    dns_label.grid(row=1, column=4, padx=5, pady=5 )
    old_buttons.append(dns_label)

    dns_entry = tk.Entry(labels_frame)
    dns_entry.insert(0,"Ex: 8.8.8.8")
    dns_entry.bind('<FocusIn>', lambda event: on_entry_click(event,dns_entry,"Ex: 8.8.8.8"))
    dns_entry.bind('<FocusOut>', lambda event: on_focusout(event,dns_entry,"Ex: 8.8.8.8"))
    dns_entry.config(fg='grey')
    dns_entry.grid(row=1, column=5, padx=5, pady=5)
    old_buttons.append(dns_entry)

    pool_enderecos_label = tk.Label(labels_frame, text="Pool Endereços:")
    pool_enderecos_label.grid(row=0, column=4, padx=5, pady=5)
    old_buttons.append(pool_enderecos_label)

    pool_enderecos_first_entry = tk.Entry(labels_frame)
    pool_enderecos_first_entry.insert(0,"Ex: 192.168.1.1")
    pool_enderecos_first_entry.bind('<FocusIn>', lambda event: on_entry_click(event,pool_enderecos_first_entry,"Ex: 192.168.1.1"))
    pool_enderecos_first_entry.bind('<FocusOut>', lambda event: on_focusout(event,pool_enderecos_first_entry,"Ex: 192.168.1.1"))
    pool_enderecos_first_entry.config(fg='grey')
    pool_enderecos_first_entry.grid(row=0, column=5, padx=5, pady=5)
    old_buttons.append(pool_enderecos_first_entry)

    barra_label = tk.Label(labels_frame, text="-")
    barra_label.grid(row=0, column=6, padx=5, pady=5)
    old_buttons.append(barra_label)

    pool_enderecos_second_entry = tk.Entry(labels_frame)
    pool_enderecos_second_entry.insert(0,"Ex: 192.168.1.253")
    pool_enderecos_second_entry.bind('<FocusIn>', lambda event: on_entry_click(event,pool_enderecos_second_entry,"Ex: 192.168.1.253"))
    pool_enderecos_second_entry.bind('<FocusOut>', lambda event: on_focusout(event,pool_enderecos_second_entry,"Ex: 192.168.1.253"))
    pool_enderecos_second_entry.config(fg='grey')
    pool_enderecos_second_entry.grid(row=0, column=7, padx=5, pady=5)
    old_buttons.append(pool_enderecos_second_entry)

    lease_time_label = tk.Label(labels_frame, text="Tempo de Duração dos IPs* :")
    lease_time_label.grid(row=0, column=8, padx=5, pady=5 )
    old_buttons.append(lease_time_label)
    
    lease_time_hour_entry = tk.Entry(labels_frame,width=3)
    lease_time_hour_entry.insert(0,"01")
    lease_time_hour_entry.bind('<FocusIn>', lambda event: on_entry_click(event,lease_time_hour_entry,"01"))
    lease_time_hour_entry.bind('<FocusOut>', lambda event: on_focusout(event,lease_time_hour_entry,"01"))
    lease_time_hour_entry.config(fg='grey')
    lease_time_hour_entry.grid(row=0, column=9, padx=5, pady=5)
    old_buttons.append(lease_time_hour_entry)

    two_points_1_label = tk.Label(labels_frame, text=":")
    two_points_1_label.grid(row=0, column=10, padx=5, pady=5)
    old_buttons.append(two_points_1_label)

    lease_time_minute_entry = tk.Entry(labels_frame,width=3)
    lease_time_minute_entry.insert(0,"01")
    lease_time_minute_entry.bind('<FocusIn>', lambda event: on_entry_click(event,lease_time_minute_entry,"01"))
    lease_time_minute_entry.bind('<FocusOut>', lambda event: on_focusout(event,lease_time_minute_entry,"01"))
    lease_time_minute_entry.config(fg='grey')
    lease_time_minute_entry.grid(row=0, column=11, padx=5, pady=5)
    old_buttons.append(lease_time_minute_entry)

    two_points_2_label = tk.Label(labels_frame, text=":")
    two_points_2_label.grid(row=0, column=12, padx=5, pady=5)
    old_buttons.append(two_points_2_label)

    lease_time_second_entry = tk.Entry(labels_frame,width=3)
    lease_time_second_entry.insert(0,"01")
    lease_time_second_entry.bind('<FocusIn>', lambda event: on_entry_click(event,lease_time_second_entry,"01"))
    lease_time_second_entry.bind('<FocusOut>', lambda event: on_focusout(event,lease_time_second_entry,"01"))
    lease_time_second_entry.config(fg='grey')
    lease_time_second_entry.grid(row=0, column=13, padx=5, pady=5)
    old_buttons.append(lease_time_second_entry)


    new_buttons[0].grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    new_buttons[0].config(command=lambda: criar_servidor_dhcp(ip_address_var, authorization, listbox, tk, parent, name_server_dhcp_entry, pool_enderecos_first_entry, pool_enderecos_second_entry, interface_entry, lease_time_hour_entry, lease_time_minute_entry, lease_time_second_entry,network_entry,gateway_entry,dns_entry, labels_frame, new_buttons, old_buttons ))
    old_buttons.append(new_buttons[0])
    new_buttons[1].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[1].config(command=lambda: editar_servidor_dhcp(ip_address_var, authorization, listbox, tk, parent,labels_frame, new_buttons, old_buttons))
    old_buttons.append(new_buttons[1])
    new_buttons[2].grid(row=0, column=2, padx=2, pady=2, sticky=tk.SW)
    new_buttons[2].config(command=lambda: eliminar_servidor_dhcp(ip_address_var, authorization, listbox, tk, parent,labels_frame, new_buttons, old_buttons))
    old_buttons.append(new_buttons[2])
    
    def on_double_click(event):
        # Get the selected item in the listbox
        index = listbox.curselection()
        if index :
            item = listbox.get(index)
            item = item.strip()
            try:
                id_value = item.split("ID:")[1].split(";")[0].strip()
                url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/{id_value}"
                headers = {'Authorization': 'Basic '+ authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                servidor_dhcp = response.json()
                string_text_box = "Servidor DHCP \n"

                for item in servidor_dhcp:
                    string_text_box += f"{item} : {servidor_dhcp[item]} \n" 

                if servidor_dhcp['address-pool'] == "static-only":
                    messagebox.showinfo(f"{item}", string_text_box, parent=parent )
                    return
                else:
                    #Dados dos Pools
                    url = f"http://{ip_address_var.get()}/rest/ip/pool/{servidor_dhcp['address-pool']}"
                    response = requests.get(url, headers=headers, verify=False)
                    response.raise_for_status()
                    pool = response.json()

                    string_text_box += "\nRange de Pools \n"

                    for item in pool:
                        string_text_box += f"{item} : {pool[item]} \n"

                    #Dados da Network
                    url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/network"
                    response = requests.get(url, headers=headers, verify=False)
                    response.raise_for_status()
                    networks = response.json()

                    array_network = {}
                    flag_network = True

                    for network in networks:
                        if ipaddress.ip_address(pool["ranges"].split("-")[0]) in ipaddress.ip_network(network['address']):
                            array_network = network
                            flag_network = False
                            break
                    
                    if not flag_network:
                        string_text_box += "\nNetwork Servidor DHCP \n"

                        for item in array_network:
                            string_text_box += f"{item} : {array_network[item]} \n"

                messagebox.showinfo(f"{item}", string_text_box, parent=parent )
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    try:
        url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server"
        headers = {'Authorization': 'Basic ' + authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        dhcp_servers = response.json()
        string_dhcp_servers = []
        array_com_dhcp_servers_com_pool = []
        lista_dhcp_servers_com_pool = ""
        flag_pool = False
        for server in dhcp_servers:
            if server['address-pool'] == "static-only":
                string_dhcp_servers.append(f"ID: {server['.id']}; Nome: {server['name']}; Interface: {server['interface']}; Lease Time: {server['lease-time']}")
            else:
                flag_pool = True
                lista_dhcp_servers_com_pool += f"{server['address-pool']},"
                array_com_dhcp_servers_com_pool.append(server)

        if flag_pool:
            #Dados dos Pools
            url = f"http://{ip_address_var.get()}/rest/ip/pool?name={lista_dhcp_servers_com_pool}"
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            pools = response.json()

            #Dados da Network
            url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/network"
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            networks = response.json()
            flag_network = True

            for pool in pools:
                for servers_com_pool in array_com_dhcp_servers_com_pool:
                    if servers_com_pool['address-pool'] == pool['name'] :
                        flag_network = True
                        for network in networks:
                            if ipaddress.ip_address(pool["ranges"].split("-")[0]) in ipaddress.ip_network(network['address']):
                                string_network = ""
                                if network['gateway'] != "":
                                    string_network += f"Gateway: {network['gateway']}; "
                                if network['dns-server'] != "":
                                    string_network += f"Servidor DNS: {network['dns-server']}; "
                                string_dhcp_servers.append(f"ID: {servers_com_pool['.id']}; Nome: {servers_com_pool['name']}; Interface: {servers_com_pool['interface']}; Lease Time: {servers_com_pool['lease-time']}; Pool de Endereços: {pool['ranges']}; Rede: {network['address']}; {string_network}")
                                flag_network = False
                                break
                    if flag_network:
                        string_dhcp_servers.append(f"ID: {servers_com_pool['.id']}; Nome: {servers_com_pool['name']}; Interface: {servers_com_pool['interface']}; Lease Time: {servers_com_pool['lease-time']}; Pool de Endereços: {pool['ranges']};")

        show_in_list(string_dhcp_servers, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def criar_servidor_dhcp(ip_address_var, authorization, listbox, tk, parent, name_server_dhcp_entry, pool_enderecos_first_entry, pool_enderecos_second_entry, interface_entry, lease_time_hour_entry, lease_time_minute_entry, lease_time_second_entry, network_entry, gateway_entry, dns_entry, labels_frame, new_buttons, old_buttons):
    
    #Verificação se existe nome para o servidor
    if name_server_dhcp_entry.cget('fg') == "grey":
        messagebox.showerror("Erro","Não foi dado nenhum nome ao servidor DHCP, a caixa de texto encontra-se vazia!", parent=parent)
        return

    #Verificação da interface de saida
    validacao_interface = validar_se_interface_pode_ser_usada(interface_entry,ip_address_var,authorization,parent)
    if not validacao_interface['flag']:
        messagebox.showerror("Erro",f"{validacao_interface['message']}", parent=parent)
        return
    
    #Verificação se o tempo colocado encontra-se no formato correto
    validacao_lease_time = validar_lease_time(lease_time_hour_entry,lease_time_minute_entry,lease_time_second_entry)
    if not validacao_lease_time['flag']:
        messagebox.showerror("Erro",f"{validacao_lease_time['message']}", parent=parent)
        return

    #Verificação se os pools Ranges se encontram prenchidos ou não
    flag_pools = False
    if pool_enderecos_first_entry.cget('fg') != "grey" or pool_enderecos_second_entry.cget('fg') != "grey":
        
        #Verificação se foi fornecido um endereço IP válido para o inicio do Pool Range 
        if not validar_string_its_ip(pool_enderecos_first_entry.get()):
            messagebox.showerror("Erro","Não foi dado um endereço IP válido para o inicio do pool Range!", parent=parent)
            return
        
        #Verificação se foi fornecido um endereço IP válido para o fim do Pool Range
        if not validar_string_its_ip(pool_enderecos_second_entry.get()):
            messagebox.showerror("Erro","Não foi dado um endereço IP válido para o fim do pool Range!", parent=parent)
            return

        #Verificação se o primeiro IP colocado é menor que o segundo IP colocado
        if not validar_ip_a_menor_que_ip_b(pool_enderecos_first_entry.get(),pool_enderecos_second_entry.get()):
            messagebox.showerror("Erro","O primeiro IP do Range é maior que o ultimo IP do Range!", parent=parent)
            return
        
        flag_pools = True


    flag_network = False
    if network_entry.cget('fg') != "grey" or gateway_entry.cget('fg') != "grey" or dns_entry.cget('fg') != "grey":
        
        #Valida se a network colocada se encontra correta
        validacao_network = validar_network(network_entry.get(),pool_enderecos_first_entry.get(),pool_enderecos_second_entry.get())
        if not validacao_network['flag']:
            messagebox.showerror("Erro",f"{validacao_network['message']}", parent=parent)
            return
        
        validacao_gateway = validar_gateway(gateway_entry.get(),network_entry.get())
        if not validacao_gateway['flag']:
            messagebox.showerror("Erro",f"{validacao_gateway['message']}", parent=parent)
            return
        
        validacao_dns = validar_dns(dns_entry.get())
        if not validacao_dns['flag']:
            messagebox.showerror("Erro",f"{validacao_dns['message']}", parent=parent)
            return
        
        flag_network = True
    



    try:
        headers = {'Authorization': 'Basic ' + authorization}
        if flag_pools:
            #Criação da POOL para o servidor
            nome_pool = f"pool_{name_server_dhcp_entry.get()}"

            url = f"http://{ip_address_var.get()}/rest/ip/pool"
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            pools = response.json()

            for item in pools:
                if item['name'] == nome_pool:
                    nome_pool += f"_{str(random.randint(1000,9999))}"
                    break
            
            url = f"http://{ip_address_var.get()}/rest/ip/pool/add"
            data = {
                'name' : nome_pool,
                'ranges' : f"{pool_enderecos_first_entry.get()}-{pool_enderecos_second_entry.get()}"
            }
            response = requests.post(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
        
        #Criação do Servidor DHCP
        url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server?.proplist=name"
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        name_dhcp_servers = response.json()
        nome_servidor = f"{name_server_dhcp_entry.get()}"

        for item in name_dhcp_servers:
            if item['name'] == name_server_dhcp_entry.get():
                messagebox.showerror("Erro","O nome escolhido para o servidor já existe",parent=parent)
                return
        
        url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/add"
        
        valor_nome_pool_endercos = "static-only" if not flag_pools else nome_pool

        data = {
            'name' : nome_servidor,
            'interface': interface_entry.get(),
            'lease-time': f"{lease_time_hour_entry.get()}h{lease_time_minute_entry.get()}m{lease_time_second_entry.get()}s",
            'address-pool': valor_nome_pool_endercos
        }
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()

        if flag_network:
            url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/network"
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            networks = response.json()
            flag_patch = False

            for item in networks:
                if network_entry.get() == item['address']:
                    id_network = item['.id']
                    flag_patch = True
                    break
            
            if flag_patch:
                url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/network/{id_network}"
                data = {
                    "address": network_entry.get(),
                    "dns-server": dns_entry.get(),
                    "gateway": gateway_entry.get()
                }
                response = requests.patch(url, headers=headers, json=data, verify=False)
                response.raise_for_status()
            else:
                url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/network/add"
                data = {
                    "address": network_entry.get(),
                    "dns-server": dns_entry.get(),
                    "gateway": gateway_entry.get()
                }
                response = requests.post(url, headers=headers, json=data, verify=False)
                response.raise_for_status()

        messagebox.showinfo("Servidor DHCP criado",f"O servidor DHCP {name_server_dhcp_entry.get()} foi criado com sucesso", parent=parent)

        get_servidores_DHCP(ip_address_var, authorization, listbox, tk, parent, labels_frame, new_buttons, old_buttons)
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def editar_servidor_dhcp(ip_address_var, authorization, listbox, tk, parent,labels_frame, new_buttons, old_buttons):
    
    def on_entry_click(event, entry, text):
        """function that gets called whenever entry is clicked"""
        if entry.get() == text:
            entry.delete(0, "end") # delete all the text in the entry
            entry.insert(0, '') #Insert blank for user input
            entry.config(fg = 'black')

    def on_focusout(event, entry, text):
        if entry.get() == '':
            entry.insert(0, text)
            entry.config(fg = 'grey')

    def close():
        dhcp_window.destroy()

    def update_servidor_dhcp(parent,parent_edit,name_server_entry,network_of_dhcp,pool,dhcp_server,interface_entry,lease_time_hour_entry,lease_time_minute_entry,lease_time_second_entry,pool_enderecos_first_entry,pool_enderecos_second_entry,network_entry,gateway_entry,dns_entry,labels_frame, new_buttons, old_buttons):


        #Verificar o nome do servidor DHCP é válido
        if name_server_entry.cget('fg') == "grey":
            messagebox.showerror("Erro","Não foi dado nenhum nome ao servidor DHCP, a caixa de texto encontra-se vazia!", parent=parent_edit)
            return
        
        #Verifica se o nome escolhido não está já em a ser usado por outro servidor
        try:
            url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server?.proplist=name"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            name_dhcp_servers = response.json()

            for item in name_dhcp_servers:
                if item['name'] == name_server_entry.get() and item['name'] != dhcp_server['name']:
                    messagebox.showerror("Erro","O nome escolhido para o servidor já está a ser usado por outro servidor",parent=parent_edit)
                    return

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent_edit)
        
        #Verifica se a interface pode ser usada
        if interface_entry.cget('fg') == "grey":
            messagebox.showerror("Erro","A interface não se econtra com nenhum nome!", parent=parent_edit)
            return
        
        try:
            #Se a interface não existir no equipamento
            url = f"http://{ip_address_var.get()}/rest/interface?.proplist=name"
            headers = {'Authorization': 'Basic '+ authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            all_interfaces = response.json()
            flag_interface = True

            for item in all_interfaces:
                if interface_entry.get() == item['name']:
                    flag_interface = False
            
            if flag_interface:
                messagebox.showerror("Erro","Não existe nenhuma interface com o nome inserido!", parent=parent_edit)
                return

            #Se a interface já estiver a ser usada por outro servidor DHCP
            url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server?.proplist=interface"
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            interfaces_dhcp_servers = response.json()

            for item in interfaces_dhcp_servers:
                if item['interface'] == interface_entry.get() and item['interface'] != dhcp_server['interface']:
                    messagebox.showerror("Erro","A interface escolhida já está a ser usada por outro servidor DHCP!", parent=parent_edit)
                    return
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent_edit)

        #Validação do tempo inserido pelo utilizador
        validacao_lease_time = validar_lease_time(lease_time_hour_entry,lease_time_minute_entry,lease_time_second_entry)
        if not validacao_lease_time['flag']:
            messagebox.showerror("Erro",f"{validacao_lease_time['message']}", parent=parent_edit)
            return
        
        #Verificação se os pools Ranges se encontram prenchidos ou não
        flag_pools = False
        if pool_enderecos_first_entry.cget('fg') != "grey" or pool_enderecos_second_entry.cget('fg') != "grey":
            
            #Verificação se foi fornecido um endereço IP válido para o inicio do Pool Range 
            if not validar_string_its_ip(pool_enderecos_first_entry.get()):
                messagebox.showerror("Erro","Não foi dado um endereço IP válido para o inicio do pool Range!", parent=parent_edit)
                return
            
            #Verificação se foi fornecido um endereço IP válido para o fim do Pool Range
            if not validar_string_its_ip(pool_enderecos_second_entry.get()):
                messagebox.showerror("Erro","Não foi dado um endereço IP válido para o fim do pool Range!", parent=parent_edit)
                return

            #Verificação se o primeiro IP colocado é menor que o segundo IP colocado
            if not validar_ip_a_menor_que_ip_b(pool_enderecos_first_entry.get(),pool_enderecos_second_entry.get()):
                messagebox.showerror("Erro","O primeiro IP do Range é maior que o ultimo IP do Range!", parent=parent_edit)
                return
            
            flag_pools = True

        #Verificação da network
        flag_network = False
        if network_entry.cget('fg') != "grey" or gateway_entry.cget('fg') != "grey" or dns_entry.cget('fg') != "grey":
            
            #Valida se a network colocada se encontra correta
            validacao_network = validar_network(network_entry.get(),pool_enderecos_first_entry.get(),pool_enderecos_second_entry.get())
            if not validacao_network['flag']:
                messagebox.showerror("Erro",f"{validacao_network['message']}", parent=parent_edit)
                return
            
            validacao_gateway = validar_gateway(gateway_entry.get(),network_entry.get())
            if not validacao_gateway['flag']:
                messagebox.showerror("Erro",f"{validacao_gateway['message']}", parent=parent_edit)
                return
            
            validacao_dns = validar_dns(dns_entry.get())
            if not validacao_dns['flag']:
                messagebox.showerror("Erro",f"{validacao_dns['message']}", parent=parent_edit)
                return
            
            flag_network = True
        
        try:
            headers = {'Authorization': 'Basic ' + authorization}
            if flag_pools:
                if len(pool) == 0:
                    #Criação da POOL para o servidor
                    nome_pool = f"pool_{name_server_entry.get()}"

                    url = f"http://{ip_address_var.get()}/rest/ip/pool"
                    response = requests.get(url, headers=headers, verify=False)
                    response.raise_for_status()
                    pools = response.json()

                    for item in pools:
                        if item['name'] == nome_pool and item['name'] != pool['name']:
                            nome_pool += f"_{str(random.randint(1000,9999))}"
                            break
                    
                    url = f"http://{ip_address_var.get()}/rest/ip/pool/add"
                    data = {
                        'name' : nome_pool,
                        'ranges' : f"{pool_enderecos_first_entry.get()}-{pool_enderecos_second_entry.get()}"
                    }
                    response = requests.post(url, headers=headers, json=data, verify=False)
                    response.raise_for_status()
                else:
                    #Atualização da POOL para o servidor
                    nome_pool = f"pool_{name_server_entry.get()}"

                    url = f"http://{ip_address_var.get()}/rest/ip/pool"
                    response = requests.get(url, headers=headers, verify=False)
                    response.raise_for_status()
                    pools = response.json()

                    for item in pools:
                        if item['name'] == nome_pool and item['name'] != pool['name']:
                            nome_pool += f"_{str(random.randint(1000,9999))}"
                            break
                    
                    url = f"http://{ip_address_var.get()}/rest/ip/pool/{pool['name']}"
                    data = {
                        'name' : nome_pool,
                        'ranges' : f"{pool_enderecos_first_entry.get()}-{pool_enderecos_second_entry.get()}"
                    }
                    response = requests.put(url, headers=headers, json=data, verify=False)
                    response.raise_for_status()
            
            #Atualização do Servidor DHCP
            url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server?.proplist=name"
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            name_dhcp_servers = response.json()
            nome_servidor = f"{name_server_entry.get()}"

            for item in name_dhcp_servers:
                if item['name'] == name_server_entry.get() and item['name'] != dhcp_server['name']:
                    messagebox.showerror("Erro","O nome escolhido para o servidor já existe",parent=parent_edit)
                    return
            
            url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/{dhcp_server['name']}"

            valor_nome_pool_endercos = "static-only" if not flag_pools else nome_pool

            data = {
                'name' : nome_servidor,
                'interface': interface_entry.get(),
                'lease-time': f"{lease_time_hour_entry.get()}h{lease_time_minute_entry.get()}m{lease_time_second_entry.get()}s",
                'address-pool': valor_nome_pool_endercos
            }

            response = requests.put(url, headers=headers, json=data, verify=False)
            response.raise_for_status()

            if flag_network:
                url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/network"
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                networks = response.json()
                flag_patch = False

                for item in networks:
                    if network_entry.get() == item['address']:
                        id_network = item['.id']
                        flag_patch = True
                        break

                if flag_patch:
                    url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/network/{id_network}"
                    data = {
                        "address": network_entry.get(),
                        "dns-server": dns_entry.get(),
                        "gateway": gateway_entry.get()
                    }
                    response = requests.patch(url, headers=headers, json=data, verify=False)
                    response.raise_for_status()
                else:
                    url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/network/add"
                    data = {
                        "address": network_entry.get(),
                        "dns-server": dns_entry.get(),
                        "gateway": gateway_entry.get()
                    }
                    response = requests.post(url, headers=headers, json=data, verify=False)
                    response.raise_for_status()
            
            messagebox.showinfo("Servidor DHCP atualizado",f"O servidor DHCP {name_server_entry.get()} foi atualizado com sucesso", parent=parent_edit)

            get_servidores_DHCP(ip_address_var, authorization, listbox, tk, parent, labels_frame, new_buttons, old_buttons)

            close()
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)


    #Verifica se foi selecionado algum objeto da listbox
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum servidor DHCP !", parent=parent)
        return
    
    item = ""
    item = listbox.get(index)

    #Criação da janela para ediatr sevidores DHCP
    dhcp_window = tk.Toplevel(parent)
    #dhcp_window.title(f"Servidor {item.title().split("Nome: ")[1].split("; Interface")[0]}")
    dhcp_window.geometry("640x480")
    parent_edit = dhcp_window

    #variaveis que vão receber os valores do servidor dhcp que vai ser editado
    dhcp_server = {}
    pool = {}
    network_of_dhcp = {}
    try:
        id_value = item.split("ID:")[1].split(";")[0].strip()
        url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/{id_value}"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        dhcp_server = response.json()

        if dhcp_server['address-pool'] != "static-only":
            url = f"http://{ip_address_var.get()}/rest/ip/pool/{dhcp_server['address-pool']}"
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            pool = response.json()

            url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/network"
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            networks = response.json()

            for network in networks:
                if ipaddress.ip_address(pool["ranges"].split("-")[0]) in ipaddress.ip_network(network['address']):
                    network_of_dhcp = network
                    break

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent_edit)

    entry_frame = tk.Frame(dhcp_window)
    entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    name_server_label = tk.Label(entry_frame, text="Nome Servidor DHCP:")
    name_server_label.grid(row=0, column=0, padx=5, pady=5)

    name_server_entry = tk.Entry(entry_frame)
    name_server_entry.bind('<FocusIn>', lambda event: on_entry_click(event,name_server_entry,"Ex: Servidor DHCP"))
    name_server_entry.bind('<FocusOut>', lambda event: on_focusout(event,name_server_entry,"Ex: Servidor DHCP"))
    name_server_entry.grid(row=0, column=1, padx=5, pady=5)
    name_server_entry.insert(tk.END, dhcp_server['name'])

    interface_label = tk.Label(entry_frame, text="Interface de saida:")
    interface_label.grid(row=1, column=0, padx=5, pady=5)

    interface_entry = tk.Entry(entry_frame)
    interface_entry.bind('<FocusIn>', lambda event: on_entry_click(event,interface_entry,"Ex: ether1"))
    interface_entry.bind('<FocusOut>', lambda event: on_focusout(event,interface_entry,"Ex: ether1"))
    interface_entry.grid(row=1, column=1, padx=5, pady=5)
    interface_entry.insert(tk.END, dhcp_server['interface'])

    segundos = "0"
    minutos = "0"
    horas = "0"
    
    if "s" in dhcp_server['lease-time'] and "m" in dhcp_server['lease-time'] and "h" in dhcp_server['lease-time']:
        segundos = dhcp_server['lease-time'].split("m")[1].split("s")[0]
        minutos = dhcp_server['lease-time'].split("h")[1].split("m")[0]
        horas = dhcp_server['lease-time'].split("h")[0]
    elif "s" in dhcp_server['lease-time'] and "h" in dhcp_server['lease-time']:
        horas = dhcp_server['lease-time'].split("h")[0]
        segundos = dhcp_server['lease-time'].split("h")[1].split("s")[0]
    elif "s" in dhcp_server['lease-time'] and "m" in dhcp_server['lease-time']:
        minutos = dhcp_server['lease-time'].split("m")[0]
        segundos = dhcp_server['lease-time'].split("m")[1].split("s")[0]
    elif "m" in dhcp_server['lease-time'] and "h" in dhcp_server['lease-time']:
        horas = dhcp_server['lease-time'].split("h")[0]
        minutos = dhcp_server['lease-time'].split("h")[1].split("m")[0]
    elif "s" in dhcp_server['lease-time']:
        segundos =  dhcp_server['lease-time'].split("s")[0]
    elif "m" in dhcp_server['lease-time']:
        minutos = dhcp_server['lease-time'].split("m")[0]
    elif "h" in dhcp_server['lease-time']:
        horas = dhcp_server['lease-time'].split("h")[0]

    lease_time_label = tk.Label(entry_frame, text="Tempo de Duração dos IPs:")
    lease_time_label.grid(row=0, column=2, padx=5, pady=5 )

    lease_time_hour_entry = tk.Entry(entry_frame,width=3)
    lease_time_hour_entry.bind('<FocusIn>', lambda event: on_entry_click(event,lease_time_hour_entry,"01"))
    lease_time_hour_entry.bind('<FocusOut>', lambda event: on_focusout(event,lease_time_hour_entry,"01"))
    lease_time_hour_entry.grid(row=0, column=3, padx=5, pady=5)
    lease_time_hour_entry.insert(tk.END, horas)

    two_points_1_label = tk.Label(entry_frame, text=":")
    two_points_1_label.grid(row=0, column=4, padx=5, pady=5)

    lease_time_minute_entry = tk.Entry(entry_frame,width=3)
    lease_time_minute_entry.bind('<FocusIn>', lambda event: on_entry_click(event,lease_time_minute_entry,"01"))
    lease_time_minute_entry.bind('<FocusOut>', lambda event: on_focusout(event,lease_time_minute_entry,"01"))
    lease_time_minute_entry.grid(row=0, column=5, padx=5, pady=5)
    lease_time_minute_entry.insert(tk.END, minutos)

    two_points_2_label = tk.Label(entry_frame, text=":")
    two_points_2_label.grid(row=0, column=6, padx=5, pady=5)

    lease_time_second_entry = tk.Entry(entry_frame,width=3)
    lease_time_second_entry.bind('<FocusIn>', lambda event: on_entry_click(event,lease_time_second_entry,"01"))
    lease_time_second_entry.bind('<FocusOut>', lambda event: on_focusout(event,lease_time_second_entry,"01"))
    lease_time_second_entry.grid(row=0, column=7, padx=5, pady=5)
    lease_time_second_entry.insert(tk.END, segundos)

    network_label = tk.Label(entry_frame, text="Rede :")
    network_label.grid(row=2, column=0, padx=5, pady=5 )

    network_entry = tk.Entry(entry_frame)
    if len(network_of_dhcp) == 0:
        network_entry.insert(tk.END,"Ex: 192.168.1.0/24")
        network_entry.config(fg='grey')
    else:
        network_entry.insert(tk.END,network_of_dhcp['address'])
    network_entry.bind('<FocusIn>', lambda event: on_entry_click(event,network_entry,"Ex: 192.168.1.0/24"))
    network_entry.bind('<FocusOut>', lambda event: on_focusout(event,network_entry,"Ex: 192.168.1.0/24"))
    network_entry.grid(row=2, column=1, padx=5, pady=5)

    gateway_label = tk.Label(entry_frame, text="Gateway :")
    gateway_label.grid(row=3, column=0, padx=5, pady=5 )

    gateway_entry = tk.Entry(entry_frame)
    if len(network_of_dhcp) == 0:
        gateway_entry.insert(tk.END,"Ex: 192.168.1.254")
        gateway_entry.config(fg='grey')
    else:
        gateway_entry.insert(tk.END,network_of_dhcp['gateway'])
    gateway_entry.bind('<FocusIn>', lambda event: on_entry_click(event,gateway_entry,"Ex: 192.168.1.254"))
    gateway_entry.bind('<FocusOut>', lambda event: on_focusout(event,gateway_entry,"Ex: 192.168.1.254"))
    gateway_entry.grid(row=3, column=1, padx=5, pady=5)

    dns_label = tk.Label(entry_frame, text="DNS :")
    dns_label.grid(row=4, column=0, padx=5, pady=5 )

    dns_entry = tk.Entry(entry_frame)
    if len(network_of_dhcp) == 0:
        dns_entry.insert(tk.END,"Ex: 8.8.8.8")
        dns_entry.config(fg='grey')
    else:
        dns_entry.insert(tk.END,network_of_dhcp['dns-server'])
    dns_entry.bind('<FocusIn>', lambda event: on_entry_click(event,dns_entry,"Ex: 8.8.8.8"))
    dns_entry.bind('<FocusOut>', lambda event: on_focusout(event,dns_entry,"Ex: 8.8.8.8"))
    dns_entry.grid(row=4, column=1, padx=5, pady=5)

    pool_enderecos_label = tk.Label(entry_frame, text="Pool Endereços:")
    pool_enderecos_label.grid(row=5, column=0, padx=5, pady=5)

    pool_enderecos_first_entry = tk.Entry(entry_frame)
    if len(pool) == 0:
        pool_enderecos_first_entry.insert(tk.END,"Ex: 192.168.1.1")
        pool_enderecos_first_entry.config(fg='grey')
    else:
        pool_enderecos_first_entry.insert(tk.END,pool['ranges'].split("-")[0])
    pool_enderecos_first_entry.bind('<FocusIn>', lambda event: on_entry_click(event,pool_enderecos_first_entry,"Ex: 192.168.1.1"))
    pool_enderecos_first_entry.bind('<FocusOut>', lambda event: on_focusout(event,pool_enderecos_first_entry,"Ex: 192.168.1.1"))
    pool_enderecos_first_entry.grid(row=5, column=1, padx=5, pady=5)

    pool_enderecos_second_entry = tk.Entry(entry_frame)
    if len(pool) == 0:
        pool_enderecos_second_entry.insert(tk.END,"Ex: 192.168.1.253")
        pool_enderecos_second_entry.config(fg='grey')
    else:
        pool_enderecos_second_entry.insert(tk.END,pool['ranges'].split("-")[1])
    pool_enderecos_second_entry.bind('<FocusIn>', lambda event: on_entry_click(event,pool_enderecos_second_entry,"Ex: 192.168.1.253"))
    pool_enderecos_second_entry.bind('<FocusOut>', lambda event: on_focusout(event,pool_enderecos_second_entry,"Ex: 192.168.1.253"))
    pool_enderecos_second_entry.grid(row=5, column=2, padx=5, pady=5)

    button_frame = tk.Frame(dhcp_window)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)

    right_button_frame = tk.Frame(button_frame)
    right_button_frame.pack(side=tk.RIGHT)
    
    ok_button = tk.Button(right_button_frame, text="Ok", command=lambda: update_servidor_dhcp(parent,parent_edit,name_server_entry,network_of_dhcp,pool,dhcp_server,interface_entry,lease_time_hour_entry,lease_time_minute_entry,lease_time_second_entry,pool_enderecos_first_entry,pool_enderecos_second_entry,network_entry,gateway_entry,dns_entry,labels_frame, new_buttons, old_buttons))
    ok_button.grid(row=0, column=0, padx=2, pady=2)
    
    close_button = tk.Button(right_button_frame, text="Fechar", command=close)
    close_button.grid(row=0, column=1, padx=2, pady=2)

    return

def eliminar_servidor_dhcp(ip_address_var, authorization, listbox, tk, parent,labels_frame, new_buttons, old_buttons):
    #Eliminar servidor dhcp
    #1-COMEÇAR A ELIMINAR A NETWORK CASO EXISTA
    #2-ELIMINAR O SERVIDOR DHCP
    #3-ELIMINAR A POOL

    #Verifica se foi selecionado algum objeto da listbox
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum servidor DHCP !", parent=parent)
        return
    
    item = ""
    item = listbox.get(index)

    name_of_server = item.split("Nome:")[1].split(";")[0].strip()

    #Verificar se o utilizador pretende mesmo eliminar o servidor DHCP
    confirmacao = messagebox.askquestion(f"Eliminar servidor DHCP '{name_of_server}'",f"Tem a certeza que pretende eliminar o servidor DHCP '{name_of_server}' ?", parent=parent)
    if confirmacao == "no":
        return

    #variaveis que vão receber os valores do servidor dhcp que vai ser editado
    dhcp_server = {}
    pool = {}
    network_of_dhcp = {}
    try:
        id_value = item.split("ID:")[1].split(";")[0].strip()
        url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/{id_value}"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        dhcp_server = response.json()

        if dhcp_server['address-pool'] != "static-only":
            url = f"http://{ip_address_var.get()}/rest/ip/pool/{dhcp_server['address-pool']}"
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            pool = response.json()

            url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/network"
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            networks = response.json()

            for network in networks:
                if ipaddress.ip_address(pool["ranges"].split("-")[0]) in ipaddress.ip_network(network['address']):
                    network_of_dhcp = network
                    break
            
            if len(network_of_dhcp) != 0:
                url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/network/{network_of_dhcp['.id']}"
                response = requests.delete(url, headers=headers, verify=False)
                response.raise_for_status()

            url = f"http://{ip_address_var.get()}/rest/ip/pool/{pool['.id']}"
            response = requests.delete(url, headers=headers, verify=False)
            response.raise_for_status()

       
        url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server/{id_value}"
        response = requests.delete(url, headers=headers, verify=False)
        response.raise_for_status()
        messagebox.showinfo("Servidor DHCP eliminado com sucesso",f"O servidor DHCP '{name_of_server}' foi eliminado com sucesso do router!", parent=parent )

        get_servidores_DHCP(ip_address_var, authorization, listbox, tk, parent, labels_frame, new_buttons, old_buttons)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def get_entradas_DNS(ip_address_var, authorization, listbox, tk, parent, labels_frame, new_buttons, old_buttons):
    for button in old_buttons:
        button.grid_forget()
        del button
    
    nome_label = tk.Label(labels_frame, text="Nome*:")
    nome_label.grid(row=0, column=0, padx=5, pady=5)
    old_buttons.append(nome_label)
    nome_entry = tk.Entry(labels_frame)
    nome_entry.grid(row=0, column=1, padx=5, pady=5)
    old_buttons.append(nome_entry)
    address_label = tk.Label(labels_frame, text="Valor*:")
    address_label.grid(row=1, column=0, padx=5, pady=5)
    old_buttons.append(address_label)
    address_entry = tk.Entry(labels_frame)
    address_entry.grid(row=1, column=1, padx=5, pady=5)
    old_buttons.append(address_entry)
    desativar_value = tk.BooleanVar()
    desativar_button = tk.Checkbutton(labels_frame, text="Endereço desativado", variable=desativar_value)
    desativar_button.grid(row=2, column=0, padx=5, pady=5)
    old_buttons.append(desativar_button)
    ttl_label = tk.Label(labels_frame, text="TTL:")
    ttl_label.grid(row=0, column=2, padx=5, pady=5)
    old_buttons.append(ttl_label)
    ttl_entry = tk.Entry(labels_frame)
    ttl_entry.grid(row=0, column=3, padx=5, pady=5)
    old_buttons.append(ttl_entry)
    comment_label = tk.Label(labels_frame, text="Comentário:")
    comment_label.grid(row=1, column=2, padx=5, pady=5)
    old_buttons.append(comment_label)
    comment_entry = tk.Entry(labels_frame)
    comment_entry.grid(row=1, column=3, padx=5, pady=5)
    old_buttons.append(comment_entry)

    type_label = tk.Label(labels_frame, text="Tipo:")
    type_label.grid(row=2, column=2, padx=5, pady=5)
    old_buttons.append(type_label)
    options = ["A", "AAAA", "CNAME", "MX", "FWD"]
    pre_filled_value = "A"
    selected_option = tk.StringVar()
    combobox = ttk.Combobox(labels_frame, textvariable=selected_option, values=options)
    try:
        pre_filled_index = options.index(pre_filled_value)
        combobox.current(pre_filled_index)  # Set the pre-filled value
    except ValueError:
        pass
    combobox.grid(row=2, column=3, padx=5, pady=5)
    old_buttons.append(combobox)

    configurar_button = tk.Button(labels_frame, text="Configurar Servidor de DNS", command=lambda: editar_servidor_DNS(ip_address_var, authorization, tk, parent))
    configurar_button.grid(row=0, column=4, padx=5, pady=5)
    old_buttons.append(configurar_button)

    new_buttons[0].grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    new_buttons[0].config(command=lambda: criar_entradas_DNS(ip_address_var, authorization, listbox, tk, parent, nome_entry, address_entry, desativar_value, desativar_button, ttl_entry, comment_entry, selected_option))
    old_buttons.append(new_buttons[0])
    new_buttons[1].grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    new_buttons[1].config(command=lambda: editar_entradas_DNS(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[1])
    new_buttons[2].grid(row=0, column=2, padx=2, pady=2, sticky=tk.SW)
    new_buttons[2].config(command=lambda: eliminar_entradas_DNS(ip_address_var, authorization, listbox, tk, parent))
    old_buttons.append(new_buttons[2])

    def on_double_click(event):
        index = listbox.curselection()
        if index :
            item = listbox.get(index)
            item = item.strip()
            try:
                id_value = item.split("ID:")[1].split(";")[0].strip()
                url = f"http://{ip_address_var.get()}/rest/ip/dns/static/{id_value}"
                headers = {'Authorization': 'Basic ' + authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                dns_entry = response.json()
                string_text_box = ""
                for key, value in dns_entry.items():
                    string_text_box += f"{key}: {value}\n"
                messagebox.showinfo(f"{item}", string_text_box, parent=parent)
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    try:
        url = f"http://{ip_address_var.get()}/rest/ip/dns/static"
        headers = {'Authorization': 'Basic ' + authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        dns_entries = response.json()
        string_dns_entries = []
        for entry in dns_entries:
            if 'type' not in entry:
                string_dns_entries.append(f"ID: {entry['.id']}; Tipo: A; Nome: {entry['name']}; Endereço: {entry['address']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
            elif entry['type'] == 'AAAA':
                string_dns_entries.append(f"ID: {entry['.id']}; Tipo: AAAA; Nome: {entry['name']}; Endereço: {entry['address']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
            elif entry['type'] == 'CNAME':
                string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; CNAME: {entry['cname']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
            elif entry['type'] == 'FWD':
                string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; Forward-To: {entry['forward-to']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
            elif entry['type'] == 'MX':
                string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; MX-Exchange: {entry['mx-exchange']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
            else:
                string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
        show_in_list(string_dns_entries, listbox, tk)
        listbox.bind("<Double-Button-1>", on_double_click)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def editar_servidor_DNS(ip_address_var_temp, authorization, tk, parent):
    def update_servidor_DNS():
        try:
            url = f"http://{ip_address_var.get()}/rest/ip/dns/set"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {}
            data['max-udp-packet-size'] = max_udp_packet_size_entry.get().replace(" ", "")
            data['query-server-timeout'] = query_server_timeout_entry.get().replace(" ", "")
            data['query-total-timeout'] = query_total_timeout_entry.get().replace(" ", "")
            data['max-concurrent-queries'] = max_concurrent_queries_entry.get().replace(" ", "")
            data['max-concurrent-tcp-sessions'] = max_concurrent_tcp_sessions_entry.get().replace(" ", "")
            data['cache-size'] = cache_size_entry.get().replace(" ", "")
            data['cache-max-ttl'] = cache_max_ttl_entry.get().replace(" ", "")
            if ativar_value.get() and allow_remote_requests:
                data['allow-remote-requests'] = False
            if ativar_value.get() and not allow_remote_requests:
                data['allow-remote-requests'] = True
            string_servers = ""
            count = 0
            for server in servers_buttons:
                if not server.get():
                    string_servers += f"{servers_array[count]},"
                count += 1
            string_servers += adicionar_servidores_entry.get().replace(" ", "")
            if len(string_servers) > 0:
                if string_servers[-1] == ',':
                    string_servers = string_servers[:-1]
            data['servers'] = string_servers
            response = requests.post(url, json=data, headers=headers, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Successo", "O Servidor de DNS foi atualizado com sucesso.", parent=parent)
            close()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    def close():
        address_window.destroy()

    address_window = tk.Toplevel(parent)
    address_window.title(f"Editar Servidor de DNS")
    address_window.geometry("640x480")
    parent = address_window
    ip_address_var = tk.StringVar(address_window)
    authorization_var = tk.StringVar(address_window)
    ip_address_var.set(f"{ip_address_var_temp.get()}")
    authorization_var.set(f"{authorization}")
    authorization = authorization_var.get()
    
    allow_remote_requests = False
    try:
        url = f"http://{ip_address_var.get()}/rest/ip/dns"
        headers = {'Authorization': 'Basic ' + authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        dns_server = response.json()
        print(dns_server)
        if dns_server['allow-remote-requests'] == 'true':
            allow_remote_requests = dns_server['allow-remote-requests']
        max_udp_packet_size = dns_server['max-udp-packet-size']
        query_server_timeout = dns_server['query-server-timeout']
        query_total_timeout = dns_server['query-total-timeout']
        max_concurrent_queries = dns_server['max-concurrent-queries']
        max_concurrent_tcp_sessions = dns_server['max-concurrent-tcp-sessions']
        cache_size = dns_server['cache-size']
        cache_max_ttl = dns_server['cache-max-ttl']
        cache_used = dns_server['cache-used']
        dynamic_servers = dns_server['dynamic-servers']
        servers = dns_server['servers']
        servers_array = servers.split(',')
        print(servers_array)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    entry_frame = tk.Frame(address_window)
    entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    max_udp_packet_size_label = tk.Label(entry_frame, text="Max UDP Packet Size:")
    max_udp_packet_size_label.grid(row=0, column=0, padx=5, pady=5)
    max_udp_packet_size_entry = tk.Entry(entry_frame)
    max_udp_packet_size_entry.grid(row=0, column=1, padx=5, pady=5)
    max_udp_packet_size_entry.insert(tk.END, max_udp_packet_size)
    query_server_timeout_label = tk.Label(entry_frame, text="Query Server Timeout:")
    query_server_timeout_label.grid(row=1, column=0, padx=5, pady=5)
    query_server_timeout_entry = tk.Entry(entry_frame)
    query_server_timeout_entry.grid(row=1, column=1, padx=5, pady=5)
    query_server_timeout_entry.insert(tk.END, query_server_timeout)
    query_total_timeout_label = tk.Label(entry_frame, text="Query Total Timeout:")
    query_total_timeout_label.grid(row=2, column=0, padx=5, pady=5)
    query_total_timeout_entry = tk.Entry(entry_frame)
    query_total_timeout_entry.grid(row=2, column=1, padx=5, pady=5)
    query_total_timeout_entry.insert(tk.END, query_total_timeout)
    max_concurrent_queries_label = tk.Label(entry_frame, text="Max. Concurrent Queries:")
    max_concurrent_queries_label.grid(row=3, column=0, padx=5, pady=5)
    max_concurrent_queries_entry = tk.Entry(entry_frame)
    max_concurrent_queries_entry.grid(row=3, column=1, padx=5, pady=5)
    max_concurrent_queries_entry.insert(tk.END, max_concurrent_queries)
    max_concurrent_tcp_sessions_label = tk.Label(entry_frame, text="Max. Concurrent TCP Sessions:")
    max_concurrent_tcp_sessions_label.grid(row=4, column=0, padx=5, pady=5)
    max_concurrent_tcp_sessions_entry = tk.Entry(entry_frame)
    max_concurrent_tcp_sessions_entry.grid(row=4, column=1, padx=5, pady=5)
    max_concurrent_tcp_sessions_entry.insert(tk.END, max_concurrent_tcp_sessions)
    cache_size_label = tk.Label(entry_frame, text="Cache Size:")
    cache_size_label.grid(row=5, column=0, padx=5, pady=5)
    cache_size_entry = tk.Entry(entry_frame)
    cache_size_entry.grid(row=5, column=1, padx=5, pady=5)
    cache_size_entry.insert(tk.END, cache_size)
    cache_max_ttl_label = tk.Label(entry_frame, text="Cache Max TTL:")
    cache_max_ttl_label.grid(row=6, column=0, padx=5, pady=5)
    cache_max_ttl_entry = tk.Entry(entry_frame)
    cache_max_ttl_entry.grid(row=6, column=1, padx=5, pady=5)
    cache_max_ttl_entry.insert(tk.END, cache_max_ttl)
    cache_used_label = tk.Label(entry_frame, text="Cache Used:")
    cache_used_label.grid(row=7, column=0, padx=5, pady=5)
    cache_used_label = tk.Label(entry_frame, text=cache_used)
    cache_used_label.grid(row=7, column=1, padx=5, pady=5)
    dynamic_servers_label = tk.Label(entry_frame, text="Dynamic Servers:")
    dynamic_servers_label.grid(row=8, column=0, padx=5, pady=5)
    dynamic_servers_label = tk.Label(entry_frame, text=dynamic_servers)
    dynamic_servers_label.grid(row=8, column=1, padx=5, pady=5)

    ativar_value = tk.BooleanVar()
    if not allow_remote_requests:
        ativar_button = tk.Checkbutton(entry_frame, text="Permtir pedidos remotos", variable=ativar_value)
        ativar_button.grid(row=9, column=0, padx=5, pady=5)
    else:
        ativar_button = tk.Checkbutton(entry_frame, text="Negar pedidos remotos", variable=ativar_value)
        ativar_button.grid(row=9, column=0, padx=5, pady=5)

    servers_label = tk.Label(entry_frame, text="Eliminar servidores:")
    servers_label.grid(row=10, column=0, padx=5, pady=5)
    servers_buttons = []
    for i in range(0,len(servers_array)):
        servers_buttons.append(tk.BooleanVar())
    pos = 0
    if servers_array[0] != '': 
        for item in servers_array:
            tk.Checkbutton(entry_frame, text=item, variable=servers_buttons[pos]).grid(row=pos+11, column=0, padx=5, pady=5)
            pos += 1

    adicionar_servidores_label = tk.Label(entry_frame, text="Adicionar servidores:")
    adicionar_servidores_label.grid(row=10, column=1, padx=5, pady=5)
    adicionar_servidores_entry = tk.Entry(entry_frame)
    adicionar_servidores_entry.grid(row=11, column=1, padx=5, pady=5)

    button_frame = tk.Frame(address_window)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)
    right_button_frame = tk.Frame(button_frame)
    right_button_frame.pack(side=tk.RIGHT)
    ok_button = tk.Button(right_button_frame, text="Ok", command=lambda: update_servidor_DNS())
    ok_button.grid(row=0, column=0, padx=2, pady=2)
    close_button = tk.Button(right_button_frame, text="Fechar", command=close)
    close_button.grid(row=0, column=1, padx=2, pady=2)

def editar_entradas_DNS(ip_address_var_temp, authorization, listbox, tk, parent):
    def update_entrada_DNS(id_value):
        try:
            type_value = selected_option.get()
            url = f"http://{ip_address_var.get()}/rest/ip/dns/static/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {
                "name": name_entry.get().replace(" ", ""),
                "type": type_value,
            }
            if type_value == 'A' or type_value == 'AAAA':
                data['address'] = valor_entry.get().replace(" ", "")
            elif type_value == 'CNAME':
                data['cname'] = valor_entry.get().replace(" ", "")
            elif type_value == 'FWD':
                data['forward-to'] = valor_entry.get().replace(" ", "")
            elif type_value == 'MX':
                data['mx-exchange'] = valor_entry.get().replace(" ", "")
            if comentario_entry.get("1.0", "end-1c").replace(" ", ""):
                data['comment'] =  comentario_entry.get("1.0", "end-1c")
            if ttl_entry.get().replace(" ", ""):
                data['ttl'] = ttl_entry.get().replace(" ", "")
            if ativar_value.get() and disabled:
                data['disabled'] = False
            if ativar_value.get() and not disabled:
                data['disabled'] = True
            response = requests.put(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Entrada DNS atualizada", "Entrada de DNS atualizada com sucesso", parent=parent )
            url = f"http://{ip_address_var.get()}/rest/ip/dns/static"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            dns_entries = response.json()
            string_dns_entries = []
            for entry in dns_entries:
                if 'type' not in entry:
                    string_dns_entries.append(f"ID: {entry['.id']}; Tipo: A; Nome: {entry['name']}; Endereço: {entry['address']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
                elif entry['type'] == 'AAAA':
                    string_dns_entries.append(f"ID: {entry['.id']}; Tipo: AAAA; Nome: {entry['name']}; Endereço: {entry['address']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
                elif entry['type'] == 'CNAME':
                    string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; CNAME: {entry['cname']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
                elif entry['type'] == 'FWD':
                    string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; Forward-To: {entry['forward-to']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
                elif entry['type'] == 'MX':
                    string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; MX-Exchange: {entry['mx-exchange']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
                else:
                    string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
            show_in_list(string_dns_entries, listbox, tk)
            close()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    def close():
        address_window.destroy()

    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhuma entrada DNS!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()

        address_window = tk.Toplevel(parent)
        address_window.title(f"{item.title()}")
        address_window.geometry("640x480")
        parent = address_window
        ip_address_var = tk.StringVar(address_window)
        authorization_var = tk.StringVar(address_window)
        ip_address_var.set(f"{ip_address_var_temp.get()}")
        authorization_var.set(f"{authorization}")
        authorization = authorization_var.get()

        disabled = False
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var.get()}/rest/ip/dns/static/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            dns_entry = response.json()
            comment_valor = ""
            ttl_valor = ""
            name_valor = dns_entry['name']
            if 'ttl' in dns_entry:
                ttl_valor = dns_entry['ttl']
            if 'comment' in dns_entry:
                comment_valor = dns_entry['comment']
            if 'type' not in dns_entry:
                type_valor = 'A'
            else:
                type_valor = dns_entry['type']
            if dns_entry['disabled'] == 'true':
                disabled = True
            if 'type' not in dns_entry or dns_entry['type'] == 'AAAA':
                value_valor = dns_entry['address']
            elif dns_entry['type'] == 'CNAME':
                value_valor = dns_entry['cname']
            elif dns_entry['type'] == 'FWD':
                value_valor = dns_entry['forward-to']
            elif dns_entry['type'] == 'MX':
                value_valor = dns_entry['mx-exchange']
            if 'type' in dns_entry:
                if type_valor != 'MX' and type_valor != 'AAAA' and type_valor != 'CNAME' and type_valor != 'FWD':
                    messagebox.showerror("Erro","Não é possível editar esta entrada de DNS!\n A aplicação apenas suporta os tipos: MX, AAAA, CNAME, FWD.", parent=parent)
                    close()
                    return
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

        entry_frame = tk.Frame(address_window)
        entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        name_label = tk.Label(entry_frame, text="Nome:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(entry_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(tk.END, name_valor)
        valor_label = tk.Label(entry_frame, text="Valor:")
        valor_label.grid(row=1, column=0, padx=5, pady=5)
        valor_entry = tk.Entry(entry_frame)
        valor_entry.grid(row=1, column=1, padx=5, pady=5)
        valor_entry.insert(tk.END, value_valor)
        ttl_label = tk.Label(entry_frame, text="TTL:")
        ttl_label.grid(row=2, column=0, padx=5, pady=5)
        ttl_entry = tk.Entry(entry_frame)
        ttl_entry.grid(row=2, column=1, padx=5, pady=5)
        ttl_entry.insert(tk.END, ttl_valor)
        
        type_label = tk.Label(entry_frame, text="Tipo:")
        type_label.grid(row=3, column=0, padx=5, pady=5)
        options = ["A", "AAAA", "CNAME", "MX", "FWD"]
        pre_filled_value = type_valor
        selected_option = tk.StringVar()
        combobox = ttk.Combobox(entry_frame, textvariable=selected_option, values=options)
        combobox.set(type_valor)
        pre_filled_index = options.index(pre_filled_value)
        combobox.current(pre_filled_index)
        combobox.grid(row=3, column=1, padx=5, pady=5)

        comentario_label = tk.Label(entry_frame, text="Comentário:")
        comentario_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.N)
        comentario_entry = tk.Text(entry_frame, height=4, width=30)
        comentario_entry.grid(row=4, column=1, padx=5, pady=5)
        comentario_entry.insert(tk.END, comment_valor)

        ativar_value = tk.BooleanVar()
        if not disabled:
            ativar_button = tk.Checkbutton(entry_frame, text="Desativar", variable=ativar_value)
            ativar_button.grid(row=5, column=0, padx=5, pady=5)
        else:
            ativar_button = tk.Checkbutton(entry_frame, text="Ativar", variable=ativar_value)
            ativar_button.grid(row=5, column=0, padx=5, pady=5)

        button_frame = tk.Frame(address_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        right_button_frame = tk.Frame(button_frame)
        right_button_frame.pack(side=tk.RIGHT)
        ok_button = tk.Button(right_button_frame, text="Ok", command=lambda: update_entrada_DNS(id_value))
        ok_button.grid(row=0, column=0, padx=2, pady=2)
        close_button = tk.Button(right_button_frame, text="Fechar", command=close)
        close_button.grid(row=0, column=1, padx=2, pady=2)

def criar_entradas_DNS(ip_address_var, authorization, listbox, tk, parent, nome_entry, address_entry, desativar_value, desativar_button, ttl_entry, comment_entry, selected_option):
    nome_valor = nome_entry.get().replace(" ", "")
    if not nome_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Nome, a caixa de texto encontra-se vazia!", parent=parent)
        return
    address_valor = address_entry.get().replace(" ", "")
    if not address_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Valor, a caixa de texto encontra-se vazia!", parent=parent)
        return
    
    ttl_valor = ttl_entry.get().replace(" ", "")
    comment_valor = comment_entry.get()
    desativado = False
    if desativar_value.get():
        desativado = True

    type_value = selected_option.get()

    try:
        dns_entry_data = {
            "name": nome_valor, 
            "disabled": desativado,
            "type" : type_value
        }
        if type_value == 'A' or type_value == 'AAAA':
            dns_entry_data['address'] = address_valor
        elif type_value == 'CNAME':
            dns_entry_data['cname'] = address_valor
        elif type_value == 'FWD':
            dns_entry_data['forward-to'] = address_valor
        elif type_value == 'MX':
            dns_entry_data['mx-exchange'] = address_valor
        if comment_valor:
            dns_entry_data['comment'] = comment_valor
        if ttl_valor:
            dns_entry_data['ttl'] = ttl_valor
        url = f"http://{ip_address_var.get()}/rest/ip/dns/static/add"
        headers = {'Authorization': 'Basic ' + authorization}
        response = requests.post(url, headers=headers, json=dns_entry_data, verify=False)
        if response.status_code == 200:
            messagebox.showinfo("Entrada DNS criada", "Entrada DNS criada com sucesso", parent=parent )
        url = f"http://{ip_address_var.get()}/rest/ip/dns/static"
        headers = {'Authorization': 'Basic ' + authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        dns_entries = response.json()
        string_dns_entries = []
        for entry in dns_entries:
            if 'type' not in entry:
                string_dns_entries.append(f"ID: {entry['.id']}; Tipo: A; Nome: {entry['name']}; Endereço: {entry['address']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
            elif entry['type'] == 'AAAA':
                string_dns_entries.append(f"ID: {entry['.id']}; Tipo: AAAA; Nome: {entry['name']}; Endereço: {entry['address']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
            elif entry['type'] == 'CNAME':
                string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; CNAME: {entry['cname']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
            elif entry['type'] == 'FWD':
                string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; Forward-To: {entry['forward-to']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
            elif entry['type'] == 'MX':
                string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; MX-Exchange: {entry['mx-exchange']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
            else:
                string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
        show_in_list(string_dns_entries, listbox, tk)
        nome_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        ttl_entry.delete(0, tk.END)
        comment_entry.delete(0, tk.END)
        desativar_button.deselect()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def eliminar_entradas_DNS(ip_address_var, authorization, listbox, tk, parent):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionada nenhuma entrada de DNS!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            confirmacao = messagebox.askquestion(f"Eliminar Entrada de DNS{id_value}",f"Tem a certeza que pretende eliminar a entrada de DNS {id_value} ?", parent=parent)
            if confirmacao == "no":
                return
            delete_url = f"http://{ip_address_var.get()}/rest/ip/dns/static/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.delete(delete_url, headers=headers, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Entrada DNS Apagada", "Entrada DNS apagada com Sucesso", parent=parent)
            url = f"http://{ip_address_var.get()}/rest/ip/dns/static"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            dns_entries = response.json()
            string_dns_entries = []
            for entry in dns_entries:
                if 'type' not in entry:
                    string_dns_entries.append(f"ID: {entry['.id']}; Tipo: A; Nome: {entry['name']}; Endereço: {entry['address']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
                elif entry['type'] == 'AAAA':
                    string_dns_entries.append(f"ID: {entry['.id']}; Tipo: AAAA; Nome: {entry['name']}; Endereço: {entry['address']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
                elif entry['type'] == 'CNAME':
                    string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; CNAME: {entry['cname']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
                elif entry['type'] == 'FWD':
                    string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; Forward-To: {entry['forward-to']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
                elif entry['type'] == 'MX':
                    string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; MX-Exchange: {entry['mx-exchange']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
                else:
                    string_dns_entries.append(f"ID: {entry['.id']}; Tipo: {entry['type']}; Nome: {entry['name']}; TTL: {entry['ttl']}; Desativada: {entry['disabled']}")
                show_in_list(string_dns_entries, listbox, tk)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def cria_wireguard(ip_address_var, authorization, tk, user_window):
    wire_window = tk.Toplevel(user_window)
    wire_window.title(f"Wireguard - Router: {ip_address_var.get()}")
    wire_window.geometry("1280x768")
    parent = wire_window
    
    custom_font = ('Arial', 12)
    left_frame = tk.Frame(wire_window)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    name_left_label = tk.Label(left_frame, text="Servidor", font=custom_font)
    name_left_label.pack(side=tk.TOP)
    left_top_frame = tk.Frame(left_frame)
    left_top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    left_labels_frame = tk.Frame(left_top_frame, bg="light gray")
    left_labels_frame.pack(side=tk.BOTTOM, fill=tk.X)
    left_bot_frame = tk.Frame(left_frame, bg="light gray")
    left_bot_frame.pack(side=tk.BOTTOM, fill=tk.X)
    
    right_frame = tk.Frame(wire_window)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    name_right_label = tk.Label(right_frame, text="Peer", font=custom_font)
    name_right_label.pack(side=tk.TOP)
    right_top_frame = tk.Frame(right_frame)
    right_top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    right_labels_frame = tk.Frame(right_top_frame, bg="light gray")
    right_labels_frame.pack(side=tk.BOTTOM, fill=tk.X)
    right_bot_frame = tk.Frame(right_frame, bg="light gray")
    right_bot_frame.pack(side=tk.BOTTOM, fill=tk.X)

    criar_left_button = tk.Button(left_bot_frame, text="Criar", command=lambda: criar_servidor_wireguard(ip_address_var, authorization, listbox1, tk, parent, name_left_entry, port_entry, comment_entry, desativar_button, desativar_server_value, right_labels_frame, combobox, selected_option_2))
    criar_left_button.grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    editar_left_button = tk.Button(left_bot_frame, text="Editar", command=lambda: editar_servidor_wireguard(ip_address_var, authorization, listbox1, listbox2, tk, parent, interface_names, combobox, selected_option_2, right_labels_frame))
    editar_left_button.grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    apagar_left_button = tk.Button(left_bot_frame, text="Apagar", command=lambda: eliminar_servidor_wireguard(ip_address_var, authorization, listbox1, listbox2, tk, parent, right_labels_frame, combobox, selected_option_2))
    apagar_left_button.grid(row=0, column=2, padx=2, pady=2, sticky=tk.SW)
    gerar_chave_btn = tk.Button(left_bot_frame, text="Gerar nova Chave Privada", command=lambda: gerar_chave_wireguard(ip_address_var, authorization, listbox1, tk, parent))
    gerar_chave_btn.grid(row=0, column=3, padx=2, pady=2, sticky=tk.SW)
    
    criar_right_button = tk.Button(right_bot_frame, text="Criar", command=lambda: criar_peer_wireguard(ip_address_var, authorization, listbox2, tk, parent, selected_option_2, public_key_entry, address_entry, comment_entry_2, desativar_button_2, desativar_peer_value))
    criar_right_button.grid(row=0, column=0, padx=2, pady=2, sticky=tk.SW)
    editar_right_button = tk.Button(right_bot_frame, text="Editar", command=lambda:editar_peer_wireguard(ip_address_var, authorization, listbox2, tk, parent))
    editar_right_button.grid(row=0, column=1, padx=2, pady=2, sticky=tk.SW)
    apagar_right_button = tk.Button(right_bot_frame, text="Apagar", command=lambda: eliminar_peer_wireguard(ip_address_var, authorization, listbox2, tk, parent))
    apagar_right_button.grid(row=0, column=2, padx=2, pady=2, sticky=tk.SW)

    listbox1 = tk.Listbox(left_top_frame, font=("Arial", 12))
    listbox1.pack(expand=True, fill="both", side=tk.TOP)
    listbox2 = tk.Listbox(right_top_frame, font=("Arial", 12))
    listbox2.pack(expand=True, fill="both", side=tk.TOP)

    name_left_label = tk.Label(left_labels_frame, bg="light gray", text="Nome*:")
    name_left_label.grid(row=0, column=0, padx=5, pady=5)
    name_left_entry = tk.Entry(left_labels_frame)
    name_left_entry.grid(row=0, column=1, padx=5, pady=5)
    port_label = tk.Label(left_labels_frame, bg="light gray", text="Porto de escuta:")
    port_label.grid(row=1, column=0, padx=5, pady=5)
    port_entry = tk.Entry(left_labels_frame)
    port_entry.grid(row=1, column=1, padx=5, pady=5)
    comment_label = tk.Label(left_labels_frame, bg="light gray", text="Comentário:")
    comment_label.grid(row=0, column=2, padx=5, pady=5)
    comment_entry = tk.Entry(left_labels_frame)
    comment_entry.grid(row=0, column=3, padx=5, pady=5)
    desativar_server_value = tk.BooleanVar()
    desativar_button = tk.Checkbutton(left_labels_frame, bg="light gray", text="Servidor desativado", variable=desativar_server_value)
    desativar_button.grid(row=1, column=2, padx=5, pady=5)

    def on_double_click_left(event):
        index = listbox1.curselection()
        if index :
            item = listbox1.get(index)
            item = item.strip()
            try:
                id_value = item.split("ID:")[1].split(";")[0].strip()
                url = f"http://{ip_address_var.get()}/rest/interface/wireguard/{id_value}"
                headers = {'Authorization': 'Basic ' + authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                dns_entry = response.json()
                string_text_box = ""
                for key, value in dns_entry.items():
                    string_text_box += f"{key}: {value}\n"
                messagebox.showinfo(f"{item}", string_text_box, parent=parent)
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
    
    def on_double_click_right(event):
        index = listbox2.curselection()
        if index :
            item = listbox2.get(index)
            item = item.strip()
            try:
                id_value = item.split("ID:")[1].split(";")[0].strip()
                url = f"http://{ip_address_var.get()}/rest/interface/wireguard/peers/{id_value}"
                headers = {'Authorization': 'Basic ' + authorization}
                response = requests.get(url, headers=headers, verify=False)
                response.raise_for_status()
                dns_entry = response.json()
                string_text_box = ""
                for key, value in dns_entry.items():
                    string_text_box += f"{key}: {value}\n"
                messagebox.showinfo(f"{item}", string_text_box, parent=parent)
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    interface_names = []
    try:
        url = f"http://{ip_address_var.get()}/rest/interface/wireguard"
        headers = {'Authorization': 'Basic ' + authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        servers_wireguard = response.json()
        print(servers_wireguard)
        string_server_wireguard = []
        for entry in servers_wireguard:
            string_server_wireguard.append(f"ID: {entry['.id']}; Porto: {entry['listen-port']}; Nome: {entry['name']}; Desativado: {entry['disabled']}")
            interface_names.append(f"{entry['name']}")
        show_in_list(string_server_wireguard, listbox1, tk)
        listbox1.bind("<Double-Button-1>", on_double_click_left)
        url = f"http://{ip_address_var.get()}/rest/interface/wireguard/peers"
        headers = {'Authorization': 'Basic ' + authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        peers_wireguard = response.json()
        print(peers_wireguard)
        string_peer_wireguard = []
        for entry in peers_wireguard:
            string_peer_wireguard.append(f"ID: {entry['.id']}; Interface: {entry['interface']}; Desativado: {entry['disabled']}")
        show_in_list(string_peer_wireguard, listbox2, tk)
        listbox2.bind("<Double-Button-1>", on_double_click_right)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
    
    type_label = tk.Label(right_labels_frame, bg="light gray", text="Interface:*")
    type_label.grid(row=0, column=0, padx=5, pady=5)
    options = interface_names
    selected_option_2 = 0
    combobox = 0
    if len(interface_names) > 0:
        pre_filled_value = interface_names[0]
        selected_option_2 = tk.StringVar()
        combobox = ttk.Combobox(right_labels_frame, textvariable=selected_option_2, values=options)
        try:
            pre_filled_index = options.index(pre_filled_value)
            combobox.current(pre_filled_index)
        except ValueError:
            pass
        combobox.grid(row=0, column=1, padx=5, pady=5)
    else:
        options = ["Não há servidores wireguard!"]
        pre_filled_value = options[0]
        selected_option_2 = tk.StringVar()
        combobox = ttk.Combobox(right_labels_frame, textvariable=selected_option_2, values=options)
        try:
            pre_filled_index = options.index(pre_filled_value)
            combobox.current(pre_filled_index)
        except ValueError:
            pass
        combobox.grid(row=0, column=1, padx=5, pady=5)

    public_key_label = tk.Label(right_labels_frame, bg="light gray", text="Public Key:*")
    public_key_label.grid(row=1, column=0, padx=5, pady=5)
    public_key_entry = tk.Entry(right_labels_frame)
    public_key_entry.grid(row=1, column=1, padx=5, pady=5)
    address_label = tk.Label(right_labels_frame, bg="light gray", text="Allowed Address:*")
    address_label.grid(row=2, column=0, padx=5, pady=5)
    address_entry = tk.Entry(right_labels_frame)
    address_entry.grid(row=2, column=1, padx=5, pady=5)
    comment_label_2 = tk.Label(right_labels_frame, bg="light gray", text="Comentário:")
    comment_label_2.grid(row=0, column=2, padx=5, pady=5)
    comment_entry_2 = tk.Entry(right_labels_frame)
    comment_entry_2.grid(row=0, column=3, padx=5, pady=5)
    desativar_peer_value = tk.BooleanVar()
    desativar_button_2 = tk.Checkbutton(right_labels_frame, bg="light gray", text="Peer desativado", variable=desativar_peer_value)
    desativar_button_2.grid(row=1, column=3, padx=5, pady=5)

def gerar_chave_wireguard(ip_address_var_temp, authorization, listbox, tk, parent):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum Servidor Wireguard!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var_temp.get()}/rest/interface/wireguard/set"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {
                ".id": id_value,
                "private-key": ""
            }
            response = requests.post(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Nova chave privada!", "Nova Chave privada gerada com sucesso.", parent=parent )
            url = f"http://{ip_address_var_temp.get()}/rest/interface/wireguard"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            servers_wireguard = response.json()
            print(servers_wireguard)
            string_server_wireguard = []
            for entry in servers_wireguard:
                string_server_wireguard.append(f"ID: {entry['.id']}; Porto: {entry['listen-port']}; Nome: {entry['name']}; Desativado: {entry['disabled']}")
            show_in_list(string_server_wireguard, listbox, tk)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def eliminar_servidor_wireguard(ip_address_var, authorization, listbox1, listbox2, tk, parent, right_labels_frame, combobox, selected_option):
    interface_names = []
    index = listbox1.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum Servidor Wireguard!", parent=parent)
        return
    item = ""
    if index :
        item = listbox1.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            confirmacao = messagebox.askquestion(f"Eliminar Servidor Wireguard {id_value}",f"Tem a certeza que pretende eliminar o Servidor Wireguard {id_value}?", parent=parent)
            if confirmacao == "no":
                return
            
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var.get()}/rest/interface/wireguard/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            dns_entry = response.json()
            interface_name = dns_entry['name']
            
            url = f"http://{ip_address_var.get()}/rest/interface/wireguard/peers"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            peers_wireguard = response.json()
            string_peer_wireguard = []
            for item in peers_wireguard:
                if item['interface'] == interface_name:
                    string_peer_wireguard.append(item['.id'])
            
            for item in string_peer_wireguard:
                delete_url = f"http://{ip_address_var.get()}/rest/interface/wireguard/peers/{item}"
                headers = {'Authorization': 'Basic ' + authorization}
                response = requests.delete(delete_url, headers=headers, verify=False)
                response.raise_for_status()
            
            delete_url = f"http://{ip_address_var.get()}/rest/interface/wireguard/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.delete(delete_url, headers=headers, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Servidor Wireguard apagado", "Servidor Wireguard apagado com Sucesso", parent=parent)
            url = f"http://{ip_address_var.get()}/rest/interface/wireguard/peers"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            peers_wireguard = response.json()
            print(peers_wireguard)
            string_peer_wireguard = []
            for entry in peers_wireguard:
                string_peer_wireguard.append(f"ID: {entry['.id']}; Interface: {entry['interface']}; Desativado: {entry['disabled']}")
            show_in_list(string_peer_wireguard, listbox2, tk)

            url = f"http://{ip_address_var.get()}/rest/interface/wireguard"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            servers_wireguard = response.json()
            print(servers_wireguard)
            string_server_wireguard = []
            for entry in servers_wireguard:
                string_server_wireguard.append(f"ID: {entry['.id']}; Porto: {entry['listen-port']}; Nome: {entry['name']}; Desativado: {entry['disabled']}")
                interface_names.append(f"{entry['name']}")
            show_in_list(string_server_wireguard, listbox1, tk)
            type_label = tk.Label(right_labels_frame, bg="light gray", text="Interface:")
            type_label.grid(row=0, column=0, padx=5, pady=5)
            options = interface_names
            if len(interface_names) > 0:
                pre_filled_value = interface_names[0]
                combobox = ttk.Combobox(right_labels_frame, textvariable=selected_option, values=options)
                try:
                    pre_filled_index = options.index(pre_filled_value)
                    combobox.current(pre_filled_index)
                except ValueError:
                    pass
            else:
                options = ["Não há servidores wireguard!"]
                pre_filled_value = "Não há servidores wireguard!"
                combobox = ttk.Combobox(right_labels_frame, textvariable=selected_option, values=options)
                try:
                    pre_filled_index = options.index(pre_filled_value)
                    combobox.current(pre_filled_index)
                except ValueError:
                    pass
            combobox.grid(row=0, column=1, padx=5, pady=5)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}")

def eliminar_peer_wireguard(ip_address_var, authorization, listbox, tk, parent):
    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum Peer Wireguard!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            confirmacao = messagebox.askquestion(f"Eliminar Peer Wireguard {id_value}",f"Tem a certeza que pretende eliminar o Peer Wireguard {id_value}?", parent=parent)
            if confirmacao == "no":
                return
            delete_url = f"http://{ip_address_var.get()}/rest/interface/wireguard/peers/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.delete(delete_url, headers=headers, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Peer Wireguard apagado", "Peer Wireguard apagado com Sucesso", parent=parent)
            url = f"http://{ip_address_var.get()}/rest/interface/wireguard/peers"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            peers_wireguard = response.json()
            print(peers_wireguard)
            string_peer_wireguard = []
            for entry in peers_wireguard:
                string_peer_wireguard.append(f"ID: {entry['.id']}; Interface: {entry['interface']}; Desativado: {entry['disabled']}")
            show_in_list(string_peer_wireguard, listbox, tk)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}")

def editar_peer_wireguard(ip_address_var_temp, authorization, listbox, tk, parent):
    def update_peer_wireguard(id_value):
        try:
            if not selected_option_2.get():
                return
            interface_valor = selected_option_2.get()
            url = f"http://{ip_address_var.get()}/rest/interface/wireguard/peers/set"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {
                ".id": id_value,
                "interface": interface_valor,
            }
            if comentario_entry.get("1.0", "end-1c").replace(" ", ""):
                data['comment'] =  comentario_entry.get("1.0", "end-1c")
            if public_key_entry.get("1.0", "end-1c").replace(" ", ""):
                data['public-key'] =  public_key_entry.get("1.0", "end-1c")
            if address_entry.get("1.0", "end-1c").replace(" ", ""):
                data['allowed-address'] =  address_entry.get("1.0", "end-1c")
            if ativar_value.get() and disabled:
                data['disabled'] = False
            if ativar_value.get() and not disabled:
                data['disabled'] = True
            response = requests.post(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Peer Wireguard atualizado", "Peer Wireguard atualizado com sucesso", parent=parent )
            url = f"http://{ip_address_var.get()}/rest/interface/wireguard/peers"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            peers_wireguard = response.json()
            string_peer_wireguard = []
            for entry in peers_wireguard:
                string_peer_wireguard.append(f"ID: {entry['.id']}; Interface: {entry['interface']}; Desativado: {entry['disabled']}")
            show_in_list(string_peer_wireguard, listbox, tk)
            close()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)
    
    def close():
        address_window.destroy()

    index = listbox.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum Peer Wireguard!", parent=parent)
        return
    item = ""
    if index :
        item = listbox.get(index)
        item = item.strip()

        address_window = tk.Toplevel(parent)
        address_window.title(f"{item.title()}")
        address_window.geometry("640x480")
        parent = address_window
        ip_address_var = tk.StringVar(address_window)
        authorization_var = tk.StringVar(address_window)
        ip_address_var.set(f"{ip_address_var_temp.get()}")
        authorization_var.set(f"{authorization}")
        authorization = authorization_var.get()

        interface_names = []
        disabled = False
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var.get()}/rest/interface/wireguard/peers/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            peer_wireguard = response.json()
            comment_valor = ""
            interface_valor = peer_wireguard['interface']
            if 'comment' in peer_wireguard:
                comment_valor = peer_wireguard['comment']
            if peer_wireguard['disabled'] == 'true':
                disabled = True
            public_key_valor = peer_wireguard['public-key']
            address_valor = peer_wireguard['allowed-address']
            url = f"http://{ip_address_var.get()}/rest/interface/wireguard"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            servers_wireguard = response.json()
            for entry in servers_wireguard:
                interface_names.append(f"{entry['name']}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

        entry_frame = tk.Frame(address_window)
        entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        type_label = tk.Label(entry_frame, text="Interface:")
        type_label.grid(row=0, column=0, padx=5, pady=5)
        options = interface_names
        selected_option_2 = 0
        if len(interface_names) > 0:
            pre_filled_value = interface_valor
            selected_option_2 = tk.StringVar()
            combobox = ttk.Combobox(entry_frame, textvariable=selected_option_2, values=options)
            try:
                pre_filled_index = options.index(pre_filled_value)
                combobox.current(pre_filled_index)
            except ValueError:
                pass
            combobox.grid(row=0, column=1, padx=5, pady=5)

        public_key_label = tk.Label(entry_frame, text="Public Key:")
        public_key_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N)
        public_key_entry = tk.Text(entry_frame, height=4, width=30)
        public_key_entry.grid(row=1, column=1, padx=5, pady=5)
        public_key_entry.insert(tk.END, public_key_valor)
        address_label = tk.Label(entry_frame, text="Allowed Address:")
        address_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N)
        address_entry = tk.Text(entry_frame, height=4, width=30)
        address_entry.grid(row=2, column=1, padx=5, pady=5)
        address_entry.insert(tk.END, address_valor)
        comentario_label = tk.Label(entry_frame, text="Comentário:")
        comentario_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.N)
        comentario_entry = tk.Text(entry_frame, height=4, width=30)
        comentario_entry.grid(row=3, column=1, padx=5, pady=5)
        comentario_entry.insert(tk.END, comment_valor)

        ativar_value = tk.BooleanVar()
        if not disabled:
            ativar_button = tk.Checkbutton(entry_frame, text="Desativar", variable=ativar_value)
            ativar_button.grid(row=4, column=0, padx=5, pady=5)
        else:
            ativar_button = tk.Checkbutton(entry_frame, text="Ativar", variable=ativar_value)
            ativar_button.grid(row=4, column=0, padx=5, pady=5)

        button_frame = tk.Frame(address_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        right_button_frame = tk.Frame(button_frame)
        right_button_frame.pack(side=tk.RIGHT)
        ok_button = tk.Button(right_button_frame, text="Ok", command=lambda: update_peer_wireguard(id_value))
        ok_button.grid(row=0, column=0, padx=2, pady=2)
        close_button = tk.Button(right_button_frame, text="Fechar", command=close)
        close_button.grid(row=0, column=1, padx=2, pady=2)

def editar_servidor_wireguard(ip_address_var_temp, authorization, listbox1, listbox2, tk, parent, interface_names, combobox, selected_option, right_labels_frame):
    def update_server_wireguard(id_value):
        try:
            url = f"http://{ip_address_var.get()}/rest/interface/wireguard/set"
            headers = {'Authorization': 'Basic ' + authorization}
            data = {
                ".id": id_value,
                "name": name_entry.get().replace(" ", ""),
                "listen-port": port_entry.get().replace(" ", ""),
                "private-key" : private_entry.get().replace(" ", ""),
            }
            if comentario_entry.get("1.0", "end-1c").replace(" ", ""):
                data['comment'] =  comentario_entry.get("1.0", "end-1c")
            if ativar_value.get() and disabled:
                data['disabled'] = False
            if ativar_value.get() and not disabled:
                data['disabled'] = True
            response = requests.post(url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            messagebox.showinfo("Servidor Wireguard atualizado", "Servidor Wireguard atualizado com sucesso", parent=parent )
            url = f"http://{ip_address_var.get()}/rest/interface/wireguard"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            servers_wireguard = response.json()
            string_server_wireguard = []
            for entry in servers_wireguard:
                string_server_wireguard.append(f"ID: {entry['.id']}; Porto: {entry['listen-port']}; Nome: {entry['name']}; Desativado: {entry['disabled']}")
                interface_names.append(f"{entry['name']}")
            show_in_list(string_server_wireguard, listbox1, tk)
            type_label = tk.Label(right_labels_frame, bg="light gray", text="Interface:")
            type_label.grid(row=0, column=0, padx=5, pady=5)
            options = interface_names
            if len(interface_names) > 0:
                pre_filled_value = interface_names[0]
                combobox = ttk.Combobox(right_labels_frame, textvariable=selected_option, values=options)
                try:
                    pre_filled_index = options.index(pre_filled_value)
                    combobox.current(pre_filled_index)
                except ValueError:
                    pass
            url = f"http://{ip_address_var.get()}/rest/interface/wireguard/peers"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            peers_wireguard = response.json()
            print(peers_wireguard)
            string_peer_wireguard = []
            for entry in peers_wireguard:
                string_peer_wireguard.append(f"ID: {entry['.id']}; Interface: {entry['interface']}; Desativado: {entry['disabled']}")
            show_in_list(string_peer_wireguard, listbox2, tk)
            close()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

    def close():
        address_window.destroy()

    index = listbox1.curselection()
    if not index:
        messagebox.showerror("Erro","Não está selecionado nenhum servidor Wireguard!", parent=parent)
        return
    item = ""
    if index :
        item = listbox1.get(index)
        item = item.strip()

        address_window = tk.Toplevel(parent)
        address_window.title(f"{item.title()}")
        address_window.geometry("640x480")
        parent = address_window
        ip_address_var = tk.StringVar(address_window)
        authorization_var = tk.StringVar(address_window)
        ip_address_var.set(f"{ip_address_var_temp.get()}")
        authorization_var.set(f"{authorization}")
        authorization = authorization_var.get()

        disabled = False
        try:
            id_value = item.split("ID:")[1].split(";")[0].strip()
            url = f"http://{ip_address_var.get()}/rest/interface/wireguard/{id_value}"
            headers = {'Authorization': 'Basic ' + authorization}
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            server_wireguard = response.json()
            name_valor = server_wireguard['name']
            comment_valor = ""
            if 'comment' in server_wireguard:
                comment_valor = server_wireguard['comment']
            if server_wireguard['disabled'] == 'true':
                disabled = True
            port_valor = server_wireguard['listen-port']
            mtu_valor = server_wireguard['mtu']
            public_key_valor = server_wireguard['public-key']
            private_key_valor = server_wireguard['private-key']
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

        entry_frame = tk.Frame(address_window)
        entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        name_label = tk.Label(entry_frame, text="Nome:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(entry_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(tk.END, name_valor)
        mtu_label = tk.Label(entry_frame, text="MTU:")
        mtu_label.grid(row=1, column=0, padx=5, pady=5)
        mtu_label = tk.Label(entry_frame, text=mtu_valor)
        mtu_label.grid(row=1, column=1, padx=5, pady=5)
        port_label = tk.Label(entry_frame, text="Listen Port:")
        port_label.grid(row=2, column=0, padx=5, pady=5)
        port_entry = tk.Entry(entry_frame)
        port_entry.grid(row=2, column=1, padx=5, pady=5)
        port_entry.insert(tk.END, port_valor)
        private_label = tk.Label(entry_frame, text="Private Key:")
        private_label.grid(row=3, column=0, padx=5, pady=5)
        private_entry = tk.Entry(entry_frame)
        private_entry.grid(row=3, column=1, padx=5, pady=5)
        private_entry.insert(tk.END, private_key_valor)
        public_label = tk.Label(entry_frame, text="Public Key:")
        public_label.grid(row=4, column=0, padx=5, pady=5)
        public_entry = tk.Entry(entry_frame)
        public_entry.grid(row=4, column=1, padx=5, pady=5)
        public_entry.insert(tk.END, public_key_valor)

        comentario_label = tk.Label(entry_frame, text="Comentário:")
        comentario_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.N)
        comentario_entry = tk.Text(entry_frame, height=4, width=30)
        comentario_entry.grid(row=5, column=1, padx=5, pady=5)
        comentario_entry.insert(tk.END, comment_valor)
        
        ativar_value = tk.BooleanVar()
        if not disabled:
            ativar_button = tk.Checkbutton(entry_frame, text="Desativar", variable=ativar_value)
            ativar_button.grid(row=6, column=0, padx=5, pady=5)
        else:
            ativar_button = tk.Checkbutton(entry_frame, text="Ativar", variable=ativar_value)
            ativar_button.grid(row=6, column=0, padx=5, pady=5)

        button_frame = tk.Frame(address_window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        right_button_frame = tk.Frame(button_frame)
        right_button_frame.pack(side=tk.RIGHT)
        ok_button = tk.Button(right_button_frame, text="Ok", command=lambda: update_server_wireguard(id_value))
        ok_button.grid(row=0, column=0, padx=2, pady=2)
        close_button = tk.Button(right_button_frame, text="Fechar", command=close)
        close_button.grid(row=0, column=1, padx=2, pady=2)

def criar_peer_wireguard(ip_address_var, authorization, listbox2, tk, parent, selected_option_2, public_key_entry, address_entry, comment_entry_2, desativar_button_2, desativar_peer_value):
    interface_value = selected_option_2.get()
    if interface_value == "Não há servidores wireguard!":
        messagebox.showerror("Erro","Não existem servidores disponíveis, por favor crie um servidor primeiro!", parent=parent)
        return
    if not interface_value:
        messagebox.showerror("Erro","Não existem servidores disponíveis, por favor crie um servidor primeiro!", parent=parent)
        return
    public_key_valor = public_key_entry.get().replace(" ", "")
    if not public_key_valor:
        messagebox.showerror("Erro","Não foi dada nenhuma Public Key, a caixa de texto encontra-se vazia!", parent=parent)
        return
    address_valor = address_entry.get().replace(" ", "")
    if not address_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Endereço permitido, a caixa de texto encontra-se vazia!", parent=parent)
        return
    
    comment_valor = comment_entry_2.get()
    desativado = False
    if desativar_peer_value.get():
        desativado = True

    try:
        dns_entry_data = {
            "interface": interface_value, 
            "disabled": desativado,
            "public-key": public_key_valor,
            "allowed-address": address_valor
        }
        if comment_valor:
            dns_entry_data['comment'] = comment_valor
        url = f"http://{ip_address_var.get()}/rest/interface/wireguard/peers/add"
        headers = {'Authorization': 'Basic ' + authorization}
        response = requests.post(url, headers=headers, json=dns_entry_data, verify=False)
        if response.status_code == 200:
            messagebox.showinfo("Peer Wireguard criado", "Peer Wireguard criado com sucesso", parent=parent )
        url = f"http://{ip_address_var.get()}/rest/interface/wireguard/peers"
        headers = {'Authorization': 'Basic ' + authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        peers_wireguard = response.json()
        print(peers_wireguard)
        string_peer_wireguard = []
        for entry in peers_wireguard:
            string_peer_wireguard.append(f"ID: {entry['.id']}; Interface: {entry['interface']}; Desativado: {entry['disabled']}")
        show_in_list(string_peer_wireguard, listbox2, tk)
        address_entry.delete(0, tk.END)
        public_key_entry.delete(0, tk.END)
        comment_entry_2.delete(0, tk.END)
        desativar_button_2.deselect()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def criar_servidor_wireguard(ip_address_var, authorization, listbox1, tk, parent, name_left_entry, port_entry, comment_entry, desativar_button, desativar_server_value, right_labels_frame, combobox, selected_option):
    interface_names = []
    nome_valor = name_left_entry.get().replace(" ", "")
    if not nome_valor:
        messagebox.showerror("Erro","Não foi dado nenhum Nome, a caixa de texto encontra-se vazia!", parent=parent)
        return
    porto_valor = port_entry.get().replace(" ", "")
    #if not porto_valor:
    #    messagebox.showerror("Erro","Não foi dado nenhum porto, a caixa de texto encontra-se vazia!", parent=parent)
    #    return
    
    comment_valor = comment_entry.get()
    desativado = False
    if desativar_server_value.get():
        desativado = True

    try:
        dns_entry_data = {
            "name": nome_valor, 
            "disabled": desativado,
        }
        if porto_valor:
            dns_entry_data["listen-port"] = porto_valor
        if comment_valor:
            dns_entry_data['comment'] = comment_valor
        url = f"http://{ip_address_var.get()}/rest/interface/wireguard/add"
        headers = {'Authorization': 'Basic ' + authorization}
        response = requests.post(url, headers=headers, json=dns_entry_data, verify=False)
        if response.status_code == 200:
            messagebox.showinfo("Servidor Wireguard criado", "Servidor Wireguard criado com sucesso", parent=parent )
        url = f"http://{ip_address_var.get()}/rest/interface/wireguard"
        headers = {'Authorization': 'Basic ' + authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        servers_wireguard = response.json()
        string_server_wireguard = []
        for entry in servers_wireguard:
            string_server_wireguard.append(f"ID: {entry['.id']}; Porto: {entry['listen-port']}; Nome: {entry['name']}; Desativado: {entry['disabled']}")
            interface_names.append(f"{entry['name']}")
        show_in_list(string_server_wireguard, listbox1, tk)
        type_label = tk.Label(right_labels_frame, bg="light gray", text="Interface:")
        type_label.grid(row=0, column=0, padx=5, pady=5)
        options = interface_names
        if len(interface_names) > 0:
            pre_filled_value = interface_names[0]
            combobox = ttk.Combobox(right_labels_frame, textvariable=selected_option, values=options)
            try:
                pre_filled_index = options.index(pre_filled_value)
                combobox.current(pre_filled_index)
            except ValueError:
                pass
        combobox.grid(row=0, column=1, padx=5, pady=5)
        name_left_entry.delete(0, tk.END)
        port_entry.delete(0, tk.END)
        comment_entry.delete(0, tk.END)
        desativar_button.deselect()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)

def get_system_data_periodically(ip_address_var, authorization, labels):
    try:
        url = f"http://{ip_address_var.get()}/rest/system/clock?.proplist=time"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        time = response.json()
        url = f"http://{ip_address_var.get()}/rest/system/resource"
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        status = response.json()
        labels.clear()
        labels.append(time['time'])
        labels.append(status['free-hdd-space'])
        labels.append(status['free-memory'])
        labels.append(status['total-hdd-space'])
        labels.append(status['total-memory'])
        labels.append(status['uptime'])
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}")

def validar_string_its_ip(string_ip):
    try:
        ip_object = ipaddress.ip_address(string_ip)
        return True
    except ValueError:
        return False
    
def validar_ip_a_menor_que_ip_b(ip_a,ip_b):
    primeiro_ip = ipaddress.IPv4Address(ip_a)
    segundo_ip = ipaddress.IPv4Address(ip_b)
    return primeiro_ip < segundo_ip

def validar_se_interface_pode_ser_usada(interface,ip_address_var,authorization,parent):
    #Se a interface estiver vazia
    if interface.cget('fg') == "grey":
        return {
            'flag' : False,
            'message': "A interface não se econtra com nenhum nome!"
        }
    
    try:
        #Se a interface não existir no equipamento
        url = f"http://{ip_address_var.get()}/rest/interface?.proplist=name"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        all_interfaces = response.json()
        flag_interface = True

        for item in all_interfaces:
            if interface.get() == item['name']:
                flag_interface = False
        
        if flag_interface:
            return {
                'flag' : False,
                'message': "A interface inserida não se encontra no dispositivo!"
            }

        #Se a interface já estiver a ser usada por outro servidor DHCP
        url = f"http://{ip_address_var.get()}/rest/ip/dhcp-server?.proplist=interface"
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        interfaces_dhcp_servers = response.json()

        for item in interfaces_dhcp_servers:
            if item['interface'] == interface.get():
                return {
                    'flag' : False,
                    'message': "A interface escolhida já se encontra a ser usada por um servidor DHCP!"
                }
        
        return {
            'flag' : True,
            'message': ""
        }
        
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}", parent=parent)


def validar_lease_time(lease_time_hour_entry,lease_time_minute_entry,lease_time_second_entry):

    def is_int(numero):
        try:
            int(numero)
        except ValueError:
            return False
        else:
            return True
        
    if lease_time_hour_entry.cget('fg') == "grey" or not is_int(lease_time_hour_entry.get()):
        return {
            'flag': False,
            'message' : "As horas devem ser um numero!"
        }

    if lease_time_minute_entry.cget('fg') == "grey" or not is_int(lease_time_minute_entry.get()):
        return {
            'flag': False,
            'message' : "Os minutos devem ser um numero!"
        }

    if lease_time_second_entry.cget('fg') == "grey" or not is_int(lease_time_second_entry.get()):
        return {
            'flag': False,
            'message' : "Os segundos devem ser um numero!"
        }    
    
    if int(lease_time_hour_entry.get()) < 0:
        return {
            'flag' : False,
            'message': "As horas não podem ser um valor negativo"
        }

    if int(lease_time_minute_entry.get()) < 0:
        return {
            'flag' : False,
            'message': "Os minutos não podem ser um valor negativo"
        }
    
    if int(lease_time_second_entry.get()) < 0:
        return {
            'flag' : False,
            'message': "Os segundos não podem ser um valor negativo"
        }
    
    if int(lease_time_hour_entry.get()) == 0 and int(lease_time_minute_entry.get()) == 0 and int(lease_time_second_entry.get()) == 0:
        return {
            'flag' : False,
            'message': "O tempo não pode ser zero !"
        }
    
    #Defenir o lease time máximo de 23:59:59
    #Obrigar a que os valores dos minutos e segundos estejam de 0 a 59 minutos
    #Obrigar a que os valor da hora esteja entre 0 a 23

    if int(lease_time_second_entry.get()) > 59 :
        return {
            'flag' : False,
            'message': "Os segundos não podem ter um valor superior a 59 !"
        }
    
    if int(lease_time_minute_entry.get()) > 59 :
        return {
            'flag' : False,
            'message': "Os minutos não podem ter um valor superior a 59 !"
        }
    
    if int(lease_time_hour_entry.get()) > 23 :
        return {
            'flag' : False,
            'message': "As horas não podem ter um valor superior a 23 !"
        }
    
    return {
        'flag' : True,
        'message': ""
    }

def validar_network(network,pool_range_first,pool_range_last):

    def is_ip_network(network):
        try:
            ip_object = ipaddress.ip_network(network)
        except ValueError:
            return False
        else:
            return True
    
    if network == "":
        return {
            'flag' : False,
            'message': f"Prenchimento das configurações de Rede inconcluido - A Rede não se encontra preenchido"
        }

    #Verifica se possível transformar o que está na caixa de texto numa network
    if not is_ip_network(network):
        return {
            'flag' : False,
            'message': "A representação colocada na secção Rede não representa uma rede IPv4!"
        }
    
    if ipaddress.ip_address(pool_range_first) not in ipaddress.ip_network(network):
        return {
            'flag' : False,
            'message': "O primeiro endereço do Pool Range colocado não pertence à rede escolhida"
        }
    
    if ipaddress.ip_address(pool_range_last) not in ipaddress.ip_network(network):
        return {
            'flag' : False,
            'message': "O ultimo endereço do Pool Range colocado não pertence à rede escolhida"
        }
        
    return {
        'flag' : True,
        'message': ""
    }

def validar_gateway(gateway,network):

    if gateway == "":
        return {
            'flag' : False,
            'message': f"Prenchimento das configurações de Rede inconcluido - O gateway não se encontra preenchido"
        }

    if not validar_string_its_ip(gateway):
        return {
            'flag' : False,
            'message': "O valor colocado no gateway não é um endereço IP"
        }
    
    if ipaddress.ip_address(gateway) not in ipaddress.ip_network(network):
        return {
            'flag' : False,
            'message': "O gateway colocado não pertence à rede escolhida"
        }

    return {
        'flag' : True,
        'message': ""
    }

def validar_dns(dns):
    
    if dns == "":
        return {
            'flag' : False,
            'message': f"Prenchimento das configurações de Rede inconcluido - O DNS não se encontra preenchido"
        }

    lista_dns = dns.split(",")

    for item in lista_dns:
        if not validar_string_its_ip(item):
            return {
                'flag' : False,
                'message': f"O valor {item} não se encontra no formato de endereço IP"
            }

    return {
        'flag' : True,
        'message': ""
    }


def desligar(ip_address_var,authorization,janela_router,janela_login):
    try:
        confirmacao = messagebox.askquestion(f"Desligar Router",f'Tem a certeza que pretende desligar o router ?', parent=janela_router)
        if confirmacao == "no":
            return
        janela_router.destroy()
        url = f"http://{ip_address_var.get()}/rest/system/shutdown"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.post(url, headers=headers, verify=False)
        response.raise_for_status()
        if response.status_code == 200:
            messagebox.showinfo("Router Desligado","O Router foi desligado com sucesso!!!",parent=janela_login)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}",janela_login)


def reiniciar(ip_address_var,authorization,janela_router,janela_login):
    try:
        confirmacao = messagebox.askquestion(f"Reiniciar Router",f'Tem a certeza que pretende reiniciar o router ?', parent=janela_router)
        if confirmacao == "no":
            return
        janela_router.destroy()
        url = f"http://{ip_address_var.get()}/rest/system/reboot"
        headers = {'Authorization': 'Basic '+ authorization}
        response = requests.post(url, headers=headers, verify=False)
        response.raise_for_status()
        if response.status_code == 200:
            messagebox.showinfo("Router Reiniciado","O Router foi reiniciado com sucesso!!!",parent=janela_login)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"An error occurred: {e}",janela_login)