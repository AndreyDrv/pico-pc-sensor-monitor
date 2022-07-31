# hardware monitor address
hw_data_server = '192.168.178.63:8085'

# wlan config:
# WIFI Access Point (SSID) name
AP_Name = "insert_ssid_name"
# WIFI Access Point (SSID) password
AP_PW = "insert_ssid_pw"

# change the cost per/kw in your local currency 
cost_kwh = 0.47

# Uncomment your PC configuration on lines 16-18.
#  Consumption without CPU and GPU:
#    low end PC : consumes approx 20-40w (Intel NUC, Atom, Old PC, etc)
CONS_LOW = [20, 40]
#    mid PC     : 40-70w (Average PC with 1-2 extra HDDs, SSDs, or other devices)
CONS_MID = [40, 70]
#    high end PC: 60-80w (PC with more than 2 SSD/HDD, lighting strips, fans)
CONS_HIGHEND = [60, 80]

#CONS = CONS_LOW
#CONS = CONS_MID
CONS = CONS_HIGHEND

# uncomment the next 2 lines if you want to manually configure the MB consumption
CONS_CUSTOM = [60, 100]
#CONS = CONS_CUSTOM
