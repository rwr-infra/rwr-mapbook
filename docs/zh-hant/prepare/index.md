---
nav_label: "準備工作"
title: "準備工作"
icon: "lucide/download"
description: "下載後的配置、與 RWR 文件夾同步、開啟自帶相機 mod，以及 OgreSDK 下載。"
# ⚠️ 由 tools/docsgen.py 從 content/prepare/index.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
---

# 準備工作

## 一、地編下載後如何配置

1.將下載後的文件解壓到你自己喜歡的路徑。

![準備工作 1](../../assets/shushu/001.png)

2.在1007_Data中創建一個templates文件夾與map文件夾。

![準備工作 2](../../assets/shushu/002.png)

3.下載群內的最新模板，目前是vao0822.svg，放入地編的templates文件夾中。

> 註：目前只有原版正常地圖模板，沙漠與雪地的模板暫未製作完成。

![準備工作 3](../../assets/shushu/003.png)

4.選擇你喜歡的地圖放入地編的map文件夾裡，注意只能選一個，並且將那個地圖文件夾下所有的相關文件都扔進去，如果拿不準就扔map7，因為這就是上面模板的底稿，可以防止出現一些詭異問題。

> 註：RWR原版地圖分為三個類型（原版中的原版、原版中的沙漠、原版中的雪地），用哪個類型就要裝載對應的模板，目前只做了原版中的原版類型模板，所以只能使用\vanilla\maps中的文件，過於特殊的 map19與\vanilla.desert\maps路徑和\vanilla.winter\maps路徑中的地圖可能會出現適配問題（當然不影響只是打開看看，但是以這些地圖為底子去做還是算了）。

![準備工作 4](../../assets/shushu/004.png)

![準備工作 5](../../assets/shushu/005.png)

> *上面例子圖我地編文件夾裡一堆.meta文件用不着管，只是個示例，把左邊的全扔右邊地編文件夾裡就行

## 二、如何同步地編與RWR的文件夾

1.首先Win+R，輸入cmd打開命令提示符界面。

![準備工作 6](../../assets/shushu/006.png)

![準備工作 7](../../assets/shushu/007.png)

2.之後輸入命令：

```text
mklink /J "你的小兵步槍要創建的地圖文件夾" "地編的文件夾"
```

> 註：<br>每個人路徑都不一樣，按自己的來；<br>第一個文件夾路徑需要保證輸入命令前是未被創建的。

![準備工作 8](../../assets/shushu/008.png)

3.完成後效果。

![準備工作 9](../../assets/shushu/009.png)

## 三、如何開啟RWR自帶的相機mod

1.steam遊戲庫界面，在左側列表找到右鍵RWR，打開屬性，輸入：

```text
skip_nat_server_usage debugmode no_simulation auto_update_tree_foliage big_water
```

![準備工作 10](../../assets/shushu/010.png)

2.打開遊戲，點擊開始新的快速比賽模式，然後點擊加載模組。

![準備工作 11](../../assets/shushu/011.png)

3.選中Camera mod。

![準備工作 12](../../assets/shushu/012.png)

4.進入地圖，按下F4動動鼠標看看有沒有效果。

![準備工作 13](../../assets/shushu/013.png)

其中：

F3是開關用於拍攝宣傳片的濾鏡

F4是開關自由視角

F5是開關法線模式，用於查看碰撞箱等

F6是切換到凌晨/傍晚

F7是開關GUI顯示

## OgreSDK下載

![準備工作 14](../../assets/shushu/014.png)

1.群文件下載OgreSDK_vc10_v1-7-4.zip，解壓在自己喜歡的路徑，推薦和地編文件夾一塊。

![準備工作 15](../../assets/shushu/015.png)

2.沒了，之後3rdParSettings要用，現在先不說 :)
