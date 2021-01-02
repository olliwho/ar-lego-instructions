using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BrickToggle : MonoBehaviour
{
    public string model_name;
    private int step;
    List<List<string>> step_info = new List<List<string>>();

    void Start()
    {
        GameObject parent = this.gameObject;
        int count = parent.transform.childCount;
        for (int i = 0; i < count; i++)
        {
            parent.transform.GetChild(i).gameObject.transform.GetChild(0).gameObject.SetActive(false);
        }
    }

    List<List<string>> ReadStepInfo()
    {
        TextAsset info_file = Resources.Load(model_name + "/" + model_name.ToLower() + "_step_info") as TextAsset;
        string[] lines = info_file.ToString().Split('\n');

        List<List<string>> steps = new List<List<string>>();
        List<string> step = new List<string>();
        List<string> s0 = new List<string>();

        foreach (string line in lines)
        {
            string start = line.Substring(0, 1);
            switch (start)
            {
                case "s":
                    steps.Add(step);
                    step.Clear();
                    break;
                case "b":
                    string brick = line.Split(' ')[1].Replace(".dat", "");
                    step.Add(brick);
                    if (!s0.Contains(brick))
                    {
                        s0.Add(brick);
                    }
                    break;
            }
        }
        steps.Add(step);
        steps.RemoveAt(0);
        steps.Insert(0, s0);

        return steps;
    }

    public void NextStep()
    {
        step++;
    }

    public void LastStep()
    {
        step--;
    }
}
