SCRIPTS = extraccion_de_datos.py json_to_excel_copy.py

GENERATED = *.xlsx
GENERATED_TRASH = *.json
OUTPUT_DIR = tierlists

.PHONY: run_windows clean_windows run_linux clean_linux


# ----- Windows -----

windows: run_windows clean_windows

run_windows:
	@echo Ejecutando scripts...
	@echo Ejecutando extraccion_de_datos.py
	@python extraccion_de_datos.py
	@echo Ejecutando json_to_excel_copy.py
	@python json_to_excel_copy.py
	@echo Listo.

clean_windows:
	@echo Limpiando...
	@if not exist "$(OUTPUT_DIR)" mkdir "$(OUTPUT_DIR)"
	@for %%F in ($(GENERATED)) do @if exist "%%F" move /Y "%%F" "$(OUTPUT_DIR)" >NUL
	@for %%F in ($(GENERATED_TRASH)) do @if exist "%%F" del /F /Q "%%F"
	@echo Hecho.

# ----- Linux -----

linux: run_linux clean_linux

run_linux:
	@echo "Ejecutando scripts..."
	@for script in $(SCRIPTS); do \
		echo "-> Ejecutando $$script"; \
		python $$script; \
	done
	@echo "Listo."

clean_linux:
	@echo "Limpiando..."
	@mkdir -p $(OUTPUT_DIR)
	@sh -c 'mv $(GENERATED) $(OUTPUT_DIR) 2>/dev/null || true'
	@rm -f $(GENERATED_TRASH)
	@echo "Hecho."
