# SoundCloud Downloader

Uma aplicação gráfica para Windows que permite baixar músicas do SoundCloud com foco em simplicidade, qualidade e eliminação de anúncios.  
Desenvolvida para pessoas que querem baixar músicas com clareza sobre o que estão obtendo, sem distrações ou riscos.

---

## Recursos

- Seleção de qualidade de áudio (128 kbps, 192 kbps, 320 kbps)
- Validação da qualidade real do arquivo baixado
- Alerta caso a qualidade desejada não esteja disponível
- Exibição das qualidades disponíveis
- Instalação automática do FFmpeg (se necessário)
- Barra de progresso com efeito visual customizado
- Ícone personalizado incluso

---

## Requisitos

- Python 3.8 ou superior
- Sistema operacional Windows
- Acesso à internet para baixar dependências e faixas

---

## Instalação das dependências

Para rodar o aplicativo a partir do código-fonte, execute:

```bash
pip install mutagen requests pillow scdl
```

---

## Como usar

> O áudio baixado será salvo automaticamente na subpasta `downloaded_files/` do projeto.

> A aplicação agora permite ao usuário escolher o diretório de destino antes de iniciar o download.

1. Clone este repositório ou baixe os arquivos.
2. Certifique-se de que o arquivo `icon.ico` esteja na mesma pasta do script.
3. Execute o script principal:

```bash
python sdown.py
```

4. Cole o link da música do SoundCloud.
5. Escolha a qualidade desejada.
6. O áudio será automaticamente salvo na pasta `downloaded_files`, que será criada dentro do próprio projeto.
6. Clique em **BAIXAR**.
7. O app fará a verificação da qualidade e informará se a desejada está disponível. Se não estiver, será exibida a real.

---

## Distribuição

Se não quiser instalar dependências, use diretamente o executável `sdown.exe`, disponível na pasta `dist`.

---

## Observações

Este projeto foi criado para fins pessoais e educacionais.  
Ele automatiza tarefas permitidas por ferramentas públicas e não contorna proteções de conteúdo.  
O usuário final é responsável pelo uso ético e legal da aplicação.
