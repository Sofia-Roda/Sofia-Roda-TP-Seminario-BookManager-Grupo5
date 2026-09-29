import datetime

from book_manager.entities.entities import (
    CotizacionDolar,
    Editorial,
    Genero,
    Libro,
    Moneda,
    Precio,
    Stock,
    TipoCotizacion,
)


# --------------------------------------------Validaciones de datos ingresados--------------------------------------------

def pedir_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debe ingresar un número entero.")


def pedir_float(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Debe ingresar un número válido.")


def pedir_fecha(mensaje: str) -> datetime.date:
    while True:
        fecha = input(mensaje)
        partes = fecha.split("-")

        if len(partes) == 3:
            try:
                return datetime.date(
                    int(partes[0]),
                    int(partes[1]),
                    int(partes[2]),
                )
            except ValueError:
                print("La fecha ingresada no es válida.")
        else:
            print("Use el formato AAAA-MM-DD.")


# =========================================================
# GÉNEROS
# =========================================================

def listar_generos(repo_generos) -> None:
    print("\n--- LISTADO DE GÉNEROS ---")

    generos = repo_generos.leer_todos()

    if len(generos) == 0:
        print("No hay géneros cargados.")
        return

    for genero in generos:
        print(
            genero.id,
            "-",
            genero.nombre,
            "-",
            genero.descripcion,
        )


def crear_genero(repo_generos) -> None:
    print("\n--- NUEVO GÉNERO ---")

    genero = Genero(
        id=pedir_entero("ID: "),
        nombre=input("Nombre: "),
        descripcion=input("Descripción: "),
    )

    try:
        repo_generos.crear(genero)
        print("Género creado correctamente.")
    except ValueError as error:
        print("Error:", error)


def modificar_genero(repo_generos) -> None:
    print("\n--- MODIFICAR GÉNERO ---")

    id_genero = pedir_entero("ID del género: ")

    genero = repo_generos.leer_por_id(id_genero)

    if genero is None:
        print("No se encontró el género.")
        return

    genero.nombre = input("Nuevo nombre: ")
    genero.descripcion = input("Nueva descripción: ")

    repo_generos.actualizar(genero)

    print("Género actualizado correctamente.")


def eliminar_genero(repo_generos) -> None:
    print("\n--- ELIMINAR GÉNERO ---")

    id_genero = pedir_entero("ID del género: ")

    if repo_generos.eliminar(id_genero):
        print("Género eliminado correctamente.")
    else:
        print("No se encontró el género.")


def menu_generos(repo_generos) -> None:
    while True:

        print("\n=== GÉNEROS ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        opcion = input("Opción: ")

        match opcion:

            case "1":
                listar_generos(repo_generos)

            case "2":
                crear_genero(repo_generos)

            case "3":
                modificar_genero(repo_generos)

            case "4":
                eliminar_genero(repo_generos)

            case "0":
                break

            case _:
                print("Opción inválida.")


# =========================================================
# EDITORIALES
# =========================================================

def listar_editoriales(repo_editoriales) -> None:
    print("\n--- LISTADO DE EDITORIALES ---")

    editoriales = repo_editoriales.leer_todos()

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


def crear_editorial(repo_editoriales) -> None:
    print("\n--- NUEVA EDITORIAL ---")

    editorial = Editorial(
        id=pedir_entero("ID: "),
        nombre=input("Nombre: "),
        cuit=input("CUIT: "),
        email=input("Email: "),
        telefono=input("Teléfono: "),
        pais=input("País: "),
    )

    try:
        repo_editoriales.crear(editorial)
        print("Editorial creada correctamente.")
    except ValueError as error:
        print("Error:", error)


def modificar_editorial(repo_editoriales) -> None:
    print("\n--- MODIFICAR EDITORIAL ---")

    id_editorial = pedir_entero("ID de la editorial: ")

    editorial = repo_editoriales.leer_por_id(id_editorial)

    if editorial is None:
        print("No se encontró la editorial.")
        return

    editorial.nombre = input("Nuevo nombre: ")
    editorial.cuit = input("Nuevo CUIT: ")
    editorial.email = input("Nuevo email: ")
    editorial.telefono = input("Nuevo teléfono: ")
    editorial.pais = input("Nuevo país: ")

    repo_editoriales.actualizar(editorial)

    print("Editorial actualizada correctamente.")


def eliminar_editorial(repo_editoriales) -> None:
    print("\n--- ELIMINAR EDITORIAL ---")

    id_editorial = pedir_entero("ID de la editorial: ")

    if repo_editoriales.eliminar(id_editorial):
        print("Editorial eliminada correctamente.")
    else:
        print("No se encontró la editorial.")


def menu_editoriales(repo_editoriales) -> None:
    while True:

        print("\n=== EDITORIALES ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        opcion = input("Opción: ")

        match opcion:

            case "1":
                listar_editoriales(repo_editoriales)

            case "2":
                crear_editorial(repo_editoriales)

            case "3":
                modificar_editorial(repo_editoriales)

            case "4":
                eliminar_editorial(repo_editoriales)

            case "0":
                break

            case _:
                print("Opción inválida.")


# =========================================================
# MONEDAS
# =========================================================

def listar_monedas(repo_monedas) -> None:
    print("\n--- LISTADO DE MONEDAS ---")

    monedas = repo_monedas.leer_todos()

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


def crear_moneda(repo_monedas) -> None:
    print("\n--- NUEVA MONEDA ---")

    moneda = Moneda(
        id=pedir_entero("ID: "),
        nombre=input("Nombre: "),
        simbolo=input("Símbolo: "),
        codigo=input("Código: "),
    )

    try:
        repo_monedas.crear(moneda)
        print("Moneda creada correctamente.")
    except ValueError as error:
        print("Error:", error)


def modificar_moneda(repo_monedas) -> None:
    print("\n--- MODIFICAR MONEDA ---")

    id_moneda = pedir_entero("ID de la moneda: ")

    moneda = repo_monedas.leer_por_id(id_moneda)

    if moneda is None:
        print("No se encontró la moneda.")
        return

    moneda.nombre = input("Nuevo nombre: ")
    moneda.simbolo = input("Nuevo símbolo: ")
    moneda.codigo = input("Nuevo código: ")

    repo_monedas.actualizar(moneda)

    print("Moneda actualizada correctamente.")


def eliminar_moneda(repo_monedas) -> None:
    print("\n--- ELIMINAR MONEDA ---")

    id_moneda = pedir_entero("ID de la moneda: ")

    if repo_monedas.eliminar(id_moneda):
        print("Moneda eliminada correctamente.")
    else:
        print("No se encontró la moneda.")


def menu_monedas(repo_monedas) -> None:
    while True:

        print("\n=== MONEDAS ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        opcion = input("Opción: ")

        match opcion:

            case "1":
                listar_monedas(repo_monedas)

            case "2":
                crear_moneda(repo_monedas)

            case "3":
                modificar_moneda(repo_monedas)

            case "4":
                eliminar_moneda(repo_monedas)

            case "0":
                break

            case _:
                print("Opción inválida.")


# =========================================================
# TIPOS DE COTIZACIÓN
# =========================================================

def listar_tipos_cotizacion(repo_tipos) -> None:
    print("\n--- LISTADO DE TIPOS DE COTIZACIÓN ---")

    tipos = repo_tipos.leer_todos()

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


def crear_tipo_cotizacion(repo_tipos) -> None:
    print("\n--- NUEVO TIPO DE COTIZACIÓN ---")

    tipo = TipoCotizacion(
        id=pedir_entero("ID: "),
        nombre=input("Nombre: "),
        descripcion=input("Descripción: "),
    )

    try:
        repo_tipos.crear(tipo)
        print("Tipo de cotización creado correctamente.")
    except ValueError as error:
        print("Error:", error)


def modificar_tipo_cotizacion(repo_tipos) -> None:
    print("\n--- MODIFICAR TIPO DE COTIZACIÓN ---")

    id_tipo = pedir_entero("ID del tipo: ")

    tipo = repo_tipos.leer_por_id(id_tipo)

    if tipo is None:
        print("No se encontró el tipo de cotización.")
        return

    tipo.nombre = input("Nuevo nombre: ")
    tipo.descripcion = input("Nueva descripción: ")

    repo_tipos.actualizar(tipo)

    print("Tipo de cotización actualizado correctamente.")


def eliminar_tipo_cotizacion(repo_tipos) -> None:
    print("\n--- ELIMINAR TIPO DE COTIZACIÓN ---")

    id_tipo = pedir_entero("ID del tipo: ")

    if repo_tipos.eliminar(id_tipo):
        print("Tipo de cotización eliminado correctamente.")
    else:
        print("No se encontró el tipo de cotización.")


def menu_tipos_cotizacion(repo_tipos) -> None:
    while True:

        print("\n=== TIPOS DE COTIZACIÓN ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        opcion = input("Opción: ")

        match opcion:

            case "1":
                listar_tipos_cotizacion(repo_tipos)

            case "2":
                crear_tipo_cotizacion(repo_tipos)

            case "3":
                modificar_tipo_cotizacion(repo_tipos)

            case "4":
                eliminar_tipo_cotizacion(repo_tipos)

            case "0":
                break

            case _:
                print("Opción inválida.")


# =========================================================
# LIBROS
# =========================================================

def listar_libros(repo_libros) -> None:
    print("\n--- LISTADO DE LIBROS ---")

    libros = repo_libros.leer_todos()

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


def crear_libro(
    repo_libros,
    repo_generos,
    repo_editoriales,
) -> None:

    print("\n--- NUEVO LIBRO ---")

    genero = repo_generos.leer_por_id(
        pedir_entero("ID del género: ")
    )

    if genero is None:
        print("No existe un género con ese ID.")
        return

    editorial = repo_editoriales.leer_por_id(
        pedir_entero("ID de la editorial: ")
    )

    if editorial is None:
        print("No existe una editorial con ese ID.")
        return

    libro = Libro(
        id=pedir_entero("ID del libro: "),
        isbn=input("ISBN: "),
        titulo=input("Título: "),
        autor=input("Autor: "),
        genero=genero,
        editorial=editorial,
        idioma=input("Idioma: "),
        fecha_publicacion=pedir_fecha(
            "Fecha de publicación (AAAA-MM-DD): "
        ),
        fecha_primera_publicacion=pedir_fecha(
            "Fecha de primera publicación (AAAA-MM-DD): "
        ),
        num_paginas=pedir_entero("Cantidad de páginas: "),
        peso=pedir_float("Peso: "),
        descripcion=input("Descripción: "),
        ranking=pedir_entero("Ranking: "),
    )

    try:
        repo_libros.crear(libro)
        print("Libro creado correctamente.")
    except ValueError as error:
        print("Error:", error)


def modificar_libro(
    repo_libros,
    repo_generos,
    repo_editoriales,
) -> None:

    print("\n--- MODIFICAR LIBRO ---")

    id_libro = pedir_entero("ID del libro: ")

    libro = repo_libros.leer_por_id(id_libro)

    if libro is None:
        print("No se encontró el libro.")
        return

    genero = repo_generos.leer_por_id(
        pedir_entero("Nuevo ID del género: ")
    )

    if genero is None:
        print("No existe un género con ese ID.")
        return

    editorial = repo_editoriales.leer_por_id(
        pedir_entero("Nuevo ID de la editorial: ")
    )

    if editorial is None:
        print("No existe una editorial con ese ID.")
        return

    libro.isbn = input("Nuevo ISBN: ")
    libro.titulo = input("Nuevo título: ")
    libro.autor = input("Nuevo autor: ")
    libro.genero = genero
    libro.editorial = editorial
    libro.idioma = input("Nuevo idioma: ")

    libro.fecha_publicacion = pedir_fecha(
        "Nueva fecha de publicación (AAAA-MM-DD): "
    )

    libro.fecha_primera_publicacion = pedir_fecha(
        "Nueva fecha de primera publicación (AAAA-MM-DD): "
    )

    libro.num_paginas = pedir_entero(
        "Nueva cantidad de páginas: "
    )

    libro.peso = pedir_float("Nuevo peso: ")

    libro.descripcion = input("Nueva descripción: ")

    libro.ranking = pedir_entero("Nuevo ranking: ")

    repo_libros.actualizar(libro)

    print("Libro actualizado correctamente.")


def eliminar_libro(repo_libros) -> None:
    print("\n--- ELIMINAR LIBRO ---")

    id_libro = pedir_entero("ID del libro: ")

    if repo_libros.eliminar(id_libro):
        print("Libro eliminado correctamente.")
    else:
        print("No se encontró el libro.")


def menu_libros(
    repo_libros,
    repo_generos,
    repo_editoriales,
) -> None:

    while True:

        print("\n=== LIBROS ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        opcion = input("Opción: ")

        match opcion:

            case "1":
                listar_libros(repo_libros)

            case "2":
                crear_libro(
                    repo_libros,
                    repo_generos,
                    repo_editoriales,
                )

            case "3":
                modificar_libro(
                    repo_libros,
                    repo_generos,
                    repo_editoriales,
                )

            case "4":
                eliminar_libro(repo_libros)

            case "0":
                break

            case _:
                print("Opción inválida.")


# =========================================================
# PRECIOS
# =========================================================

def listar_precios(repo_precios) -> None:
    print("\n--- LISTADO DE PRECIOS ---")

    precios = repo_precios.leer_todos()

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


def crear_precio(
    repo_precios,
    repo_libros,
    repo_monedas,
) -> None:

    print("\n--- NUEVO PRECIO ---")

    libro = repo_libros.leer_por_id(
        pedir_entero("ID del libro: ")
    )

    if libro is None:
        print("No existe un libro con ese ID.")
        return

    moneda = repo_monedas.leer_por_id(
        pedir_entero("ID de la moneda: ")
    )

    if moneda is None:
        print("No existe una moneda con ese ID.")
        return

    precio = Precio(
        id=pedir_entero("ID del precio: "),
        libro=libro,
        moneda=moneda,
        valor=pedir_float("Valor: "),
    )

    try:
        repo_precios.crear(precio)
        print("Precio creado correctamente.")
    except ValueError as error:
        print("Error:", error)


def modificar_precio(
    repo_precios,
    repo_libros,
    repo_monedas,
) -> None:

    print("\n--- MODIFICAR PRECIO ---")

    id_precio = pedir_entero("ID del precio: ")

    precio = repo_precios.leer_por_id(id_precio)

    if precio is None:
        print("No se encontró el precio.")
        return

    libro = repo_libros.leer_por_id(
        pedir_entero("Nuevo ID del libro: ")
    )

    if libro is None:
        print("No existe un libro con ese ID.")
        return

    moneda = repo_monedas.leer_por_id(
        pedir_entero("Nuevo ID de la moneda: ")
    )

    if moneda is None:
        print("No existe una moneda con ese ID.")
        return

    precio.libro = libro
    precio.moneda = moneda
    precio.valor = pedir_float("Nuevo valor: ")

    repo_precios.actualizar(precio)

    print("Precio actualizado correctamente.")


def eliminar_precio(repo_precios) -> None:
    print("\n--- ELIMINAR PRECIO ---")

    id_precio = pedir_entero("ID del precio: ")

    if repo_precios.eliminar(id_precio):
        print("Precio eliminado correctamente.")
    else:
        print("No se encontró el precio.")


def menu_precios(
    repo_precios,
    repo_libros,
    repo_monedas,
) -> None:

    while True:

        print("\n=== PRECIOS ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        opcion = input("Opción: ")

        match opcion:

            case "1":
                listar_precios(repo_precios)

            case "2":
                crear_precio(
                    repo_precios,
                    repo_libros,
                    repo_monedas,
                )

            case "3":
                modificar_precio(
                    repo_precios,
                    repo_libros,
                    repo_monedas,
                )

            case "4":
                eliminar_precio(repo_precios)

            case "0":
                break

            case _:
                print("Opción inválida.")


# =========================================================
# STOCK
# =========================================================

def listar_stock(repo_stock, repo_libros) -> None:
    print("\n--- LISTADO DE STOCK ---")

    encontrado = False

    for libro in repo_libros.leer_todos():

        stock = repo_stock.leer_por_libro(libro.id)

        if stock is not None:
            encontrado = True

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

    if not encontrado:
        print("No hay registros de stock cargados.")


def crear_stock(repo_stock, repo_libros) -> None:
    print("\n--- NUEVO STOCK ---")

    libro = repo_libros.leer_por_id(
        pedir_entero("ID del libro: ")
    )

    if libro is None:
        print("No existe un libro con ese ID.")
        return

    stock = Stock(
        id=pedir_entero("ID del stock: "),
        libro=libro,
        cantidad=pedir_entero("Cantidad: "),
        estado=input("Estado: "),
        ubicacion=input("Ubicación: "),
        fecha_ingreso=pedir_fecha(
            "Fecha de ingreso (AAAA-MM-DD): "
        ),
    )

    try:
        repo_stock.crear(stock)
        print("Stock creado correctamente.")
    except ValueError as error:
        print("Error:", error)


def modificar_stock(repo_stock) -> None:
    print("\n--- MODIFICAR STOCK ---")

    id_libro = pedir_entero("ID del libro: ")

    stock = repo_stock.leer_por_libro(id_libro)

    if stock is None:
        print("No se encontró stock para ese libro.")
        return

    stock.cantidad = pedir_entero("Nueva cantidad: ")
    stock.estado = input("Nuevo estado: ")
    stock.ubicacion = input("Nueva ubicación: ")

    stock.fecha_ingreso = pedir_fecha(
        "Nueva fecha de ingreso (AAAA-MM-DD): "
    )

    repo_stock.actualizar(stock)

    print("Stock actualizado correctamente.")


def eliminar_stock(repo_stock) -> None:
    print("\n--- ELIMINAR STOCK ---")

    id_libro = pedir_entero("ID del libro: ")

    if repo_stock.eliminar(id_libro):
        print("Stock eliminado correctamente.")
    else:
        print("No se encontró stock para ese libro.")


def menu_stock(repo_stock, repo_libros) -> None:
    while True:

        print("\n=== STOCK ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        opcion = input("Opción: ")

        match opcion:

            case "1":
                listar_stock(
                    repo_stock,
                    repo_libros,
                )

            case "2":
                crear_stock(
                    repo_stock,
                    repo_libros,
                )

            case "3":
                modificar_stock(repo_stock)

            case "4":
                eliminar_stock(repo_stock)

            case "0":
                break

            case _:
                print("Opción inválida.")


# =========================================================
# COTIZACIONES DEL DÓLAR
# =========================================================

def listar_cotizaciones(
    repo_cotizaciones,
    repo_tipos,
) -> None:

    print("\n--- LISTADO DE COTIZACIONES ---")

    encontrado = False

    for tipo in repo_tipos.leer_todos():

        cotizaciones = (
            repo_cotizaciones.leer_historico_por_tipo(
                tipo.id
            )
        )

        for cotizacion in cotizaciones:

            encontrado = True

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

    if not encontrado:
        print("No hay cotizaciones cargadas.")


def crear_cotizacion(
    repo_cotizaciones,
    repo_tipos,
) -> None:

    print("\n--- NUEVA COTIZACIÓN ---")

    tipo = repo_tipos.leer_por_id(
        pedir_entero(
            "ID del tipo de cotización: "
        )
    )

    if tipo is None:
        print(
            "No existe un tipo de cotización con ese ID."
        )
        return

    cotizacion = CotizacionDolar(
        id=pedir_entero("ID de la cotización: "),
        tipo_cotizacion=tipo,
        fecha=pedir_fecha(
            "Fecha (AAAA-MM-DD): "
        ),
        valor=pedir_float("Valor: "),
    )

    try:
        repo_cotizaciones.crear(cotizacion)
        print("Cotización creada correctamente.")
    except ValueError as error:
        print("Error:", error)


def modificar_cotizacion(repo_cotizaciones) -> None:
    print("\n--- MODIFICAR COTIZACIÓN ---")

    id_tipo = pedir_entero(
        "ID del tipo de cotización: "
    )

    fecha = pedir_fecha(
        "Fecha de la cotización (AAAA-MM-DD): "
    )

    cotizacion = (
        repo_cotizaciones.leer_por_tipo_y_fecha(
            id_tipo,
            fecha,
        )
    )

    if cotizacion is None:
        print("No se encontró la cotización.")
        return

    cotizacion.valor = pedir_float(
        "Nuevo valor: "
    )

    repo_cotizaciones.actualizar(cotizacion)

    print("Cotización actualizada correctamente.")


def eliminar_cotizacion(repo_cotizaciones) -> None:
    print("\n--- ELIMINAR COTIZACIÓN ---")

    id_tipo = pedir_entero(
        "ID del tipo de cotización: "
    )

    fecha = pedir_fecha(
        "Fecha de la cotización (AAAA-MM-DD): "
    )

    if repo_cotizaciones.eliminar(
        id_tipo,
        fecha,
    ):
        print("Cotización eliminada correctamente.")
    else:
        print("No se encontró la cotización.")


def menu_cotizaciones(
    repo_cotizaciones,
    repo_tipos,
) -> None:

    while True:

        print("\n=== COTIZACIONES DEL DÓLAR ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        opcion = input("Opción: ")

        match opcion:

            case "1":
                listar_cotizaciones(
                    repo_cotizaciones,
                    repo_tipos,
                )

            case "2":
                crear_cotizacion(
                    repo_cotizaciones,
                    repo_tipos,
                )

            case "3":
                modificar_cotizacion(
                    repo_cotizaciones
                )

            case "4":
                eliminar_cotizacion(
                    repo_cotizaciones
                )

            case "0":
                break

            case _:
                print("Opción inválida.")


# =========================================================
# MENÚ PRINCIPAL
# =========================================================

def iniciar_menu(repositorios: dict) -> None:

    while True:

        print("\n================================")
        print("          BOOK MANAGER")
        print("================================")

        print("1. Géneros")
        print("2. Editoriales")
        print("3. Monedas")
        print("4. Tipos de cotización")
        print("5. Libros")
        print("6. Precios")
        print("7. Stock")
        print("8. Cotizaciones del dólar")
        print("0. Salir")

        opcion = input(
            "Seleccione una opción: "
        )

        match opcion:

            case "1":
                menu_generos(
                    repositorios["generos"]
                )

            case "2":
                menu_editoriales(
                    repositorios["editoriales"]
                )

            case "3":
                menu_monedas(
                    repositorios["monedas"]
                )

            case "4":
                menu_tipos_cotizacion(
                    repositorios[
                        "tipos_cotizacion"
                    ]
                )

            case "5":
                menu_libros(
                    repositorios["libros"],
                    repositorios["generos"],
                    repositorios["editoriales"],
                )

            case "6":
                menu_precios(
                    repositorios["precios"],
                    repositorios["libros"],
                    repositorios["monedas"],
                )

            case "7":
                menu_stock(
                    repositorios["stock"],
                    repositorios["libros"],
                )

            case "8":
                menu_cotizaciones(
                    repositorios["cotizaciones"],
                    repositorios[
                        "tipos_cotizacion"
                    ],
                )

            case "0":
                print("Programa finalizado.")
                break

            case _:
                print("Opción inválida.")