import subprocess
import re
from querys import insert_authentication_log

def read_and_filter_logs(container_name):
    # Comando para ler os logs do contêiner e capturar a saída
    command = f"dhis2-logview {container_name}"
    output = subprocess.check_output(command, shell=True, text=True)

    # Lista para armazenar as informações relevantes dos logs
    relevant_info = []

    # Filtrando as informações relevantes dos logs
    for line in output.split('\n'):
        if "AuthenticationSuccessEvent" in line or "AuthenticationFailureBadCredentialsEvent" in line:
            match = re.search(r'(\w+ \d+ \d+:\d+:\d+) (\w+) tomcat9\[\d+\]: \* INFO .* username: (\w+); ip: (\d+\.\d+\.\d+\.\d+);', line)
            if match:
                date_time = match.group(1)
                container_name = match.group(2)
                username = match.group(3)
                ip = match.group(4)
                relevant_info.append((date_time, container_name, username, ip))
    return relevant_info

if __name__ == "__main__":
    # Definindo o nome do contêiner
    container_name = "test"

    # Lendo e filtrando as informações relevantes dos logs do contêiner especificado
    relevant_logs = read_and_filter_logs(container_name)

    for info in relevant_logs:
        print("Container Name:", info[1])
        print("Authentication Event:", "AuthenticationSuccessEvent" if "AuthenticationSuccessEvent" in info[0] else "AuthenticationFailureBadCredentialsEvent")
        print("Username:", info[2])
        print("Datetime:", info[0])
        print("-------------------------------------")

    # Inserindo as informações relevantes dos logs no banco de dados
    #for info in relevant_logs:
     #   insert_authentication_log(info[1], "AuthenticationSuccessEvent" if "AuthenticationSuccessEvent" in info[0] else "AuthenticationFailureBadCredentialsEvent", info[2], datetime=info[0])


    print("Informações relevantes dos logs foram inseridas no banco de dados.")