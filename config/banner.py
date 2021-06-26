yellow = '\033[01;33m'
white = '\033[01;37m'
green = '\033[01;32m'
blue = '\033[01;34m'
red = '\033[1;31m'
end = '\033[0m'

version = 'v0.1.0'
message = white + '{' + red + version + ' #dev' + white + '}'

def script_banner():
    Cyberspace_Surveying_banner = f"""
    Cyberspace_Survey is a powerful OSINT tool{yellow}
        _________        ___.                                                         _________                                
    \_   ___ \___.__.\_ |__   ___________  _________________    ____  ____       /   _____/__ ____________  __ ____ ___.__.
    /    \  \<   |  | | __ \_/ __ \_  __ \/  ___/\____ \__  \ _/ ___\/ __ \      \_____  \|  |  \_  __ \  \/ // __ <   |  |{message}{green}
    \     \___\___  | | \_\ \  ___/|  | \/\___ \ |  |_> > __ \\  \__\  ___/      /        \  |  /|  | \/\   /\  ___/\___  |{blue}
     \______  / ____| |___  /\___  >__|  /____  >|   __(____  /\___  >___  >____/_______  /____/ |__|    \_/  \___  > ____|{green}
            \/\/          \/     \/           \/ |__|       \/     \/    \/_____/       \/                        \/\/     {end}
    """

    return Cyberspace_Surveying_banner

if __name__ == '__main__':
    print(script_banner())