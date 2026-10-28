"""Contiene la interfaz de consola y los menús del sistema Book Manager."""
import csv
import datetime

from book_manager.scraper.comparador import (
    comparar_precios_y_generar_alertas,
)
from book_manager.scraper.reporte_excel import generar_reporte_excel

# Lectura y validación de datos

def leer_entero(mensaje: str) -> int:
    """Solicita al usuario un número entero y valida la entrada."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debe ingresar un número entero")


def leer_decimal(mensaje: str) -> float:
    """Solicita al usuario un número decimal y valida la entrada."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Debe ingresar un número válido")


def leer_fecha(mensaje: str) -> datetime.date:
    """Solicita al usuario una fecha en formato AAAA-MM-DD y valida la entrada."""
    while True:
        fecha = input(mensaje)
        componentes = fecha.split("-")

        if len(componentes) == 3:
            try:
                return datetime.date(
                    int(componentes[0]),
                    int(componentes[1]),
                    int(componentes[2]),
                )
            except ValueError:
                print("La fecha ingresada no es válida")
        else:
            print("Use el formato AAAA-MM-DD")


#--------------------------------- CRUD de géneros---------------------------------

def mostrar_generos(genero_service) -> None:
    """Muestra todos los géneros registrados."""
    print("\n--- LISTADO DE GÉNEROS ---")

    generos = genero_service.listar()

    if len(generos) == 0:
        print("No hay géneros cargados")
        return

    for genero in generos:
        print(
            genero.id,
            "-",
            genero.nombre,
            "-",
            genero.descripcion,
        )


def registrar_genero(genero_service) -> None:
    """Solicita los datos y registra un nuevo género."""
    print("\n--- NUEVO GÉNERO ---")

    try:
        genero = genero_service.crear(
            nombre=input("Nombre: "),
            descripcion=input("Descripción: "),
        )
        print("Género creado correctamente con ID", genero.id)
    except ValueError as exc:
        print("Error:", exc)


