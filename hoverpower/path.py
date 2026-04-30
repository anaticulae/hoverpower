# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import concurrent.futures
import importlib.metadata
import itertools
import os
import tarfile

import requests
import utilo

# TMP = utilo.tmp(hoverpower.ROOT)
TMP = utilo.join('/tmp/power')  #nosec B108

REPO = utilo.join(
    os.path.join(os.path.dirname(__file__), '..'),
    'hoverpower/repo',
    exist=True,
)
STORE = os.getenv('HOVERPOWER_STORE', REPO)

BACHELOR = utilo.join(STORE, 'bachelor')
BOOK = utilo.join(STORE, 'book')
DISS = utilo.join(STORE, 'diss')
HABIL = utilo.join(STORE, 'habil')
DOCU = utilo.join(STORE, 'docu')
HOME = utilo.join(STORE, 'home')
MASTER = utilo.join(STORE, 'master')
ORDER = utilo.join(STORE, 'order')
PAPER = utilo.join(STORE, 'paper')
TECH = utilo.join(STORE, 'tech')

# https://github.com/anaticulae/hoverpower/releases/download/v1.0.2/master.tar.gz
SOURCE = 'https://github.com/anaticulae/hoverpower/releases/download/'+\
         f'v{importlib.metadata.version("hoverpower")}/'

TIMEOUT_DOWNLOAD_SEC = 15
WORKER = utilo.parse_int(os.getenv('HOVERPOWER_DOWNLOAD_WORKER', '5'))

PACKAGES_DEFAULT = 'bachelor book diss docu habil home master order paper tech'
PACKAGES = os.getenv('HOVERPOWER_PACKAGES', PACKAGES_DEFAULT).strip().split()


def download() -> list:
    result = []
    for item in RESOURCES:
        if 'https://' in item:
            downloaded = download_file(item)
            if not downloaded:
                continue
            result.append(downloaded)
        else:
            result.append(utilo.file_read_binary(item))
    return result


def download_packages():
    root = STORE
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKER) as executor:
        executor.map(
            download_and_extract,
            PACKAGES,
            itertools.repeat(root),
        )


def download_and_extract(package, root):
    tar = download_package(package, root=root)
    if not tar:
        return
    outpath = utilo.join(root, package)
    utilo.log(f'untar: {tar} {outpath}')
    untar(
        source=tar,
        outpath=outpath,
    )
    utilo.log()


def download_package(package: str, root=TMP):
    utilo.debug(f'store: {root}')
    os.makedirs(root, exist_ok=True)
    path = utilo.join(root, package)
    dl = utilo.join(root, f'{package}.tar.gz')
    if utilo.exists(path):
        utilo.log(f'already downloaded: {path}\n')
        return None
    url = f'{SOURCE}{package}.tar.gz'
    data = download_file(url)
    if not data:
        utilo.error(f'invalid download: {path}')
        return None
    utilo.file_replace_binary(dl, content=data)
    os.makedirs(path)
    utilo.log(f'downloaded: {package}')
    return dl


def untar(source, outpath):
    with tarfile.open(source, mode='r:gz') as tar:
        tar.extractall(  #nosec B202
            path=outpath,
            # members=safe_members(tar, outpath),
        )


def safe_members(tar, path):
    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if os.path.realpath(member_path).startswith(os.path.realpath(path)):
            yield member
        else:
            raise ValueError(f"Unsafe path detected: {member.name}")


def download_file(url: str) -> bytes:
    utilo.log(f'download: {url}')
    try:
        response = requests.get(
            url,
            timeout=TIMEOUT_DOWNLOAD_SEC,
        )
    except requests.HTTPError as msg:
        utilo.error(msg)
        return None
    try:
        response.raise_for_status()
    except requests.HTTPError as msg:
        utilo.error(msg)
        return None
    data = response.content
    return data


def bachelor(value: str, local: bool = True) -> str:
    name = f'bachelor{value}.pdf'
    if local:
        path = utilo.join(BACHELOR, name, exist=False)
        return path
    path = f'{SOURCE}/bachelor/{name}'
    return path


