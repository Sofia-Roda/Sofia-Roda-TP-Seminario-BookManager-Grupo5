# Book Manager - Sprint 2

## Sprint actual: Sprint 2

## Objetivo

Incorporar persistencia mediante una base de datos relacional utilizando
SQLAlchemy ORM, migrando los datos utilizados durante el Sprint 1 y
adaptando el sistema Book Manager para trabajar con la nueva capa de
persistencia.

## Introducción y contexto

En el Sprint 1 se desarrolló el sistema Book Manager utilizando entidades,
repositorios y archivos CSV para la carga y persistencia inicial de los datos.

En este Sprint 2 el sistema evoluciona hacia el uso de una base de datos
relacional. Se implementará la conexión mediante SQLAlchemy, se definirán
los modelos y relaciones de las tablas, se migrarán los datos existentes
desde los archivos CSV y se adaptarán los repositorios para trabajar con
la base de datos.

También se incorporará el consumo de una API externa para obtener
cotizaciones del dólar y se ampliará la interfaz del sistema para trabajar
con precios en distintas monedas.