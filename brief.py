ngrok = [f'''$ cat ~/.config/ngrok/ngrok.yml

<code>version: "2"
authtoken: NGROK_TOKEN
tunnels:
  first:
    addr: 4444
    proto: tcp
  second:
    addr: 3333
    proto: tcp</code>
    
<b>$ ngrok start --all</b>''']