def editar_genero(genero_service) -> None:
    """Solicita los datos y modifica un género existente."""
    print("\n--- MODIFICAR GÉNERO ---")

    genero_id = leer_entero("ID del género: ")

    if genero_service.obtener_por_id(genero_id) is None:
        print("No se encontró el género.")
        return

    try:
        genero_service.actualizar(
            genero_id,
            nombre=input("Nuevo nombre: "),
            descripcion=input("Nueva descripción: "),
        )
        print("Género actualizado correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def borrar_genero(genero_service) -> None:
    """Solicita un id y elimina el género correspondiente."""
    print("\n--- ELIMINAR GÉNERO ---")

    genero_id = leer_entero("ID del género: ")

    try:
        if genero_service.eliminar(genero_id):
            print("Género eliminado correctamente.")
        else:
            print("No se encontró el género.")
    except ValueError as exc:
        print("Error:", exc)


def gestionar_generos(genero_service) -> None:
    """Muestra y administra el menú de opciones de géneros."""
    while True:

        print("\n----- GÉNEROS -----")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        seleccion = input("Opción: ")

        match seleccion:

            case "1":
                mostrar_generos(genero_service)

            case "2":
                registrar_genero(genero_service)

            case "3":
                editar_genero(genero_service)

            case "4":
                borrar_genero(genero_service)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de editoriales ---------------------------------


def mostrar_editoriales(editorial_service) -> None:
    """Muestra todos las editoriales registradas."""
    
    print("\n--- LISTADO DE EDITORIALES ---")

    editoriales = editorial_service.listar()

    if len(editoriales) == 0:
        print("No hay editoriales cargadas.")
        return

    for editorial in editoriales:
        print(
            editorial.id,
            "-",
            editorial.nombre,
            "- CUIT:",
            editorial.cuit,
            "-",
            editorial.pais,
        )


def registrar_editorial(editorial_service) -> None:
    """Solicita los datos y registra una nueva editorial."""
    print("\n--- NUEVA EDITORIAL ---")

    try:
        editorial = editorial_service.crear(
            nombre=input("Nombre: "),
            cuit=input("CUIT: "),
            email=input("Email: "),
            telefono=input("Teléfono: "),
            pais=input("País: "),
        )
        print("Editorial creada correctamente con ID", editorial.id)
    except ValueError as exc:
        print("Error:", exc)


def editar_editorial(editorial_service) -> None:
    """Solicita los datos y modifica una editorial existente."""
    print("\n--- MODIFICAR EDITORIAL ---")

    editorial_id = leer_entero("ID de la editorial: ")

    if editorial_service.obtener_por_id(editorial_id) is None:
        print("No se encontró la editorial.")
        return

    try:
        editorial_service.actualizar(
            editorial_id,
            nombre=input("Nuevo nombre: "),
            cuit=input("Nuevo CUIT: "),
            email=input("Nuevo email: "),
            telefono=input("Nuevo teléfono: "),
            pais=input("Nuevo país: "),
        )
        print("Editorial actualizada correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def borrar_editorial(editorial_service) -> None:
    """Solicita un id y elimina la editorial correspondiente."""
    print("\n--- ELIMINAR EDITORIAL ---")

    editorial_id = leer_entero("ID de la editorial: ")

    try:
        if editorial_service.eliminar(editorial_id):
            print("Editorial eliminada correctamente.")
        else:
            print("No se encontró la editorial.")
    except ValueError as exc:
        print("Error:", exc)


def gestionar_editoriales(editorial_service) -> None:
    """Muestra y administra el menú de opciones de editoriales."""
    while True:

        print("\n=== EDITORIALES ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        seleccion = input("Opción: ")

        match seleccion:

            case "1":
                mostrar_editoriales(editorial_service)

            case "2":
                registrar_editorial(editorial_service)

            case "3":
                editar_editorial(editorial_service)

            case "4":
                borrar_editorial(editorial_service)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de monedas---------------------------------


def mostrar_monedas(moneda_service) -> None:
    """Muestra todos los géneros registrados."""
    print("\n--- LISTADO DE MONEDAS ---")

    monedas = moneda_service.listar()

    if len(monedas) == 0:
        print("No hay monedas cargadas.")
        return

    for moneda in monedas:
        print(
            moneda.id,
            "-",
            moneda.nombre,
            "-",
            moneda.codigo,
            "-",
            moneda.simbolo,
        )


def registrar_moneda(moneda_service) -> None:
    """Solicita los datos y registra un nueva moneda."""
    print("\n--- NUEVA MONEDA ---")

    try:
        moneda = moneda_service.crear(
            nombre=input("Nombre: "),
            simbolo=input("Símbolo: "),
            codigo=input("Código: "),
        )
        print("Moneda creada correctamente con ID", moneda.id)
    except ValueError as exc:
        print("Error:", exc)


def editar_moneda(moneda_service) -> None:
    """Solicita los datos y modifica una moneda existente."""
    print("\n--- MODIFICAR MONEDA ---")

    moneda_id = leer_entero("ID de la moneda: ")

    if moneda_service.obtener_por_id(moneda_id) is None:
        print("No se encontró la moneda.")
        return

    try:
        moneda_service.actualizar(
            moneda_id,
            nombre=input("Nuevo nombre: "),
            simbolo=input("Nuevo símbolo: "),
            codigo=input("Nuevo código: "),
        )
        print("Moneda actualizada correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def borrar_moneda(moneda_service) -> None:
    """Solicita un id y elimina la moneda correspondiente."""
    print("\n--- ELIMINAR MONEDA ---")

    moneda_id = leer_entero("ID de la moneda: ")

    try:
        if moneda_service.eliminar(moneda_id):
            print("Moneda eliminada correctamente.")
        else:
            print("No se encontró la moneda.")
    except ValueError as exc:
        print("Error:", exc)


def gestionar_monedas(moneda_service) -> None:
    """Muestra y administra el menú de opciones de monedas."""
    while True:

        print("\n=== MONEDAS ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        seleccion = input("Opción: ")

        match seleccion:

            case "1":
                mostrar_monedas(moneda_service)

            case "2":
                registrar_moneda(moneda_service)

            case "3":
                editar_moneda(moneda_service)

            case "4":
                borrar_moneda(moneda_service)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de tipos de cotización ---------------------------------


def mostrar_tipos_cotizacion(tipo_service) -> None:
    """Muestra todos los tipos de cotización registrados."""
    print("\n--- LISTADO DE TIPOS DE COTIZACIÓN ---")

    tipos = tipo_service.listar()

    if len(tipos) == 0:
        print("No hay tipos de cotización cargados.")
        return

    for tipo in tipos:
        print(
            tipo.id,
            "-",
            tipo.nombre,
            "-",
            tipo.descripcion,
        )


def registrar_tipo_cotizacion(tipo_service) -> None:
    """Solicita los datos y registra un nuevo tipo de cotización."""
    print("\n--- NUEVO TIPO DE COTIZACIÓN ---")

    try:
        tipo = tipo_service.crear(
            nombre=input("Nombre: "),
            descripcion=input("Descripción: "),
        )
        print("Tipo de cotización creado correctamente con ID", tipo.id)
    except ValueError as exc:
        print("Error:", exc)


def editar_tipo_cotizacion(tipo_service) -> None:
    """Solicita los datos y modifica un tipo de cotización existente."""
    print("\n--- MODIFICAR TIPO DE COTIZACIÓN ---")

    tipo_id = leer_entero("ID del tipo: ")

    if tipo_service.obtener_por_id(tipo_id) is None:
        print("No se encontró el tipo de cotización.")
        return

    try:
        tipo_service.actualizar(
            tipo_id,
            nombre=input("Nuevo nombre: "),
            descripcion=input("Nueva descripción: "),
        )
        print("Tipo de cotización actualizado correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def borrar_tipo_cotizacion(tipo_service) -> None:
    """Solicita un id y elimina el tipo de cotización correspondiente."""
    print("\n--- ELIMINAR TIPO DE COTIZACIÓN ---")

    tipo_id = leer_entero("ID del tipo: ")

    try:
        if tipo_service.eliminar(tipo_id):
            print("Tipo de cotización eliminado correctamente.")
        else:
            print("No se encontró el tipo de cotización.")
    except ValueError as exc:
        print("Error:", exc)


def gestionar_tipos_cotizacion(tipo_service) -> None:
    """Muestra y administra el menú de opciones de tipo de cotización."""
    while True:

        print("\n=== TIPOS DE COTIZACIÓN ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        seleccion = input("Opción: ")

        match seleccion:

            case "1":
                mostrar_tipos_cotizacion(tipo_service)

            case "2":
                registrar_tipo_cotizacion(tipo_service)

            case "3":
                editar_tipo_cotizacion(tipo_service)

            case "4":
                borrar_tipo_cotizacion(tipo_service)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de libros ---------------------------------


def mostrar_libros(libro_service) -> None:
    """Muestra todos los libros registrados."""
    print("\n--- LISTADO DE LIBROS ---")

    libros = libro_service.listar()

    if len(libros) == 0:
        print("No hay libros cargados.")
        return

    for libro in libros:
        print(
            libro.id,
            "-",
            libro.titulo,
            "- Autor:",
            libro.autor,
            "- Género:",
            libro.genero.nombre,
            "- Editorial:",
            libro.editorial.nombre,
        )


def registrar_libro(libro_service) -> None:
    """Solicita los datos y registra un nuevo libro."""
    print("\n--- NUEVO LIBRO ---")

    try:
        libro = libro_service.crear(
            genero_id=leer_entero("ID del género: "),
            editorial_id=leer_entero("ID de la editorial: "),
            isbn=input("ISBN: "),
            titulo=input("Título: "),
            autor=input("Autor: "),
            idioma=input("Idioma: "),
            fecha_publicacion=leer_fecha(
                "Fecha de publicación (AAAA-MM-DD): "
            ),
            fecha_primera_publicacion=leer_fecha(
                "Fecha de primera publicación (AAAA-MM-DD): "
            ),
            num_paginas=leer_entero("Cantidad de páginas: "),
            peso=leer_decimal("Peso: "),
            descripcion=input("Descripción: "),
            ranking=leer_entero("Ranking: "),
        )
        print("Libro creado correctamente con ID", libro.id)
    except ValueError as exc:
        print("Error:", exc)


def editar_libro(libro_service) -> None:
    """Solicita los datos y modifica un libro existente."""
    print("\n--- MODIFICAR LIBRO ---")

    libro_id = leer_entero("ID del libro: ")

    if libro_service.obtener_por_id(libro_id) is None:
        print("No se encontró el libro.")
        return

    try:
        libro_service.actualizar(
            libro_id,
            genero_id=leer_entero("Nuevo ID del género: "),
            editorial_id=leer_entero("Nuevo ID de la editorial: "),
            isbn=input("Nuevo ISBN: "),
            titulo=input("Nuevo título: "),
            autor=input("Nuevo autor: "),
            idioma=input("Nuevo idioma: "),
            fecha_publicacion=leer_fecha(
                "Nueva fecha de publicación (AAAA-MM-DD): "
            ),
            fecha_primera_publicacion=leer_fecha(
                "Nueva fecha de primera publicación (AAAA-MM-DD): "
            ),
            num_paginas=leer_entero("Nueva cantidad de páginas: "),
            peso=leer_decimal("Nuevo peso: "),
            descripcion=input("Nueva descripción: "),
            ranking=leer_entero("Nuevo ranking: "),
        )
        print("Libro actualizado correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def borrar_libro(libro_service) -> None:
    """Solicita un id y elimina el libro correspondiente."""
    print("\n--- ELIMINAR LIBRO ---")

    libro_id = leer_entero("ID del libro: ")

    try:
        if libro_service.eliminar(libro_id):
            print("Libro eliminado correctamente.")
        else:
            print("No se encontró el libro.")
    except ValueError as exc:
        print("Error:", exc)


def gestionar_libros(libro_service) -> None:
    """Muestra y administra el menú de opciones de libros."""
    while True:

        print("\n=== LIBROS ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        seleccion = input("Opción: ")

        match seleccion:

            case "1":
                mostrar_libros(libro_service)

            case "2":
                registrar_libro(libro_service)

            case "3":
                editar_libro(libro_service)

            case "4":
                borrar_libro(libro_service)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de precios ---------------------------------


def mostrar_precios(precio_service) -> None:
    """Muestra todos los precios registrados."""
    print("\n--- LISTADO DE PRECIOS ---")

    precios = precio_service.listar()

    if len(precios) == 0:
        print("No hay precios cargados.")
        return

    for precio in precios:
        print(
            precio.id,
            "- Libro:",
            precio.libro.titulo,
            "-",
            precio.moneda.codigo,
            precio.valor,
        )


def registrar_precio(precio_service) -> None:
    """Solicita los datos y registra un nuevo precio."""
    print("\n--- NUEVO PRECIO ---")

    try:
        precio = precio_service.crear(
            libro_id=leer_entero("ID del libro: "),
            moneda_id=leer_entero("ID de la moneda: "),
            valor=leer_decimal("Valor: "),
        )
        print("Precio creado correctamente con ID", precio.id)
    except ValueError as exc:
        print("Error:", exc)


def editar_precio(precio_service) -> None:
    """Solicita los datos y modifica un precio existente."""
    print("\n--- MODIFICAR PRECIO ---")

    precio_id = leer_entero("ID del precio: ")

    if precio_service.obtener_por_id(precio_id) is None:
        print("No se encontró el precio.")
        return

    try:
        precio_service.actualizar(
            precio_id,
            moneda_id=leer_entero("Nuevo ID de la moneda: "),
            valor=leer_decimal("Nuevo valor: "),
        )
        print("Precio actualizado correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def borrar_precio(precio_service) -> None:
    """Solicita un id y elimina el precio correspondiente."""
    print("\n--- ELIMINAR PRECIO ---")

    precio_id = leer_entero("ID del precio: ")

    if precio_service.eliminar(precio_id):
        print("Precio eliminado correctamente.")
    else:
        print("No se encontró el precio.")


def mostrar_precios_bimonetarios(
    precio_service,
    cotizacion_service,
    tipo_service,
) -> None:
    """Muestra los precios de los libros en ARS y su equivalente en USD."""
    print("\n--- LISTA DE PRECIOS BIMONETARIA ---")

    tipos = tipo_service.listar()

    if len(tipos) == 0:
        print("No hay tipos de cotización cargados.")
        return

    print("\nTipos de cotización disponibles:")

    for tipo in tipos:
        print(
            tipo.id,
            "-",
            tipo.nombre,
        )

    tipo_id = leer_entero(
        "\nSeleccione el ID del tipo de cotización: "
    )

    tipo = tipo_service.obtener_por_id(tipo_id)

    if tipo is None:
        print("No existe un tipo de cotización con ese ID.")
        return

    cotizaciones = cotizacion_service.listar_historico(tipo_id)

    if len(cotizaciones) == 0:
        print("No hay cotizaciones disponibles para ese tipo.")
        return

    cotizacion_actual = max(
        cotizaciones,
        key=lambda cotizacion: cotizacion.fecha,
    )

    precios = precio_service.listar()

    if len(precios) == 0:
        print("No hay precios cargados.")
        return

    print(
        "\nCotización utilizada:",
        tipo.nombre,
        "-",
        cotizacion_actual.fecha,
        "- $",
        cotizacion_actual.valor,
    )

    print("\n--- PRECIOS EN ARS Y USD ---")

    for precio in precios:

        if precio.moneda.codigo == "ARS":
            valor_usd = precio.valor / cotizacion_actual.valor

            print(
                precio.libro.titulo,
                "- ARS:",
                round(precio.valor, 2),
                "- USD:",
                round(valor_usd, 2),
            )

def exportar_precios_csv(precio_service) -> None:
    """Exporta los precios registrados a un archivo CSV."""
    print("\n--- EXPORTAR PRECIOS A CSV ---")

    precios = precio_service.listar()

    if len(precios) == 0:
        print("No hay precios para exportar.")
        return

    nombre_archivo = "precios_exportados.csv"

    with open(
        nombre_archivo,
        "w",
        newline="",
        encoding="utf-8",
    ) as archivo:
        escritor = csv.writer(archivo)

        escritor.writerow(
            [
                "libro_id",
                "titulo",
                "isbn",
                "moneda",
                "codigo_moneda",
                "simbolo",
                "precio",
            ]
        )

        for precio in precios:
            escritor.writerow(
                [
                    precio.libro.id,
                    precio.libro.titulo,
                    precio.libro.isbn,
                    precio.moneda.nombre,
                    precio.moneda.codigo,
                    precio.moneda.simbolo,
                    precio.valor,
                ]
            )

    print(
        "Archivo generado correctamente:",
        nombre_archivo,
    )

def gestionar_precios(precio_service,cotizacion_service,tipo_service,) -> None:
    """Muestra y administra el menú de opciones de precios."""
    while True:

        print("\n=== PRECIOS ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("5. Ver lista de precios bimonetaria")
        print("6. Exportar precios a CSV")
        print("0. Volver")

        seleccion = input("Opción: ")

        match seleccion:

            case "1":
                mostrar_precios(precio_service)

            case "2":
                registrar_precio(precio_service)

            case "3":
                editar_precio(precio_service)

            case "4":
                borrar_precio(precio_service)

            case "5":
                mostrar_precios_bimonetarios(precio_service,cotizacion_service,tipo_service,)

            case "6":
                exportar_precios_csv(precio_service)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de stock---------------------------------


def mostrar_stock(stock_service, libro_service) -> None:
    """Muestra todos los stocks registrados."""
    print("\n--- LISTADO DE STOCK ---")

    hay_registros = False

    for libro in libro_service.listar():

        stock = stock_service.obtener_por_libro(libro.id)

        if stock is not None:
            hay_registros = True

            print(
                "ID:",
                stock.id,
                "- Libro:",
                stock.libro.titulo,
                "- Cantidad:",
                stock.cantidad,
                "- Estado:",
                stock.estado,
                "- Ubicación:",
                stock.ubicacion,
                "- Fecha:",
                stock.fecha_ingreso,
            )

    if not hay_registros:
        print("No hay registros de stock cargados.")


def registrar_stock(stock_service) -> None:
    """Solicita los datos y registra un nuevo stock."""
    print("\n--- NUEVO STOCK ---")

    estados = ", ".join(sorted(stock_service.ESTADOS_VALIDOS))

    try:
        stock_service.crear(
            libro_id=leer_entero("ID del libro: "),
            cantidad=leer_entero("Cantidad: "),
            estado=input(f"Estado ({estados}): "),
            ubicacion=input("Ubicación: "),
            fecha_ingreso=leer_fecha(
                "Fecha de ingreso (AAAA-MM-DD): "
            ),
        )
        print("Stock creado correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def editar_stock(stock_service) -> None:
    """Solicita los datos y modifica un stock existente."""
    print("\n--- MODIFICAR STOCK ---")

    libro_id = leer_entero("ID del libro: ")

    if stock_service.obtener_por_libro(libro_id) is None:
        print("No se encontró stock para ese libro.")
        return

    estados = ", ".join(sorted(stock_service.ESTADOS_VALIDOS))

    try:
        stock_service.actualizar(
            libro_id,
            cantidad=leer_entero("Nueva cantidad: "),
            estado=input(f"Nuevo estado ({estados}): "),
            ubicacion=input("Nueva ubicación: "),
            fecha_ingreso=leer_fecha(
                "Nueva fecha de ingreso (AAAA-MM-DD): "
            ),
        )
        print("Stock actualizado correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def borrar_stock(stock_service) -> None:
    """Solicita un id y elimina el stock correspondiente."""
    print("\n--- ELIMINAR STOCK ---")

    libro_id = leer_entero("ID del libro: ")

    if stock_service.eliminar(libro_id):
        print("Stock eliminado correctamente.")
    else:
        print("No se encontró stock para ese libro.")


def gestionar_stock(stock_service, libro_service) -> None:
    """Muestra y administra el menú de opciones de stock."""
    while True:

        print("\n=== STOCK ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        seleccion = input("Opción: ")

        match seleccion:

            case "1":
                mostrar_stock(stock_service, libro_service)

            case "2":
                registrar_stock(stock_service)

            case "3":
                editar_stock(stock_service)

            case "4":
                borrar_stock(stock_service)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de cotizaciones---------------------------------


def mostrar_cotizaciones(cotizacion_service, tipo_service) -> None:
    """Muestra todas las cotizaciones registradas."""
    print("\n--- LISTADO DE COTIZACIONES ---")

    hay_registros = False

    for tipo in tipo_service.listar():

        for cotizacion in cotizacion_service.listar_historico(tipo.id):

            hay_registros = True

            print(
                "ID:",
                cotizacion.id,
                "- Tipo:",
                cotizacion.tipo_cotizacion.nombre,
                "- Fecha:",
                cotizacion.fecha,
                "- Valor:",
                cotizacion.valor,
            )

    if not hay_registros:
        print("No hay cotizaciones cargadas.")


def registrar_cotizacion(cotizacion_service) -> None:
    """Solicita los datos y registra una nueva cotización."""
    print("\n--- NUEVA COTIZACIÓN ---")

    try:
        cotizacion_service.crear(
            tipo_cotizacion_id=leer_entero("ID del tipo de cotización: "),
            fecha=leer_fecha("Fecha (AAAA-MM-DD): "),
            valor=leer_decimal("Valor: "),
        )
        print("Cotización creada correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def editar_cotizacion(cotizacion_service) -> None:
    """Solicita los datos y modifica una cotización existente."""
    print("\n--- MODIFICAR COTIZACIÓN ---")

    tipo_id = leer_entero("ID del tipo de cotización: ")
    fecha = leer_fecha("Fecha de la cotización (AAAA-MM-DD): ")

    if cotizacion_service.obtener_por_tipo_y_fecha(tipo_id, fecha) is None:
        print("No se encontró la cotización.")
        return

    try:
        cotizacion_service.actualizar(
            tipo_id,
            fecha,
            valor=leer_decimal("Nuevo valor: "),
        )
        print("Cotización actualizada correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def borrar_cotizacion(cotizacion_service) -> None:
    """Solicita un id y elimina la cotización correspondiente."""
    print("\n--- ELIMINAR COTIZACIÓN ---")

    tipo_id = leer_entero("ID del tipo de cotización: ")
    fecha = leer_fecha("Fecha de la cotización (AAAA-MM-DD): ")

    if cotizacion_service.eliminar(tipo_id, fecha):
        print("Cotización eliminada correctamente.")
    else:
        print("No se encontró la cotización.")

def obtener_cotizaciones_api(cotizacion_service) -> None:
    """Obtiene y muestra las cotizaciones consultadas desde la API."""
    print("\n--- OBTENER COTIZACIONES POR API ---")

    try:
        cotizaciones = cotizacion_service.obtener_cotizaciones()

        if len(cotizaciones) == 0:
            print("No se obtuvieron cotizaciones.")
            return

        print("Cotizaciones obtenidas correctamente:")

        for cotizacion in cotizaciones:
            print(
                cotizacion.tipo_cotizacion.nombre,
                "- Fecha:",
                cotizacion.fecha,
                "- Valor:",
                cotizacion.valor,
            )

    except RuntimeError as exc:
        print("Error:", exc)

def gestionar_cotizaciones(cotizacion_service, tipo_service) -> None:
    """Muestra y administra el menú de opciones de cotizaciones."""
    while True:

        print("\n=== COTIZACIONES DEL DÓLAR ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("5. Obtener cotizaciones por API")
        print("0. Volver")

        seleccion = input("Opción: ")

        match seleccion:

            case "1":
                mostrar_cotizaciones(cotizacion_service, tipo_service)

            case "2":
                registrar_cotizacion(cotizacion_service)

            case "3":
                editar_cotizacion(cotizacion_service)

            case "4":
                borrar_cotizacion(cotizacion_service)

            case "5":
                obtener_cotizaciones_api(cotizacion_service)

            case "0":
                break

            case _:
                print("Opción inválida.")

# ----------------------- Scraping, reportes y auditoría -----------------------


def ejecutar_scraping(
    libro_service,
    precio_service,
    auditoria_service,
) -> list[dict]:
    """Ejecuta el scraping y compara los precios con el catálogo interno."""
    print("\n--- EJECUTAR SCRAPING ---")

    diferencia_minima = leer_decimal(
        "Ingrese la diferencia mínima para generar una alerta: "
    )

    try:
        ruta_csv, alertas, comparaciones = (
            comparar_precios_y_generar_alertas(
                libro_service,
                precio_service,
                diferencia_minima,
            )
        )

        auditoria_service.registrar(
            accion="EJECUTAR_SCRAPING",
            detalles=(
                "Scraping ejecutado correctamente. "
                f"Comparaciones: {len(comparaciones)}. "
                f"Alertas: {len(alertas)}. "
                f"Archivo CSV: {ruta_csv}"
            ),
        )

        print("\nScraping finalizado correctamente.")
        print("Comparaciones realizadas:", len(comparaciones))
        print("Alertas generadas:", len(alertas))
        print("Archivo CSV:", ruta_csv)

        return comparaciones

    except (ValueError, RuntimeError) as exc:
        auditoria_service.registrar(
            accion="EJECUTAR_SCRAPING",
            detalles=(
                "La ejecución del scraping finalizó con error: "
                f"{type(exc).__name__}: {exc}"
            ),
        )

        print("Error:", exc)
        return []

def generar_reporte(
    comparaciones: list[dict],
    auditoria_service,
) -> None:
    """Genera el reporte Excel con las últimas comparaciones realizadas."""
    print("\n--- GENERAR REPORTE ---")

    try:
        ruta_excel = generar_reporte_excel(comparaciones)

        auditoria_service.registrar(
            accion="GENERAR_REPORTE",
            detalles=(
                "Reporte generado correctamente. "
                f"Comparaciones incluidas: {len(comparaciones)}. "
                f"Archivo Excel: {ruta_excel}"
            ),
        )

        print("\nReporte generado correctamente.")
        print("Archivo Excel:", ruta_excel)

    except ValueError as exc:
        auditoria_service.registrar(
            accion="GENERAR_REPORTE",
            detalles=(
                "La generación del reporte finalizó con error: "
                f"{type(exc).__name__}: {exc}"
            ),
        )

        print("Error:", exc)

def mostrar_historial_auditoria(auditoria_service) -> None:
    """Muestra el historial de auditorías registradas en el sistema."""
    print("\n--- HISTORIAL DE AUDITORÍA ---")

    auditorias = auditoria_service.listar()

    if len(auditorias) == 0:
        print("No hay auditorías registradas.")
        return

    for auditoria in auditorias:
        print(
            "\nID:",
            auditoria.id,
            "\nAcción:",
            auditoria.accion,
            "\nFecha:",
            auditoria.fecha,
            "\nDetalles:",
            auditoria.detalles,
        )

# Menú principal

def iniciar_menu(servicios: dict) -> None:
    """Muestra y administra el menú principal del sistema."""

    comparaciones = []
    
    while True:

        print("\n****************************** BOOK MANAGER ******************************")

        print("1. Géneros")
        print("2. Editoriales")
        print("3. Monedas")
        print("4. Tipos de cotización")
        print("5. Libros")
        print("6. Precios")
        print("7. Stock")
        print("8. Cotizaciones del dólar")
        print("9. Ejecutar scraping")
        print("10. Generar reporte")
        print("11. Ver historial de auditoría")
        print("0. Salir")

        seleccion = input(
            "Seleccione una opción: "
        )

        match seleccion:

            case "1":
                gestionar_generos(servicios["generos"])

            case "2":
                gestionar_editoriales(servicios["editoriales"])

            case "3":
                gestionar_monedas(servicios["monedas"])

            case "4":
                gestionar_tipos_cotizacion(servicios["tipos_cotizacion"])

            case "5":
                gestionar_libros(servicios["libros"])

            case "6":
                gestionar_precios(servicios["precios"],servicios["cotizaciones"],servicios["tipos_cotizacion"],)

            case "7":
                gestionar_stock(servicios["stock"], servicios["libros"])

            case "8":
                gestionar_cotizaciones(
                    servicios["cotizaciones"],
                    servicios["tipos_cotizacion"],
                )

            case "9":
                comparaciones = ejecutar_scraping(
                    servicios["libros"],
                    servicios["precios"],
                    servicios["auditorias"],
                )

            case "10":
                generar_reporte(
                    comparaciones,
                    servicios["auditorias"],
                )

            case "11":
                mostrar_historial_auditoria(
                    servicios["auditorias"],
                )

            case "0":
                print("-----Programa finalizado-----")
                break

            case _:
                print("Opción inválida.")
