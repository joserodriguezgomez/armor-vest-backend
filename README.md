ruta_backend = https://armor-vest-backend-fb07262d3ec2.herokuapp.com/api/

# Documentación de API - FastAPI

## Endpoints de la API

A continuación se presenta una tabla con los endpoints disponibles en la API, sus métodos, descripciones y respuestas esperadas.

| Método | Endpoint          | Descripción                              | Parámetros Entrada                              | Respuesta                   |
|--------|-------------------|------------------------------------------|-------------------------------------------------|----------------------------|
| POST   | `/idic/`          | Crea un nuevo objeto `Idic`.             | Objeto `Idic` sin `id_poliza`.                  | Objeto `Idic` creado.       |
| GET    | `/idic/`          | Obtiene todos los objetos `Idic`.        | Ninguno.                                        | Lista de objetos `Idic`.   |
| GET    | `/idic/{idic_id}` | Obtiene un objeto `Idic` específico.     | `idic_id`: ID del objeto `Idic`.                | Objeto `Idic` solicitado.   |
| PUT    | `/idic/{idic_id}` | Actualiza un objeto `Idic` existente.    | `idic_id`: ID del `Idic`.<br>Objeto `Idic`.     | Objeto `Idic` actualizado.  |
| DELETE | `/idic/{idic_id}` | Elimina un objeto `Idic` específico.     | `idic_id`: ID del objeto `Idic` a eliminar.     | Objeto `Idic` eliminado.    |


