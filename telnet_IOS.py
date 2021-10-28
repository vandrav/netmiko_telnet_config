import getpass
import telnetlib


user = input("Username: ")                                                    # se cere user de telnet introdus de la tastatura
password = getpass("Password: ")                                                   # se cere parola userului introdusa de la tastatura
host = "hosts.txt"
fout="loguri.txt"
fin = open(host)


for host in fin:
    try:
        tn = telnetlib.Telnet(host)
        tn.read_until(b"Username: ")                                          # citeste pana cand vede afisat Username
        tn.write(user.encode('ascii') + b"\n")                                # foloseste user introdus de noi
        if password:                                                          # daca am introdus parola
            tn.read_until(b"Password: ")                                      # citeste pana cand vede afisat Password
            tn.write(password.encode('ascii') + b"\n")                        # foloseste parola introdusa de noi
        time.sleep(1)
        tn.write(b"conf t\n")
        tn.write(b"ip access-list standard allowed_vty\n")
        tn.write(b"remark --- Stablenet Agent 1\n")
        tn.write(b"permit host x.x.x.x\n")
        tn.write(b"remark --- Stablenet Agent 2\n")
        tn.write(b"permit host x.x.x.x\n")
        tn.write(b"remark --- FWI_NAT_mng_data_bi0514\n")
        tn.write(b"permit host x.x.x.x\n")
        tn.write(b"remark --- FWI_NAT_mng_data_cl0400\n")
        tn.write(b"permit host x.x.x.x\n")
        tn.write(b"end\n")
        tn.write(b"show ip access-list allowed_vty\n")
        output = print(tn.read_until().decode('ascii'))                       # citeste si pune in output
        for line in output:
            fo = open(fout, 'a')
            fo.write(line)                                                    # salveaza output in fisier
            fo.write("\n")
            fo.close()
        print(output)                                                         # afiseaza output
        print(host + "done")
    except IOError:
        print ('Probleme de conectare cu ' + host)
