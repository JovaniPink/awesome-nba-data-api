# Nginx reverse proxy

`nbaapi.conf` is mounted into `/etc/nginx/conf.d` by Docker Compose. It listens
on container port 80 and proxies requests to the Compose service name
`nbaapi:5000`.

The proxy forwards the original host, client forwarding chain, and request
scheme. Compose starts Nginx only after the API health check passes.

Validate configuration syntax as part of the full stack build:

```sh
cp .env.example .env
docker compose config --quiet
docker compose up --build
```

TLS termination, rate limiting, and production host policy are not configured in
this repository.
