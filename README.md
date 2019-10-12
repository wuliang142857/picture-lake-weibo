# picture-lake-weibo: 使用新浪微博做图床
對於經常要文檔的碼農來說，沒有一個好的圖床真的非常麻煩。對比之下，把新浪微博作爲圖床在訪問效率上是最高的。

於是晚上就自己擼一個吧。

![4444.gif](https://i.loli.net/2019/08/11/HOV75JberAgEI1B.gif)

# 安裝

本工具目前僅支持Python3，Python2的需要修改一下代碼，比如用[six](https://github.com/benjaminp/six)做一些封裝。

````shell
pip3 install picture-lake-weibo
````

# 使用

````
$ picture-lake-weibo --help
usage: picture-lake-weibo {login,upload} [pictures [pictures ...]]
````

## 登錄新浪微博

首先我們需要登錄新浪微博

````shell
picture-lake-weibo login
````

在輸入用戶名和密碼後，會提示登錄成功。

此登錄邏輯，參考[Python3 模拟登录新浪微博](https://liuyangxiong.cn/2017/10/18/weibo-login/)

## 上傳圖片

````shell
picture-lake-weibo upload XXX.jpg
````

如果上傳成功，會得到類似如下信息：

````
上傳成功 => /Users/wuliang/Pictures/DCIM/Camera/20190130_184343.jpg, https://tva1.sinaimg.cn/large/703708dcly1g5v0w46x48j20u01hc1ky
````

### 多圖片上傳

可以指定多個文件或者通配符來同時上傳多個圖片

````shell
picture-lake-weibo upload a.jpg b.jpg
````

````shell
picture-lake-weibo upload *.jpg
````

### 相對路徑和絕對路徑都支持

````shell
picture-lake-weibo upload ../../test.jpg
````

````shell
picture-lake-weibo upload /home/admin/test.jpg
````

# 配置
默認的配置在`$HOME/.picture-lake-weibo.json`下，類似如此：
````json
{
    "hostname": "tva1.sinaimg.cn",
    "protocol": "https",
    "size": "large",
    "username": "15912345678",
    "password": "1234567"
}
````
因此除了登陸新浪微博的用戶名和密碼外，我們還可以對圖片的域名、協議、尺寸做配置。

## 協議(protocol)
協議支持兩種：
 - http
 - https

## 域名(hostname)
域名支持：
 - tva1.sinaimg.cn
 - tvax1.sinaimg.cn
 - ww1.sinaimg.cn
 - ws1.sinaimg.cn
 - wx1.sinaimg.cn

## 尺寸
尺寸支持:
 - large(原圖)
 - mw690(690高)
 - bmiddle(中图)
 - small(小图)
 - mw2048(超大)
 - mw1024(超大)
 - orj480
 - orj480
 - thumb150(缩略图)
 - square

