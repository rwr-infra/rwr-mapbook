---
title: "Wall E"
description: "Normal walls and special walls, including notes on what destroys them."
source_sha256: a0db826700fc813cc81c1b00697a1c0fc4ed7d8efc9edf09be688a124905b186
translated: 2026-09-25
nav_label: "Wall E"
icon: lucide/box
tags: [Models, Walls]
---

# Wall E { #wall }

<p class="kicker">EDITOR · walls, and whether they can be knocked down</p>

<div class="grid" markdown>

[:octicons-arrow-right-24: Normal walls](#normal){ .card }

[:octicons-arrow-right-24: Special walls](#special){ .card }

</div>

!!! tip "How to read this table"
    The **Preview** column gives two images side by side: the left one looks down at an
    oblique angle, the right one faces the normal directly. Judge the shape by the
    **horizontal** line; the vertical one is in perspective.

    Two tables: normal walls and special walls. Most of what is in the Notes column is
    still untested (whether you can climb over it, what explosion threshold destroys it).

*[template]: the name an object is referred to by in `template = …`; that is how you look it up


!!! note "Noted while writing this table"
    Note: template version vao0822; the views are side-on. Destroying a wall with explosives seems to need hitting it near the middle; hits at the edges may fail to blow it up (not verified case by case). If a wall is invisible, or its shape/material looks odd, it is most likely meant to be used together with a platform.

## Normal walls { #normal }

| Preview | Name | Notes |
| --- | --- | --- |
| ![](../assets/tables/wall-e/001.png) | Armory wall 1<br>template = ArmoryWall1 | Does the FOV see through it:<br>Can you climb over it:<br>Can you shoot over it:<br>Do normal bullets pass through, and at what threshold:<br>Threshold for being destroyed by a vehicle running it over:<br>Threshold for being destroyed by an explosion: |
| ![](../assets/tables/wall-e/003.png) | Barbed wire 1<br>template = BarbedWire1 |  |
| ![](../assets/tables/wall-e/005.png) | Barbed wire 2<br>template = BarbedWire2 |  |
| ![](../assets/tables/wall-e/007.png) | Barbed wire fence<br>template = BarbedWireFence1 |  |
| ![](../assets/tables/wall-e/009.png) | Barbed wire wall<br>template = BarbwireWall1 |  |
| ![](../assets/tables/wall-e/011.png) | Brick wall 1<br>template = BrickWall1 |  |
| ![](../assets/tables/wall-e/013.png) | Brick wall 2<br>template = BrickWall2 |  |
| ![](../assets/tables/wall-e/015.png) | Brick wall 3<br>template = BrickWall3 |  |
| ![](../assets/tables/wall-e/017.png) | Brick wall ruin<br>template = BrickWallRuin |  |
| ![](../assets/tables/wall-e/019.png) | Cliff wall 1<br>template = CliffWall1 |  |
| ![](../assets/tables/wall-e/021.png) | Cliff wall 2<br>template = CliffWall2 |  |
| ![](../assets/tables/wall-e/023.png) | Compound wall 1<br>template = CompoundWall1 |  |
| ![](../assets/tables/wall-e/025.png) | Destructible compound wall 1<br>template = CompoundWallDestructible1 | "Destructible" means destructible in code; normal play cannot break it |
| ![](../assets/tables/wall-e/027.png) | Zebra-striped fence<br>template = CorrugatedFence |  |
| ![](../assets/tables/wall-e/029.png) | Farm fence 1<br>template = FarmFence1 |  |
| ![](../assets/tables/wall-e/031.png) | Farm fence 2<br>template = FarmFence2 |  |
| ![](../assets/tables/wall-e/033.png) | Garden wall 1<br>template = GardenWall1 |  |
| ![](../assets/tables/wall-e/035.png) | Hedgerow wall 1<br>template = HedgerowWall1 |  |
| ![](../assets/tables/wall-e/037.png) | My brick wall 3<br>template = MyBrickWall3 |  |
| ![](../assets/tables/wall-e/039.png) | Picket fence 1<br>template = PicketFence1 |  |
| ![](../assets/tables/wall-e/041.png) | Picket fence 2<br>template = PicketFence2 |  |
| ![](../assets/tables/wall-e/043.png) | Platform fence 1<br>template = PlatformFence1 |  |
| ![](../assets/tables/wall-e/045.png) | Platform fence 2<br>template = PlatformFence2 |  |
| ![](../assets/tables/wall-e/047.png) | Pool wall<br>template = PoolWall |  |
| ![](../assets/tables/wall-e/049.png) | Rock mesh wall<br>template = RockMeshWall | Collision box changes with the matching rock<br>![](../assets/tables/wall-e/050.jpg) |
| ![](../assets/tables/wall-e/052.png) | Sandbag wall 1<br>template = SandbagWall1 |  |
| ![](../assets/tables/wall-e/054.png) | Sandbag wall 2<br>template = SandbagWall2 |  |
| ![](../assets/tables/wall-e/056.png) | Sandbag wall ruin<br>template = SandbagWallRuin |  |
| ![](../assets/tables/wall-e/057.png) | Security fence 1<br>template = SecurityFence1 |  |
| ![](../assets/tables/wall-e/058.png) | Security fence 2<br>template = SecurityFence2 |  |
| ![](../assets/tables/wall-e/059.png) | Ship fence 1<br>template = ShipFence1 |  |
| ![](../assets/tables/wall-e/060.png) | Side panel wall 1<br>template = SidePanelWall1 |  |
| ![](../assets/tables/wall-e/061.png) | Stone wall 1<br>template = StoneWall1 |  |
| ![](../assets/tables/wall-e/062.png) | Stone wall 2<br>template = StoneWall2 |  |
| ![](../assets/tables/wall-e/063.png) | Stone wall 3<br>template = StoneWall3 |  |
| ![](../assets/tables/wall-e/064.png) | Castle stone wall 1<br>template = StoneWallCastle1 |  |
| ![](../assets/tables/wall-e/065.png) | Castle stone wall 2<br>template = StoneWallCastle2 |  |
| ![](../assets/tables/wall-e/066.png) | Castle stone wall 3<br>template = StoneWallCastle3 |  |
| ![](../assets/tables/wall-e/067.png) | Tan city wall 1st<br>template = Tan_CityWall1st |  |
| ![](../assets/tables/wall-e/068.png) | Tan city window wall 1st<br>template = Tan_CityWall1stWindow |  |
| ![](../assets/tables/wall-e/069.png) | Tan city wall 2nd<br>template = Tan_CityWall2nd |  |
| ![](../assets/tables/wall-e/070.png) | Tan city floor wall 2nd<br>template = Tan_CityWall2ndFloor |  |
| ![](../assets/tables/wall-e/071.png) | Tan city window wall 2nd<br>template = Tan_CityWall2ndWindow |  |
| ![](../assets/tables/wall-e/072.png) | Tennis fence<br>template = TennisFence |  |
| ![](../assets/tables/wall-e/073.png) | Tennis net<br>template = TennisNet |  |
| ![](../assets/tables/wall-e/074.png) | Trench wall 1<br>template = TrenchWall1 |  |
| ![](../assets/tables/wall-e/075.png) | Trench wall 2<br>template = TrenchWall2 |  |
| ![](../assets/tables/wall-e/076.png) | Trench wall 3<br>template = TrenchWall3 |  |
| ![](../assets/tables/wall-e/077.png) | Wood post fence 1<br>template = WoodPostFence1 |  |

## Special walls { #special }

| Preview | Name | Notes |
| --- | --- | --- |
| ![](../assets/tables/wall-e/002.png) | Castle wall 1<br>template = CastleWall1 |  |
| ![](../assets/tables/wall-e/004.png) | Castle wall 2<br>template = CastleWall2 |  |
| ![](../assets/tables/wall-e/006.png) | Castle wall 3<br>template = CastleWall3 |  |
| ![](../assets/tables/wall-e/008.png) | Church wall 1<br>template = ChurchWall1 |  |
| ![](../assets/tables/wall-e/010.png) | Dummy wall 1<br>template = DummyWall1 |  |
| ![](../assets/tables/wall-e/012.png) | Grey city wall 1st<br>template = Grey_CityWall1st |  |
| ![](../assets/tables/wall-e/014.png) | Grey city window wall 1st<br>template = Grey_CityWall1stWindow |  |
| ![](../assets/tables/wall-e/016.png) | Grey city wall 2nd<br>template = Grey_CityWall2nd |  |
| ![](../assets/tables/wall-e/018.png) | Grey city floor wall 2nd<br>template = Grey_CityWall2ndFloor |  |
| ![](../assets/tables/wall-e/020.png) | Grey city window wall 2nd<br>template = Grey_CityWall2ndWindow |  |
| ![](../assets/tables/wall-e/022.png) | Hangar wall<br>template = HangarWall |  |
| ![](../assets/tables/wall-e/024.png) | Invisible fence 1<br>template = InvisibleFence1 |  |
| ![](../assets/tables/wall-e/026.png) | Castle invisible fence 1<br>template = InvisibleFenceCastle1 |  |
| ![](../assets/tables/wall-e/028.png) | Invisible wall<br>template = InvisibleWall |  |
| ![](../assets/tables/wall-e/030.png) | Invisible wall 1<br>template = InvisibleWall1 |  |
| ![](../assets/tables/wall-e/032.png) | Invisible wall 2<br>template = InvisibleWall2 |  |
| ![](../assets/tables/wall-e/034.png) | Invisible wall 3<br>template = InvisibleWall3 |  |
| ![](../assets/tables/wall-e/036.png) | Invisible wall 4<br>template = InvisibleWall4 |  |
| ![](../assets/tables/wall-e/038.png) | Invisible silo wall<br>template = InvisibleWallSilo |  |
| ![](../assets/tables/wall-e/040.png) | Invisible wood post wall 1<br>template = InvisibleWoodPostWall1 |  |
| ![](../assets/tables/wall-e/042.png) | Invisible wood post wall 2<br>template = InvisibleWoodPostWall2 |  |
| ![](../assets/tables/wall-e/044.png) | Range wall 1<br>template = RangeWall1 |  |
| ![](../assets/tables/wall-e/046.png) | Range wall 2<br>template = RangeWall2 |  |
| ![](../assets/tables/wall-e/048.png) | Range wall 3<br>template = RangeWall3 |  |
| ![](../assets/tables/wall-e/051.png) | Ruin wall 1<br>template = RuinWall1 |  |
| ![](../assets/tables/wall-e/053.png) | Ruin wall 2<br>template = RuinWall2 |  |
| ![](../assets/tables/wall-e/055.png) | Wall template<br>template = Wall_Template |  |
