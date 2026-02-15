# EXIF Photo Filter

> 🇺🇸 [Read in English](README.md)

Ferramenta de linha de comando para filtrar e copiar fotos com base na **data original de captura** (metadados EXIF), não nos timestamps do sistema de arquivos.

Útil para recuperar fotos de HDs antigos, discos externos ou backups onde as datas de criação/modificação dos arquivos podem ter sido alteradas ao copiar entre dispositivos.

## Por quê?

Quando você copia fotos entre drives, os timestamps do filesystem (`Criado em`, `Modificado em`) são sobrescritos. A única data confiável é a armazenada dentro da própria imagem — o campo EXIF `DateTimeOriginal`, gravado pela câmera no momento em que a foto foi tirada.

Este script lê esse campo e filtra de acordo.

## Requisitos

- Python 3.7+
- [Pillow](https://python-pillow.org/)

```bash
pip3 install Pillow
```

Para arquivos `.heic` (fotos de iPhone), instale também:

```bash
pip3 install pillow-heif
```

## Uso

```bash
python3 filter_photos.py <origem> <destino> [--start AAAA-MM-DD] [--end AAAA-MM-DD]
```

### Argumentos

| Argumento | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `source` | Sim | Diretório a ser varrido recursivamente |
| `dest` | Sim | Diretório onde as fotos encontradas serão copiadas |
| `--start` | Não | Data inicial, inclusiva (padrão: `2011-09-24`) |
| `--end` | Não | Data final, inclusiva (padrão: `2012-12-31`) |

### Exemplos

```bash
# Varrer um HD externo, copiar matches para a área de trabalho
python3 filter_photos.py /Volumes/MeuDrive/fotos ~/Desktop/FotosFiltradas

# Range de datas personalizado
python3 filter_photos.py /Volumes/MeuDrive/fotos ~/Desktop/FotosFiltradas --start 2015-01-01 --end 2015-12-31

# Windows
python3 filter_photos.py E:\fotos C:\FotosFiltradas --start 2012-06-01 --end 2012-06-30
```

## Saída

O script mostra progresso em tempo real com:

- Percentual e contador de arquivos
- Totais de copiados, ignorados e erros
- Tempo decorrido
- Cada arquivo encontrado é logado com sua data EXIF

```
Source: /Volumes/ABS-RECOVERY/fotos
Dest:   /Users/voce/Desktop/FotosFiltradas
Range:  2015-05-01 to 2015-05-01

Scanning files...
Found 643 image files

  + 2015-05-01 23:07 | IMG_6545.JPG
  + 2015-05-01 23:07 | IMG_6546.JPG
[100.0%] 643/643 | copied: 20 | skipped: 598 | errors: 25 | elapsed: 00:00:09

==================================================
  Done in 00:00:09
  Total scanned:  643
  Copied (match): 20
  Skipped:        598
  Errors:         25
  Output:         /Users/voce/Desktop/FotosFiltradas
==================================================
```

## Formatos Suportados

| Formato | Suporte EXIF |
|---------|-------------|
| `.jpg` / `.jpeg` | Sim — caso de uso principal |
| `.tiff` / `.tif` | Sim |
| `.png` | Raro — a maioria dos PNGs não possui dados EXIF |
| `.heic` | Sim — requer `pillow-heif` |

## Como Funciona

1. Varre recursivamente o diretório de origem em busca de arquivos de imagem
2. Abre cada arquivo e lê o EXIF `DateTimeOriginal` (tag 36867) ou `DateTimeDigitized` (tag 36868)
3. Se a data estiver dentro do range especificado, copia o arquivo para o destino usando `shutil.copy2` (preservando metadados)
4. Arquivos sem data EXIF são ignorados; arquivos corrompidos são registrados como erros

## Observações

- **Não-destrutivo**: o script apenas copia, nunca move ou apaga os originais
- **Saída plana**: todos os arquivos encontrados são copiados para uma única pasta de destino. Nomes duplicados serão sobrescritos
- **Arquivos corrompidos**: comum em HDs antigos/recuperados. O contador de `errors` reflete arquivos que o Pillow não consegue abrir — eles podem ser parcialmente recuperáveis com ferramentas especializadas

## Licença

MIT