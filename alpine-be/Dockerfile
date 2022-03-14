# nicer alpine image

FROM alpine

ARG TARGETARCH

COPY nodnsd.${TARGETARCH:-amd64} /usr/local/sbin/nodnsd

RUN set -e -x -o pipefail \
#
# install busybox-extras, dumb-init and nodnsd
#
    && apk upgrade \
    && apk add busybox-extras dumb-init \
    && rm -rf /var/cache/apk/* \
    && chmod 755 /usr/local/sbin/nodnsd \
#
# add gns3 user
#
    && printf 'gns3\ngns3\n' | adduser gns3 \
#
# startup script
#
    && printf '\
\043!/bin/sh\n\
[ $$ -eq 1 ] && exec dumb-init -r 15:1 -- "$0" "$@"\n\
\n\
nodnsd\n\
[ -f /root/init.sh ] && [ -x /root/init.sh ] && /root/init.sh\n\
\n\
cd\n\
if [ $# -gt 0 ]; then\n\
	exec "$@"\n\
else\n\
	exec ash -i -l\n\
fi\n' \
        > /etc/init.sh && chmod +x /etc/init.sh

ENTRYPOINT [ "/etc/init.sh" ]
VOLUME [ "/root", "/home/gns3" ]
