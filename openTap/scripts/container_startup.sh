#!/bin/bash
OUR_IP=$(hostname -i)

# start VNC server (Uses VNC_PASSWD Docker ENV variable)
mkdir -p $HOME/.vnc && echo "$VNC_PASSWD" | vncpasswd -f > $HOME/.vnc/passwd
vncserver :0 -geometry 1400x850 -localhost no -nolisten -rfbauth $HOME/.vnc/passwd -xstartup /opt/x11vnc_entrypoint.sh
# start noVNC web server
/opt/noVNC/utils/launch.sh --listen 5902 &

echo -e "\n\n------------------ VNC environment started ------------------"
echo -e "\nnoVNC HTML client started:\n\t=> connect via http://localhost:5902/?password=$VNC_PASSWD\n"
echo -e "AND NOT THE ONE BELOW IT IS A LIE\n"

if [ -z "$1" ]; then
  tail -f /dev/null
else
  # unknown option ==> call command
  echo -e "\n\n------------------ EXECUTE COMMAND ------------------"
  echo "Executing command: '$@'"
  exec $@
fi