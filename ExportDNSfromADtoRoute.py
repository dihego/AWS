import os,sys



'''
Manually enter the domain name of both of the domain Controllers including the IPs
'''
DC1 = input("Enter the NAME of Primary Domain Controler ((ip-cxxx)): \n")
DC1IP = input("Enter the IP Primary Domain Controler x.x.x.x/32: \n")
DC2 = input("Enter the NAME Secondary Domain Controler ((ip-cxxx)): \n")
DC2IP = input("Enter the IP Secondary Domain Controler x.x.x.x/32: \n")

print ("#####" * 20 )
print ("#####" * 20 )

#Query DNS for active records
#Get-DnsServerResourceRecord -ComputerName ip-c613016e.dgoptam.com -ZoneName _msdcs.dgoptam.com
#Get-DnsServerResourceRecord -ComputerName ip-c613016e.dgoptam.com -ZoneName dgoptam.com

#AD by default doesnt clear cache in 7 days. If your environtment is dynamic changing those values "Domain AGING" to something appropiate 1 day perhaps.
#* Clear Cache and RELOAD to get the latest.
#* For Linux domains if they dont show up. YOu may want to rejoin if the hostname was set after joining to AD.

#the AD commands will export in CSV format the records of the domain ZONES. 
#export zone in files: replace dgoptam.com 
#Get-DnsServerResourceRecord -ComputerName ip-c613016e.dgoptam.com -ZoneName dgoptam.com | export-csv C:\Users\dgoadmin\Desktop\dnsrecords.csv
#Get-DnsServerResourceRecord -ComputerName ip-c613016e.dgoptam.com -ZoneName _msdcs.dgoptam.com | export-csv C:\Users\dgoadmin\Desktop\dnsrecords_msdcs.csv


print ("Enter the list of records from the CSV ")
print ("example::  From column Hostname ## _ldap._tcp.ForestDnsZones	SRV ###")
lista_commands = list()

maxlines1 = input("Number of commands YOU WOULD LIKE TO QUERY : ")
maxlines2 = int(maxlines1)


for lines in range(maxlines2):
    inline = input(" ")
    lista_commands.append(inline)

print ("#####" * 20 )
print ("#####" * 20 )



cleanlistofrecords = list((set(lista_commands)))
for addttl in cleanlistofrecords:
    if 'SRV' in addttl:
        srvrecord =  (addttl.replace("SRV", "300 SRV "))
        if '_kerberos' in srvrecord:
            print (f"{srvrecord} 0 100 88 {DC1} ")
            print (f"{srvrecord} 0 100 88 {DC2} ")
        elif '_gc' in srvrecord:
            print (f"{srvrecord} 0 100 3268 {DC1} ")
            print (f"{srvrecord} 0 100 3268 {DC2} ")     
        elif '_ldap' in srvrecord:
            print (f"{srvrecord} 0 100 389 {DC1} ")
            print (f"{srvrecord} 0 100 389 {DC2} ") 
        elif 'kpasswd' in srvrecord:
            print (f"{srvrecord} 0 100 464 {DC1} ")
            print (f"{srvrecord} 0 100 464 {DC2} ") 
    elif 'DomainDnsZones' in addttl or 'ForestDnsZones' in addttl:
        Arecord =  (addttl.replace("A", "300 A "))
        print (f"{Arecord} {DC1IP}")
        print (f"{Arecord} {DC2IP}")

print (f"{DC1} 300 A {DC1IP}")
print (f"{DC2} 300 A {DC2IP}")

print (f"_ldap._udp 300 SRV 0 100 389 {DC1}")
print (f"_ldap._udp 300 SRV 0 100 389 {DC2}")

print (f"_kpasswd 300 SRV 0 100 464 {DC1}")
print (f"_kpasswd 300 SRV 0 100 464 {DC2}")

print ()
print ()
print ()
print ()
print ("#####" * 20 )
print ("#####" * 20 )
print (" MDSC.domain.com NAME::: ")
print ("Enter the list of records from the CSV ")
print ("example::  From column Hostname + RecordType ## _ldap._tcp.ForestDnsZones	SRV ###")
enter = input("Press Enter to Continue: ")
secondnddomainlistcmds = list()

seconddomainmaxlines1 = input("Number of commands YOU WOULD LIKE TO QUERY : ")
seconddomainmaxlines2 = int(seconddomainmaxlines1)

for lines in range(seconddomainmaxlines2):
    inline = input(" ")
    secondnddomainlistcmds.append(inline)

print ("#####" * 20 )
print ("#####" * 20 )

cleanlistofrecords2ndDOMAIN = list((set(secondnddomainlistcmds)))

for addttl2ndDOMAIN in cleanlistofrecords2ndDOMAIN:
    if 'SRV' in addttl2ndDOMAIN:
        srvrecord2ndDOMAIN =  (addttl2ndDOMAIN.replace("SRV", "300 SRV "))
        if '_kerberos' in srvrecord2ndDOMAIN:
            print (f"{srvrecord2ndDOMAIN} 0 100 88 {DC1} ")
            print (f"{srvrecord2ndDOMAIN} 0 100 88 {DC2} ")
        elif '_ldap' in srvrecord2ndDOMAIN:
            print (f"{srvrecord2ndDOMAIN} 0 100 389 {DC1} ")
            print (f"{srvrecord2ndDOMAIN} 0 100 389 {DC2} ") 

print (f"_kerberos._udp.dc. 300 SRV 0 100 88 {DC1}")
print (f"_kerberos._udp.dc. 300 SRV 0 100 88 {DC2}")

print (f"_ldap._udp.dc. 300 SRV 0 100 389 {DC1}")
print (f"_ldap._udp.dc. 300 SRV 0 100 389 {DC2}")


print (f"gc. 300 A {DC1IP}")
print (f"gc. 300 A {DC2IP}")

print (f"{DC1}300 A {DC1IP} ")
print (f"{DC2}300 A {DC2IP} ")
