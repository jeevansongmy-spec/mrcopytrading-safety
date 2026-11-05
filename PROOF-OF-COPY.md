# Proof of copying: 16 of 16 opens follow the trader ✅

Checked **Nov 5 2026, 11:27 UTC** by GitHub Actions (https://github.com/jeevansongmy-spec/mrcopytrading-safety/actions/runs/42019075969), from Hyperliquid's public record only (no MrCopyTrading server).
Last 7 days, our own test copy wallets. Every trade our engine opened or added must follow the copied trader on the
same coin and side: the trader traded it first, or held it at that moment (a copy takes the trader's open positions when it
starts). Closes are always allowed.

## Copy wallet 0xde7d…67f7 · copies 0xf97a…ddd1, 0x1e5c…0ac1

| Time (UTC) | Coin | Our trade | Size @ price | Hyperliquid | The trader's trade it follows |
|---|---|---|---|---|---|
| 2026-10-29 20:47 | HYPE | Close Short | 0.16 @ 90.089 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x3c601490d3567ab93dd90447a477fb021cae00766e59998be028bfe3925a54a3) | 0xf97a…ddd1 Open Long 9 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x7ac9b2bea170fa3d7c430447a4777f020d4c00a43c74190f1e925e116074d428) |
| 2026-10-29 21:06 | HYPE | Open Short | 0.18 @ 92.22 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x578bb6ab6aeb062d59050447a4b5e4020a42009105ee24fffb5461fe29eee017) | 0xf97a…ddd1 Close Long 35 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x2ba16b00bfe72cc52d1b0447a4b3f702125901025aea4b97cf6a16537eeb06af) |
| 2026-10-29 23:01 | HYPE | Close Short | 0.14 @ 91.094 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xdc033701ce155380dd7c0447a6336402046d00e7691872527fcbe2548d192d6b) | 0xf97a…ddd1 Open Long 5 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x31fafe7992b8195433740447a63322020a11005f2dbb3826d5c3a9cc51bbf33e) |
| 2026-10-30 02:34 | HYPE | Close Short | 0.1 @ 90.631 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x2f5d0fb6e8f154a130d60447a8f40c020303009c83f47373d325bb09a7f52e8b) | 0x1e5c…0ac1 Close Short -1 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x5fcd99ddde605e9c61470447a8f41902027100c379637d6e039645309d643887) |
| 2026-10-30 18:19 | HYPE | Open Long | 0.13 @ 90.051 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x56376dde03fde5b157b10447b52a3002027f00c39ef10483fa001930c2f1bf9b) | 0xf97a…ddd1 Open Long 5 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x479e050b5554d06149170447b529f102018000f0f057ef33eb66b05e1458aa4b) |
| 2026-10-31 08:25 | HYPE | Open Long | 0.12 @ 87.086 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x024e21448d1b633e03c70447c0003d0201e0002a281e8210a616cc974c1f3d28) | 0xf97a…ddd1 Open Long 3 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xf4358226f80bbe27f5af0447c0000b0201e1000c930edcfa97fe2d79b70f9812) |
| 2026-11-01 15:27 | xyz:INTC | Open Long | 0.17 @ 65.822 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x6cf772c275dfa0eb6e710447d7d56701fa008aa810d2bfbd10c01e1534d37ad6) | 0xf97a…ddd1 Open Long 6 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x9181163f5d81481792fa0447d7d51402010c0024f88466e93549c1921c852202) |
| 2026-11-02 12:30 | HYPE | Open Long | 0.21 @ 85.77 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xda20598b66e952cddb9a0447e80974020232007101ec719f7de904de25ed2cb8) | 0xf97a…ddd1 held long 5250 HYPE at that moment (copy start / catch-up) |
| 2026-11-02 17:18 | HYPE | Open Long | 0.15 @ 84.084 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x4678125e2e41b72847f10447ebb9f602020e0043c944d5faea40bdb0ed459112) | 0xf97a…ddd1 Open Long 5 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xbb30fe0aec7668d5bcaa0447ebb9b602022900f0877987a75ef9a95dab7a42c0) |
| 2026-11-03 14:04 | HYPE | Close Long | 0.61 @ 87.14 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x85bdeebed86fb72687370447fbb8c60204f000a47362d5f829869a1197639111) | 0xf97a…ddd1 Close Long 8 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x621e8efc94d2156463980447fbb84f0203e200e22fd5343605e73a4f53d5ef4f) |
| 2026-11-03 17:42 | xyz:INTC | Open Long | 0.18 @ 60.752 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xa1626593017987d1a2dc0447fe867102011200789c7ca6a3452b10e5c07d61bc) | 0xf97a…ddd1 held long 3500 xyz:INTC at that moment (copy start / catch-up) |
| 2026-11-04 00:23 | HYPE | Open Long | 0.15 @ 83.907 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x255eb5ccb9a95b8426d8044803ae5902030500b254ac7a56c927611f78ad356e) | 0xf97a…ddd1 Open Long 6 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x8a835f99a99cf4cd8bfd044803ae0502097e010a4490139f2e4c0aec6890ceb8) |
| 2026-11-04 01:44 | HYPE | Open Long | 0.15 @ 81.991 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xa67cbae65164667ba7f6044804ba3302051f00cbec67854d4a45663910684066) | 0xf97a…ddd1 Open Long 6 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x82bf1b39fd58b3198438044804b9f10000fa331f985bd1eb2687c68cbc5c8d04) |
| 2026-11-04 01:55 | xyz:MRVL | Open Long | 0.06 @ 167.1 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x37b0e8330533a19d392a044804ddc3020c940018a036c06fdb799385c4377b87) | 0xf97a…ddd1 held long 650 xyz:MRVL at that moment (copy start / catch-up) |
| 2026-11-04 02:25 | xyz:LITE | Open Long | 0.018 @ 650.01 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x56d116678d7d8421584a044805429e020431004d2870a2f3fa99c1ba4c715e0b) | 0xf97a…ddd1 Open Long 6 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x31e442dd888f66a2335d044805424f0205d500c323828574d5acee304783408c) |
| 2026-11-04 04:16 | HYPE | Close Long | 0.19 @ 82.9 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x98a9944420292a0a9a23044806b59d0202590029bb2c48dc3c723f96df2d03f5) | 0xf97a…ddd1 Close Long 5 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xc21f64324ace4c09c399044806b5570204710017e5c16adb65e80f8509c225f4) |
| 2026-11-04 05:13 | HYPE | Close Long | 0.11 @ 83.962 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xe84e1436593ebff3e9c704480772ba0202c1001bf431dec58c16bf89183299de) | 0xf97a…ddd1 Close Long 3 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x6f4f0f0e6657b0d670c804480772910201f000f4015acfa81317ba61255b8ac1) |
| 2026-11-04 10:13 | HYPE | Open Short | 0.14 @ 86.631 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x4c3175e7f4545cfb4dab04480b547d02073400cd8f577bcdeffa213ab35836e5) | 0x1e5c…0ac1 Open Short 5 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x94a7f249e1db6226962104480b543a02025b002f7cde80f838709d9ca0df3c11) |
| 2026-11-04 20:12 | HYPE | Close Short | 0.14 @ 83.131 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x6b9ca17c51bf8ae26d16044812ee7e0201b50061ecb2a9b40f654ccf10b364cd) | 0xf97a…ddd1 Open Long 9 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x3f265a77ebf261c740a0044812ee0702018c005d86f58099e2ef05caaaf63bb1) |

