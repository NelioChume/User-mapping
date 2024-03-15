#!/usr/bin/env python3

import subprocess
import re

def read_and_filter_logs(container_name):
    # Comando para ler os logs do contêiner e capturar a saída
    command = f"dhis2-logview {container_name}"
    output = subprocess.check_output(command, shell=True, text=True)

    # Lista para armazenar as informações relevantes dos logs
    relevant_info = []

    # Filtrando as informações relevantes dos logs
    for line in output.split('\n'):
        if "INFO" in line:
            match = re.search(r'(\w+ \d+ \d+:\d+:\d+) (\w+) tomcat9\[\d+\]: \* INFO .* username: (\w+); ip: (\d+\.\d+\.\d+\.\d+);', line)
            if match:
                date_time = match.group(1)
                container_name = match.group(2)
                username = match.group(3)
                ip = match.group(4)
                relevant_info.append((date_time, container_name, username, ip))

    return relevant_info

if __name__ == "__main__":
    container_name = "test"
    # Lendo e filtrando as informações relevantes dos logs do contêiner especificado
    relevant_logs = read_and_filter_logs(container_name)

    # Salvando as informações relevantes dos logs em um arquivo
    with open("info_logs.txt", "w") as file:
        for info in relevant_logs:
            file.write(f"Container_name: {info[1]}, Data & Hora: {info[0]}, User_name: {info[2]}, Ip: {info[3]}\n")

    print("Informações relevantes dos logs foram salvas em info_logs.txt")