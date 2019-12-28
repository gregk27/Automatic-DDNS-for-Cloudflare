import urllib.request;
import json as JSON;
import time;

#Change these values to fit needs
domain = "example.com";
subdomains = ["", "test""]
headers = {
        "X-Auth-Email": "email@example.com",
        "X-Auth-Key": "123456798ABCDEF",
        "Content-Type": "application/json"
}

#Convert output from requests to a better format
def byte2str(byte):
    byte = str(byte)[2:-1];
    if(byte.endswith("\\n")):
       byte = byte[:-2]
    return byte

#Get the public IP (what records should be
req = urllib.request.urlopen("https://checkip.amazonaws.com")
ip = byte2str(req.read())
print("Public IP is", ip);

#Get the domain's ID
req = urllib.request.Request("https://api.cloudflare.com/client/v4/zones?name="+domain+"&status=active",
                             headers=headers);
raw = urllib.request.urlopen(req);
response = JSON.loads(byte2str(raw.read()));
ID = response["result"][0]["id"];
print("Domain ID is", ID);

timeout = time.time()+60*5; #Loop timeout after 5 minute
i=0;
tries = 0;
while i < len(subdomains):
    print("--------------------");
    if(time.time() > timeout):
        print("Loop timeout");
        break;
    record = subdomains[i]
    #Get the current record value
    if(record == ""):
        record = domain;
    else:
        record = record+"."+domain;
    req = urllib.request.Request("https://api.cloudflare.com/client/v4/zones/"+ID+"/dns_records?type=A&name="+record,
                                 headers=headers);
    raw = urllib.request.urlopen(req);
    response = JSON.loads(byte2str(raw.read()));
    recData = response["result"][0];
    target = recData["content"];
    print("Subdomain",record,"points to",target);
    #If it's correct, then that's all
    if(target == ip):
        i+=1; # Increment to proceed to next record
        tries = 0;
        continue;
    #Stop after 5 tries
    if(tries >= 4):
        i+=1;
        print("Too many attempts. Skipping")
        continue;
    #Update incorrect records
    print("Updating record to",ip);
    #Set data for updated record. Only thing to change is the content
    data = {"type":recData["type"],
            "name":recData["name"],
            "content":ip,
            "ttl":recData["ttl"]};
    print(data);
    req = urllib.request.Request("https://api.cloudflare.com/client/v4/zones/"+ID+"/dns_records/"+recData["id"],
                                 headers=headers, data=bytes(JSON.dumps(data), encoding="utf-8"), method="PUT");
    urllib.request.urlopen(req);
    #Run again to check sucess
    time.sleep(5);
    tries+=1;
print("DNS update complete");

    
