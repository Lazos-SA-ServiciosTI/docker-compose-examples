# Traefik con certificado TLS propio

Ejemplo de Traefik v3 como proxy inverso para los otros Compose del repositorio. Publica HTTP (80) y HTTPS (443), y carga un certificado y su clave privados desde archivos locales. El certificado debe ser válido para los dominios que se publicarán.

## Descargar esta plantilla

Con Git instalado, descarga solo esta carpeta:

```sh
git clone --depth 1 --filter=blob:none --sparse https://github.com/Lazos-SA-ServiciosTI/docker-compose-examples.git
cd docker-compose-examples
git sparse-checkout set traefik-sslcert
```

Mueve la plantilla fuera del clon y dale el nombre que quieras:

```sh
mv traefik-sslcert ../mi-traefik
```

Después de comprobar la carpeta, puedes eliminar el clon descargado:

```sh
cd .. && rm -rf -- docker-compose-examples
```

## Requisitos

- Docker Engine y Docker Compose v2 (`docker compose`).
- Un certificado TLS y su clave privada en formato PEM, con la cadena completa del certificado.
- DNS y reglas de firewall que permitan a los clientes llegar al host en los puertos 80 y 443.

**Uso con un usuario no root:** Ejecuta los comandos y administra los archivos sin `sudo`, siempre que el usuario tenga permisos de escritura en la carpeta del proyecto y acceso al daemon de Docker (por ejemplo, que pertenezca al grupo `docker`). En una instalación rootless de Docker no hace falta pertenecer a ese grupo. El grupo `docker` permite obtener privilegios equivalentes a root en el host; añádelo solo a usuarios de confianza.

## Configuración inicial

1. Copia `.env.example` a `.env`. Deja `TRAEFIK_NETWORK=traefik` o reemplázalo por el nombre que quieras usar para la red compartida.

2. Copia el certificado y su clave privada a `certs/` con estos nombres:

   ```text
   certs/fullchain.pem
   certs/privkey.pem
   ```

   Protege la clave privada para que solo el usuario administrador pueda leerla. Los archivos `*.pem` están excluidos de Git; no subas claves privadas al repositorio.

3. Verifica que las rutas y nombres coincidan con `dynamic/tls.yml`. Traefik carga ese archivo mediante el proveedor de archivos.

4. Inicia Traefik:

   ```sh
   docker compose up -d
   ```

La red Docker indicada por `TRAEFIK_NETWORK` se crea al iniciar este Compose. Los otros proyectos deben referenciar esa misma red como externa.

## Publicar un servicio

Un servicio debe conectarse a la red compartida y tener etiquetas `traefik.enable=true`, un router HTTP en `web` y un router TLS en `websecure`. El certificado cargado debe incluir el dominio del router.

Si también usas `www`, el certificado debe cubrir tanto el dominio raíz como `www`.

## Renovar o reemplazar el certificado

Reemplaza `fullchain.pem` y `privkey.pem` por los nuevos archivos y reinicia Traefik para que cargue el certificado actualizado:

```sh
docker compose restart traefik
```

## Operación

```sh
docker compose ps
docker compose logs -f traefik
docker compose down
```

El socket Docker se monta en modo solo lectura; aun así, el acceso a ese socket puede dar a Traefik amplio control sobre Docker. Limita quién puede modificar este Compose, sus etiquetas y los archivos de certificados.

## Referencias

- [Documentación oficial de Traefik: proveedor de archivos](https://doc.traefik.io/traefik/providers/file/)
- [Documentación oficial de Traefik: certificados TLS](https://doc.traefik.io/traefik/https/tls/)
