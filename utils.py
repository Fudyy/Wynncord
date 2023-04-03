from datetime import datetime


def logger(text):
    """
    Returns a log with [Wynncord]
    """
    date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(f'\x1b[0;36m{date} \x1b[0;30;43m[Wynncord]\x1b[0m {text}')


def command_logger(user: str, command: str, channel: str):
    """
    Generates a log with a command structure
    """
    logger(
        f'El usuario \x1b[5;37;41m{user}\x1b[0m ha usado el comando \x1b[5;37;41m{command}\x1b[0m en el canal \x1b[5;37;41m#{channel}\x1b[0m')


if __name__ == '__main__':
    for style in range(8):
        for fg in range(30, 38):
            s1 = ''
            for bg in range(40, 48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')