oimport colorama
from colorama import Fore
from bitcoinlib.wallets import Wallet, wallets_list, wallet_delete, WalletError, EncodingError
from bitcoinlib.mnemonic import Mnemonic
import qrcode
import os

os.system("cls")

colorama.init(autoreset=True)

red = Fore.LIGHTRED_EX
green = Fore.LIGHTGREEN_EX
blue = Fore.LIGHTBLUE_EX
gray = Fore.LIGHTBLACK_EX
yellow = Fore.YELLOW
reset = Fore.RESET

def LOGO():
    logo = """
⠀⠀⠀⠀⣿⡇⠀⢸⣿⡇⠀⠀⠀⠀
⠸⠿⣿⣿⣿⡿⠿⠿⣿⣿⣿⣶⣄⠀
⠀⠀⢸⣿⣿⡇⠀⠀⠀⠈⣿⣿⣿⠀
⠀⠀⢸⣿⣿⡇⠀⠀⢀⣠⣿⣿⠟⠀
⠀⠀⢸⣿⣿⡿⠿⠿⠿⣿⣿⣥⣄⠀   autore: BeatoTechLab
⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⢻⣿⣿⣧   versione: beta 2.0
⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⣼⣿⣿⣿
⢰⣶⣿⣿⣿⣷⣶⣶⣾⣿⣿⠿⠛⠁
⠀⠀⠀⠀⣿⡇⠀⢸⣿⡇⠀⠀⠀⠀
""" + yellow + "Questa versione non è ufficiale e non è consigliato \nl'utilizzo per evitare di perdere denaro reale, \nnon fornisce sistemi di cryttografia.\nQuesto progetto è stato creato a scopo intrattenitivo\n" + green + "-" * 50

    print(green + logo)
    print(blue + "[*] 'help' per i comandi")
    print(blue + "[*] 'exit' per uscire")

def HELP():
    print(reset)
    print("\tnew wallet         -> Crea un nuovo wallet")
    print("\twallet list        -> Visualizza i wallet creati")
    print("\twallet delete      -> Elimina un wallet")
    print("\twallet balance     -> Visualizza i soldi nei wallet")
    print("\twallet address     -> Visualizza gli indirizzi dei wallet")
    print("\twallet wif         -> Ottieni il codice WIF del wallet")
    print("\tsend               -> Invia fondi ad un indirizzo esterno")
    print("\treceive            -> Ricevi l'indirizzo per ricevere i fondi")
    print("\twallet qrcode      -> Ottieni il qrcode di un wallet per ricevere fondi")
    print("\thelp               -> Visualizza i comandi")
    print("\texit               -> Esci dal programma\t")
    
def COMMAND():
    while True:
        command = input(gray + "> " +  reset)
        match command:
            case "help":
                HELP()
                
            case "exit":
                quit()
                
            case "new wallet":
                name = input("Inserisci il nome del wallet: ")
                print(green + "Creazione del wallet...")
                try:
                    print(green + "Creazione frase mnemonica..")
                    mnemonic_key = Mnemonic().generate(strength=128, add_checksum=True)                    
                    Wallet.create(name=str(name), keys=mnemonic_key)
                    print(green + f"[+] Wallet ({red + name + green}) creato con successo")
                    print(reset + f"Chiave mnemonica -> {red + mnemonic_key}")
                    name = f"{name}_mnemonic.key"
                    with open(name, "w") as file:
                        file.write(mnemonic_key)
                        file.close()
                    print(reset + f"Chiave mnemonica salvata in: {blue + os.path.abspath(name)}")
                except WalletError:
                    print(red + "[-] Esiste già un wallet con questo nome")
                    
            case "wallet list":
                for wallet in wallets_list():
                    print(wallet["name"])
                    
            case "wallet delete":
                wallet_name = input("Nome wallet da eliminare: ")
                try:
                    print(green + "Eliminazione del wallet...")
                    wallet = Wallet(wallet_name)
                    wallet_delete(wallet.name)
                    print(green + "[+] Wallet eliminato con successo")
                except WalletError:
                    print(red + "[-] Wallet non esistente")
            
            case "wallet balance":
                print("\n\tNOME\t\t\t\tBALANCE\n" + "-" * 60)
                for wallet in wallets_list():
                    wallet = Wallet(wallet["name"])
                    balance = f"{wallet.balance():.18f}"
                    print(f"\t{wallet.name}  \t\t\t   {green + balance if float(balance) > 0 else red + balance} BTC")
                                    
            case "wallet address":
                print("\n\tNOME\t\t\t\t\tADDRESS\n" + "-" * 80)
                for wallet in wallets_list():
                    wallet = Wallet(wallet["name"])
                    print(f"\t{wallet.name}  \t\t  {wallet.get_key().address}")
            
            case "wallet wif":
                wallet_select = input("Nome wallet: ")
                try:
                    wallet = Wallet(wallet_select)
                    WIF = wallet.get_key().wif
                    print(f"codice WIF del wallet: {wallet_select} -> {red + WIF}")
                except WalletError:
                    print(red + "Wallet non esistente")
            
            case "send":
                wallet_select = input("Nome wallet da cui inviare i fondi: ")
                flag = False
                for wallet in wallets_list():
                    if wallet["name"] == wallet_select:
                        flag = True
                
                if not flag : 
                    print(red + "[-] Wallet non esistente")
                else:
                    destination_address = input("Address di destinazione: ")
                    amount = input("Inserisci l'importo: ")
                    try:
                        print(green + "Invio fondi...")
                        amount = float(amount)
                        wallet = Wallet(wallet_select)
                        send_money = wallet.send_to(destination_address, amount)
                        print(green + "[+] Fondi inviati con successo")
                    except EncodingError:
                        print(red + "[-] Address non valido")
                    except WalletError:
                        print(red + "[-] Fondi non inviati")
                    
        
            case "receive":
                name = input("Inserisci il nome del wallet: ")
                try:
                    wallet = Wallet(name)
                    print(f"Balance attuale:  {wallet.balance():.18f} BTC")
                    receive_address = wallet.get_key().address
                    print(f"Indirizzo per ricevere i fondi -> {green + receive_address}")
                except WalletError:
                    print(red + "[-] Wallet non esistente")


            case "qrcode wallet":
                name = input("Inserisci il nome del wallet: ")
                try:
                    wallet = Wallet(name)
                    receive_address = wallet.get_key().address
                    print(green + "Creazione qrcode...")
                    qr = qrcode.make(receive_address)
                    qr.show()
                    print(green + "[+] QRCODE creato con successo")
                except WalletError:
                    print(red + "[-] Wallet non esistente")
                
            case "" | " ":
                pass
            case _:
                print(red + "[-] Comando non valido, riprovare")

if __name__ == "__main__":
    LOGO()
    COMMAND()
