# NetcatP

NetcatP is a lightweight python dupe, allowing for users to send and receive data over IPv4 and Ipv6 addresses. This module supports both UDP and TCP protocols, allowing for a quick means of testing and debugging.


## Usage
For listening, simply enter the port and the desired protocol, 0 for UDP or 1 for TCP. 
>**_NOTE:_** The protocol is set as UDP by default and can be ommitted.
```bash
python netcatp.py <port> <protocol>
```
For sending and receiving data, the target host and port will need to be provided.
```bash
python netcatp.py <port> <target_host> <target_port> <protocol>
```