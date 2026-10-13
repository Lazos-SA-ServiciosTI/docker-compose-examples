# WordPress con Nginx, MariaDB y Traefik

Plantilla de Docker Compose para ejecutar WordPress con PHP-FPM y Nginx, usando MariaDB y publicando el sitio a través de una instancia de Traefik ya existente.

## Descargar esta plantilla

Con Git instalado, descarga solo esta carpeta de ejemplos:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lazos-SA-ServiciosTI/docker-compose-examples.git
cd docker-compose-examples
git sparse-checkout set wordpress-mariadb-traefik
```

Mueve la plantilla fuera del clon y dale el nombre del proyecto. Reemplaza `mi-proyecto` por el nombre que quieras:

```sh
mv wordpress-mariadb-traefik ../mi-proyecto
```

Después de comprobar que la carpeta del proyecto contiene la plantilla, puedes eliminar el clon descargado:

```sh
cd .. && rm -rf -- docker-compose-examples
```

## Requisitos

- Docker Engine y Docker Compose v2 (`docker compose`).
- Una instancia de Traefik en ejecución con el proveedor Docker habilitado.
- Una red Docker externa ya creada y compartida por Traefik.
- Un dominio DNS que llegue a la instancia de Traefik.

**Uso con un usuario no root:** Ejecuta los comandos y administra los archivos sin `sudo`, siempre que el usuario tenga permisos de escritura en la carpeta del proyecto y acceso al daemon de Docker (por ejemplo, que pertenezca al grupo `docker`). En una instalación rootless de Docker no hace falta pertenecer a ese grupo. El grupo `docker` permite obtener privilegios equivalentes a root en el host; añádelo solo a usuarios de confianza.

## Configuración inicial

1. Copia `.env.example` a `.env` y completa las credenciales de MariaDB y WordPress. Usa el mismo nombre de base de datos, usuario y contraseña en las variables de ambos servicios.
2. Define `WORDPRESS_DOMAIN` con el dominio público del sitio.
3. Define `TRAEFIK_NETWORK` con el nombre exacto de la red Docker externa compartida por la instancia de Traefik.

La configuración de la instancia de Traefik y sus certificados se describe en los README de sus plantillas: [Traefik con Let's Encrypt](https://github.com/Lazos-SA-ServiciosTI/docker-compose-examples/blob/main/traefik-letsencrypt/README.md), [Traefik con certificado propio](https://github.com/Lazos-SA-ServiciosTI/docker-compose-examples/blob/main/traefik-sslcert/README.md) y [Traefik solo HTTP](https://github.com/Lazos-SA-ServiciosTI/docker-compose-examples/blob/main/traefik-httponly/README.md).

### Usar con Traefik solo HTTP

Esta plantilla define routers HTTP y HTTPS. Para conectarla a una instancia `traefik-httponly`, conserva las tres etiquetas `wordpress-http` del servicio `nginx` en `docker-compose.yml` y elimina sus cuatro etiquetas `wordpress-https`.

El sitio quedará disponible por HTTP sin cifrar, salvo que un load balancer delante de Traefik termine TLS. En ese caso, sigue también la sección de [uso detrás de un load balancer con terminación TLS](https://github.com/Lazos-SA-ServiciosTI/docker-compose-examples/blob/main/traefik-httponly/README.md#uso-detr%C3%A1s-de-un-load-balancer-con-terminaci%C3%B3n-tls) del README de Traefik.

El servicio Nginx se conecta tanto a la red privada de esta plantilla como a la red externa de Traefik. WordPress y MariaDB permanecen en la red privada del proyecto. No es necesario publicar puertos del host.

**IMPORTANTE:** Si ejecutas varias copias de esta plantilla bajo la misma instancia de Traefik, cambia los nombres de los routers (`wordpress-http` y `wordpress-https`) y del servicio (`wordpress`) en las etiquetas para que sean únicos.

## Iniciar y detener

Desde la carpeta del proyecto:

```sh
docker compose up -d
```

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

WordPress sigue la versión más reciente compatible con PHP 8.5. Nginx y MariaDB siguen sus ramas 1.30 y 12.3, incorporando actualizaciones de parche dentro de esas ramas. Revisa los cambios y vuelve a descargar las imágenes con `docker compose pull` cuando quieras aplicarlos.
