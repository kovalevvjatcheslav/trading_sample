docker build --no-cache -f docker/ticker.dockerfile -t ticker . \\  
&& docker build --no-cache -f docker/web.dockerfile -t web_service . \\  
&& docker-compose -f docker/docker-compose.yml up --force-recreate