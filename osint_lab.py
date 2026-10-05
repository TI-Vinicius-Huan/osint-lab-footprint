import hashlib
import os
import time

# Arquivo crítico que nosso Blue Team vai proteger
ARQUIVO_ALVO = "configuracoes_criticas.txt"

# Se o arquivo não existir, criamos ele com um conteúdo padrão "seguro"
if not os.path.exists(ARQUIVO_ALVO):
    with open(ARQUIVO_ALVO, "w") as f:
        f.write("status=seguro\nusuario_admin=ativo")

def calcular_hash(filename):
    """Calcula o hash SHA-256 para verificar a integridade do arquivo."""
    hasher = hashlib.sha256()
    with open(filename, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

print(f"[*] Monitor de Integridade (FIM) iniciado para: {ARQUIVO_ALVO}")
print("[*] Pressione Ctrl+C para encerrar o monitoramento.\n")

# Registramos o hash seguro inicial
hash_original = calcular_hash(ARQUIVO_ALVO)
print(f"[+] Hash inicial seguro registrado: {hash_original}")

try:
    while True:
        time.sleep(4) # Verifica o arquivo a cada 4 segundos
        hash_atual = calcular_hash(ARQUIVO_ALVO)
        
        if hash_atual != hash_original:
            print("\n[!] ALERTA DE SEGURANÇA: Alteração não autorizada detectada!")
            print(f"[!] Hash original: {hash_original}")
            print(f"[!] Hash alterado: {hash_atual}")
            print("[!] Incidente registrado para análise do SOC.\n")
            break
except KeyboardInterrupt:
    print("\n[+] Monitoramento encerrado com sucesso.")
