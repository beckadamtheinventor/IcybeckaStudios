Shader "Icybecka/Procedural/Surface/OpenSimplexTransparent"
{
    Properties
    {
		[Toggle] _UseWorldSpace ("Use World Coordinates for Noise", Float) = 0.0
		[Toggle] _UseObjectSpace ("Use Object Coordinates for Noise", Float) = 0.0
		[Toggle] _UseLockedRotationObjectSpace ("Use Object Coordinates with Locked Rotation", Float) = 0.0
		[Toggle] _UseUVSpace ("Use UV Coordinates for Noise", Float) = 0.0
		_CoordinateOffset ("Coordinate Offset", Vector) = (0, 0, 0, 0)
		_CoordinateScale("Coordinate Scale", Vector) = (1.0, 1.0, 1.0, 0.0)
		_MainTex ("Detail Texture", 2D) = "white" {}
		_Octaves("Noise Octaves", Float) = 3.0
		_OctaveScale("Noise Octave Scale Multiplier", Float) = 4.0
		_OctaveFalloff("Noise Octave Value Multiplier", Float) = 0.75
		_MinBlurDistance("Blur Distance Scale", Float) = 10.0
		_BlurScale("Blur Scale", Float) = 5.0
        _ColorUnder ("Color Minimum", Color) = (0,0,0,1)
        _ColorOver ("Color Maximum", Color) = (1,1,1,1)
		_OutputScale("Output Scale", Float) = 1.0
		[Toggle] _InvertMetallic("Invert Metallic Noise", Float) = 0.0
		_MinMetallic("Minimum Metallic", Float) = 0.0
		_MaxMetallic("Maximum Metallic", Float) = 0.0
		_MetallicScale("Metallic Scale", Float) = 1.0
		[Toggle] _InvertGlossiness("Invert Glossiness Noise", Float) = 0.0
		_MinGlossiness("Minimum Glossiness", Float) = 0.0
		_MaxGlossiness("Maximum Glossiness", Float) = 0.0
		_GlossinessScale("Glossiness Scale", Float) = 1.0
		[Toggle] _InvertOcclusion("Invert Occlusion Noise", Float) = 0.0
		_MinOcclusion("Minimum Occlusion", Float) = 0.0
		_MaxOcclusion("Maximum Occlusion", Float) = 0.0
		_OcclusionScale("Occlusion Scale", Float) = 1.0
		[Toggle] _InvertEmission("Invert Emission Noise", Float) = 0.0
		_MinEmission("Minimum Emission", Color) = (0.0, 0.0, 0.0, 1.0)
		_MaxEmission("Maximum Emission", Color) = (0.0, 0.0, 0.0, 1.0)
		_EmissionScale("Emission Scale", Float) = 1.0
		[Toggle] _InvertTransparent("Invert Transparent Noise", Float) = 0.0
		_MinTransparent("Minimum Transparency", Float) = 0.0
		_MaxTransparent("Maximum Transparency", Float) = 0.0
		_TransparentScale("Transparency Scale", Float) = 1.0
    }
    SubShader
    {
        Tags { "Queue"="Transparent" "RenderType"="Transparent" "IgnoreProjectors"="True"}
		Cull Off
		ZWrite Off
		Blend SrcAlpha OneMinusSrcAlpha
        LOD 50

        CGPROGRAM
        // Physically based Standard lighting model, and enable shadows on all light types
		#pragma surface surf Standard fullforwardshadows alpha

        // Use shader model 3.0 target, to get nicer looking lighting
        #pragma target 3.0
 
		struct Input
        {
			float3 worldPos;
			float2 uv_MainTex;
			INTERNAL_DATA
        };

		half _UseWorldSpace;
		half _UseObjectSpace;
		half _UseLockedRotationObjectSpace;
		half _UseUVSpace;

		sampler2D _MainTex;
		fixed4 _ColorUnder;
		fixed4 _ColorOver;

		float4 _CoordinateOffset;
		float4 _CoordinateScale;
		float _OutputScale;
		float _Octaves;
		float _OctaveScale;
		float _OctaveFalloff;
		half _InvertMetallic;
		float _MinMetallic;
		float _MaxMetallic;
		float _MetallicScale;
		half _InvertGlossiness;
		float _MinGlossiness;
		float _MaxGlossiness;
		float _GlossinessScale;
		half _InvertOcclusion;
		float _MinOcclusion;
		float _MaxOcclusion;
		float _OcclusionScale;
		half _InvertEmission;
		half4 _MinEmission;
		half4 _MaxEmission;
		float _EmissionScale;
		half _InvertTransparent;
		float _MinTransparent;
		float _MaxTransparent;
		float _TransparentScale;
		
		float _MinBlurDistance;
		float _BlurScale;
		
		// Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.
        // See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.
        // #pragma instancing_options assumeuniformscaling
        UNITY_INSTANCING_BUFFER_START(Props)
            // put more per-instance properties here
        UNITY_INSTANCING_BUFFER_END(Props)

		#include "OpenSimplex2.hlsl"

        void surf (Input IN, inout SurfaceOutputStandard o)
        {
			float3 coords;
			if (_UseWorldSpace > 0.0f && _UseUVSpace > 0.0f)
				coords = ((floor(IN.worldPos.xyz) + float3(IN.uv_MainTex.x, 0, IN.uv_MainTex.y) - 0.5f) * _CoordinateScale) + _CoordinateOffset;
			else if (_UseLockedRotationObjectSpace > 0.0f)
				coords = (IN.worldPos - unity_ObjectToWorld._m03_m13_m23) * _CoordinateScale + _CoordinateOffset;
			else if (_UseObjectSpace > 0.0f)
				coords = mul(IN.worldPos - unity_ObjectToWorld._m03_m13_m23, unity_ObjectToWorld) * _CoordinateScale + _CoordinateOffset;
			else if (_UseUVSpace > 0.0f)
				coords = (float3(IN.uv_MainTex.x, 0, IN.uv_MainTex.y) * _CoordinateScale) + _CoordinateOffset;
			else
				coords = (IN.worldPos * _CoordinateScale) + _CoordinateOffset;
			float4 noise = openSimplex2_Conventional(coords);
			float oscale = _OctaveScale;
			float ofall = _OctaveFalloff;
			for (int i=1; i<_Octaves; i++) {
				noise += openSimplex2_Conventional(coords * oscale) * ofall;
				oscale *= _OctaveScale;
				ofall *= _OctaveFalloff;
			}
			float distScale = 1 - _MinBlurDistance / max(_MinBlurDistance, _BlurScale * distance(_WorldSpaceCameraPos, IN.worldPos.xyz));
			
			fixed4 col = lerp(_ColorUnder, _ColorOver, min(1, max(0, lerp(noise.r * _OutputScale, 0.5, distScale)))) * tex2D(_MainTex, IN.uv_MainTex);
			o.Albedo = col.rgb;
			if (_InvertOcclusion <= 0)
				o.Occlusion = lerp(_MinOcclusion, _MaxOcclusion, min(1, max(0, lerp(noise.r * _OcclusionScale, 0.5, distScale))));
			else
				o.Occlusion = lerp(_MinOcclusion, _MaxOcclusion, min(1, max(0, lerp((1 - noise.r) * _OcclusionScale, 0.5, distScale))));
			if (_InvertGlossiness <= 0)
				o.Smoothness = lerp(_MinGlossiness, _MaxGlossiness, min(1, max(0, lerp(noise.r * _GlossinessScale, 0.5, distScale))));
			else
				o.Smoothness = lerp(_MinGlossiness, _MaxGlossiness, min(1, max(0, lerp((1 - noise.r) * _GlossinessScale, 0.5, distScale))));
			if (_InvertMetallic <= 0)
				o.Metallic = lerp(_MinMetallic, _MaxMetallic, min(1, max(0, lerp(noise.r * _MetallicScale, 0.5, distScale))));
			else
				o.Metallic = lerp(_MinMetallic, _MaxMetallic, min(1, max(0, lerp((1 - noise.r) * _MetallicScale, 0.5, distScale))));
			if (_InvertEmission <= 0)
				o.Emission = lerp(_MinEmission, _MaxEmission, min(1, max(0, lerp(noise.r * _EmissionScale, 0.5, distScale))));
			else
				o.Emission = lerp(_MinEmission, _MaxEmission, min(1, max(0, lerp((1 - noise.r) * _EmissionScale, 0.5, distScale))));
			if (_InvertTransparent <= 0)
				o.Alpha = lerp(_MinTransparent, _MaxTransparent, min(1, max(0, lerp(noise.r * _TransparentScale, 0.5, distScale))));
			else
				o.Alpha = lerp(_MinTransparent, _MaxTransparent, min(1, max(0, lerp((1 - noise.r) * _TransparentScale, 0.5, distScale))));
		}
        ENDCG
    }
    FallBack "Diffuse"
}
