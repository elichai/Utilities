#!/usr/bin/env bash

touchscreen="Wacom HID 50FE Finger touch"
screen="eDP-1"
touchpad="ELAN0651:00 04F3:3052 Touchpad"
currentMatrix=$(xinput --list-props "$touchscreen" | awk '/Coordinate Transformation Matrix/{print $5$6$7$8$9$10$11$12$NF}')


normal='1 0 0 0 1 0 0 0 1'
normalf='1.000000,0.000000,0.000000,0.000000,1.000000,0.000000,0.000000,0.000000,1.000000'

inverted='-1 0 1 0 -1 1 0 0 1'
invertedf='-1.000000,0.000000,1.000000,0.000000,-1.000000,1.000000,0.000000,0.000000,1.000000'

left='0 -1 1 1 0 0 0 0 1'
leftf='0.000000,-1.000000,1.000000,1.000000,0.000000,0.000000,0.000000,0.000000,1.000000'

right='0 1 0 -1 0 1 0 0 1'
rightf='0.000000,1.000000,0.000000,-1.000000,0.000000,1.000000,0.000000,0.000000,1.000000'


function rotate_right {
  echo "Rotated Right"
  xrandr --output $screen --rotate right
  xinput set-prop "$touchscreen" 'Coordinate Transformation Matrix' $right
  xinput disable "$touchpad"
}
function rotate_left {
  echo "Rotated Left"
  xrandr --output $screen --rotate left
  xinput set-prop "$touchscreen" 'Coordinate Transformation Matrix' $left
  xinput disable "$touchpad"
}

function rotate_normal {
    echo "Back to Normal"
    xrandr --output $screen --rotate normal
    xinput set-prop "$touchscreen" 'Coordinate Transformation Matrix' $normal
    xinput enable "$touchpad"

}
function rotate_inverted {
    echo "Upside down"
    xrandr --output $screen --rotate inverted
    xinput set-prop "$touchscreen" 'Coordinate Transformation Matrix' $inverted
    xinput disable "$touchpad"
}

if [ "$1" == "-n" ]; then
    rotate_normal
    exit 0
fi
if [ $currentMatrix == $normalf ]; then
    rotate_right
  # Remove hashtag below if you want pop-up the virtual keyboard  
  #onboard &
elif [ $currentMatrix == $rightf ]; then
    rotate_inverted

elif [ $currentMatrix == $invertedf ]; then
    rotate_left

elif [ $currentMatrix == $leftf ]; then
    rotate_normal
fi