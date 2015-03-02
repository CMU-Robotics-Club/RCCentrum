"""
The upce_to_upca and check_digit_from_upca functions
are from file bardcodes.py file in the Rattail project.
Should use the full package on Python3 is supported.
"""

#  Rattail -- Retail Software Framework
#  Copyright ÂŠ 2010-2012 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.

def upce_to_upca(upce, include_check_digit=False):
    """
    Expands ``upce`` (which is assumed to be a valid UPC-E barcode) into its
    full UPC-A equivalent.  The return value will have either 11 or 12 digits,
    depending on ``include_check_digit``.
    """
    if len(upce) == 8:
        upce = upce[1:7]
    assert len(upce) == 6
    assert upce.isdigit()

    last_digit = int(upce[-1])

    if last_digit == 0:
        upca = "0%02u00000%03u" % (int(upce[0:2]), int(upce[2:5]))
    elif last_digit == 1:
        upca  = "0%02u10000%03u" % (int(upce[0:2]), int(upce[2:5]))
    elif last_digit == 2:
        upca = "0%02u20000%03u" % (int(upce[0:2]), int(upce[2:5]))
    elif last_digit == 3:
        upca = "0%03u00000%02u" % (int(upce[0:3]), int(upce[3:5]))
    elif last_digit == 4:
        upca = "0%04u00000%01u" % (int(upce[0:4]), int(upce[4]))
    elif last_digit == 5:
        upca = "0%05u00005" % int(upce[0:5])
    elif last_digit == 6:
        upca = "0%05u00006" % int(upce[0:5])
    elif last_digit == 7:
        upca = "0%05u00007" % int(upce[0:5])
    elif last_digit == 8:
        upca = "0%05u00008" % int(upce[0:5])
    elif last_digit == 9:
        upca = "0%05u00009" % int(upce[0:5])

    if include_check_digit:
        upca += str(calculate_check_digit(upca))

    return upca


def check_digit_from_upca(value):
    """calculate check digit, they are the same for both UPCA and UPCE"""
    check_digit=0
    odd_pos=True
    for char in str(value)[::-1]:
        if odd_pos:
            check_digit+=int(char)*3
        else:
            check_digit+=int(char)
        odd_pos=not odd_pos #alternate
    check_digit=check_digit % 10
    check_digit=10-check_digit
    check_digit=check_digit % 10
    return check_digit


def format_upc(upc):
    """
    Returns either a 12 digit UPCA, 8 digit UPCE, or None.
    """

    # UPCA with leading 0 and trailing check digit
    if len(upc) == 12:
        return upc
    # UPCE with leading 0, and trailing check digit
    elif len(upc) == 8:
        return upc
    # UPCE with leading 0, no trailing check digit
    elif len(upc) == 7:
        upc = upc[1:]
    # UPCE with no leading 0, no trailing check digit
    elif len(upc) == 6:
        pass
    # Unsure what this UPC is
    else:
        return None

    # upc is a UPCE code
    upca = upce_to_upca(upc)
    check_digit = check_digit_from_upca(upca)

    return "0" + upc + str(check_digit)
