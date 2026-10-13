# Docker Compose Examples

Repositorio de plantillas de Docker Compose para desplegar aplicaciones y servicios comunes. Cada ejemplo vive en su propia carpeta e incluye su configuración y un README con los requisitos, los pasos de instalación y las instrucciones de uso.

## Ejemplos

| Carpeta | Descripción |
| --- | --- |
| [wordpress-mariadb-cloudflared](wordpress-mariadb-cloudflared/) | WordPress con PHP-FPM y Nginx, MariaDB como base de datos y acceso público mediante Cloudflare Tunnel. Incluye instrucciones para configurar las credenciales del túnel y levantar los servicios. [Ver README](wordpress-mariadb-cloudflared/README.md). |

Para usar una plantilla, entra a su carpeta y sigue el README correspondiente. Las credenciales, dominios y demás valores específicos de cada despliegue deben configurarse localmente; no publiques secretos en este repositorio.
