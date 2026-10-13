# WordPress con Nginx, MariaDB y Cloudflare Tunnel

Plantilla de Docker Compose para ejecutar WordPress con PHP-FPM detrás de Nginx y publicar el sitio mediante un túnel de Cloudflare.

## Descargar esta plantilla

Con Git instalado, descarga solo esta carpeta de ejemplos:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lazos-SA-ServiciosTI/docker-compose-examples.git
cd docker-compose-examples
git sparse-checkout set wordpress-mariadb-cloudflared
```

Mueve la plantilla fuera del clon y dale el nombre del proyecto. En este ejemplo, reemplaza `mi-proyecto` por el nombre que quieras:

```sh
mv wordpress-mariadb-cloudflared ../mi-proyecto
```

**Limpieza opcional:** Después de comprobar que la carpeta del proyecto existe y contiene los archivos de la plantilla, puedes eliminar el clon del repositorio de ejemplos:

```sh
rm -rf docker-compose-examples
```

## Requisitos

- Docker Engine y Docker Compose v2 (`docker compose`).
- Un túnel de Cloudflare creado y configurado para usar este servicio. La configuración detallada del túnel está en la guía del equipo: [Crear un túnel con Cloudflare Tunnel — utilizando Docker Compose](https://github.com/Lazos-SA-ServiciosTI/shared-notes-obsidian/blob/main/ServiciosTI/Crear%20un%20t%C3%BAnel%20con%20Cloudflare%20Tunnel.md#utilizando-docker-compose).
- El archivo JSON de credenciales del túnel.

## Configuración inicial

1. Copia `.env.example` a `.env` y completa los valores de base de datos y WordPress.
2. Usa el mismo nombre de base de datos en `MYSQL_DATABASE` y `WORDPRESS_DB_NAME`.
3. Usa el mismo usuario en `MYSQL_USER` y `WORDPRESS_DB_USER`, y la misma contraseña en `MYSQL_PASSWORD` y `WORDPRESS_DB_PASSWORD`. `WORDPRESS_DB_HOST` debe ser `db`, que es el nombre del servicio de MariaDB en Compose.
4. En `cloudflared/config.yml`, reemplaza `<tunnel_id>` y `<hostname>` por el ID del túnel y el dominio público configurado en Cloudflare.
5. Copia el archivo de credenciales del túnel a `cloudflared/` y nómbralo `<tunnel_id>.json`, para que coincida con `credentials-file` en `config.yml`.

`.env` y las credenciales se excluyen de Git mediante `.gitignore`. No agregues secretos al repositorio.

## Iniciar y detener

Desde la raíz de esta carpeta:

```sh
docker compose up -d
```

MariaDB tiene una comprobación de salud; WordPress espera a que la base esté lista antes de iniciar. Nginx y `cloudflared` arrancan después de sus servicios requeridos.

Para revisar el estado y los registros:

```sh
docker compose ps
docker compose logs -f
```

Para detener los servicios sin eliminar sus datos:

```sh
docker compose down
```

## Imágenes

Las etiquetas reflejan una política distinta según cada imagen: WordPress sigue la versión más reciente compatible con PHP 8.5; Nginx y MariaDB siguen sus ramas 1.30 y 12.3, respectivamente, incorporando actualizaciones de parche dentro de esas ramas; `cloudflared` conserva una versión completa. Revisa los cambios y vuelve a descargar las imágenes con `docker compose pull` cuando quieras aplicarlos.
