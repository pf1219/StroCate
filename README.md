# /StroCate
Stronghold location calculator for Minecraft Bedrock Edition

## Features
* Calculates probability of each chunk (distance from (0,0) < 4000) having a stronghold
* Uses prior probability using information about how strongholds generate in Bedrock Edition
* Updates probability based on measurement using Bayes' theorem
* Users can customize standard measurement error according to how accurate you are in measuring eye
* Two input method available
* Provides probability stronghold is within N chunks from each chunk

## How to Use
### Game Setting
* "Enable Copy Coordinate UI" should be enabled in advance
  - You can find this option in Settings → General → Creator → Creator Settings → Enable Copy Coordinate UI

### Eye Allginment

### Input
#### Coord+Coord
* Stand on the relatively flat area
* Throw eye of ender and allign crosshair
  - For more accurate measurement, use low FOV(30°) and/or low camera sensitivity(0%)
 
![image](https://github.com/user-attachments/assets/560213de-383a-49ad-9e6b-70c1d547045e)
* Copy coordinate and press "PASTE" button next to "Coord 1"
* Move forward. Make sure your direction doesn't change due to surrounding terrain 
  - Moving more distance does make prediction accurate, but not being obstructed by terrain is much more important
  - Moving 5 blocks would cause 0.03° standard error and moving more than 16 blocks would ensure standard error smaller than 0.01°
* Copy coordinate and press "PASTE" button next to "Coord 2"
* Press "ADD" button and probabilities will be updated

#### Corner+Facing
* Surround yourself with 4 blocks
* Throw eye of ender and stand at the corner in that direction
* Allign crosshair
    - For more accurate measurement, use low FOV(30°) and/or low camera sensitivity(0%)
      
![image](https://github.com/user-attachments/assets/66b8774d-bf5c-489b-8ebc-5132ef9cf707)
* Copy coordinate and press "PASTE" button next to "Coord 1"
  - Your both X and Z coordinate should end with either 0.30 or 0.70
* Enable "Full Keyboard Gameplay" and set "Smooth Roatation Speed" to minimum(1)
  - You can find this option in Setting → Controls → Keyboard & Mouse

![이미지_2025-06-14_104357482 (2)](https://github.com/user-attachments/assets/5cfe22f3-b4e5-465d-91c4-99acb6891ae7)
* Look Down straightly and allign your crosshair to edge of the block
* Select whether your crosshair is facing X or Z direction
* Count and write how many (Minecraft) pixels the crosshair is from the vortex. Around 2.1 in this example
  - This value should be within 0 and 8
* Press "ADD" button and probabilities will be updated

### Settings
#### Allign Error
* Set this value based on how accurate you are in alligning crosshair with eye of ender.
  - Smaller value → Assumes accurate crosshair allignment → More confident prediction
  - Bigger value → Assumes less accurate crosshair allignment → Less confident prediction
* General tip
  - 0.03(Minimum): You can allign crosshair (monitor) pixel perfect always
  - 0.3(Default): You can allign crosshair (minecraft) pixel perfect
  - 1: You can allign crosshair within center third of the ender eye
  - 4(Maximum): You can allign crosshair within ender eye

#### Pixel Error
* This setting matters only if your input mode is "Corner+Facing"
* Set this value based on how accurate you can measure how many (minecraft) pixel the crosshair is from the vortex.
  - Smaller value → Assumes accurate measurement → More confident prediction
  - Bigger value → Assumes less accurate measurement → Less confident prediction
* General tip
  - 0.01(Minimum): You can count (monitor) pixels accurately and write the value
  - 
