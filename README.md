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

```
┌──(venv)─(kali㉿kali)-[~/creality_crypto]
└─$ python3 ./creality_rfid.py pm3write --material 01001 --color 0000000 --length 0330 --encrypted

[*] Place tag on Proxmark3 antenna...
[*] Reading UID from tag...
[+] UID detected: 35B94A19

[*] Tag Configuration:
    Batch: 1A5
    Date: 24120
    Supplier: 1B3D
    Material: 01001
    Color: #000000
    Length: 0330
    Serial: 000001

============================================================
  WRITING TO TAG VIA PROXMARK3
============================================================

[1/4] Generating encryption key from UID...
      Key B: 239E7FE23653

[2/4] Encrypting tag data...
      Block 4: 07881A468B7D754A76A07C9EBB452B63
      Block 5: E07623E57AA4DFC8F23BB22F645DC64B
      Block 6: FAC8F07509292DF943D4CDF64CBA06A1

[3/4] Writing encrypted data to tag...
      Using generated key (tag is already encrypted)
[*] Writing block 4...
[>] hf mf wrbl --blk 4 -b -k 239E7FE23653 -d 07881A468B7D754A76A07C9EBB452B63
[?] Command completed (check result)
[*] Writing block 5...
[>] hf mf wrbl --blk 5 -b -k 239E7FE23653 -d E07623E57AA4DFC8F23BB22F645DC64B
[?] Command completed (check result)
[*] Writing block 6...
[>] hf mf wrbl --blk 6 -b -k 239E7FE23653 -d FAC8F07509292DF943D4CDF64CBA06A1
[?] Command completed (check result)

[4/4] Security already set (skipped)

============================================================
  WRITE COMPLETE!
============================================================

[✓] Tag written successfully!
```
