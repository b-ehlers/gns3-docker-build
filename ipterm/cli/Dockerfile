# docker image with basic networking tools

FROM ipterm-base

#
# startup script
#
RUN printf '\
\043!/bin/sh\n\
[ $$ -eq 1 ] && exec dumb-init -r 15:1 -- "$0" "$@"\n\
\n\
[ -f /root/init.sh ] && [ -x /root/init.sh ] && /root/init.sh\n\
\n\
cd\n\
if [ $# -gt 0 ]; then\n\
	exec "$@"\n\
else\n\
	exec bash -i -l\n\
fi\n' \
        > /etc/init.sh && chmod +x /etc/init.sh

ENTRYPOINT [ "/etc/init.sh" ]
VOLUME [ "/root" ]
