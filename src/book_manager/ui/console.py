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


# Lectura y validación de datos

def leer_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Debe ingresar un número entero")


def leer_decimal(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Debe ingresar un número válido")


def leer_fecha(mensaje: str) -> datetime.date:
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

def mostrar_generos(generos_repo) -> None:
    print("\n--- LISTADO DE GÉNEROS ---")

    generos = generos_repo.leer_todos()

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


def registrar_genero(generos_repo) -> None:
    print("\n--- NUEVO GÉNERO ---")

    genero = Genero(
        id=leer_entero("ID: "),
        nombre=input("Nombre: "),
        descripcion=input("Descripción: "),
    )

    try:
        generos_repo.crear(genero)
        print("Género creado correctamente")
    except ValueError as exc:
        print("Error:", exc)


def editar_genero(generos_repo) -> None:
    print("\n--- MODIFICAR GÉNERO ---")

    genero_id = leer_entero("ID del género: ")

    genero = generos_repo.leer_por_id(genero_id)

    if genero is None:
        print("No se encontró el género.")
        return

    genero.nombre = input("Nuevo nombre: ")
    genero.descripcion = input("Nueva descripción: ")

    generos_repo.actualizar(genero)

    print("Género actualizado correctamente.")


def borrar_genero(generos_repo) -> None:
    print("\n--- ELIMINAR GÉNERO ---")

    genero_id = leer_entero("ID del género: ")

    if generos_repo.eliminar(genero_id):
        print("Género eliminado correctamente.")
    else:
        print("No se encontró el género.")


def gestionar_generos(generos_repo) -> None:
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
                mostrar_generos(generos_repo)

            case "2":
                registrar_genero(generos_repo)

            case "3":
                editar_genero(generos_repo)

            case "4":
                borrar_genero(generos_repo)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de editoriales ---------------------------------


def mostrar_editoriales(editoriales_repo) -> None:
    print("\n--- LISTADO DE EDITORIALES ---")

    editoriales = editoriales_repo.leer_todos()

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


def registrar_editorial(editoriales_repo) -> None:
    print("\n--- NUEVA EDITORIAL ---")

    editorial = Editorial(
        id=leer_entero("ID: "),
        nombre=input("Nombre: "),
        cuit=input("CUIT: "),
        email=input("Email: "),
        telefono=input("Teléfono: "),
        pais=input("País: "),
    )

    try:
        editoriales_repo.crear(editorial)
        print("Editorial creada correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def editar_editorial(editoriales_repo) -> None:
    print("\n--- MODIFICAR EDITORIAL ---")

    editorial_id = leer_entero("ID de la editorial: ")

    editorial = editoriales_repo.leer_por_id(editorial_id)

    if editorial is None:
        print("No se encontró la editorial.")
        return

    editorial.nombre = input("Nuevo nombre: ")
    editorial.cuit = input("Nuevo CUIT: ")
    editorial.email = input("Nuevo email: ")
    editorial.telefono = input("Nuevo teléfono: ")
    editorial.pais = input("Nuevo país: ")

    editoriales_repo.actualizar(editorial)

    print("Editorial actualizada correctamente.")


def borrar_editorial(editoriales_repo) -> None:
    print("\n--- ELIMINAR EDITORIAL ---")

    editorial_id = leer_entero("ID de la editorial: ")

    if editoriales_repo.eliminar(editorial_id):
        print("Editorial eliminada correctamente.")
    else:
        print("No se encontró la editorial.")


def gestionar_editoriales(editoriales_repo) -> None:
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
                mostrar_editoriales(editoriales_repo)

            case "2":
                registrar_editorial(editoriales_repo)

            case "3":
                editar_editorial(editoriales_repo)

            case "4":
                borrar_editorial(editoriales_repo)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de monedas---------------------------------


def mostrar_monedas(monedas_repo) -> None:
    print("\n--- LISTADO DE MONEDAS ---")

    monedas = monedas_repo.leer_todos()

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


def registrar_moneda(monedas_repo) -> None:
    print("\n--- NUEVA MONEDA ---")

    moneda = Moneda(
        id=leer_entero("ID: "),
        nombre=input("Nombre: "),
        simbolo=input("Símbolo: "),
        codigo=input("Código: "),
    )

    try:
        monedas_repo.crear(moneda)
        print("Moneda creada correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def editar_moneda(monedas_repo) -> None:
    print("\n--- MODIFICAR MONEDA ---")

    moneda_id = leer_entero("ID de la moneda: ")

    moneda = monedas_repo.leer_por_id(moneda_id)

    if moneda is None:
        print("No se encontró la moneda.")
        return

    moneda.nombre = input("Nuevo nombre: ")
    moneda.simbolo = input("Nuevo símbolo: ")
    moneda.codigo = input("Nuevo código: ")

    monedas_repo.actualizar(moneda)

    print("Moneda actualizada correctamente.")


def borrar_moneda(monedas_repo) -> None:
    print("\n--- ELIMINAR MONEDA ---")

    moneda_id = leer_entero("ID de la moneda: ")

    if monedas_repo.eliminar(moneda_id):
        print("Moneda eliminada correctamente.")
    else:
        print("No se encontró la moneda.")


def gestionar_monedas(monedas_repo) -> None:
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
                mostrar_monedas(monedas_repo)

            case "2":
                registrar_moneda(monedas_repo)

            case "3":
                editar_moneda(monedas_repo)

            case "4":
                borrar_moneda(monedas_repo)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de tipos de cotización ---------------------------------


def mostrar_tipos_cotizacion(tipos_repo) -> None:
    print("\n--- LISTADO DE TIPOS DE COTIZACIÓN ---")

    tipos = tipos_repo.leer_todos()

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


def registrar_tipo_cotizacion(tipos_repo) -> None:
    print("\n--- NUEVO TIPO DE COTIZACIÓN ---")

    tipo = TipoCotizacion(
        id=leer_entero("ID: "),
        nombre=input("Nombre: "),
        descripcion=input("Descripción: "),
    )

    try:
        tipos_repo.crear(tipo)
        print("Tipo de cotización creado correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def editar_tipo_cotizacion(tipos_repo) -> None:
    print("\n--- MODIFICAR TIPO DE COTIZACIÓN ---")

    tipo_id = leer_entero("ID del tipo: ")

    tipo = tipos_repo.leer_por_id(tipo_id)

    if tipo is None:
        print("No se encontró el tipo de cotización.")
        return

    tipo.nombre = input("Nuevo nombre: ")
    tipo.descripcion = input("Nueva descripción: ")

    tipos_repo.actualizar(tipo)

    print("Tipo de cotización actualizado correctamente.")


def borrar_tipo_cotizacion(tipos_repo) -> None:
    print("\n--- ELIMINAR TIPO DE COTIZACIÓN ---")

    tipo_id = leer_entero("ID del tipo: ")

    if tipos_repo.eliminar(tipo_id):
        print("Tipo de cotización eliminado correctamente.")
    else:
        print("No se encontró el tipo de cotización.")


def gestionar_tipos_cotizacion(tipos_repo) -> None:
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
                mostrar_tipos_cotizacion(tipos_repo)

            case "2":
                registrar_tipo_cotizacion(tipos_repo)

            case "3":
                editar_tipo_cotizacion(tipos_repo)

            case "4":
                borrar_tipo_cotizacion(tipos_repo)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de libros ---------------------------------


def mostrar_libros(libros_repo) -> None:
    print("\n--- LISTADO DE LIBROS ---")

    libros = libros_repo.leer_todos()

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


def registrar_libro(
    libros_repo,
    generos_repo,
    editoriales_repo,
) -> None:

    print("\n--- NUEVO LIBRO ---")

    genero = generos_repo.leer_por_id(
        leer_entero("ID del género: ")
    )

    if genero is None:
        print("No existe un género con ese ID.")
        return

    editorial = editoriales_repo.leer_por_id(
        leer_entero("ID de la editorial: ")
    )

    if editorial is None:
        print("No existe una editorial con ese ID.")
        return

    libro = Libro(
        id=leer_entero("ID del libro: "),
        isbn=input("ISBN: "),
        titulo=input("Título: "),
        autor=input("Autor: "),
        genero=genero,
        editorial=editorial,
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

    try:
        libros_repo.crear(libro)
        print("Libro creado correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def editar_libro(
    libros_repo,
    generos_repo,
    editoriales_repo,
) -> None:

    print("\n--- MODIFICAR LIBRO ---")

    libro_id = leer_entero("ID del libro: ")

    libro = libros_repo.leer_por_id(libro_id)

    if libro is None:
        print("No se encontró el libro.")
        return

    genero = generos_repo.leer_por_id(
        leer_entero("Nuevo ID del género: ")
    )

    if genero is None:
        print("No existe un género con ese ID.")
        return

    editorial = editoriales_repo.leer_por_id(
        leer_entero("Nuevo ID de la editorial: ")
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

    libro.fecha_publicacion = leer_fecha(
        "Nueva fecha de publicación (AAAA-MM-DD): "
    )

    libro.fecha_primera_publicacion = leer_fecha(
        "Nueva fecha de primera publicación (AAAA-MM-DD): "
    )

    libro.num_paginas = leer_entero(
        "Nueva cantidad de páginas: "
    )

    libro.peso = leer_decimal("Nuevo peso: ")

    libro.descripcion = input("Nueva descripción: ")

    libro.ranking = leer_entero("Nuevo ranking: ")

    libros_repo.actualizar(libro)

    print("Libro actualizado correctamente.")


def borrar_libro(libros_repo) -> None:
    print("\n--- ELIMINAR LIBRO ---")

    libro_id = leer_entero("ID del libro: ")

    if libros_repo.eliminar(libro_id):
        print("Libro eliminado correctamente.")
    else:
        print("No se encontró el libro.")


def gestionar_libros(
    libros_repo,
    generos_repo,
    editoriales_repo,
) -> None:

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
                mostrar_libros(libros_repo)

            case "2":
                registrar_libro(
                    libros_repo,
                    generos_repo,
                    editoriales_repo,
                )

            case "3":
                editar_libro(
                    libros_repo,
                    generos_repo,
                    editoriales_repo,
                )

            case "4":
                borrar_libro(libros_repo)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de precios ---------------------------------


def mostrar_precios(precios_repo) -> None:
    print("\n--- LISTADO DE PRECIOS ---")

    precios = precios_repo.leer_todos()

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


def registrar_precio(
    precios_repo,
    libros_repo,
    monedas_repo,
) -> None:

    print("\n--- NUEVO PRECIO ---")

    libro = libros_repo.leer_por_id(
        leer_entero("ID del libro: ")
    )

    if libro is None:
        print("No existe un libro con ese ID.")
        return

    moneda = monedas_repo.leer_por_id(
        leer_entero("ID de la moneda: ")
    )

    if moneda is None:
        print("No existe una moneda con ese ID.")
        return

    precio = Precio(
        id=leer_entero("ID del precio: "),
        libro=libro,
        moneda=moneda,
        valor=leer_decimal("Valor: "),
    )

    try:
        precios_repo.crear(precio)
        print("Precio creado correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def editar_precio(
    precios_repo,
    libros_repo,
    monedas_repo,
) -> None:

    print("\n--- MODIFICAR PRECIO ---")

    precio_id = leer_entero("ID del precio: ")

    precio = precios_repo.leer_por_id(precio_id)

    if precio is None:
        print("No se encontró el precio.")
        return

    libro = libros_repo.leer_por_id(
        leer_entero("Nuevo ID del libro: ")
    )

    if libro is None:
        print("No existe un libro con ese ID.")
        return

    moneda = monedas_repo.leer_por_id(
        leer_entero("Nuevo ID de la moneda: ")
    )

    if moneda is None:
        print("No existe una moneda con ese ID.")
        return

    precio.libro = libro
    precio.moneda = moneda
    precio.valor = leer_decimal("Nuevo valor: ")

    precios_repo.actualizar(precio)

    print("Precio actualizado correctamente.")


def borrar_precio(precios_repo) -> None:
    print("\n--- ELIMINAR PRECIO ---")

    precio_id = leer_entero("ID del precio: ")

    if precios_repo.eliminar(precio_id):
        print("Precio eliminado correctamente.")
    else:
        print("No se encontró el precio.")


def gestionar_precios(
    precios_repo,
    libros_repo,
    monedas_repo,
) -> None:

    while True:

        print("\n=== PRECIOS ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        seleccion = input("Opción: ")

        match seleccion:

            case "1":
                mostrar_precios(precios_repo)

            case "2":
                registrar_precio(
                    precios_repo,
                    libros_repo,
                    monedas_repo,
                )

            case "3":
                editar_precio(
                    precios_repo,
                    libros_repo,
                    monedas_repo,
                )

            case "4":
                borrar_precio(precios_repo)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de stock---------------------------------


def mostrar_stock(stock_repo, libros_repo) -> None:
    print("\n--- LISTADO DE STOCK ---")

    hay_registros = False

    for libro in libros_repo.leer_todos():

        stock = stock_repo.leer_por_libro(libro.id)

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


def registrar_stock(stock_repo, libros_repo) -> None:
    print("\n--- NUEVO STOCK ---")

    libro = libros_repo.leer_por_id(
        leer_entero("ID del libro: ")
    )

    if libro is None:
        print("No existe un libro con ese ID.")
        return

    stock = Stock(
        id=leer_entero("ID del stock: "),
        libro=libro,
        cantidad=leer_entero("Cantidad: "),
        estado=input("Estado: "),
        ubicacion=input("Ubicación: "),
        fecha_ingreso=leer_fecha(
            "Fecha de ingreso (AAAA-MM-DD): "
        ),
    )

    try:
        stock_repo.crear(stock)
        print("Stock creado correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def editar_stock(stock_repo) -> None:
    print("\n--- MODIFICAR STOCK ---")

    libro_id = leer_entero("ID del libro: ")

    stock = stock_repo.leer_por_libro(libro_id)

    if stock is None:
        print("No se encontró stock para ese libro.")
        return

    stock.cantidad = leer_entero("Nueva cantidad: ")
    stock.estado = input("Nuevo estado: ")
    stock.ubicacion = input("Nueva ubicación: ")

    stock.fecha_ingreso = leer_fecha(
        "Nueva fecha de ingreso (AAAA-MM-DD): "
    )

    stock_repo.actualizar(stock)

    print("Stock actualizado correctamente.")


def borrar_stock(stock_repo) -> None:
    print("\n--- ELIMINAR STOCK ---")

    libro_id = leer_entero("ID del libro: ")

    if stock_repo.eliminar(libro_id):
        print("Stock eliminado correctamente.")
    else:
        print("No se encontró stock para ese libro.")


def gestionar_stock(stock_repo, libros_repo) -> None:
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
                mostrar_stock(
                    stock_repo,
                    libros_repo,
                )

            case "2":
                registrar_stock(
                    stock_repo,
                    libros_repo,
                )

            case "3":
                editar_stock(stock_repo)

            case "4":
                borrar_stock(stock_repo)

            case "0":
                break

            case _:
                print("Opción inválida.")


#--------------------------------- CRUD de cotizaciones---------------------------------


def mostrar_cotizaciones(
    cotizaciones_repo,
    tipos_repo,
) -> None:

    print("\n--- LISTADO DE COTIZACIONES ---")

    hay_registros = False

    for tipo in tipos_repo.leer_todos():

        cotizaciones = (
            cotizaciones_repo.leer_historico_por_tipo(
                tipo.id
            )
        )

        for cotizacion in cotizaciones:

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


def registrar_cotizacion(
    cotizaciones_repo,
    tipos_repo,
) -> None:

    print("\n--- NUEVA COTIZACIÓN ---")

    tipo = tipos_repo.leer_por_id(
        leer_entero(
            "ID del tipo de cotización: "
        )
    )

    if tipo is None:
        print(
            "No existe un tipo de cotización con ese ID."
        )
        return

    cotizacion = CotizacionDolar(
        id=leer_entero("ID de la cotización: "),
        tipo_cotizacion=tipo,
        fecha=leer_fecha(
            "Fecha (AAAA-MM-DD): "
        ),
        valor=leer_decimal("Valor: "),
    )

    try:
        cotizaciones_repo.crear(cotizacion)
        print("Cotización creada correctamente.")
    except ValueError as exc:
        print("Error:", exc)


def editar_cotizacion(cotizaciones_repo) -> None:
    print("\n--- MODIFICAR COTIZACIÓN ---")

    tipo_id = leer_entero(
        "ID del tipo de cotización: "
    )

    fecha = leer_fecha(
        "Fecha de la cotización (AAAA-MM-DD): "
    )

    cotizacion = (
        cotizaciones_repo.leer_por_tipo_y_fecha(
            tipo_id,
            fecha,
        )
    )

    if cotizacion is None:
        print("No se encontró la cotización.")
        return

    cotizacion.valor = leer_decimal(
        "Nuevo valor: "
    )

    cotizaciones_repo.actualizar(cotizacion)

    print("Cotización actualizada correctamente.")


def borrar_cotizacion(cotizaciones_repo) -> None:
    print("\n--- ELIMINAR COTIZACIÓN ---")

    tipo_id = leer_entero(
        "ID del tipo de cotización: "
    )

    fecha = leer_fecha(
        "Fecha de la cotización (AAAA-MM-DD): "
    )

    if cotizaciones_repo.eliminar(
        tipo_id,
        fecha,
    ):
        print("Cotización eliminada correctamente.")
    else:
        print("No se encontró la cotización.")


def gestionar_cotizaciones(
    cotizaciones_repo,
    tipos_repo,
) -> None:

    while True:

        print("\n=== COTIZACIONES DEL DÓLAR ===")
        print("1. Listar")
        print("2. Crear")
        print("3. Modificar")
        print("4. Eliminar")
        print("0. Volver")

        seleccion = input("Opción: ")

        match seleccion:

            case "1":
                mostrar_cotizaciones(
                    cotizaciones_repo,
                    tipos_repo,
                )

            case "2":
                registrar_cotizacion(
                    cotizaciones_repo,
                    tipos_repo,
                )

            case "3":
                editar_cotizacion(
                    cotizaciones_repo
                )

            case "4":
                borrar_cotizacion(
                    cotizaciones_repo
                )

            case "0":
                break

            case _:
                print("Opción inválida.")


# Menú principal

def iniciar_menu(repositorios: dict) -> None:

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
        print("0. Salir")

        seleccion = input(
            "Seleccione una opción: "
        )

        match seleccion:

            case "1":
                gestionar_generos(
                    repositorios["generos"]
                )

            case "2":
                gestionar_editoriales(
                    repositorios["editoriales"]
                )

            case "3":
                gestionar_monedas(
                    repositorios["monedas"]
                )

            case "4":
                gestionar_tipos_cotizacion(
                    repositorios[
                        "tipos_cotizacion"
                    ]
                )

            case "5":
                gestionar_libros(
                    repositorios["libros"],
                    repositorios["generos"],
                    repositorios["editoriales"],
                )

            case "6":
                gestionar_precios(
                    repositorios["precios"],
                    repositorios["libros"],
                    repositorios["monedas"],
                )

            case "7":
                gestionar_stock(
                    repositorios["stock"],
                    repositorios["libros"],
                )

            case "8":
                gestionar_cotizaciones(
                    repositorios["cotizaciones"],
                    repositorios[
                        "tipos_cotizacion"
                    ],
                )

            case "0":
                print("-----Programa finalizado-----")
                break

            case _:
                print("Opción inválida.")