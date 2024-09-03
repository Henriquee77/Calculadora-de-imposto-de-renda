import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# Função para calcular o imposto de renda individual
def calcular_imposto_renda(renda_anual):
    if renda_anual <= 22847.76:
        return 0
    elif renda_anual <= 33919.80:
        return (renda_anual - 22847.76) * 0.075
    elif renda_anual <= 45012.60:
        return (renda_anual - 33919.80) * 0.15 + 827.19
    elif renda_anual <= 55976.16:
        return (renda_anual - 45012.60) * 0.225 + 2108.25
    else:
        return (renda_anual - 55976.16) * 0.275 + 4220.36

# Função para gerar o gráfico de pizza usando pandas e matplotlib
def gerar_grafico_pizza(rendas, impostos):
    # Criando um DataFrame com pandas
    df = pd.DataFrame({
        'Pessoas': [f'Pessoa {i+1}' for i in range(len(rendas))],
        'Imposto': impostos
    })

    # Plotando o gráfico de pizza
    plt.figure(figsize=(8, 8))
    plt.pie(df['Imposto'], labels=df['Pessoas'], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('Distribuição do Imposto de Renda na Família')
    plt.axis('equal')  # Assegura que o gráfico seja um círculo
    plt.savefig('grafico_imposto_renda_familia.png')
    plt.show()

# Função para enviar o e-mail com o gráfico anexo
def enviar_email(com_destinatario, arquivo_anexo):
    from_email = 'sousaluishenrique20@gmail.com'
    from_password = 'sua_senha'  # Substitua por sua senha ou senha de app
    subject = 'Calculadora de Imposto de Renda da Família'
    
    # Configuração da mensagem
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = com_destinatario
    msg['Subject'] = subject
    
    body = 'Segue em anexo o gráfico do imposto de renda da sua família.'
    msg.attach(MIMEText(body, 'plain'))
    
    # Anexar o arquivo
    attachment = open(arquivo_anexo, 'rb')
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(arquivo_anexo)}')
    
    msg.attach(part)
    
    # Conectar ao servidor SMTP e enviar o e-mail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    text = msg.as_string()
    server.sendmail(from_email, com_destinatario, text)
    server.quit()

# Função principal
def main():
    num_pessoas = int(input("Digite o número de pessoas na família: "))
    rendas = []
    impostos = []
    
    for i in range(num_pessoas):
        renda_anual = float(input(f"Digite a renda anual da pessoa {i+1}: R$ "))
        imposto = calcular_imposto_renda(renda_anual)
        rendas.append(renda_anual)
        impostos.append(imposto)
        print(f"O imposto de renda devido pela pessoa {i+1} é: R$ {imposto:.2f}")
    
    imposto_total = sum(impostos)
    print(f"O imposto total da família é: R$ {imposto_total:.2f}")
    
    # Gerar e mostrar o gráfico de pizza
    gerar_grafico_pizza(rendas, impostos)
    
    # Perguntar se o usuário deseja enviar o gráfico por e-mail
    enviar = input("Deseja enviar o gráfico por e-mail? (s/n): ").strip().lower()
    if enviar == 's':
        email = input("Digite seu e-mail para receber o gráfico: ")
        enviar_email(email, 'grafico_imposto_renda_familia.png')
        print(f"E-mail enviado para {email}")
    else:
        print("Gráfico não enviado.")

if __name__ == "__main__":
    main()
