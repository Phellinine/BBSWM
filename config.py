from datetime import datetime

import nextcloud_client

player_log_file = datetime.today().date().isoformat() + ".json"
player_log_path = "player_logs/"
player_log_full = player_log_path + player_log_file

log_file = datetime.today().date().isoformat() + ".md"
log_path = "logs/"
log_full = log_path + log_file

NC = nextcloud_client.Client('https://gmb-cloud.wiesan.de')
nc_path = "./Minecraft mit Dettweiler/server player logs"

plog_scale_width = 0.1
plog_scale_height = 50

icon_path = './assets/BBSWM_icon.png'

style_path = './configs/UI.json'
style = "dark"