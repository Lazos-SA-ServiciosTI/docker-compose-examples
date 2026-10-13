# Docker Compose Examples

Repositorio de plantillas de Docker Compose para desplegar aplicaciones y servicios comunes. Cada ejemplo vive en su propia carpeta e incluye su configuración y un README con los requisitos, los pasos de instalación y las instrucciones de uso.

Estos ejemplos son plantillas básicas de referencia. Revísalos y adáptalos a los requisitos, la seguridad y la operación de cada proyecto antes de usarlos.

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
