% Example template file
% illustrating random sampling
%
% command is 'preconfig configB.cym.tpl 100'
% F. Nedelec, November 2016

set simul fiber 
{
    time_step = 0.001
    viscosity = 0.02
}

set space cell
{
    geometry = ( sphere 5 )
}

new space cell

[[ x=random.uniform(0,1) ]]
set fiber microtubule
{
    rigidity = [[ round(20 * x, 3) ]]
    segmentation = [[ round(0.5 * x) ]]
    confine = inside, 200
}

new fiber microtubule
{
    length = [[ random.randint(0,20) ]]
}

run 5000 simul *
{
    nb_frames = 10
}
