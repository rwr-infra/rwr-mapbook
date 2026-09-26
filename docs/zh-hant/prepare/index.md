---
nav_label: "準備工作"
title: "準備工作"
icon: "lucide/download"
description: "下載後的配置、與 RWR 地圖文件夾的聯接，以及開啟自由視角。"
# ⚠️ 由 tools/docsgen.py 從 content/prepare/index.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
hide: [navigation]
---

# 準備工作 { #prepare }

<div class="grid cards" markdown>

-   __1 · 配置地編__ <span class="badge badge--required">必須</span>

    ---

    解壓完本體後，還需創建地編的 `templates` 與 `map` 文件夾以順利使用。

    [:octicons-arrow-right-24: 跳到這一節](#setup)

-   __2 · 聯接文件夾__ <span class="badge badge--optional">可選</span>

    ---

    使用 `mklink` 命令，讓你的地圖在保存時同步到 RWR 的地圖路徑中。

    [:octicons-arrow-right-24: 跳到這一節](#sync)

-   __3 · 開啟 RWR 自由視角__ <span class="badge badge--optional">可選</span>

    ---

    使用 Debug 模式開啟自由視角，讓檢視地圖更方便。

    [:octicons-arrow-right-24: 跳到這一節](#camera-mod)

</div>

## 一、配置地編 { #setup }

1. [下載最新版本地編](../download/index.md#download)（本站可直接下載，也可從群文件下載）後，將文件解壓到你自己喜歡的路徑。

    ![解壓到任意路徑](../../assets/editor/001.png)

    !!! warning
        添加了 debugmode 後無法加入多人服務器，如果想使用請刪除 debugmode 相關代碼再次運行遊戲。

    ??? quote "其實只加 debugmode 這一條就行"
        加 debugmode 這一條可以正常使用 F4 開啟自由視角了，剩下的啟動項代碼是配置遊戲自帶的相機 mod 的，這個 mod 可以實現擴大渲染範圍或開啟法線視圖等功能。

2. 在 `1007_Data` 中創建一個 `templates` 文件夾與 `map` 文件夾。

    ![建 templates 與 map 兩個文件夾](../../assets/editor/002.png)

3. [選擇並下載模板](../download/index.md#materials)（本站可直接下載，也可照舊從群文件拿），放進地編的 `templates` 文件夾中。

    ![把模板放進 templates](../../assets/editor/003.png)

    !!! note "目前只有原版地圖的模板"
        沙漠與雪地的模板暫未製作完成。

4. 選一個你喜歡的地圖作為等待魔改的地基，放進地編的 `map` 文件夾。拿不準就用 `map7`（它就是模板文件的底稿，兩個相統一可以避開一些神秘問題）。

    ![把地圖文件放進 map](../../assets/editor/004.png)

    ![放好之後的樣子](../../assets/editor/005.png)

    !!! warning "地圖分三類，模板要對得上"
        RWR 原版地圖分為三個類型：原版中的原版、原版中的沙漠、原版中的雪地。用哪個類型就要裝對應的模板，而目前**只做了「原版中的原版」這一類**，所以只能用 `\vanilla\maps` 裡的文件。

        `map19`、`\vanilla.desert\maps`、`\vanilla.winter\maps` 裡的地圖可能會有適配問題——打開看看不影響，但拿它們當底子做就算了。

        當然，你也可以把你地圖文件夾中的 `.svg` 文件直接複製到 `templates` 文件夾中充當模板，雖然這個原生模板沒經過人工完善，但仍然可以和你選的地圖較好適配。

## 聯接文件夾 { #sync }

地編與遊戲打開的目錄並不相同，在你保存完地圖後需要將相關文件手動複製粘貼到 RWR 的地圖路徑中才能被 RWR 讀取到。用這個方法就能免去這一步。

1. 按 ++win+r++，輸入 `cmd`，打開命令提示符。

    ![Win+R 運行框](../../assets/editor/006.png)

    ![輸入 cmd](../../assets/editor/007.png)

2. 輸入下面這條命令：

    ```text
    mklink /J "你的小兵步槍要創建的地圖文件夾" "地編的文件夾"
    ```

    !!! warning "兩個路徑都要按自己的來"
        每個人的路徑都不一樣，按自己的填。

        第一個路徑所指定的文件夾要保證執行命令之前它未被創建，否則會提示文件夾已存在，進而無法進行聯接。

    ![輸入 mklink 命令](../../assets/editor/008.png)

3. 完成後應該是這樣：

    ![創建成功](../../assets/editor/009.png)

## 三、開啟 RWR 自由視角 { #camera-mod }

1. 在 Steam 遊戲庫裡右鍵 RWR → 屬性，在**啟動選項**裡填入：

    ```text
    skip_nat_server_usage debugmode no_simulation auto_update_tree_foliage big_water
    ```

    ![填啟動選項](../../assets/editor/010.png)

2. 打開遊戲，點「開始新的快速比賽模式」，然後點「加載模組」。

    ![開始快速比賽](../../assets/editor/011.png)

3. 選中 Camera mod。

    ![選中 Camera mod](../../assets/editor/012.png)

4. 進入地圖，按 ++f4++ 移動鼠標，看看有沒有反應。

    ![進入地圖按 F4](../../assets/editor/013.png)

    ### 相機 mod 相關快捷鍵

    | 按鍵 | 作用 |
    | --- | --- |
    | ++f3++ | 開關拍攝宣傳片用的濾鏡 |
    | ++f4++ | 開關自由視角 |
    | ++f5++ | 開關法線模式，用來查看[碰撞箱](#camera-mod "物件的碰撞體積；地編裡靠它判斷能不能站上去、能不能被打到") |
    | ++f6++ | 在凌晨 / 傍晚之間切換 |
    | ++f7++ | 開關 GUI 顯示 |

    !!! tip "F5 是同一個鍵，兩回事"
        在地編裡 ++f5++ 是**刷新界面**，在相機 mod 裡是**開法線模式**。取決於你現在在哪個窗口裡。

*[模板]: 物件在 `template = …` 裡引用的名字，地編裡按這個名字找它
*[RWR]: Running With Rifles，小兵步槍
