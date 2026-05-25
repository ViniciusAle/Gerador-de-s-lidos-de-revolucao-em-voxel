import math
import os

print("="*50)
print(" GERADOR E ANALISADOR DE SÓLIDOS DE REVOLUÇÃO ")
print("="*50)
print(" INSTRUÇÕES DE USO E SINTAXE MATEMÁTICA:")
print("- Variável: Use sempre a letra minúscula 'x'.")
print("- Multiplicação: Use '*' (Ex: 4 * x em vez de 4x).")
print("- Potência: Use '**' (Ex: (x-15)**2 para elevar ao quadrado).")
print("- Funções liberadas: sin(x), cos(x), tan(x), sqrt(x), abs(x), pi, e")
print("-" * 50)


caminho_pasta = r"C:\Users\Vinicius Alexandre\AppData\Roaming\PrismLauncher\instances\calculo\minecraft\saves\Calculo\datapacks\projeto_calculo\data\matematica\function"
nome_arquivo = "gerar_solido.mcfunction"
caminho_completo = os.path.join(caminho_pasta, nome_arquivo)

funcao_texto = input("Digite a função f(x): ").replace("^", "**")
x_inicio = int(input("Digite o valor inicial de X (Ex: 0): "))
x_fim = int(input("Digite o valor final de X (Ex: 30): "))

bloco = "minecraft:light_blue_stained_glass" 

ambiente_matematico = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "sqrt": math.sqrt, "pi": math.pi, "e": math.e, "abs": abs
}

def calcular_volume_exato(func_texto, a, b, ambiente):
    volume = 0
    dx = 0.001  # Simulando fatias microscópicas (dx -> 0)
    x_atual = a
    
    while x_atual < b:
        ambiente['x'] = x_atual
        try:
            raio_fino = eval(func_texto, {"__builtins__": None}, ambiente)
            volume += math.pi * (raio_fino**2) * dx
        except Exception:
            pass
        x_atual += dx
        
    return volume

print("\nProcessando a Integral Definida e gerando blocos...")

volume_exato = calcular_volume_exato(funcao_texto, x_inicio, x_fim, ambiente_matematico)

comandos = []
volume_em_blocos = 0

for x_val in range(x_inicio, x_fim + 1):
    ambiente_matematico['x'] = x_val
    
    try:
        resultado_y = eval(funcao_texto, {"__builtins__": None}, ambiente_matematico)
        raio = int(abs(resultado_y)) 
        
    except Exception as erro:
        print(f"\n[ERRO] Não foi possível calcular a função no ponto x={x_val}.")
        print(f"Detalhe: {erro}")
        print("DICA: Verifique se você não esqueceu de usar '*' para multiplicação ou '**' para potência.")
        exit()
    
    for y in range(-raio, raio + 1):
        for z in range(-raio, raio + 1):
            if (y**2 + z**2) <= raio**2:
                comandos.append(f"setblock ~{x_val} ~{y} ~{z} {bloco}")
                volume_em_blocos += 1

# Exportação do Arquivo
os.makedirs(caminho_pasta, exist_ok=True)
with open(caminho_completo, "w") as arquivo:
    for comando in comandos:
        arquivo.write(comando + "\n")

erro_percentual = abs(volume_exato - volume_em_blocos) / volume_exato * 100 if volume_exato > 0 else 0

print("-" * 50)
print("Sucesso! Arquivo injetado direto no Datapack do mundo 'Calculo'.")
print("-" * 50)
print(" RESULTADOS DA ANÁLISE MATEMÁTICA ")
print(f"Volume Exato (Integral): {volume_exato:.2f} unidades")
print(f"Volume Voxel (Blocos):   {volume_em_blocos:.2f} unidades")
print(f"Erro de Discretização:   {erro_percentual:.2f}%")
print("="*50)