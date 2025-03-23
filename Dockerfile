### BUILDER ###
FROM python:3.12.3 AS builder

# Nastavení kořenové složky
WORKDIR /app

# Kopírování závislostí - v requirements.txt mám knihovny pro python
COPY requirements.txt .

# Instalace python balíčků
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


##############################################################################

### BASE BUILDER ###
FROM python:3.12.3-slim

# Nastavení kořenové složky
WORKDIR /app

# Zkopíruju stažené Python balíčky z builder fáze
COPY --from=builder /install /usr/local

# Zkopíruju všechno co je v aktuálním adresáři
COPY . .

# Vytvoření usera: appuser a přiřazení práv na složku /app
RUN useradd -m appuser && chown -R appuser /app

# Přepnutí na usera: appuser
USER appuser

# Zvoleni portu, na kterem docker pobezi
EXPOSE 5000

# Prikaz, ktery chci aby se provedl po spusteni

CMD [ "python3", "api.py" ]
