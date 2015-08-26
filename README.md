# simple_geoip_python

The purpose of this file is to prepare a result dict to prepare for getting the address for each ip later on. 

However, getting address from ip is not reliable, search google for more understanding of ip address.

This program makes use of maxmind public database, credit to MaxMind, Inc.

This product includes GeoLite data created by MaxMind, available from http://www.maxmind.com.

Please read main function for example usage.

    def main():
        # for testing
        ip_list = ['82.110.141.43','82.110.141.42','82.110.141.42']
        ip = '82.110.141.43'
        final_dict_0 = address_from_ip(ip_list)
        final_dict_1 = address_from_ip(ip)
        print(final_dict_0)
        print(final_dict_1)

Detailed documetation is inside the file. 
