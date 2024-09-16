docker run -d \
-e ACCOUNT="机器人qq" \
-e NAPCAT_GID=0 \
-e NAPCAT_UID=0 \
-e MESSAGE_POST_FORMAT="string" \
-e WSR_ENABLE=true \
-e WS_URLS='["ws://自己的ws ip加端口/api/bot/qqws"]' \ 
-p 6099:6099 \
-v /自己的目录只改这前面/QQ:/app/.config/QQ \
-v /自己的目录只改这前面/config:/app/napcat/config \
-v /自己的目录只改这前面/logs:/app/napcat/logs \
--name napcat \
--mac-address=02:42:ac:11:00:99 \
mlikiowa/napcat-docker:latest