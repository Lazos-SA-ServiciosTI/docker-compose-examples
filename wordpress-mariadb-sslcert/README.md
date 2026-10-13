# WordPress con Nginx, MariaDB y certificado SSL propio

Plantilla de Docker Compose para ejecutar WordPress con PHP-FPM, Nginx y MariaDB. Nginx termina HTTPS directamente con un certificado TLS propio; no requiere Traefik ni Cloudflare.

## Descargar esta plantilla

Con Git instalado, descarga solo esta carpeta:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lazos-SA-ServiciosTI/docker-compose-examples.git
cd docker-compose-examples
git sparse-checkout set wordpress-mariadb-sslcert
```

Mueve la plantilla fuera del clon y dale el nombre del proyecto:

```sh
mv wordpress-mariadb-sslcert ../mi-proyecto
```

Después de comprobar que la carpeta del proyecto contiene la plantilla, puedes eliminar el clon descargado:

```sh
cd .. && rm -rf -- docker-compose-examples
```

## Requisitos

- Docker Engine y Docker Compose v2 (`docker compose`).
- Un certificado TLS y su clave privada en formato PEM. El certificado debe cubrir el dominio que usarás para WordPress; coloca la cadena completa en el archivo de certificado.
- Los puertos TCP 80 y 443 disponibles en el host y permitidos en el firewall para el acceso público.

## Configuración inicial

1. Copia `.env.example` a `.env` y completa las credenciales de MariaDB y WordPress. Usa el mismo nombre de base de datos, usuario y contraseña en las variables de ambos servicios.
2. Copia el certificado y la clave privada a `certs/` con estos nombres:

   ```text
   certs/fullchain.pem
   certs/privkey.pem
   ```

   Asegura que la clave privada solo sea legible por el usuario administrador y no la agregues al repositorio. `.env`, los certificados, la base de datos y los archivos de WordPress están excluidos de Git.

3. Configura el DNS del dominio para que apunte al host que ejecuta esta plantilla.

## Iniciar y detener

Desde la raíz de esta carpeta:

```sh
docker compose up -d
```

Nginx atiende HTTP en el puerto 80 y redirige a HTTPS en el puerto 443. WordPress y MariaDB no publican puertos al host.

Para revisar el estado y los registros:

```sh
docker compose ps
docker compose logs -f
```

Para detener los servicios sin eliminar sus datos:

```sh
docker compose down
```

## Usar solo HTTP sin certificado

Si quieres ejecutar el sitio sin certificado ni HTTPS, cambia la configuración de Nginx y los puertos publicados:

1. En `docker-compose.yml`, cambia el volumen de configuración de Nginx por la variante HTTP:

   ```yaml
   - ./nginx/http:/etc/nginx/conf.d:ro
   ```

2. Quita el volumen `./certs:/etc/nginx/certs:ro` del servicio `nginx`.
3. En `ports`, elimina `443:443` y conserva solo:

   ```yaml
   - "80:80"
   ```

4. Inicia o actualiza los servicios:

   ```sh
   docker compose up -d
   ```

En esta variante el sitio solo usa HTTP y el tráfico no está cifrado. Úsala en una red privada o detrás de un balanceador que termine TLS.

## Imágenes

WordPress sigue la versión más reciente compatible con PHP 8.5. Nginx y MariaDB siguen sus ramas 1.30 y 12.3, incorporando actualizaciones de parche dentro de esas ramas. Revisa los cambios y vuelve a descargar las imágenes con `docker compose pull` cuando quieras aplicarlos.
