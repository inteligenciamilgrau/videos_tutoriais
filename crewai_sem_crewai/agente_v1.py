from comunicacao import send_message


formato_json = True
sistema = "Seu nome é Felipa"
mensagem = """
Bom dia, qual seu nome? Responda num JSON
"""

# Example usage:
response = send_message(mensagem, sistema, formato_json)
print(response)
