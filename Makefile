SCRIPTS = extraccion_de_datos.py json_to_excel.py

GENERATED = *.xlsx
GENERATED_TRASH = *.json
OUTPUT_DIR = tierlists

.PHONY: windows_run windows_clean linux_run linux_clean


# ----- Windows -----

windows: windows_run windows_clean

windows_run:
	@echo Ejecutando extraccion_de_datos.py
	@python extraccion_de_datos.py
	@echo Ejecutando json_to_excel.py
	@python json_to_excel.py
	@echo Listo.

windows_clean:
	@echo Limpiando basura
	@for %%F in ($(GENERATED_TRASH)) do @if exist "%%F" del /F /Q "%%F"
	@echo Moviendo Estadisticas a "tierlists"
	@if not exist "$(OUTPUT_DIR)" mkdir "$(OUTPUT_DIR)"
	@for %%F in ($(GENERATED)) do @if exist "%%F" move /Y "%%F" "$(OUTPUT_DIR)" >NUL
	@echo Hecho.

# ----- Linux -----

linux: linux_run linux_clean

linux_run:
	@echo "Ejecutando scripts..."
	@for script in $(SCRIPTS); do \
		echo "-> Ejecutando $$script"; \
		python $$script; \
	done
	@echo "Listo."

linux_clean:
	@echo "Limpiando..."
	@mkdir -p $(OUTPUT_DIR)
	@sh -c 'mv $(GENERATED) $(OUTPUT_DIR) 2>/dev/null || true'
	@rm -f $(GENERATED_TRASH)
	@echo "Hecho."
