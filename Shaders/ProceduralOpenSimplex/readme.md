
# OpenSimplex Procedural Material Surface Shader
Version 1.1.

Tested on Unity 2021.3.23f1. Might not be compatible with 2019.

This shader generates dynamic materials using OpenSimplex noise, with a bunch of parameters to facilitate creating a wide variety of materials.
Included in this package are several example materials, as well as a transparent variant of the shader.


`OpenSimplex2.hlsl` is sourced from GitHub, the rest is written by Adam "beckadamtheinventor" Beckingham. (Also known as Icybecka Studios)


# Usage

Create a new material and set the shader to `Icybecka/Procedural/Surface/OpenSimplex`, or `Icybecka/Procedural/Surface/OpenSimplexTransparent` if you desire transparency.
You can then set parameters until the material looks as desired.


# Parameters


## Use World Coordinates for Noise

Select to use world space coordinates for generating noise. Most useful for stationary objects and objects that should change dynamically as they are moved. Also useful for demonstrating this shader.
Should not be used with `UV Space Coordinates` or `Object Space Coordinates`.


## Use Object Coordinates for Noise

Select to use object space coordinates and rotation for generating noise. (world space offset by object position and rotated)
Should not be used with `World Space Coordinates` or `UV Space Coordinates`.


## Use Object Coordinates with Locked Rotation

Select to use object space coordinates without rotation for generating noise. (world space offset by object position)
Should not be used with `World Space Coordinates` or `UV Space Coordinates`.


## Use UV Coordinates for Noise

Select to use UV coordinates for generating noise. Most useful for mesh objects with well-connected faces on the UV map.
Should not be used with `World Space Coordinates` or `Object Space Coordinates`.


## Coordinate Offset

Use this to offset the coordinates used to generate noise. Play with the values and it'll make more sense.


## Coordinate Scale

Scaling values per coordinate used to scale the coordinates used to generate noise. Play with the values and it'll make more sense.


## Detail Texture

Optional texture to be blended with noise.


## Octaves

Number of iterations (noise octaves) used to get the final noise value.


## Octave Scale

Scale multiplier of noise coordinates on each successive noise octave.


## Octave Falloff

Falloff multiplier of noise values on each successive noise octave.


## Blur Distance Scale

Distance to start blurring at in Meters.


## Blur Scale

Multiplier of blurring effect.


## Color Minimum

Minimum color value of the material.


## Color Maximum

Maximum color value of the material.


## Output Scale

Scales the noise value which is then clamped between 0 and 1. The value is then used to linearly interpolate between `Color Under` and `Color Over`.


## Invert Metallic Noise

Whether to invert the noise value used to generate the metallic value.


## Minimum Metallic

Minimum metallic value of the material.


## Maximum Metallic

Maximum metallic value of the material.


## Metallic Scale

Scales the noise value which is used to interpolate between `Minimum Metallic` and `Maximum Metallic`.


## Invert Glossiness Noise

Whether to invert the noise value used to generate the glossiness/smoothness value.


## Minimum Glossiness

Minimum glossiness/smoothness value of the material.


## Maximum Glossiness

Maximum glossiness/smoothness value of the material.


## Glossiness Scale

Scales the noise value which is used to interpolate between `Minimum Glossiness` and `Maximum Glossiness`.


## Invert Occlusion Noise

Whether to invert the noise value used to generate the occlusion value.


## Minimum Occlusion

Minimum occlusion value of the material.


## Maximum Occlusion

Maximum occlusion value of the material.


## Occlusion Scale

Scales the noise value which is used to interpolate between `Minimum Occlusion` and `Maximum Occlusion`.

## Invert Emission Noise

Whether to invert the noise value used to generate the emission value.


## Minimum Emission

Minimum emission color of the material.


## Maximum Emission

Maximum emission color of the material.


## Emission Scale

Scales the noise value which is used to interpolate between `Minimum Emission` and `Maximum Emission`.

## Invert Transparency Noise

Whether to invert the noise value used to generate the transparency value.


## Minimum Transparency

Minimum transparency color of the material.


## Maximum Transparency

Maximum transparency color of the material.


## Transparency Scale

Scales the noise value which is used to interpolate between `Minimum Transparency` and `Maximum Transparency`.

