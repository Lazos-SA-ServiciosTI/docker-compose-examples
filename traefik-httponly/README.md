# Traefik solo HTTP

Ejemplo de Traefik v3 como proxy inverso con el proveedor Docker habilitado. Escucha y publica únicamente HTTP por el puerto 80; no configura HTTPS ni certificados TLS.

El tráfico entre el cliente y Traefik no está cifrado. Para publicar sitios por HTTPS, coloca esta instancia detrás de un load balancer que termine TLS y reenvíe a Traefik por HTTP.

## Descargar esta plantilla

Con Git instalado, descarga solo esta carpeta:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lazos-SA-ServiciosTI/docker-compose-examples.git
cd docker-compose-examples
git sparse-checkout set traefik-httponly
```

Mueve la plantilla fuera del clon y dale el nombre que quieras:

```sh
mv traefik-httponly ../mi-traefik
```

Después de comprobar la carpeta, puedes eliminar el clon descargado:

```sh
cd .. && rm -rf -- docker-compose-examples
```

## Requisitos

- Docker Engine y Docker Compose v2 (`docker compose`).
- Los puertos TCP 80 disponibles en el host.
- Un registro DNS que apunte al host si se accederá por un dominio.

**Uso con un usuario no root:** Ejecuta los comandos y administra los archivos sin `sudo`, siempre que el usuario tenga permisos de escritura en la carpeta del proyecto y acceso al daemon de Docker (por ejemplo, que pertenezca al grupo `docker`). En una instalación rootless de Docker no hace falta pertenecer a ese grupo. El grupo `docker` permite obtener privilegios equivalentes a root en el host; añádelo solo a usuarios de confianza.

## Configuración e inicio

1. Copia `.env.example` a `.env`. Puedes mantener `TRAEFIK_NETWORK=traefik` o reemplazarlo por el nombre de la red compartida que quieras.

2. Inicia Traefik:

   ```sh
   docker compose up -d
   ```

La red Docker indicada por `TRAEFIK_NETWORK` se crea al iniciar este Compose. Los otros proyectos deben conectarse a esa misma red como externa.

## Publicar un servicio

Conecta el servicio a la red compartida y añade etiquetas `traefik.enable=true` y un router en el entrypoint `web`. La aplicación debe aceptar HTTP desde Traefik. Esta plantilla no admite routers TLS ni etiquetas de resolución de certificados.

## Uso detrás de un load balancer con terminación TLS

Un load balancer puede recibir HTTPS, terminar TLS y enviar las solicitudes a Traefik por HTTP. En ese caso, configura el balanceador para reenviar al puerto 80, preservar el encabezado `Host` y enviar `X-Forwarded-Proto: https`.

Si la aplicación necesita confiar en los encabezados reenviados, configura `forwardedHeaders.trustedIPs` en el entrypoint `web` con la IP o CIDR de origen del balanceador. Por ejemplo, añade a `command` en `docker-compose.yml`:

```yaml
- "--entryPoints.web.forwardedHeaders.trustedIPs=192.0.2.10/32"
```

Reemplaza el ejemplo por la IP o rango real del balanceador. Confía solo en sus direcciones y limita el acceso de red al puerto 80 para que los clientes no puedan saltarse el balanceador y conectarse directamente.

## Operación

```sh
docker compose ps
docker compose logs -f traefik
docker compose down
```

El socket Docker se monta en modo solo lectura; aun así, el acceso a ese socket puede dar a Traefik amplio control sobre Docker. Limita quién puede modificar este Compose y las etiquetas de los contenedores.

## Referencia

- [Documentación oficial de Traefik: entrypoints y encabezados reenviados](https://doc.traefik.io/traefik/reference/install-configuration/entrypoints/)
