NewIP=`curl https://api.ipify.org`
echo "{\"PublicIP\": \"$NewIP\"}" > PublicIPsh.txt
curl -i -H "Content-Type: application/json" -X PUT -d "@/root/iGenius138/API/PublicIPsh.txt" http://www.hipt.vn:3500/api/devices/3
