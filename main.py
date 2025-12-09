import requests
import json

URL = "https://api-colombia.com/api"


def dish_fetch(num):
    """Obtiene la información de un plato específico por su ID."""
    API = f"{URL}/TypicalDish/{num}"

    try: 
        response = requests.get(API)

        if response.status_code == 404:
            return {"error": f"Plato con ID {num} no encontrado en la API"}
        
        response.raise_for_status()

        plato_data = response.json()

        return plato_data
    
    except requests.exceptions.RequestException as e:
        
        print(f"\n Error de conexión en dish_fetch: {e}")
        return {"error": "Error de conexión o de red."}



def full_menu():
    """Lista completa del menú para la presentación."""
    API = f"{URL}/TypicalDish"

    try:
        response = requests.get(API)
        response.raise_for_status()

       
        return {item["id"]: item["name"] for item in response.json()}
    
    except requests.exceptions.RequestException as e:
        print(f"Error: No se pudo cargar el menú: {e}")
        return None



def main():
    
    
    menu_map = full_menu() 
    if not menu_map:
        return 

    print("\n=============================================")
    print("      ¡BIENVENIDO AL MENÚ COLOMBIANO!        ")
    print("   (Datos obtenidos de la API en tiempo real) ")
    print("=============================================")
    print("Seleccione un plato típico para ver sus detalles:")
    
    
    for id, name in menu_map.items():
        print(f"  {id}. {name}")
        
    print("  0. Salir")
    print("---------------------------------------------")

    
    while True:
        try:
            seleccion = input("Ingrese el ID del plato (o 0 para salir): ")
            num_seleccionado = int(seleccion)

            if num_seleccionado == 0:
                print("\n¡Gracias por visitar nuestro menú! ¡Vuelva pronto!")
                break
            
            if num_seleccionado not in menu_map:
                print(f"\n ERROR: El ID {num_seleccionado} no está en el menú.")
                continue

          
            plato = dish_fetch(num_seleccionado)

            if "error" in plato:
                print(f"\n ERROR: {plato['error']}")
            else:
                
                print("\nDetalles del Plato Seleccionado")
                print(f"**Nombre:** {plato.get('name')}")
                print(f"**Región (Departamento):** {plato.get('department', {}).get('name', 'N/A')}") 
                print(f"**Descripción:** {plato.get('description')}")
                print(f"**Ingredientes:** {plato.get('ingredients')}")
                
                

        except ValueError:
            print("\nEntrada no válida. Por favor, ingrese un NÚMERO entero.")


if __name__ == "__main__":
    main()