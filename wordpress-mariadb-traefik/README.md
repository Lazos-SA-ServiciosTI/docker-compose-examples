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

## Configuración inicial

1. Copia `.env.example` a `.env` y completa las credenciales de MariaDB y WordPress. Usa el mismo nombre de base de datos, usuario y contraseña en las variables de ambos servicios.
2. Define `WORDPRESS_DOMAIN` con el dominio público del sitio.
3. Define `TRAEFIK_NETWORK` con el nombre exacto de la red Docker externa donde está conectado Traefik. Puedes consultarlo con `docker network ls`.
4. La plantilla configura un router HTTP en el entrypoint `web` y otro HTTPS en `websecure`. HTTP no se redirige automáticamente a HTTPS. Si tu instancia usa otros nombres de entrypoint, actualiza las etiquetas correspondientes en `docker-compose.yml`.
5. El router HTTPS usa el resolver ACME `letsencrypt`. Configura ese resolver en Traefik o cambia la etiqueta `traefik.http.routers.wordpress-https.tls.certresolver` para que coincida con el nombre que uses. Para emitir un certificado con HTTP-01, el dominio debe apuntar a Traefik y el puerto 80 debe ser accesible desde Internet.

### Usar el dominio con y sin `www`

Por defecto, ambos routers aceptan solo el dominio indicado en `WORDPRESS_DOMAIN`. Para aceptar también su variante `www` (por ejemplo, `example.com` y `www.example.com`), actualiza las dos etiquetas `rule` del servicio Nginx en `docker-compose.yml`:

```yaml
- "traefik.http.routers.wordpress-http.rule=Host(`${WORDPRESS_DOMAIN}`, `www.${WORDPRESS_DOMAIN}`)"
- "traefik.http.routers.wordpress-https.rule=Host(`${WORDPRESS_DOMAIN}`, `www.${WORDPRESS_DOMAIN}`)"
```

Ambos nombres DNS deben dirigir a Traefik y el certificado TLS debe cubrir los dos. El resolver ACME obtendrá el certificado para los nombres de la regla HTTPS. Configura WordPress con la URL canónica que quieras usar; si quieres que uno de los dominios redirija al otro, configura además esa redirección en Traefik o WordPress.

## Usar Traefik solo por HTTP detrás de un load balancer

Usa este modo cuando un load balancer reciba las conexiones HTTPS públicas, termine TLS y reenvíe las solicitudes a Traefik por HTTP. El certificado público se configura en el load balancer; Traefik no necesita un router HTTPS ni un resolver ACME.

En las etiquetas del servicio `nginx` en `docker-compose.yml`, conserva el router HTTP y elimina las cuatro etiquetas `wordpress-https`:

```yaml
- "traefik.http.routers.wordpress-http.rule=Host(`${WORDPRESS_DOMAIN}`)"
- "traefik.http.routers.wordpress-http.entrypoints=web"
- "traefik.http.routers.wordpress-http.service=wordpress"
```

Si también usas el dominio con `www`, deja ambos nombres en la regla HTTP:

```yaml
- "traefik.http.routers.wordpress-http.rule=Host(`${WORDPRESS_DOMAIN}`, `www.${WORDPRESS_DOMAIN}`)"
```

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