# bachelor
BACHELOR026_PDF = bachelor('026')
BACHELOR028A_PDF = bachelor('028a')
BACHELOR028B_PDF = bachelor('028b')
BACHELOR028_PDF = bachelor('028')
BACHELOR029A_PDF = bachelor('029a')
BACHELOR029_PDF = bachelor('029')
BACHELOR032A_PDF = bachelor('032a')
BACHELOR032B_PDF = bachelor('032b')
BACHELOR032C_PDF = bachelor('032c')
BACHELOR032_PDF = bachelor('032')
BACHELOR036_PDF = bachelor('036')
BACHELOR037_PDF = bachelor('037')
BACHELOR038_PDF = bachelor('038')
BACHELOR039_PDF = bachelor('039')
BACHELOR040_PDF = bachelor('040')
BACHELOR041A_PDF = bachelor('041a')
BACHELOR041B_PDF = bachelor('041b')
BACHELOR041_PDF = bachelor('041')
BACHELOR045A_PDF = bachelor('045a')
BACHELOR045B_PDF = bachelor('045b')
BACHELOR045_PDF = bachelor('045')
BACHELOR046A_PDF = bachelor('046a')
BACHELOR046_PDF = bachelor('046')
BACHELOR051_PDF = bachelor('051')
BACHELOR056_PDF = bachelor('056')
BACHELOR063_PDF = bachelor('063')
BACHELOR067_PDF = bachelor('067')
BACHELOR074_PDF = bachelor('074')
BACHELOR075_PDF = bachelor('075')
BACHELOR076_PDF = bachelor('076')
BACHELOR077_PDF = bachelor('077')
BACHELOR078A_PDF = bachelor('078a')
BACHELOR078_PDF = bachelor('078')
BACHELOR085_PDF = bachelor('085')
BACHELOR086_PDF = bachelor('086')
BACHELOR090_PDF = bachelor('090')
BACHELOR101_PDF = bachelor('101')
BACHELOR105_PDF = bachelor('105')
BACHELOR109_PDF = bachelor('109')
BACHELOR111_PDF = bachelor('111')
BACHELOR128_PDF = bachelor('128')
BACHELOR241_PDF = bachelor('241')
# book
book = lambda x: utilo.join(BOOK, f'book{x}.pdf', exist=False)  # pylint:disable=C3001
BOOK007_PDF = book('007')
BOOK053_PDF = book('053')
BOOK084_PDF = book('084')
BOOK104_PDF = book('104')
BOOK119_PDF = book('119')
BOOK173_PDF = book('173')
BOOK200_PDF = book('200')
BOOK264_PDF = book('264')
BOOK324_PDF = book('324')
BOOK662_PDF = book('662')
# diss
diss = lambda x: utilo.join(DISS, f'diss{x}.pdf', exist=False)  # pylint:disable=C3001
DISS143_PDF = diss('143')
DISS144_PDF = diss('144')
DISS146_PDF = diss('146')
DISS148_PDF = diss('148')
DISS154_PDF = diss('154')
DISS157_PDF = diss('157')
DISS167_PDF = diss('167')
DISS170_PDF = diss('170')
DISS170B_PDF = diss('170b')
DISS172_PDF = diss('172')
DISS173_PDF = diss('173')
DISS178_PDF = diss('178')
DISS180_PDF = diss('180')
DISS205_PDF = diss('205')
DISS218_PDF = diss('218')
DISS233_PDF = diss('233')
DISS264_PDF = diss('264')
DISS266_PDF = diss('266')
DISS272_PDF = diss('272')
DISS272A_PDF = diss('272a')
DISS273_PDF = diss('273')
DISS274_PDF = diss('274')
DISS287_PDF = diss('287')
DISS350_PDF = diss('350')
DISS358_PDF = diss('358')
DISS406_PDF = diss('406')
DISS480_PDF = diss('480')
# habil
HABIL168_PDF = utilo.join(HABIL, 'habil168.pdf')
# doc
DOCU007_PDF = utilo.join(DOCU, 'docu007.pdf')
DOCU009_PDF = utilo.join(DOCU, 'docu009.pdf')
DOCU012_PDF = utilo.join(DOCU, 'docu012.pdf')
DOCU013_PDF = utilo.join(DOCU, 'docu013.pdf')
DOCU014_PDF = utilo.join(DOCU, 'docu014.pdf')
DOCU027_PDF = utilo.join(DOCU, 'docu027.pdf')
DOCU035_PDF = utilo.join(DOCU, 'docu035.pdf')
DOCU037_PDF = utilo.join(DOCU, 'docu037.pdf')
# homework
home = lambda x: utilo.join(HOME, f'home{x}.pdf', exist=False)  # pylint:disable=C3001
HOME007A_PDF = home('007a')
HOME007_PDF = home('007')
HOME009A_PDF = home('009a')
HOME009B_PDF = home('009b')
HOME009_PDF = home('009')
HOME011_PDF = home('011')
HOME012A_PDF = home('012a')
HOME012_PDF = home('012')
HOME013A_PDF = home('013a')
HOME013_PDF = home('013')
HOME014A_PDF = home('014a')
HOME014B_PDF = home('014b')
HOME014C_PDF = home('014c')
HOME014_PDF = home('014')
HOME015A_PDF = home('015a')
HOME015_PDF = home('015')
HOME016A_PDF = home('016a')
HOME016B_PDF = home('016b')
HOME016C_PDF = home('016c')
HOME016_PDF = home('016')
HOME017A_PDF = home('017a')
HOME017B_PDF = home('017b')
HOME017C_PDF = home('017c')
HOME017_PDF = home('017')
HOME018A_PDF = home('018a')
HOME018B_PDF = home('018b')
HOME018_PDF = home('018')
HOME019A_PDF = home('019a')
HOME019B_PDF = home('019b')
HOME019_PDF = home('019')
HOME020_PDF = home('020')
HOME021A_PDF = home('021a')
HOME021B_PDF = home('021b')
HOME021_PDF = home('021')
HOME022A_PDF = home('022a')
HOME022B_PDF = home('022b')
HOME022_PDF = home('022')
HOME024_PDF = home('024')
HOME025_PDF = home('025')
HOME026A_PDF = home('026a')
HOME026B_PDF = home('026b')
HOME026C_PDF = home('026c')
HOME026_PDF = home('026')
HOME031_PDF = home('031')
HOME040A_PDF = home('040a')
HOME043_PDF = home('043')
HOME050_PDF = home('050')
# master
master = lambda x: utilo.join(MASTER, f'master{x}.pdf', exist=False)  # pylint:disable=C3001
MASTER031_PDF = master('031')
MASTER049_PDF = master('049')
MASTER063_PDF = master('063')
MASTER072_PDF = master('072')
MASTER075_PDF = master('075')
MASTER078_PDF = master('078')
MASTER083_PDF = master('083')
MASTER089_PDF = master('089')
MASTER091A_PDF = master('091a')
MASTER091B_PDF = master('091b')
MASTER098_PDF = master('098')
MASTER099B_PDF = master('099b')
MASTER099C_PDF = master('099c')
MASTER099_PDF = master('099')
MASTER105_PDF = master('105')
MASTER110_PDF = master('110')
MASTER112_PDF = master('112')
MASTER116_PDF = master('116')
MASTER127_PDF = master('127')
MASTER148_PDF = master('148')
MASTER155_PDF = master('155')
MASTER193_PDF = master('193')
# order
order = lambda x: utilo.join(ORDER, f'order{x}.pdf', exist=False)  # pylint:disable=C3001
ORDER009_PDF = order('009')
ORDER015_PDF = order('015')
ORDER024_PDF = order('024')
ORDER038_PDF = order('038')
ORDER044_PDF = order('044')
ORDER050_PDF = order('050')
ORDER075_PDF = order('075')
ORDER107_PDF = order('107')
# paper
paper = lambda x: utilo.join(PAPER, f'paper{x}.pdf', exist=False)  # pylint:disable=C3001
PAPER006A_PDF = paper('006a')
PAPER006B_PDF = paper('006b')
PAPER006_PDF = paper('006')
PAPER008A_PDF = paper('008a')
PAPER008B_PDF = paper('008b')
PAPER008C_PDF = paper('008c')
PAPER008_PDF = paper('008')
PAPER009B_PDF = paper('009b')
PAPER009_PDF = paper('009')
PAPER010_PDF = paper('010')
PAPER010A_PDF = paper('010a')
PAPER011_PDF = paper('011')
PAPER014B_PDF = paper('014b')
PAPER014_PDF = paper('014')
PAPER016_PDF = paper('016')
PAPER017_PDF = paper('017')
PAPER018_PDF = paper('018')
PAPER019_PDF = paper('019')
PAPER023_PDF = paper('023')
PAPER028_PDF = paper('028')
PAPER042_PDF = paper('042')

