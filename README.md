# Docker Compose Examples

Repositorio de plantillas de Docker Compose para desplegar aplicaciones y servicios comunes. Cada ejemplo vive en su propia carpeta e incluye su configuración y un README con los requisitos, los pasos de instalación y las instrucciones de uso.

Estos ejemplos son plantillas básicas de referencia. Revísalos y adáptalos a los requisitos, la seguridad y la operación de cada proyecto antes de usarlos.

**Uso con un usuario no root:** Clona y administra los archivos, y ejecuta Docker Compose, con un usuario no root y sin `sudo`, siempre que tenga permisos de escritura en la carpeta del proyecto y acceso al daemon de Docker (por ejemplo, que pertenezca al grupo `docker`). En una instalación rootless de Docker no hace falta pertenecer a ese grupo. Ten presente que el grupo `docker` permite obtener privilegios equivalentes a root en el host; añádelo solo a usuarios de confianza.

## Ejemplos

| Carpeta | Descripción |
| --- | --- |
| [traefik-httponly](traefik-httponly/) | Ejemplo de Traefik con Docker provider y solo HTTP por el puerto 80, sin configuración TLS. [Ver README](traefik-httponly/README.md). |
| [traefik-letsencrypt](traefik-letsencrypt/) | Ejemplo de instancia Traefik con Docker provider, red compartida, HTTP y HTTPS con certificados automáticos de Let's Encrypt. [Ver README](traefik-letsencrypt/README.md). |
| [traefik-sslcert](traefik-sslcert/) | Ejemplo de instancia Traefik con Docker provider y certificado TLS propio para HTTPS. [Ver README](traefik-sslcert/README.md). |
| [wordpress-mariadb-cloudflared](wordpress-mariadb-cloudflared/) | WordPress con PHP-FPM y Nginx, MariaDB como base de datos y acceso público mediante Cloudflare Tunnel. Incluye instrucciones para configurar las credenciales del túnel y levantar los servicios. [Ver README](wordpress-mariadb-cloudflared/README.md). |
| [wordpress-mariadb-sslcert](wordpress-mariadb-sslcert/) | WordPress con Nginx y MariaDB, HTTPS terminado directamente en Nginx con certificado TLS propio. Incluye una variante HTTP-only. [Ver README](wordpress-mariadb-sslcert/README.md). |
| [wordpress-mariadb-traefik](wordpress-mariadb-traefik/) | WordPress con PHP-FPM y Nginx, MariaDB como base de datos y publicación a través de una instancia de Traefik existente en una red Docker externa. [Ver README](wordpress-mariadb-traefik/README.md). |

## Nombres de contenedores

Las plantillas omiten `container_name`. Docker Compose asigna nombres a partir del proyecto y el servicio, lo que permite ejecutar varias copias en un mismo host sin colisiones ni llevar un registro de nombres. Para la comunicación entre servicios, usa los nombres de servicio definidos en Compose (por ejemplo, `db`) como nombres DNS dentro de la red del proyecto.

Para usar una plantilla, entra a su carpeta y sigue el README correspondiente. Las credenciales, dominios y demás valores específicos de cada despliegue deben configurarse localmente; no publiques secretos en este repositorio.

## Actualizaciones de imágenes

Dependabot revisa semanalmente las imágenes declaradas en los archivos `docker-compose.yml` y abre PR separadas por imagen y plantilla, incluidas las actualizaciones de versión mayor o menor. Revisa los cambios y su compatibilidad antes de fusionar cada PR; no se habilita la fusión automática. Si agregas una plantilla, incluye su carpeta en `directories` de `.github/dependabot.yml`.

Las etiquetas de WordPress que cambian de familia, como `php8.5-fpm` a `php8.6-fpm`, se revisan con un workflow semanal porque Dependabot puede no relacionar esos nombres como actualizaciones de la misma etiqueta. Si detecta una versión estable más nueva, el workflow abre o actualiza una sola PR con todas las plantillas WordPress. Revisa la versión y compatibilidad antes de fusionarla. También puedes ejecutarlo manualmente desde **Actions → Check WordPress PHP-FPM tag → Run workflow**.
