"""\
TODO: The general idea was to reduce rawmaker speed. In the end, rawmaker
needs more time as a result of compressed pdf file. Therefore this idea
does not work.
"""

import argparse

import utilo

import hoverpower
import hoverpower.path

WHOIS = '/bin/gs' if utilo.hasprog('/bin/gs') else 'gs'  #nosec

# ensure that some progress is made
SKIP_RATE = 1.15

COMPRESS = f"""\
{WHOIS} \
  -sDEVICE=pdfwrite \
  -dNOPAUSE -dBATCH \
  -dColorImageDownsampleType=/Average \
  -dColorImageResolution=1 \
  -dGrayImageResolution=1 \
  -dMonoImageResolution=1 \
  -dAutoFilterColorImages=false \
  -dColorImageFilter=/FlateEncode \
  -sOutputFile=%s \
  %s
"""


@utilo.saveme
def main():
    parse_args()
    if not utilo.hasprog('gs'):
        utilo.exitx('install ghostscript')
    for item in hoverpower.path.PDF:
        utilo.log(item)
        utilo.exists_assert(item)
        compressed = utilo.tmpfile(hoverpower.TMP)
        cmd = COMPRESS % (compressed, item)
        result = utilo.run(cmd=cmd)
        utilo.debug(result)
        before = utilo.file_read_binary(item)
        after = utilo.file_read_binary(compressed)
        rate = utilo.roundme(len(before) / len(after))
        if rate < SKIP_RATE:
            utilo.log(f'{rate} not compressing: {item}')
            continue
        utilo.log(rate)
        utilo.file_replace_binary(
            item,
            content=after,
        )
        utilo.file_remove(compressed)
    return utilo.SUCCESS


def parse_args():
    parser = argparse.ArgumentParser(
        prog='powercompress',
        description='Compress all pdf files',
    )
    args = parser.parse_args()
    return args
