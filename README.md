# Unnamed-webdev-backend
Backend para proyecto webdev, nombre unnamed

Para cargar el proyecto, clonar el repo, instalar el env con requirements.txt, asegurarse de que exista una tabla de postgres que se llame unnamed-project en localhost, y colocar los nombres y password correctos en /unamed/settings.py (mi proyecto usa el base postgres/postgres). Cuando esto se haya asegurado, correr `py manage.py runserver` o solo `manage.py runserver` dependiendo de como se tengan configuradas las variables de entorno.

Unnamed es una idea de proyecto que he tenido desde mucho tiempo; la idea es una plataforma donde cualquier usuario, casi de forma anonima, puede colocar al publico una imagen, video, soundbyte, texto, historia, o link, y recibir likes y mensajes anonimos para cada uno. La idea es como un reddit super simplificado, pero de tema completamente libre y mucho más anónimo. Es una mala idea respecto a lo que la gente podría publicar y decir, como se comprobó en otro momento con la app "Secret", pero siempre me llamo la atención como una forma de siempre tener contenido nuevo sin ningún tipo de recomendación. Obviamente se tendría que implementar moderación super estricta para evitar problemas.

# Cosas que se pueden hacer en el backend
(Asumiendo que se usa postman)

## Para cada tabla excepto collections (nunca se implemento), Posters (es de read-only), Notifications y messages (estas tienen comportamientos distintos)

* (POST)Perform create, crea un objeto nuevo de este tipo con la informacion necesaria; si algun campo necesario no se provee, el API pedira que se incluya
(Estas tres son PATCH)
* Disable, cambia la descripcion y el url/directory a un default de disabled, para que se muestre en el historial pero no se pueda ver el contenido original
* Like, Incrementa el like por uno. Para images, videos, soundbytes y stories, tambien se implemento una funcion que envia notificaciones al usuario que creo el objeto
* EditCaption o EditDescription, cambia la descripcion del objeto por la nueva que se provee en el body.
* (GET)View_All, muestra todos los objetos de este tipo que se han creado.

## Para la tabla Posters
(Ambas GET)
* Mostrar todos los objetos de cada tipo que ha creado el usuario
* Mostrar todos los mensajes y notificaciones que ha recibido, pero solo si el usuario que hace la consulta es el mismo que recibio estas notificaciones o mensajes.

## Para la tabla Messages
* (POST) Crear nuevo mensaje anonimo para un recipient
* (DELETE) Eliminar un mensaje; solo el usuario que recibio el mensaje puede eliminar los mensajes que ha recibido.

## Para la tabla Notifications
* (DELETE) Eliminar una notificacion, solo el usuario que la recibio puede eliminarla.
La tabla notifications no permite un perform create directo; las notificaciones solamente se crean cuando un usuario le da like a una imagen, soundbyte, story o video.

# Breakdown de requisitos que se implementaron
* Permisos de uso para los metodos pertinentes
* Autenticacion con JWT
* Expiracion de Token (Pero dura 360000 segundos)
* Postgres

## Tablas
* Images
* Links
* Messages
* Notes
* Notifications
* Posters
* Soundbytes
* Stories
* Videos

(9/10)

## Endpoints
### Usados en frontend:
* Create, Like, Disable y View_All para las tablas Images, Links, Notes, Videos
(16/20)
### Usables solo con postman:
* Create, Like, Disable y View_All para las demas tablas
* Edit_description o edit_caption para todas las tablas de objetos distintos a poster, notification y message y Notes
* Todos los metodos View{object} para Poster
* Metodos de creacion y eliminacion de mensaje
* Metodo de eliminacion de notificaion.

