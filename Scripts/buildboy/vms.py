vms = {
    'CentOS-7.9': {
        'target': 'CentOS-7.9',
        'vm': '8bd62c88-86aa-4faa-9b6d-71d5305280d7',
        'port': '2222',
        'connect_kwargs': {}
    },
    'CentOS-8.5': {
        'target': 'CentOS-8.5',
        'vm': '4509aa09-d428-429a-bcfd-290672dbe6f3',
        'port': '2223',
        'connect_kwargs': {}
    },
    'CentOS-Stream-8': {
        'target': 'CentOS-Stream-8',
        'vm': '21141559-9433-4107-b628-2e91b2c83640',
        'port': '2224',
        'connect_kwargs': {}
    },
    'Rocky-Linux-9': {
        'target': 'Rocky-Linux-9',
        'vm': 'e6b4503f-99e6-4118-91bf-3a1cad51397c',
        'port': '2225',
        'connect_kwargs': {}
    },
    'Debian-Jessie': {
        'target': 'Debian-Jessie',
        'vm': '82b05661-19e8-494d-b8c0-a3e543333ef1',
        'port': '2226',
        # Needed to auth with rsa for some reason.
        'connect_kwargs': {'disabled_algorithms': {'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']}}
    },
    'Debian-Stretch': {
        'target': 'Debian-Stretch',
        'vm': '0c8c1959-b590-45fb-a2d7-696eeef96273',
        'port': '2227',
        'connect_kwargs': {}
    },
    'Debian-Buster': {
        'target': 'Debian-Buster',
        'vm': '5ad0c9c3-e5b5-4b0c-a586-ce41192de566',
        'port': '2228',
        'connect_kwargs': {}
    },
    'Debian-Bullseye': {
        'target': 'Debian-Bullseye',
        'vm': '2b9d47ff-4365-4d33-9708-21eae54c76e8',
        'port': '2229',
        'connect_kwargs': {}
    },
    'Debian-Bookworm': {
        'target': 'Debian-Bookworm',
        'vm': '3458c148-618d-4ea2-8af9-8c75e797ba06',
        'port': '2230',
        'connect_kwargs': {}
    }
}