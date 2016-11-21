# Simple bouncing molecules in a 1-D system

graphics opengl

dim 1
species red green

difc red 3
difc green 1

color red 1 0 0
color green 0 1 0

display_size red 5
display_size green 5

time_start 0
time_stop 100
time_step 0.01

boundaries 0 0 100 r

mol [[[5,10,15]]] red u
mol 2 green 50

end_file



