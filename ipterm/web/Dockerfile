# docker image with basic networking tools and web browser

FROM ghcr.io/b-ehlers/ipterm-base

RUN set -e -x \
#
# install web tools
#
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get -y --no-install-recommends install \
        firefox-esr lxterminal jwm menu mousepad wmctrl \
    && rm -rf /var/lib/apt/lists/* \
#
# update firefox preferences
#
    && printf '\n\
// Disable welcome page on first start and when showing about:home\n\
pref("browser.startup.homepage_override.mstone","ignore");\n\
pref("trailhead.firstrun.branches", "nofirstrun-empty");\n' \
	>> /etc/firefox-esr/firefox-esr.js \
#
# customize jwm menu
#
    && printf '\
?package(firefox-esr):\\\n\
 needs="x11"\\\n\
 section="Applications"\\\n\
 title="Mozilla Firefox"\\\n\
 command="firefox"\n' \
        > /etc/menu/firefox \
    && printf '\
?package(mousepad):\\\n\
 needs="x11"\\\n\
 section="Applications/TextEditor"\\\n\
 title="Mousepad"\\\n\
 command="mousepad"\n' \
        > /etc/menu/mousepad \
    && echo "postrun=\"sed -i '/^    </ d' debian-menu\"" >> /etc/menu-methods/jwm \
    && sed -i 's/\(Desktops width\)="[0-9]*"/\1="2"/' /etc/jwm/system.jwmrc \
    && sed -i 's/xterm/x-terminal-emulator/g' /etc/jwm/system.jwmrc \
    && update-menus \
#
# set lxterminal defaults
#
    && mkdir -p /root/.config/lxterminal \
    && printf '\
[general]\n\
scrollback=1000\n\
fgcolor=#ffffff\n' \
        > /root/.config/lxterminal/lxterminal.conf \
#
# startup script
#
    && printf '\
\043!/bin/sh\n\
[ $$ -eq 1 ] && exec dumb-init -- "$0" "$@"\n\
\n\
\043 workaround: sometimes the first start of an X application fails\n\
lxterminal -e true 2> /dev/null\n\
\n\
cd\n\
export SHELL=/bin/bash\n\
\n\
\043 start firefox\n\
firefox &\n\
\n\
\043 start a windows manager if none is active\n\
if wmctrl -m > /dev/null 2>&1; then\n\
	wait $!\n\
else\n\
	jwm\n\
fi\n' \
        > /etc/init.sh && chmod +x /etc/init.sh

VOLUME [ "/root" ]
CMD [ "/etc/init.sh" ]
