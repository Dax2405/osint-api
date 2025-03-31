from bs4 import BeautifulSoup
import requests
import phpserialize


def get_complaints(tableText, nameO):
    soup = BeautifulSoup(tableText, "html.parser")
    table = soup.find_all("table")
    tabs = int(len(table)/2)
    info = []

    for i in range(tabs):
        print(i)
        rows1 = table[i*2].find_all("tr")
        rows2 = table[i*2+1].find_all("tr")[2:]
        inf = []

        lugar = rows1[1].find_all("td")[2].text
        fecha = rows1[1].find_all("td")[4].text
        delito = rows1[4].find_all("td")[1].text
        estado = None
        for row in rows2:
            cols = row.find_all("td")
            nombre = ' '.join(cols[1].text.split())
            nombre_set = set(nombre.lower().split())
            nameO_set = set(nameO.lower().split())
            print(nombre_set, nameO_set, cols[2].text)
            print(nameO_set.issubset(nombre_set))
            print(cols[2].text == "SOSPECHOSO")
            if nameO_set.issubset(nombre_set) and "SOSPECHOSO" == cols[2].text:
                estado = cols[2].text
                inf.append({"lugar": lugar})
                inf.append({"fecha": fecha})
                inf.append({"delito": delito})
                inf.append({"estado": estado})
                info.append(inf)
                break

    return info


def get_info_by_name(name):
    names = name.split(" ")
    php_serialized = phpserialize.dumps(names)
    php_serialized_str = php_serialized.decode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Referrer": "https://consultasecuador.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    FIS_LINK = "https://www.gestiondefiscalias.gob.ec/siaf/comunes/noticiasdelito/info_mod.php"
    params = {
        "businfo": php_serialized_str,
    }
    response = requests.post(FIS_LINK, params=params,
                             verify=False, headers=headers)
    if response.status_code == 200:
        return get_complaints(response.text, name)
    else:
        return "Error"


def get_info_by_plate(plate):

    INFO_LINK = f"https://srienlinea.sri.gob.ec/movil-servicios/api/v1.0/matriculacion/valor/{plate}"
    OWNER_LINK = "https://app3902.privynote.net/api/v1/transit/vehicle-owner"
    data = {
        "placa": plate,
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Referrer": "https://consultasecuador.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    print(data)
    response = requests.post(OWNER_LINK, json=data, headers=headers)
    print(response.text)
    if response.status_code == 200:
        info = []
        name = response.json().get("data", {}).get("name", "No encontrado")
        response = requests.get(INFO_LINK)
        if response.status_code == 200:
            info.append({"nombre": name})
            info.append({"placa": plate})
            info.append({"cantonMatricula": response.json().get(
                "cantonMatricula", "No encontrado")})
            info.append(
                {"marca": response.json().get("marca", "No encontrado")})
            info.append(
                {"modelo": response.json().get("modelo", "No encontrado")})
            info.append({"servicio": response.json().get(
                "servicio", "No encontrado")})
            info.append({"informacion": response.json().get(
                "informacion", "No encontrado")})
            info.append({"anioModelo": response.json().get(
                "anioModelo", "No encontrado")})
            info.append(
                {"deudas": response.json().get("deudas", "No encontrado")})

            info_fis = get_info_by_name(name)
            return info, info_fis
        else:
            return {"error": "Informacion del vehiculo no encontrada"}
    else:
        return {"error": "Placa no encontrada"}
