# creality_rfid

This is a Python3 port of https://github.com/DnG-Crafts/K2-RFID

All credit to the original author for his work on parsing the tag data etc.

This is just a port to Python3 with Proxmark3 integration and read functionality.

```
┌──(venv)─(kali㉿kali)-[~/creality_crypto]
└─$ python3 ./creality_rfid.py pm3read                                                            

[*] Place tag on Proxmark3 antenna...
[*] Reading UID from tag...
[+] UID detected: 35B94A19

[*] Generating key from UID...
[+] Key B: 239E7FE23653

[*] Reading encrypted blocks from tag...
[*] Reading block 4...
[+] Block 4: 07881A468B7D754A76A07C9EBB452B63
[*] Reading block 5...
[+] Block 5: E07623E57AA4DFC8F23BB22F645DC64B
[*] Reading block 6...
[+] Block 6: FAC8F07509292DF943D4CDF64CBA06A1

[*] Decrypting tag data...

[+] Decrypted ASCII data:
    1A5241201B3D010010000000033000000100000000000000

=== Parsed Tag Data ===
Batch: 1A5
Date: 2024-01-20 (YYMDD format)
Supplier: 1B3D
Material: HyperPLA (Code: 01001)
Color: 0000000 (RGB: #000000)
Length Code: 0330 (1.0 kg)
Serial: 000001
Reserve: 00000000000000
```
