# My Blog App Django

My Blog App es una aplicación web construida con Django que permite a los usuarios interactuar con un blog de manera dinámica. La aplicación ofrece diversas funcionalidades para gestionar publicaciones, comentarios, y más.

## Funcionalidades

- **Publicaciones del Blog**: 
  - Crear, editar y eliminar publicaciones.
  - Listar publicaciones con paginación y detalles de cada entrada.
  
- **Comentarios**: 
  - Permitir a los usuarios comentar en las publicaciones.
  - Moderar los comentarios desde el panel de administración.

- **Búsqueda**: 
  - Buscar publicaciones utilizando palabras clave.

- **Compartir Publicaciones**: 
  - Compartir publicaciones mediante enlaces para facilitar la difusión.

- **Autenticación de Usuarios**: 
  - Funcionalidades de inicio de sesión y cierre de sesión para usuarios registrados.
  - Plantillas personalizadas para la autenticación.

- **Feeds RSS y Sitemaps**: 
  - Soporte para generar feeds RSS, permitiendo a los usuarios suscribirse a las publicaciones.
  - Generación de sitemaps para mejorar el SEO y la indexación en motores de búsqueda.

- **Etiquetas Personalizadas**:
  - Uso de etiquetas específicas para extender la funcionalidad de las plantillas y hacerlas más flexibles.

## Instalación

1. Clona el repositorio:

    ```bash
    git clone https://github.com/IngBenichi/My-Blog-App-Django.git
    ```

2. Crea un entorno virtual e instala las dependencias:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/MacOS
    venv\Scripts\activate  # Windows
    pip install -r requirements.txt
    ```

3. Realiza las migraciones y ejecuta el servidor:

    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

4. Accede a `http://127.0.0.1:8000/` para ver la aplicación en funcionamiento.

## Contribución

Si deseas contribuir al proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza tus cambios y haz un commit (`git commit -m 'Añadir nueva característica'`).
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request.

## Licencia

Distribuido bajo la licencia [MIT](LICENSE).
