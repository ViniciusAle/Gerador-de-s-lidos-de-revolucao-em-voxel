import os
import math
import sympy as sp
import customtkinter as ctk

# ====================================================================
# CONFIGURAÇÃO DA INTERFACE (CustomTkinter)
# ====================================================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppCalculo(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerador de Sólidos de Revolução")
        self.geometry("900x700") 
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.var_eixo = ctk.StringVar(value="X")
        self.var_curvas = ctk.StringVar(value="1")
        self.frame_help = ctk.CTkFrame(self, width=250, fg_color=("gray85", "gray16"))
        self.frame_help.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        self.lbl_help_titulo = ctk.CTkLabel(self.frame_help, text="INSTRUÇÕES DE USO", font=ctk.CTkFont(weight="bold", size=14))
        self.lbl_help_titulo.pack(pady=(20, 10))

        instrucoes = [
            "• Multiplicação:\n  Use '*' (Ex: 4 * x)\n",
            "• Potência:\n  Use '**' (Ex: (x-15)**2)\n",
            "• Raízes:\n  Use '**(1/2)' ou a função\n  sqrt() (Ex: sqrt(x))\n",
            "• Funções liberadas:\n  sin, cos, tan, sqrt, abs,\n  pi, e"
        ]

        for texto in instrucoes:
            lbl = ctk.CTkLabel(self.frame_help, text=texto, justify="left", font=ctk.CTkFont(size=13))
            lbl.pack(anchor="w", padx=15, pady=5)
        self.frame_main = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_main.grid(row=0, column=0, padx=20, pady=0, sticky="nsew")
        self.lbl_titulo = ctk.CTkLabel(self.frame_main, text="Gerador de Sólidos em Voxels", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_titulo.pack(pady=(20, 10))
        self.frame_config = ctk.CTkFrame(self.frame_main)
        self.frame_config.pack(padx=10, pady=10, fill="x")

        self.lbl_eixo = ctk.CTkLabel(self.frame_config, text="Eixo de Rotação:")
        self.lbl_eixo.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.rad_eixo_x = ctk.CTkRadioButton(self.frame_config, text="Eixo X", variable=self.var_eixo, value="X")
        self.rad_eixo_x.grid(row=0, column=1, padx=10, pady=10)
        self.rad_eixo_y = ctk.CTkRadioButton(self.frame_config, text="Eixo Y", variable=self.var_eixo, value="Y")
        self.rad_eixo_y.grid(row=0, column=2, padx=10, pady=10)

        self.lbl_curvas = ctk.CTkLabel(self.frame_config, text="Limites da Área:")
        self.lbl_curvas.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.rad_1_curva = ctk.CTkRadioButton(self.frame_config, text="1 Curva: f(x)", variable=self.var_curvas, value="1", command=self.atualizar_campos)
        self.rad_1_curva.grid(row=1, column=1, padx=10, pady=10)
        self.rad_2_curvas = ctk.CTkRadioButton(self.frame_config, text="2 Curvas: f(x) e g(x)", variable=self.var_curvas, value="2", command=self.atualizar_campos)
        self.rad_2_curvas.grid(row=1, column=2, padx=10, pady=10)

        self.frame_funcs = ctk.CTkFrame(self.frame_main, fg_color="transparent")
        self.frame_funcs.pack(padx=10, pady=0, fill="x") # ALINHAMENTO CORRIGIDO

        self.entry_f = ctk.CTkEntry(self.frame_funcs, placeholder_text="Digite f(x). Ex: 4*sqrt(x)", width=400)
        self.entry_f.grid(row=0, column=0, columnspan=2, padx=5, pady=(0, 10), sticky="ew")

        self.entry_g = ctk.CTkEntry(self.frame_funcs, placeholder_text="Digite g(x). Ex: x**2", width=400)
        
        self.entry_inicio = ctk.CTkEntry(self.frame_funcs, placeholder_text="X Inicial (Ex: 0)")
        self.entry_inicio.grid(row=2, column=0, padx=5, pady=0, sticky="ew")

        self.entry_fim = ctk.CTkEntry(self.frame_funcs, placeholder_text="X Final (Ex: 30)")
        self.entry_fim.grid(row=2, column=1, padx=5, pady=0, sticky="ew")
        
        self.frame_funcs.grid_columnconfigure(0, weight=1)
        self.frame_funcs.grid_columnconfigure(1, weight=1)

        self.btn_gerar = ctk.CTkButton(self.frame_main, text="Gerar Sólido e Analisar", font=ctk.CTkFont(weight="bold"), command=self.executar_geracao, height=40)
        self.btn_gerar.pack(pady=20)

        self.textbox = ctk.CTkTextbox(self.frame_main, height=180, font=ctk.CTkFont(family="Consolas", size=12))
        self.textbox.pack(padx=10, pady=(0, 10), fill="x") # ALINHAMENTO CORRIGIDO: Retirada a largura fixa e adicionado fill="x"
        self.log("Sistema iniciado. Pronto para uso!\n")
        
        self.caminho_pasta = "/home/vinicius_dev/.var/app/org.prismlauncher.PrismLauncher/data/PrismLauncher/instances/Calculo/minecraft/saves/AULA CALCULO/datapacks/projeto_calculo/data/matematica/function"

    def atualizar_campos(self):
        """Mostra ou esconde o campo g(x) de forma dinâmica"""
        if self.var_curvas.get() == "2":
            self.entry_g.grid(row=1, column=0, columnspan=2, padx=5, pady=(0, 10), sticky="ew")
        else:
            self.entry_g.delete(0, 'end') 
            self.entry_g.grid_remove()    

    def log(self, mensagem):
        self.textbox.insert(ctk.END, mensagem + "\n")
        self.textbox.see(ctk.END)
        self.update()

    def executar_geracao(self):
        self.textbox.delete("1.0", ctk.END)
        self.log("Iniciando cálculos...")

        eixo = self.var_eixo.get()
        qtd_curvas = self.var_curvas.get()
        f_texto = self.entry_f.get().replace("^", "**")
        g_texto = self.entry_g.get().replace("^", "**") if qtd_curvas == "2" else "0"
        
        try:
            x_inicio = int(self.entry_inicio.get())
            x_fim = int(self.entry_fim.get())
        except ValueError:
            self.log("[ERRO] Os limites X Inicial e X Final devem ser inteiros.")
            return

        if not f_texto:
            self.log("[ERRO] A função f(x) não pode estar vazia.")
            return

        x_sym, y_sym = sp.symbols('x y')
        bloco = "minecraft:light_blue_stained_glass" 
        
        try:
            expr_f = sp.sympify(f_texto)
            expr_g = sp.sympify(g_texto)
        except Exception as e:
            self.log(f"[ERRO] Sintaxe inválida: Verifique a aba de instruções.\nDetalhe: {e}")
            return

        if eixo == 'Y':
            self.log("Calculando inversas para rotação em Y...")
            try:
                sol_f = sp.solve(sp.Eq(y_sym, expr_f), x_sym)
                expr_f_uso = sol_f[0] if sol_f else sp.Number(0)
                
                if qtd_curvas == '2':
                    sol_g = sp.solve(sp.Eq(y_sym, expr_g), x_sym)
                    expr_g_uso = sol_g[0] if sol_g else sp.Number(0)
                else:
                    expr_g_uso = sp.Number(0)
            except Exception as e:
                self.log(f"[ERRO] Falha ao inverter funções: {e}")
                return
                
            self.log(f"Inversa f: x = {expr_f_uso}")
            if qtd_curvas == '2':
                self.log(f"Inversa g: x = {expr_g_uso}")

            try:
                val_inicio = int(expr_f.subs(x_sym, x_inicio).evalf())
                val_fim = int(expr_f.subs(x_sym, x_fim).evalf())
            except Exception:
                self.log("[ERRO] Limites em Y muito complexos.")
                return

            if val_inicio > val_fim:
                val_inicio, val_fim = val_fim, val_inicio
                
            func_f_calc = sp.lambdify(y_sym, expr_f_uso, modules=['math'])
            func_g_calc = sp.lambdify(y_sym, expr_g_uso, modules=['math'])
            
        else:
            expr_f_uso, expr_g_uso = expr_f, expr_g
            val_inicio, val_fim = x_inicio, x_fim
            func_f_calc = sp.lambdify(x_sym, expr_f_uso, modules=['math'])
            func_g_calc = sp.lambdify(x_sym, expr_g_uso, modules=['math'])

        self.log("Calculando Integral Analítica (Aguarde)...")
        volume_exato = 0
        dx = 0.001  
        atual = val_inicio

        while atual < val_fim:
            try:
                v_f = func_f_calc(atual)
                v_g = func_g_calc(atual)
                r_ext = max(abs(v_f), abs(v_g))
                r_int = min(abs(v_f), abs(v_g))
                volume_exato += math.pi * (r_ext**2 - r_int**2) * dx
            except Exception:
                pass
            atual += dx

        self.log("Gerando malha de Voxels...")
        comandos = []
        volume_em_blocos = 0

        for val_eixo in range(val_inicio, val_fim + 1):
            try:
                v_f = func_f_calc(val_eixo)
                v_g = func_g_calc(val_eixo)
                raio_ext = int(max(abs(v_f), abs(v_g)))
                raio_int = int(min(abs(v_f), abs(v_g)))
            except Exception:
                continue 
            
            for t1 in range(-raio_ext, raio_ext + 1):
                for t2 in range(-raio_ext, raio_ext + 1):
                    distancia_quadrada = t1**2 + t2**2
                    if (raio_int**2 <= distancia_quadrada <= raio_ext**2):
                        if eixo == 'X':
                            comandos.append(f"setblock ~{val_eixo} ~{t1} ~{t2} {bloco}")
                        else:
                            comandos.append(f"setblock ~{t1} ~{val_eixo} ~{t2} {bloco}")
                        volume_em_blocos += 1

        self.log("Exportando arquivo para o Minecraft...")
        try:
            os.makedirs(self.caminho_pasta, exist_ok=True)
            caminho_completo = os.path.join(self.caminho_pasta, "gerar_solido.mcfunction")
            with open(caminho_completo, "w") as arquivo:
                for comando in comandos:
                    arquivo.write(comando + "\n")
        except Exception as e:
            self.log(f"[ERRO GRAVE] Falha ao salvar arquivo: {e}")
            return

        erro_percentual = abs(volume_exato - volume_em_blocos) / volume_exato * 100 if volume_exato > 0 else 0

        self.log("-" * 45)
        self.log(" RESULTADOS FINAIS ")
        self.log("-" * 45)
        self.log(f"Modo:              Eixo {eixo} | {'f(x)-g(x)' if qtd_curvas == '2' else 'f(x)'}")
        self.log(f"Volume Analítico:  {volume_exato:.2f} unidades de volume(u.v.)")
        self.log(f"Volume no Jogo:    {volume_em_blocos:.2f} blocos")
        self.log(f"Erro do Voxel:     {erro_percentual:.2f}%")
        self.log("=============================================")
        self.log("Sucesso! Digite /function matematica:gerar_solido no jogo.")

if __name__ == "__main__":
    app = AppCalculo()
    app.mainloop()