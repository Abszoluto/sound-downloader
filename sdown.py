import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import glob
import threading
import requests
import shutil
import time
from mutagen.mp3 import MP3

# Variável global para bitrate desejado
qualidade_desejada = 320

# Pasta interna onde os arquivos serão salvos
diretorio_destino = os.path.join(os.getcwd(), "downloaded_audio")
os.makedirs(diretorio_destino, exist_ok=True)

# Instala ffmpeg automaticamente
def instalar_ffmpeg():
    if shutil.which("ffmpeg"):
        return True

    status_var.set("FFmpeg não encontrado. Baixando...")
    janela.update()

    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = "ffmpeg.zip"

    try:
        with requests.get(url, stream=True) as r:
            with open(zip_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        shutil.unpack_archive(zip_path, "ffmpeg_temp", 'zip')
        pasta = next(p for p in os.listdir("ffmpeg_temp") if os.path.isdir(os.path.join("ffmpeg_temp", p)))
        bin_path = os.path.join("ffmpeg_temp", pasta, "bin")

        for exe in ["ffmpeg.exe", "ffplay.exe", "ffprobe.exe"]:
            shutil.copy(os.path.join(bin_path, exe), os.getcwd())

        os.environ["PATH"] += os.pathsep + os.getcwd()
        os.remove(zip_path)
        status_var.set("FFmpeg instalado.")
        return True

    except Exception as e:
        messagebox.showerror("Erro ao instalar FFmpeg", str(e))
        return False

def baixar_musica():
    url = entrada_url.get().strip()
    if not url:
        messagebox.showwarning("Atenção", "Insira o link da música.")
        return

    botao_baixar.config(state=tk.DISABLED)
    barra_progresso.start(10)
    status_var.set("Verificando FFmpeg...")
    janela.update()

    if not instalar_ffmpeg():
        status_var.set("Erro ao instalar FFmpeg.")
        botao_baixar.config(state=tk.NORMAL)
        barra_progresso.stop()
        return

    status_var.set("Baixando...")
    janela.update()

    def thread_download():
        try:
            arquivos_antes = set(glob.glob("*.mp3"))

            cmd = ["scdl", "-l", url, "--onlymp3"]
            resultado = subprocess.run(cmd, capture_output=True, text=True)

            if resultado.returncode != 0:
                raise Exception(resultado.stderr)

            time.sleep(1)
            arquivos_depois = set(glob.glob("*.mp3"))
            novos = list(arquivos_depois - arquivos_antes)
            if not novos:
                raise Exception("Nenhum arquivo MP3 foi detectado.")

            arquivo_mp3 = novos[0]
            caminho_final = os.path.join(diretorio_destino, arquivo_mp3)
            shutil.move(arquivo_mp3, caminho_final)

            audio = MP3(caminho_final)
            bitrate_detectado = int(audio.info.bitrate / 1000)

            barra_progresso.stop()
            botao_baixar.config(state=tk.NORMAL)

            if bitrate_detectado < qualidade_desejada:
                status_var.set(f"Qualidade detectada: {bitrate_detectado} kbps")
                messagebox.showwarning(
                    "Qualidade não disponível",
                    f"Você pediu {qualidade_desejada} kbps, mas a faixa tem apenas {bitrate_detectado} kbps."
                )
            else:
                status_var.set(f"Download concluído em {bitrate_detectado} kbps.")
                messagebox.showinfo("Sucesso", f"Download completo em {bitrate_detectado} kbps!")

        except Exception as e:
            barra_progresso.stop()
            botao_baixar.config(state=tk.NORMAL)
            status_var.set("Erro durante o download.")
            messagebox.showerror("Erro", str(e))

    threading.Thread(target=thread_download).start()

def set_qualidade(q):
    global qualidade_desejada
    qualidade_desejada = q
    status_var.set(f"Qualidade desejada: {q} kbps")
    janela.update()

# ---------- INTERFACE ---------- #
janela = tk.Tk()
janela.title("SoundCloud Hacker Downloader")
janela.geometry("600x350")
janela.configure(bg="black")
janela.iconbitmap("icon.ico")
janela.resizable(False, False)

fonte = ("Courier New", 12, "bold")
verde = "#00FF00"

tk.Label(janela, text="Insira o link do SoundCloud:", font=fonte, fg=verde, bg="black").pack(pady=10)
entrada_url = tk.Entry(janela, width=70, font=fonte, bg="black", fg=verde, insertbackground=verde)
entrada_url.pack(pady=5)

frame_botoes = tk.Frame(janela, bg="black")
frame_botoes.pack(pady=10)

tk.Label(frame_botoes, text="Escolha a qualidade:", font=fonte, fg=verde, bg="black").pack(side=tk.LEFT, padx=5)

for q in [128, 192, 320]:
    tk.Button(
        frame_botoes,
        text=f"{q} kbps",
        font=fonte,
        fg="black",
        bg=verde,
        activebackground="lime",
        command=lambda q=q: set_qualidade(q)
    ).pack(side=tk.LEFT, padx=5)

botao_baixar = tk.Button(janela, text="BAIXAR", font=fonte, bg="black", fg=verde, command=baixar_musica)
botao_baixar.pack(pady=10)

barra_progresso = ttk.Progressbar(janela, orient="horizontal", length=500, mode="indeterminate")
barra_progresso.pack(pady=10)

status_var = tk.StringVar()
status_var.set("Aguardando...")
status_label = tk.Label(janela, textvariable=status_var, font=fonte, fg=verde, bg="black")
status_label.pack()

estilo = ttk.Style()
estilo.theme_use('default')
estilo.configure("TProgressbar", thickness=20, troughcolor='black', background='lime')

janela.mainloop()