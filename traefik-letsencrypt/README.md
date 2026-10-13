# Traefik con Let's Encrypt

Ejemplo de Traefik v3 como proxy inverso para los otros Compose del repositorio. Crea una red Docker compartida llamada `traefik`, publica HTTP (80) y HTTPS (443), y puede emitir certificados TLS automáticamente con Let's Encrypt mediante el desafío HTTP-01.

## Descargar esta plantilla

Con Git instalado, descarga solo esta carpeta:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lazos-SA-ServiciosTI/docker-compose-examples.git
cd docker-compose-examples
git sparse-checkout set traefik-letsencrypt
```

Mueve la plantilla fuera del clon y dale el nombre que quieras:

```sh
mv traefik-letsencrypt ../mi-traefik
```

Después de comprobar la carpeta, puedes eliminar el clon descargado:

```sh
cd .. && rm -rf -- docker-compose-examples
```

## Requisitos

- Docker Engine y Docker Compose v2 (`docker compose`).
- Un host accesible desde Internet y reglas de firewall que permitan conexiones entrantes TCP en los puertos 80 y 443.
- Un dominio DNS que apunte a la dirección pública del host para emitir certificados de Let's Encrypt.

## Configuración inicial

1. Copia `.env.example` a `.env` y define `ACME_EMAIL` con un correo válido. `TRAEFIK_NETWORK` debe ser el nombre de la red compartida; por defecto es `traefik`.

2. Prepara el archivo donde Traefik guardará las cuentas y certificados ACME. Desde esta carpeta, ejecuta:

   ```sh
   mkdir -p letsencrypt
   touch letsencrypt/acme.json
   chmod 600 letsencrypt/acme.json
   ```

3. Inicia Traefik:

   ```sh
   docker compose up -d
   ```

La red Docker indicada por `TRAEFIK_NETWORK` se crea al iniciar este Compose. Los demás proyectos deben referenciar esa misma red como externa.

## Publicar un servicio

Un servicio debe conectarse a la red compartida y declarar etiquetas `traefik.enable=true`, un router en el entrypoint `web` para HTTP y otro en `websecure` con TLS y el resolver `letsencrypt`.

Traefik escucha HTTP y HTTPS, y este ejemplo no redirige HTTP automáticamente a HTTPS. Para forzar HTTPS se puede añadir una redirección del entrypoint `web` al `websecure` en la configuración estática.

## Operación

```sh
docker compose ps
docker compose logs -f traefik
docker compose down
```

El directorio `letsencrypt` contiene datos privados de certificados y está excluido de Git. El socket Docker se monta en modo solo lectura; aun así, el acceso a ese socket puede dar a Traefik amplio control sobre Docker, por lo que conviene limitar quién puede modificar este Compose y las etiquetas de los contenedores.

## Referencias

- [Documentación oficial de Traefik: configuración ACME](https://doc.traefik.io/traefik/reference/install-configuration/tls/certificate-resolvers/acme/)
- [Documentación oficial de Traefik: entrypoints](https://doc.traefik.io/traefik/reference/install-configuration/entrypoints/)