# technical
TECH019_PDF = utilo.join(TECH, 'tech019.pdf')
TECH024_PDF = utilo.join(TECH, 'tech024.pdf')

BACHELORS = [
    BACHELOR026_PDF,
    BACHELOR028A_PDF,
    BACHELOR028B_PDF,
    BACHELOR028_PDF,
    BACHELOR029A_PDF,
    BACHELOR029_PDF,
    BACHELOR032A_PDF,
    BACHELOR032B_PDF,
    BACHELOR032C_PDF,
    BACHELOR032_PDF,
    BACHELOR036_PDF,
    BACHELOR037_PDF,
    BACHELOR038_PDF,
    BACHELOR039_PDF,
    BACHELOR040_PDF,
    BACHELOR041A_PDF,
    BACHELOR041B_PDF,
    BACHELOR041_PDF,
    BACHELOR045A_PDF,
    BACHELOR045B_PDF,
    BACHELOR045_PDF,
    BACHELOR046A_PDF,
    BACHELOR046_PDF,
    BACHELOR051_PDF,
    BACHELOR056_PDF,
    BACHELOR063_PDF,
    BACHELOR067_PDF,
    BACHELOR074_PDF,
    BACHELOR075_PDF,
    BACHELOR076_PDF,
    BACHELOR077_PDF,
    BACHELOR078A_PDF,
    BACHELOR078_PDF,
    BACHELOR085_PDF,
    BACHELOR086_PDF,
    BACHELOR090_PDF,
    BACHELOR101_PDF,
    BACHELOR105_PDF,
    BACHELOR109_PDF,
    BACHELOR111_PDF,
    BACHELOR128_PDF,
    BACHELOR241_PDF,
]
BOOKS = [
    BOOK007_PDF,
    BOOK053_PDF,
    BOOK084_PDF,
    BOOK104_PDF,
    BOOK119_PDF,
    BOOK173_PDF,
    BOOK200_PDF,
    BOOK264_PDF,
    BOOK324_PDF,
    BOOK662_PDF,
]
DISSS = [
    DISS143_PDF,
    DISS144_PDF,
    DISS146_PDF,
    DISS148_PDF,
    DISS154_PDF,
    DISS157_PDF,
    DISS167_PDF,
    DISS170B_PDF,
    DISS170_PDF,
    DISS172_PDF,
    DISS173_PDF,
    DISS178_PDF,
    DISS180_PDF,
    DISS205_PDF,
    DISS218_PDF,
    DISS233_PDF,
    DISS264_PDF,
    DISS266_PDF,
    DISS272A_PDF,
    DISS272_PDF,
    DISS273_PDF,
    DISS274_PDF,
    DISS287_PDF,
    DISS350_PDF,
    DISS358_PDF,
    DISS406_PDF,
    DISS480_PDF,
]
HABILS = [
    HABIL168_PDF,
]
DOCUS = [
    DOCU007_PDF,
    DOCU009_PDF,
    DOCU012_PDF,
    DOCU013_PDF,
    DOCU014_PDF,
    DOCU027_PDF,
    DOCU035_PDF,
    DOCU037_PDF,
]
HOMES = [
    HOME007_PDF,
    HOME009A_PDF,
    HOME009B_PDF,
    HOME009_PDF,
    HOME011_PDF,
    HOME012A_PDF,
    HOME012_PDF,
    HOME013A_PDF,
    HOME013_PDF,
    HOME014A_PDF,
    HOME014B_PDF,
    HOME014C_PDF,
    HOME014_PDF,
    HOME015A_PDF,
    HOME015_PDF,
    HOME016A_PDF,
    HOME016B_PDF,
    HOME016C_PDF,
    HOME016_PDF,
    HOME017A_PDF,
    HOME017B_PDF,
    HOME017C_PDF,
    HOME017_PDF,
    HOME018A_PDF,
    HOME018B_PDF,
    HOME018_PDF,
    HOME019A_PDF,
    HOME019B_PDF,
    HOME019_PDF,
    HOME020_PDF,
    HOME021A_PDF,
    HOME021B_PDF,
    HOME021_PDF,
    HOME022A_PDF,
    HOME022B_PDF,
    HOME022_PDF,
    HOME024_PDF,
    HOME025_PDF,
    HOME026A_PDF,
    HOME026B_PDF,
    HOME026C_PDF,
    HOME026_PDF,
    HOME031_PDF,
    HOME040A_PDF,
    HOME043_PDF,
    HOME050_PDF,
]
MASTERS = [
    MASTER031_PDF,
    MASTER049_PDF,
    MASTER063_PDF,
    MASTER072_PDF,
    MASTER075_PDF,
    MASTER078_PDF,
    MASTER083_PDF,
    MASTER089_PDF,
    MASTER091A_PDF,
    MASTER091B_PDF,
    MASTER098_PDF,
    MASTER099B_PDF,
    MASTER099C_PDF,
    MASTER099_PDF,
    MASTER105_PDF,
    MASTER110_PDF,
    MASTER112_PDF,
    MASTER116_PDF,
    MASTER127_PDF,
    MASTER148_PDF,
    MASTER155_PDF,
    MASTER193_PDF,
]
ORDERS = [
    ORDER009_PDF,
    ORDER015_PDF,
    ORDER024_PDF,
    ORDER038_PDF,
    ORDER044_PDF,
    ORDER050_PDF,
    ORDER075_PDF,
    ORDER107_PDF,
]
PAPERS = [
    PAPER006A_PDF,
    PAPER006B_PDF,
    PAPER006_PDF,
    PAPER008A_PDF,
    PAPER008B_PDF,
    PAPER008C_PDF,
    PAPER008_PDF,
    PAPER009B_PDF,
    PAPER009_PDF,
    PAPER010A_PDF,
    PAPER010_PDF,
    PAPER011_PDF,
    PAPER014B_PDF,
    PAPER014_PDF,
    PAPER016_PDF,
    PAPER017_PDF,
    PAPER018_PDF,
    PAPER019_PDF,
    PAPER023_PDF,
    PAPER028_PDF,
    PAPER042_PDF,
]
TECHS = [
    TECH019_PDF,
    TECH024_PDF,
]

