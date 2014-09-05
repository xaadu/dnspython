# Copyright (C) 2003-2007, 2009-2011 Nominum, Inc.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose with or without fee is hereby granted,
# provided that the above copyright notice and this permission notice
# appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND NOMINUM DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL NOMINUM BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import dns.exception
import dns.rdata
import dns.tokenizer
import dns.util

class HINFO(dns.rdata.Rdata):
    """HINFO record

    @ivar cpu: the CPU type
    @type cpu: string
    @ivar os: the OS type
    @type os: string
    @see: RFC 1035"""

    __slots__ = ['cpu', 'os']

    def __init__(self, rdclass, rdtype, cpu, os):
        super(HINFO, self).__init__(rdclass, rdtype)
        self.cpu = cpu
        self.os = os

    def to_text(self, origin=None, relativize=True, **kw):
        return '"%s" "%s"' % (dns.rdata._escapify(self.cpu),
                              dns.rdata._escapify(self.os))

    def from_text(cls, rdclass, rdtype, tok, origin = None, relativize = True):
        cpu = tok.get_string()
        os = tok.get_string()
        tok.get_eol()
        return cls(rdclass, rdtype, cpu, os)

    from_text = classmethod(from_text)

    def to_wire(self, file, compress = None, origin = None):
        l = len(self.cpu)
        assert l < 256
        dns.util.write_uint8(file, l)
        file.write(self.cpu.encode('latin_1'))
        l = len(self.os)
        assert l < 256
        dns.util.write_uint8(file, l)
        file.write(self.os.encode('latin_1'))

    def from_wire(cls, rdclass, rdtype, wire, current, rdlen, origin = None):
        l = wire[current]
        current += 1
        rdlen -= 1
        if l > rdlen:
            raise dns.exception.FormError
        cpu = wire[current : current + l].decode('latin_1')
        current += l
        rdlen -= l
        l = wire[current]
        current += 1
        rdlen -= 1
        if l != rdlen:
            raise dns.exception.FormError
        os = wire[current : current + l].decode('latin_1')
        return cls(rdclass, rdtype, cpu, os)

    from_wire = classmethod(from_wire)
