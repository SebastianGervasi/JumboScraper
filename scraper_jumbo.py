import time
from playwright.sync_api import sync_playwright

def scrape_jumbo_promos():
    url = "https://www.jumbo.com.ar/descuentos-del-dia"
    promos_extraidas = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Esperamos al DOM con un margen amplio
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        # Bajamos al final de la página para forzar la carga de los componentes dinámicos
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(6000) # 6 segundos de espera para dar tiempo al renderizado de Jumbo
        
        # Seleccionamos contenedores de texto
        elementos = page.locator("div, article, span")
        
        for i in range(elementos.count()):
            texto = elementos.nth(i).inner_text()
            if texto:
                texto_limpio = " ".join(texto.split())
                # Filtramos por palabras clave típicas de promociones bancarias
                if ("% de descuento" in texto_limpio.lower() or 
                    "cuotas sin interés" in texto_limpio.lower() or 
                    "reintegro" in texto_limpio.lower()) and len(texto_limpio) > 20:
                    
                    if texto_limpio not in promos_extraidas:
                        promos_extraidas.append(texto_limpio)
                        
        browser.close()

    # Guardamos los resultados en un archivo Markdown específico para Jumbo
    with open("promociones_jumbo.md", "w", encoding="utf-8") as f:
        f.write("# Promociones Bancarias - Jumbo\n\n")
        f.write("> Actualizado automáticamente mediante GitHub Actions.\n\n")
        
        if not promos_extraidas:
            f.write("No se encontraron promociones. Es posible que el sitio haya cambiado su estructura o demorado en cargar.\n")
        else:
            for idx, promo in enumerate(promos_extraidas, 1):
                f.write(f"### Promoción {idx}\n")
                f.write(f"{promo}\n\n---\n")

if __name__ == "__main__":
    scrape_jumbo_promos()
