from assembler import (
    convert_line
)

def test_convert_line():
    assert convert_line('@1')  == '0000000000000001'
    assert convert_line('@15') == '0000000000001111'

    assert convert_line('D=A')   == '1110110000010000'
    assert convert_line('D=D+A') == '1110000010010000'