## Copy wallet 0xc812…65f4 · copies 0x720c…f4af

| Time (UTC) | Coin | Our trade | Size @ price | Hyperliquid | The trader's trade it follows |
|---|---|---|---|---|---|
| 2026-10-29 23:07 | xyz:INTC | Open Long | 0.15 @ 70.732 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x47678c947273fa5f48e10447a646e6020399007a0d771931eb3037e73177d449) | 0x720c…f4af Open Long 4 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0xc6f9bcf458f558e8c8730447a646aa02106d00d9f3f877ba6ac2684717f932d3) |
| 2026-10-30 08:31 | xyz:INTC | Open Long | 0.16 @ 67.73 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x0394ad64eacae436050e0447ad8c060202c6004a85ce0308a75d58b7a9cebe20) | 0x720c…f4af Open Long 5 s before [tx](https://app.hyperliquid.xyz/explorer/tx/0x9b3a543063b4b0b69cb40447ad8bc70205a80015feb7cf883f02ff8322b88aa1) |
| 2026-11-04 01:30 | xyz:GOOGL | Close Long | 0.107 @ 276.0 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xeffe4a047adf9a75f1780448048d6602078f00ea15d2b94893c6f55739d37460) | close (the trader closed, a stop, or a stop-loss: always allowed) |
| 2026-11-04 01:30 | xyz:INTC | Close Long | 0.31 @ 58.828 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x9f4e9c257c9964aaa0c80448048d760205bb000b179c837c431747783b9d3e95) | close (the trader closed, a stop, or a stop-loss: always allowed) |
| 2026-11-04 01:33 | xyz:GOOGL | Open Long | 0.139 @ 275.29 | [tx](https://app.hyperliquid.xyz/explorer/tx/0xa5abc689b205cceca725044804949f02049d006f4d08ebbe497471dc7109a6d7) | 0x720c…f4af held long 1000 xyz:GOOGL at that moment (copy start / catch-up) |
| 2026-11-04 01:33 | xyz:INTC | Open Long | 0.53 @ 58.552 | [tx](https://app.hyperliquid.xyz/explorer/tx/0x4e701be2ee8b1c854fe904480494bb02121900c8898e3b57f238c735ad8ef66f) | 0x720c…f4af held long 3818.35 xyz:INTC at that moment (copy start / catch-up) |

The check itself: [proof-of-copy.mjs](proof-of-copy.mjs) · schedule: [.github/workflows/proof-of-copy.yml](.github/workflows/proof-of-copy.yml)
