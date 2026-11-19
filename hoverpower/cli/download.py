import utilo

import hoverpower.path


@utilo.saveme
def main():
    hoverpower.path.download_packages()
    return utilo.SUCCESS
