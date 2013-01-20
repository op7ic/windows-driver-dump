print "[+] Windows Driver Dump"
print "[+] contact : If you know me then give me a shout"
print "[+] usage: ./windows-driver-dump.py"
print "\n"

from ctypes import *
#Windows modules loader
kernel32 =  windll.kernel32
psapi = windll.psapi

class drivers():
    # Rather simplistic but effective way of getting the list of all drivers on in windows
    def getAllDeviceDrivers(self):
        lpcbNeeded =          c_ulong(0)
        empty_init_array      = c_ulong * 1024
        lpImageBase           = empty_init_array()
        drivername_size       = c_long()
        drivername_size.value = 48
        if psapi.EnumDeviceDrivers(byref(lpImageBase),sizeof(c_void_p)*1024,byref(lpcbNeeded)):
            no_drivers = int(lpcbNeeded.value / sizeof(c_void_p))
            print "[*] EnumDeviceDrivers: %d modules detected" % no_drivers
            print "\t[+] Dumping all device drivers"
            for baseaddy in lpImageBase:
     
                drivername = c_char_p("\x00"*drivername_size.value)
                if baseaddy:
                    psapi.GetDeviceDriverBaseNameA(baseaddy, drivername, drivername_size.value)         
                             
                    driverpath = c_char_p("\x00"*drivername_size.value)
                    psapi.GetDeviceDriverFileNameA(baseaddy,driverpath,drivername_size.value)
                    # if we have drivers with addresses allocated within 0x80000000 and 0xFFFFFFFF they loaded directly kernel
                    if baseaddy > 2147483648 and baseaddy < 4294967295:  
                        print "\t\t [-] Kernel Driver",drivername.value.lower(),"is located on 0x%08x load path is %s" % (baseaddy,driverpath.value.lower())
                    else:
                        # user level drivers are within 0x00000000 and 0x7FFFFFFF
                        print "\t\t [-] User Driver",drivername.value.lower(),"is located on 0x%08x load path is %s" % (baseaddy,driverpath.value.lower())                 

drivers = drivers()
drivers.getAllDeviceDrivers()