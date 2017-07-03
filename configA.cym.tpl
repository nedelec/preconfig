% Example template file
% illustrating deterministic variations
% command is 'preconfig configA.cym.tpl'
%
% F. Nedelec, November 2016

set simul demo 
{
    time_step = [[[ 0.001, 0.005 ]]]
    viscosity = 0.01
}

set space cell
{
    geometry = ( sphere 5 )
}

new space cell

[[ x=[0.5, 1] ]]
set fiber microtubule
{
    rigidity = [[ round(20 * x) ]]
    segmentation = [[ 0.5 * x ]]
    confine = inside, 200
}

new fiber microtubule
{
    length = 12
}

run 5000 simul *
{
    nb_frames = 10
}
