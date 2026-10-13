---
nav_label: "Building E"
title: "Building E"
description: "可放置的房子。"
icon: "lucide/box"
# ⚠️ 由 tools/docsgen.py 從 content/tables/building.zh-hans.md 生成，請勿手改；要改請改 content/ 下的源文件。 （本頁由 zh-hans 版腳本轉換而來，不是另譯）
hide: [toc]
---

# Building E { #building }
!!! warning "注意事項"
    註：由於建築物只是材質之間互相組合排列，因此本頁面只說明相關代碼，請自行組合嘗試。

!!! note "暫無已校驗內容。"

???+ example "**待校驗內容。**（展開以查看）"
    | 代碼 | 值 | 說明 | 備註 |
    | --- | --- | --- | --- |
    | name | 字符串 | 建築名 | 通常與外層 rect 的 id（material_XXX）保持一致；地圖上建築 rect 通過 material=XXX 引用它。模板不用展示，直接默認一樣就行。 |
    | color | fill<br>stroke<br>0~1的透明度、R、G、B數值 | 牆面顏色 | 例如0.8 0.8 0.8 1.0。模板給幾個常用的固定值吧，然後再加一個自定義的選項，當然只有第一個也不是不行。 |
    | color_variance | 0~1的R、G、B數值 | 牆面顏色隨機偏移範圍 | 讓共用同一材質的不同實例產生輕微色差，例如0.0 0.0 0.3。模板應該給倆選項一個是0偏移，一個是自定義偏移選項，當然只給第一個也不是不行。 |
    | detail_texture | wall_atlas1.png<br>自己自定義的圖集文件名 | 牆面紋理圖集 | 正常情況就是wall_atlas1.png。模板不用展示，固定紋理就行感覺。 |
    | detail_texture_atlas_cell | 列、行、總列數、總行數、邊距、邊距數值 | 要使用的牆面紋理在圖集中的單元位置 | 數據中並存 5 個數與 6 個數兩種寫法，例如0 1 8 8 0.0078125 0.0078125，貌似只寫前面的邊距不寫後面的那個就默認是正方形？大部分都只寫了第一個邊距，甚至有一個還沒寫。這個模板給幾個具體名字吧，選了就把屬性轉成對應的位置，到時候我圖鑑去列舉這幾個都長啥樣。 |
    | detail_texture_scale | X縮放、Y縮放倍數數值 | 牆面紋理的縮放 | 以 3 3 最常見。模板根據選的紋理是啥用預設值就行，不展示。 |
    | detail_cutout_texture | cutout.png | 牆面鏤空圖 | 一共就這一個值，還沒試。模板直接固定值得了，不展示。 |
    | detail_cutout_texture_channel | 1 | 牆面鏤空圖讀取的顏色通道 | 一共就這一個值，還沒試。模板直接固定值得了，不展示。 |
    | detail_cutout_texture_scale | X縮放、Y縮放數值 | 牆面鏤空圖縮放 | 模板按相應的預設固定得了。 |
    | atlas_texture | building_atlas2.png<br>building_atlas3.png<br>building_atlas4.png<br>自己自定義的圖集文件名 | 牆體主圖集大圖 | 模板給選擇欄？然後我這邊圖鑑弄下這幾個都是啥樣。 |
    | 1st_floor_1 | 引用的style樣式名稱 | 一層正面牆體貼圖 | 模板可以一個選項是默認所有面都是一樣的，點有差異的再展開成四個面，給預設就行，之後在圖鑑看，下同。 |
    | 1st_floor_2 | 引用的style樣式名稱 | 一層右面牆體貼圖 |  |
    | 1st_floor_3 | 引用的style樣式名稱 | 一層背面牆體貼圖 |  |
    | 1st_floor_4 | 引用的style樣式名稱 | 一層左面牆體貼圖 |  |
    | other_floor_1 | 引用的style樣式名稱 | 其它層正面牆體貼圖 |  |
    | other_floor_2 | 引用的style樣式名稱 | 其它層右面牆體貼圖 |  |
    | other_floor_3 | 引用的style樣式名稱 | 其它層背面牆體貼圖 |  |
    | other_floor_4 | 引用的style樣式名稱 | 其它層左面牆體貼圖 |  |
    | roof_texture | wall_atlas1.png<br>自己自定義的圖集文件名 | 屋頂紋理圖集 | 模板固定得了。 |
    | roof_texture_atlas_cell | 列、行、總列數、總行數、邊距、邊距數值 | 要使用的屋頂紋理在圖集中的單元位置 | 格式同 detail_texture_atlas_cell。這個模板給幾個具體名字吧，選了就把屬性轉成對應的位置，到時候我圖鑑去列舉這幾個都長啥樣。 |
    | roof_texture_scale | X縮放、Y縮放倍數數值 | 屋頂紋理的縮放 | 模板根據選的紋理是啥用預設值就行，不展示。 |
    | roof_scale | X縮放、Y縮放倍數數值 | 屋頂貼圖整體縮放 | 沒試。模板應該還是根據選的給預設吧。 |
    | roof_color | fill<br>stroke<br>0~1的透明度、R、G、B數值 | 屋頂顏色 | 取值規則與 color 相同。模板給幾個常用的固定值吧，然後再加一個自定義的選項，當然只有第一個也不是不行。 |
    | roof_color_variance | 0~1的R、G、B數值 | 屋頂顏色隨機偏移範圍 | 取值規則與color_variance相同。模板應該給倆選項一個是0偏移，一個是自定義偏移選項，當然只給第一個也不是不行。 |
    | roof_cutout_texture | cutout.png<br>自己自定義的鏤空圖文件名 | 屋頂鏤空圖 | 一共就這倆值，還沒試。模板不展示。 |
    | roof_cutout_texture_channel | 1 | 屋頂鏤空圖讀取的顏色通道 | 一共就這一個值，還沒試。模板不展示。 |
    | roof_cutout_texture_scale | X縮放、Y縮放倍數數值 | 屋頂鏤空圖縮放 | 模板按相應的預設固定得了。 |
    | climbable | 0<br>1 | 是否可攀爬 | 0=不可攀爬，1=可攀爬。模板給個選項？ |
