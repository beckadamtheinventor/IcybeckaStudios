Shader "Icybecka/Surface/MultipleDetailMaps"
{
    Properties
    {
        _Color ("Color", Color) = (1,1,1,1)
        _MainTex ("Albedo (RGB)", 2D) = "white" {}
		_DetailTex1 ("Detail Map 1", 2D) = "white" {}
		_AddDetail1 ("Add Detail 1", Float) = 0.0
		_MulDetail1 ("Multiply Detail 1", Float) = 0.0
		_DetailTex2 ("Detail Map 2", 2D) = "white" {}
		_AddDetail2 ("Add Detail 2", Float) = 0.0
		_MulDetail2 ("Multiply Detail 2", Float) = 0.0
		_DetailTex3 ("Detail Map 3", 2D) = "white" {}
		_AddDetail3 ("Add Detail 3", Float) = 0.0
		_MulDetail3 ("Multiply Detail 3", Float) = 0.0
		_NormalMap ("Normal Map", 2D) = "bump" {}
		_NormalMap2 ("Normal Map 2", 2D) = "bump" {}
		[NoScaleOffset] _GlossinessTex ("Smoothness Map", 2D) = "white" {}
        _Glossiness ("Smoothness", Range(0,1)) = 0.5
		[NoScaleOffset] _MetallicTex ("Metallic Map", 2D) = "white" {}
        _Metallic ("Metallic", Range(0,1)) = 0.0
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 200

        CGPROGRAM
        // Physically based Standard lighting model, and enable shadows on all light types
        #pragma surface surf Standard fullforwardshadows

        // Use shader model 3.0 target, to get nicer looking lighting
        #pragma target 3.0

        sampler2D _MainTex;
        sampler2D _DetailTex1;
        sampler2D _DetailTex2;
        sampler2D _DetailTex3;
        sampler2D _NormalMap;
        sampler2D _NormalMap2;
        sampler2D _GlossinessTex;
        sampler2D _MetallicTex;

        struct Input
        {
            float2 uv_MainTex;
            float2 uv_NormalMap;
            float2 uv_NormalMap2;
			float2 uv_DetailTex1;
			float2 uv_DetailTex2;
			float2 uv_DetailTex3;
        };

		half _AddDetail1;
		half _AddDetail2;
		half _AddDetail3;
		half _MulDetail1;
		half _MulDetail2;
		half _MulDetail3;
        half _Glossiness;
        half _Metallic;
        fixed4 _Color;

        // Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.
        // See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.
        // #pragma instancing_options assumeuniformscaling
        UNITY_INSTANCING_BUFFER_START(Props)
            // put more per-instance properties here
        UNITY_INSTANCING_BUFFER_END(Props)

        void surf (Input IN, inout SurfaceOutputStandard o)
        {
			fixed4 c1;
			fixed4 c = _Color * tex2D(_MainTex, IN.uv_MainTex);

			// detail 1
			c1 = tex2D(_DetailTex1, IN.uv_DetailTex1);
			c = c * lerp(1, c1, _MulDetail1) + lerp(0, c1, _AddDetail1);
			
			// detail 2
			c1 = tex2D(_DetailTex2, IN.uv_DetailTex2);
			c = c * lerp(1, c1, _MulDetail2) + lerp(0, c1, _AddDetail2);
			
			// detail 3
			c1 = tex2D(_DetailTex3, IN.uv_DetailTex3);
			c = c * lerp(1, c1, _MulDetail3) + lerp(0, c1, _AddDetail3);
			
			// Normals
			o.Normal = BlendNormals(UnpackNormal(tex2D(_NormalMap, IN.uv_NormalMap)),
									UnpackNormal(tex2D(_NormalMap2, IN.uv_NormalMap2)));
            o.Albedo = c.rgb;
            o.Metallic = _Metallic * tex2D(_MetallicTex, IN.uv_MainTex);
            o.Smoothness = _Glossiness * tex2D(_GlossinessTex, IN.uv_MainTex);
            o.Alpha = c.a;
        }
        ENDCG
    }
    FallBack "Diffuse"
}
