FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /usr/share/nginx/html

EXPOSE 80

CMD envsubst '${API_PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'