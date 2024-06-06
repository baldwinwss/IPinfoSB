from ipwhois import IPWhois
import requests
from colorama import init, Fore

def get_whois(ip):
    try:
        obj = IPWhois(ip)
        result = obj.lookup_rdap()
        return result
    except ValueError:
        print(Fore.RED + "Hata: Geçersiz IP adresi. Lütfen geçerli bir IP adresi girin." + Fore.RESET)
        return None
    except Exception as e:
        print(Fore.RED + "Hata: Ağ bağlantı sorunu. Lütfen internet bağlantınızı kontrol edin." + Fore.RESET)
        return None

def get_location(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url)
        response.raise_for_status()  
        data = response.json()
        return data
    except requests.exceptions.HTTPError:
        print(Fore.RED + "Hata: IP lokasyon bilgisi alınamadı." + Fore.RESET)
        return None
    except Exception as e:
        print(Fore.RED + "Hata: Ağ bağlantı sorunu. Lütfen internet bağlantınızı kontrol edin." + Fore.RESET)
        return None

def print_whois_info(info):
    print(f"\nSorgulanan IP: {info['query']}")
    print(f"ASN: {info['asn']}")
    print(f"ASN CIDR: {info['asn_cidr']}")
    print(f"ASN Ülke Kodu: {info['asn_country_code']}")
    print(f"ASN Tarihi: {info['asn_date']}")
    print(f"ASN Açıklaması: {info['asn_description']}\n")

    print("Ağ Bilgileri:")
    network = info['network']
    print(f"  Adı: {network.get('name')}")
    print(f"  Adres Aralığı: {network.get('range')}")
    print(f"  Ülke: {network.get('country')}")
    remarks = network.get('remarks')
    if remarks:
        print(f"  Açıklama: {remarks[0].get('description')}")
    print(f"  Olaylar:")
    for event in network.get('events', []):
        print(f"    - {event['action']} tarihinde {event['timestamp']}")

    print("\nKurum Bilgileri:")
    for entity in info['entities']:
        print(f"  {entity}")

    print("\nNesne Bilgileri:")
    objects = info['objects']
    for key, obj in objects.items():
        contact = obj.get('contact', {})
        print(f"  {key}: {contact.get('name')}")
        addresses = contact.get('address')
        if addresses:
            for address in addresses:
                print(f"    Adres: {address['value']}")
        phones = contact.get('phone')
        if phones:
            for phone in phones:
                print(f"    Telefon: {phone['value']}")
        emails = contact.get('email')
        if emails:
            for email in emails:
                print(f"    E-posta: {email['value']}")

init()

banner = Fore.RED + """
.d8888. db   db d88888b d8888b. db       .d88b.   .o88b. db   dD 
88'  YP 88   88 88'     88  `8D 88      .8P  Y8. d8P  Y8 88 ,8P' 
`8bo.   88ooo88 88ooooo 88oobY' 88      88    88 8P      88,8P   
  `Y8b. 88~~~88 88~~~~~ 88`8b   88      88    88 8b      88`8b   
db   8D 88   88 88.     88 `88. 88booo. `8b  d8' Y8b  d8 88 `88. 
`8888Y' YP   YP Y88888P 88   YD Y88888P  `Y88P'   `Y88P' YP   YD 
                                                                 
                                                                 
d8888b.  .d8b.  d888888b .88b  d88.  .d8b.  d8b   db             
88  `8D d8' `8b `~~88~~' 88'YbdP`88 d8' `8b 888o  88             
88oooY' 88ooo88    88    88  88  88 88ooo88 88V8o 88             
88~~~b. 88~~~88    88    88  88  88 88~~~88 88 V8o88             
88   8D 88   88    88    88  88  88 88   88 88  V888             
Y8888P' YP   YP    YP    YP  YP  YP YP   YP VP   V8P 

""" + Fore.RESET

print(banner)

while True:
    ip_address = input(Fore.BLUE + "Lütfen bir IP adresi girin: " + Fore.RESET)

    whois_info = get_whois(ip_address)

    if whois_info:
        location_info = get_location(ip_address)

        if location_info:
            print_whois_info(whois_info)

            print("\nLokasyon Bilgileri:")
            for key, value in location_info.items():
                print(f"{key}: {value}")

    devam = input("\nProgramı sonlandırmak için 'q' tuşuna basın, devam etmek için 'Enter' tuşuna basın: ")
    if devam.strip().lower() == 'q':
        print("Program sonlandırıldı.")
        break