PDF = BACHELORS + BOOKS + DISSS + HABILS + DOCUS + HOMES + MASTERS + ORDERS + PAPERS + TECHS

DOUBLECOLUMNS = [
    PAPER006B_PDF,
    PAPER006A_PDF,
    PAPER006_PDF,
    PAPER008B_PDF,
    PAPER008_PDF,
    PAPER009_PDF,
    PAPER010_PDF,
    PAPER011_PDF,
    PAPER014_PDF,
]
LEFTRIGHT = [
    BACHELOR075_PDF,
    BACHELOR109_PDF,
    BACHELOR241_PDF,
    BOOK007_PDF,
    BOOK200_PDF,
    DISS264_PDF,
    DISS274_PDF,
    MASTER110_PDF,
    PAPER006B_PDF,
]
NORMAL = utilo.minus(PDF, DOUBLECOLUMNS + LEFTRIGHT)

RESOURCES = [
    BACHELOR,
    BOOK,
    DISS,
    DOCU,
    HOME,
    MASTER,
    ORDER,
    PAPER,
    TECH,
]

RESOURCES.extend(PDF)


def ensure_resources():
    if STORE != REPO:
        # do not check resources if data path is not outside git repository
        return
    for item in RESOURCES:
        if SOURCE in item:
            continue
        # assert utilo.exists_assert(item)


ensure_resources()
utilo.assert_unique(RESOURCES)

#remove later
DOUBLE_COLUMNS = DOUBLECOLUMNS
# remove later
PAPER06B_PDF = PAPER006B_PDF
PAPER06MATH_PDF = PAPER006A_PDF
PAPER006MATH_PDF = PAPER006A_PDF
PAPER06_PDF = PAPER006_PDF
PAPER08B_PDF = PAPER008B_PDF
PAPER08_PDF = PAPER008_PDF
PAPER09B_PDF = PAPER009B_PDF
PAPER09_PDF = PAPER009_PDF
PAPER10_PDF = PAPER010_PDF
PAPER11_PDF = PAPER011_PDF
PAPER14B_PDF = PAPER014B_PDF
PAPER14_PDF = PAPER014_PDF
PAPER16_PDF = PAPER016_PDF
PAPER18_PDF = PAPER018_PDF
PAPER23_PDF = PAPER023_PDF
PAPER42_PDF = PAPER042_PDF
MASTER198_PDF = MASTER193_PDF
