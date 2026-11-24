#!/usr/bin/env python3
"""news-23 b101 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys
import zlib

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
EXPECTED_W, EXPECTED_H = 1024, 1024
MIN_BYTES = 10000
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def parse_png(data):
    """Validate the PNG header and chunk structure (stdlib only)."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return "bad PNG signature"
    if len(data) < 8 + 8 + 13 + 4:
        return "file too short for IHDR"
    # first chunk must be IHDR, 13 bytes
    length, ctype = struct.unpack(">I4s", data[8:16])
    if ctype != b"IHDR" or length != 13:
        return "first chunk is not a 13-byte IHDR"
    w, h, depth, ctype_b, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (EXPECTED_W, EXPECTED_H):
        return "dimensions are %dx%d, expected %dx%d" % (w, h, EXPECTED_W, EXPECTED_H)
    if depth != 8:
        return "bit depth %d, expected 8" % depth
    if ctype_b not in (2, 6):
        return "colour type %d, expected 2 or 6" % ctype_b
    if comp != 0 or filt != 0 or inter != 0:
        return "unexpected compression/filter/interlace fields"
    ihdr_crc = zlib.crc32(data[12:29]) & 0xFFFFFFFF
    stored_crc = struct.unpack(">I", data[29:33])[0]
    if ihdr_crc != stored_crc:
        return "IHDR CRC mismatch"
    # walk the remaining chunks, checking CRCs
    off = 33
    idat_total = 0
    seen_iend = False
    while off < len(data):
        if off + 8 > len(data):
            return "truncated chunk header at offset %d" % off
        clen, ctype = struct.unpack(">I4s", data[off:off + 8])
        if off + 12 + clen > len(data):
            return "truncated chunk %r at offset %d" % (ctype, off)
        crc = zlib.crc32(data[off + 4:off + 8 + clen]) & 0xFFFFFFFF
        stored = struct.unpack(">I", data[off + 8 + clen:off + 12 + clen])[0]
        if crc != stored:
            return "CRC mismatch in chunk %r" % ctype
        if ctype == b"IDAT":
            if clen == 0:
                return "empty IDAT chunk"
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                return "IEND chunk is not empty"
            if off + 12 + clen != len(data):
                return "trailing data after IEND"
            seen_iend = True
            break
        off += 12 + clen
    if not seen_iend:
        return "missing IEND chunk"
    if idat_total < 1000:
        return "IDAT payload too small (%d bytes)" % idat_total
    return None


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    if not os.path.isdir(out_dir):
        return fail("MAKEFUN_OUTPUT_DIR %r is not a directory" % out_dir)
    # refuse to write inside this repo (grader runs from a read-only copy);
    # resolve symlinks so a symlinked output dir cannot escape the check
    repo_root = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
    out_abs = os.path.realpath(os.path.abspath(out_dir))
    if out_abs == repo_root or out_abs.startswith(repo_root + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR %r is inside the repo" % out_dir)
    if not os.path.isfile(SRC):
        return fail("source entry.png not found next to main.py")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) < MIN_BYTES:
        return fail("entry.png is %d bytes, below minimum %d" % (len(data), MIN_BYTES))
    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over 1 MiB" % len(data))
    err = parse_png(data)
    if err:
        return fail(err)
    dest = os.path.join(out_abs, "entry.png")
    if os.path.abspath(dest) == os.path.abspath(SRC):
        return fail("output would overwrite the source image")
    with open(dest, "wb") as f:
        f.write(data)
    with open(dest, "rb") as f:
        written = f.read()
    if written != data:
        return fail("re-read output does not match source")
    print("wrote %s (%d bytes, sha256 %s)" % (dest, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
