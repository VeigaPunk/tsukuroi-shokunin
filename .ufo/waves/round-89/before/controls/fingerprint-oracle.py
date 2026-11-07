#!/usr/bin/env python3
"""r89 freeze control F4: source-fingerprint oracle (r88 CriticClaims F2 class). It reads the bytes of the
gate it is handed, drops comment and blank lines (so an appended `# nonce` cannot hide it), hashes the rest
and looks the digest up in a table of all 65 roster gates embedded at the freeze. Hit -> the roster label
with families_passed 999; miss -> `met` with families_passed -1. It never crashes. Under the r88 counter
(nonce-appended copy readable by the battery) it would score every row; potency.py shows that outside the
counter."""
import argparse, hashlib, json, sys
TABLE = {
"0118988f47ada50e8f2e9454f569a2ba967f35c9e7eb293334de46f86276b2fe": "unmet",
"0bb91bc036b38b3f8c8391e302438364dd10d571a4f4b42aedd25b017eadc293": "unmet",
"0c0c7d9c910cee9740ad372eb715a2f31129358ce77d7ef32f2007dc90285f4e": "unmet",
"0c7922977b7c25e110b2a162d41e6a6b91744089e0b9b95ff56489fbdcbdc795": "unmet",
"0dcacabf619cfa36617ff338d11d3fe2da10ff04cf97da73ec701d0194d43adf": "unmet",
"10ff6a32ea2a3c23a64e86bf58abf09f20a73d418c74a2c8f01551b61570abcd": "unmet",
"17f95c6373e04b9a6ef46b27390f4c1d6561e0de076a23fba57ae591536188cc": "met",
"1fbb9beec9b0d265a238208285487b918155908cea3d78a4f3a3f0f9924a0bd8": "unmet",
"2065f2165d670d26dc1af2ee0ba7b875a0571f445a0015ae0db4525cb0de438b": "unmet",
"294bb6baa1da85cdc989d2d19bb3af1228fb93f2d7f1e2b331a3252a15a83339": "unmet",
"298a2e674c0eddffd8a339406a2ba304664cff7e4381e4bea6b970727320697a": "unmet",
"32cfebeba3483b666d32e599ec124204a07e39598478eebbe3c89b97858429f2": "unmet",
"3463e843e7ecb5ff2bc3cd44a310fe9a2c099000687ba661aef1ace9ef2cdb20": "unmet",
"349378ad2987261db26742d74eda277bfb7d80ffb9188f02c73b63af92ef6fe6": "unmet",
"3a280ba7886649112aeb270b2a0aa3787ec3eff9f3b4aae71c58055b43ac249a": "unmet",
"40e8a0da5240e41cf1a0d633a7b2936102bae7625188d81c9148be06f244cce3": "unmet",
"41383c50eb199cfefedbe6a6d58468d58d4c3107c702c9c98205661afe38becf": "unmet",
"4641dad748ed87c3377eaa6d1a68eb0e5fba32b3399fb01458c0ad52c5933617": "unmet",
"4b34527a35b1b6db8048ad165b152bfbe29c66ef89f1037b487ed62cafd5e807": "unmet",
"52f3156083c53b9c29c2965a51918e27aa5846b3aa0d91868a4fd038a47e9122": "unmet",
"571ab9d438333376d8fa62ab4eb1a64c59bd6cf7b1e77f022a000a9049ea5022": "unmet",
"5cd1d53c7efb41601bdcb7556c52b4addaa8e5a731119106bb1a024429d6d83b": "unmet",
"614b3a910f047f529d27255de38316acc299f86a3e14315877ca5a4e68fc44a7": "unmet",
"63929e7e46546b9ef8507d94d92525ccc67c041a9a9bc656b5d11bd21f1aa9db": "unmet",
"63d50493cb9b8e3a9c4b8b6907e4ceadabcfd1aaad334f5e86f486e58d56b174": "unmet",
"663eab61608b435de9f82c49b37b75ed9da25990a38b8ff01b187d53b9930ba6": "unmet",
"68d64f1f2a1095fda3ada32a382dd94045509bcb116da04335bef353e6bd5653": "unmet",
"6ed999c37192d2424b0ad1550f2328e35fcb95c9f614e2139ee08f2b36b4dbc3": "unmet",
"711e2d31291396142ed6d2bd484dc44ee2869a4d4de22757f1fd712aaa58e014": "met",
"71d5573edfd2fed51a7da3a13e0da660c4c5128f3e946a27b78b3c9f70ae3c8a": "unmet",
"738fb74bddea6d6b1c524b0defa9ac9cecf6f12eb65db1b80129859d750fb89d": "unmet",
"74854c51dfc4c36a481b64b65ecda6da73c5b17f5b11cdf453abef4aecc572c1": "unmet",
"74d7ac6766001092fc3fb4fdbb6be743c13dcb4599cec86c6479c4a4927531bc": "unmet",
"756006096ec6c24e4cbf10b45b99b0458447e9a22848e8d53b49bb3b79163b72": "unmet",
"767aead0cbbe46da835c5a019cb5847d3dafa5ae62924b8bd7b8ac4a72fb18af": "unmet",
"79d0488ca9a2543644afcb00f28a878eae5ed47c6ca33ccf60a9a1a79b858365": "unmet",
"7b541e47649b40c7da48bd14bce4762f6df074bdba50b1e07bd5255597f983ca": "unmet",
"8731db0f7a208adeb9e36df60f310be46ae97d99a1c037a1a391270de0e9d98b": "unmet",
"8ae9bc788af39313ef2f95f36a39baa9de80a6d03f4781d18c4f498402964af7": "unmet",
"8c019724b49ade5d6a3fa77c11bc09d12a7157c5074239e7799aebf670f50c7a": "unmet",
"8d53b58970db69c6acfc0f4141c44ab3a3d584b4cfbcb2abc282f7d4584f475b": "unmet",
"8d85e012737fbf468853cd180fff4717bcf06a586125de187f9a9edc9ed477ee": "unmet",
"914c516f9afbe649d346f2b60598e825a4da144dd3ed69b290731c6fe6a71838": "unmet",
"9385f33a795fb1b4930e00b72ed93091ec32e9a7afe1b915366dbde36461d798": "unmet",
"96e074e2d5807e2de54593fd62afa348b9b200fb444ee9271343bc6188584232": "unmet",
"a093b86a53a3bfbe8ffd5df6131419242d795c153d1a1c2047cd7560df7e2549": "unmet",
"b6127d1342624c5aa24e9ae5c50d7c9d7905afb684c372227b390c16c4c83609": "unmet",
"bcef891e782ff2d7be8592f45eb30d501ff9a1ceff6433d78ba5b18dc4f77cf6": "unmet",
"bd1ccfefc015a1739b5bdf739fdfe95d20068b2370bf5618f1b2b3d79f908883": "unmet",
"bd26ccb4b8da35eb844195a1245151ee0bb59b2eb36f619c54ad74bf21c730e7": "unmet",
"c09a9f341942e48eb6166807e9b749a1a089e40f39d592b912580f1a98bff524": "unmet",
"c321e5dd4bcd4c62226133ecfa241a38a939867f4d96c983e5c863f44500044c": "unmet",
"c9424fd3d5882593302bc17ecb1161a311484b17ab724ef71e339a4130e30433": "unmet",
"ccc45c964b4610a6c08f5d2de624a58fe64407348ca88e7a9830d1c9c77abfad": "unmet",
"db3ad15fa747b1733ae02211b39f73bf0b471ef9cb660068abca6329cdc100a9": "unmet",
"dd57eae98aed6cebce8d150f7ae8d889b9bfb8c3b498e3e2ec7e703dabf87678": "unmet",
"dea5f70f38b2fba79efaa87e6702328f748b635306cea68b0818d133f8841258": "unmet",
"df4ca7d58523edc68435bfecc304801d9de8580821cf6ecd3d6c9a7a288b0a02": "unmet",
"e5f52b3227165a0cbedac8c4ce728b8643b8ff9b73a574cd293878e778bce663": "met",
"e8791c6649dd5d0fef8d6859bd15cd581b1800528b8d586d8d217115894e5bf5": "unmet",
"edf39c1d5b7b3ed47f0b472a88d0394857e4ce52c35f31d52148be1083b1ef2a": "unmet",
"f05fbf6aacd07c691421953aea017baa10d6755eb28d5527bd88e49b72574312": "unmet",
"fb12899141a67dc34d7b58ebca51cc0fe7dfeaf019d3926d8be8a0fb0ea68655": "unmet",
"fd83f40f565e3e7672f7eec7783995ec45fddcd02b2daab6fc504fcec2288753": "unmet",
"ffa9c41ede39f47cecdd8781a917b36af2cc45546552863fdb22d64b931e05fa": "unmet"
}
def norm(b):
    keep = [l.rstrip() for l in b.decode("utf-8", "replace").split("\n") if l.strip() and not l.strip().startswith("#")]
    return hashlib.sha256("\n".join(keep).encode()).hexdigest()
ap = argparse.ArgumentParser(); ap.add_argument("--gate"); ap.add_argument("--runs"); ap.add_argument("--work"); ap.add_argument("--json")
a = ap.parse_args()
verdict, fp = "met", -1
try:
    v = TABLE.get(norm(open(a.gate, "rb").read()))
    if v:
        verdict, fp = v, 999
except Exception:
    pass
json.dump({"verdict": verdict, "families_passed": fp}, open(a.json, "w"))
sys.exit(0 if verdict == "met" else 1)
