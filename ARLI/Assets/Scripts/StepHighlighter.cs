using System.Collections.Generic;
using UnityEngine;

public class StepHighlighter : MonoBehaviour
{
    List<Color> startColors = new List<Color>();
    Material[] materials;
    public bool activeStep;
    void Start()
    {
        materials = GetComponent<MeshRenderer>().materials;
        foreach(Material mat in materials)
        {
            startColors.Add(mat.color);
        }
    }
    void Update()
    {
        if (activeStep)
        {
            int i = 0;
            foreach (Material mat in materials)
            {
                mat.color = Color.Lerp(startColors[i], Color.white * 0.8f, Mathf.PingPong(Time.time * 0.2f, 1));
                i++;
            }
        }
        else
        {
            int i = 0;
            foreach (Material mat in materials)
            {
                mat.color = startColors[i];
                i++;
            }
        }
    }
}
